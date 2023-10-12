from flask import Flask,abort
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (OTLPSpanExporter,)
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging
import time
import random
import os
import requests

app = Flask(__name__)

merged = dict()
merged.update({
    "service.name": "frontend",
    "service.version": "1.0.0",
})

resource = Resource.create(merged)

resource = Resource.create(merged)
logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)
Lexporter = OTLPLogExporter(insecure=True,endpoint=os.environ["COLLECTOR_SERVICE_ADDR"])
logger_provider.add_log_record_processor(BatchLogRecordProcessor(Lexporter))
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)

tracer_provider = TracerProvider(resource=resource)
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=os.environ["COLLECTOR_SERVICE_ADDR"],insecure=True))
tracer_provider.add_span_processor(span_processor)
RequestsInstrumentor().instrument()
trace.set_tracer_provider(tracer_provider)
FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)



@app.route('/')
def index():
    with tracer.start_as_current_span("index"):
        if random.random() <= 0.02:
            for _ in range(50):
                resp = requests.get(url="http://backend:5000/")
                logging.info("backend requested")
                time.sleep(.05)
        else:
            resp = requests.get(url="http://backend:5000/")
            logging.info("backend requested")
        print(resp.status_code)
        return "🐏"

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=5000)

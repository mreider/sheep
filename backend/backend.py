from flask import Flask, abort
from multiprocessing import Pool
from multiprocessing import cpu_count
import logging
import time
import random
from opentelemetry import trace
from opentelemetry import metrics as metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (OTLPSpanExporter,)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import (AggregationTemporality,PeriodicExportingMetricReader,)
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


import os

app = Flask(__name__)

merged = dict()
merged.update({
    "service.name": "backend",
    "service.version": "1.0.0",
})

Mexporter = OTLPMetricExporter(
    endpoint=os.environ["COLLECTOR_SERVICE_ADDR"],
    preferred_temporality={Counter: AggregationTemporality.DELTA},
    insecure=True)

resource = Resource.create(merged)
tracer_provider = TracerProvider(resource=resource)
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=os.environ["COLLECTOR_SERVICE_ADDR"],insecure=True))
tracer_provider.add_span_processor(span_processor)
format = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
LoggingInstrumentor().instrument(set_logging_format=format)
RequestsInstrumentor().instrument()
trace.set_tracer_provider(tracer_provider)
FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)
reader = PeriodicExportingMetricReader(Mexporter) 
provider = MeterProvider(metric_readers=[reader], resource=resource)
set_meter_provider(provider)
meter = get_meter_provider().get_meter("sheep-meter", "1.0.0")
sheep_counter = meter.create_counter(
  name="sheep_counter",
  description="How many sheep?"
)

def leak(x):
    error_emitted = 0
    # leak CPU fo 15 seconds
    t_end = time.time() + 15
    while time.time() < t_end:
        x*x

@app.route('/')
def index():
    try:
        with tracer.start_as_current_span("backend"):
            attributes = { "breed": "suffolk" }
            sheep_counter.add(int(1), attributes)
            if random.random() <= 0.02:
                processes = cpu_count()
                with tracer.start_as_current_span("log error"):
                    logging.error("bad things happend")
                print('utilizing %d cores\n' % processes)
                pool = Pool(processes)
                pool.map(leak, range(processes))
                raise ValueError("500 error")
            return "🐏"
    except Exception as e:
        abort(500)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=5000)
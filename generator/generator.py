import time
import schedule
import requests

def do_constantly():
    resp = requests.get(url="http://frontend:5000/")
    print(resp.status_code)

schedule.every(7).seconds.do(do_constantly)

while True:
    schedule.run_pending()
    time.sleep(.5)

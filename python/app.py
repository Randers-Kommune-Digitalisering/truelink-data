import sys
import logging
import threading
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

from config.settings import FLASK_SERVER_PORT, DEBUG
from utils.utils import route_files
from utils.truelinkSFTP import list_all_files

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = Flask(__name__)
sched = BackgroundScheduler()

def weekly_job():
    filelist, conn = list_all_files()
    route_files(filelist, conn)

@app.get('/')
def readinessprobe():
    if len(sched.get_jobs()):
        return jsonify({'status': 'running'})

if __name__ == '__main__':
    # Run on deployment
    t = threading.Thread(target=weekly_job, name="Deploy")
    t.start()
    
    # Run at 5 am every Monday
    sched.add_job(weekly_job, 'cron', day_of_week='mon', hour=5)
    sched.start()

    app.run(host='0.0.0.0', port=FLASK_SERVER_PORT, debug=DEBUG)
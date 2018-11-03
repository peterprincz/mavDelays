from flask import *
from datetime import datetime, date
import mav
from flask_cors import CORS, cross_origin
import threading
from train import Train
from database import Session, engine, Base


app = Flask(__name__, static_url_path='')
CORS(app)


@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/counter")
def counter():
    return jsonify(mav_data)


def add_train_to_db(session, trains_in_db, train):
    train_in_db = False
    for db_train in trains_in_db:
        if train.origin_start == db_train.origin_start and train.origin_arrival == db_train.origin_arrival and train.route == db_train.route:
            train_in_db = True
            if db_train.real_arrival != train.real_arrival or db_train.real_start != train.real_start:
                session.query(Train).filter(Train.id == db_train.id).update({'real_start': train.real_start, 'real_arrival': train.real_arrival})
                break
    if train_in_db is False:
        session.add(train)

def get_delays():
    threading.Timer(250.0, get_delays).start()
    mav_data["last_update_time"] = datetime.utcnow()
    result = {"vac_to_bp": {}, "bp_to_vac": {}}
    result["vac_to_bp"]["counter"] = 0
    result["vac_to_bp"]["minutes"] = 0
    result["vac_to_bp"]["delayed_trains"] = []
    result["bp_to_vac"]["counter"] = 0
    result["bp_to_vac"]["minutes"] = 0
    result["bp_to_vac"]["delayed_trains"] = []

    vac_to_bp = mav.MavSchedule("vác", "nyugati")
    bp_to_vac = mav.MavSchedule("nyugati", "vác")
    date_format_string = '%H:%M'

    vac_to_bp_counter = 0
    vac_to_bp_minute_counter = 0
    bp_to_vac_counter = 0
    bp_to_vac_minute_counter = 0

    session = Session()

    today_midnight_unix = datetime.combine(date.today(), datetime.min.time()).timestamp()

    trains_in_db = session.query(Train).filter(Train.date > today_midnight_unix)

    for train in vac_to_bp.trains:
        if train.origin_arrival != train.real_arrival and train.real_arrival is not "":
            origin = datetime.strptime(train.origin_arrival, date_format_string)
            real = datetime.strptime(train.real_arrival, date_format_string)
            if real > origin:
                add_train_to_db(session, trains_in_db, train)
                result["vac_to_bp"]["counter"] += 1
                result["vac_to_bp"]["minutes"] += int((real - origin).seconds/60)
                result["vac_to_bp"]["delayed_trains"].append(train.serialize())

    for train in bp_to_vac.trains:
        train_in_db = False
        if train.origin_arrival != train.real_arrival and train.real_arrival is not "":
            origin = datetime.strptime(train.origin_arrival, date_format_string)
            real = datetime.strptime(train.real_arrival, date_format_string)
            if real > origin:
                add_train_to_db(session, trains_in_db, train)
                result["bp_to_vac"]["counter"] += 1
                result["bp_to_vac"]["minutes"] += int((real - origin).seconds/60)
                result["bp_to_vac"]["delayed_trains"].append(train.serialize())

    session.commit()
    session.close()
    mav_data["delays"] = result


if __name__ == "__main__":
    mav_data = {}
    mav_data["start_time"] = datetime.utcnow()
    mav_data["delays"] = {}
    get_delays()
    app.config["JSON_AS_ASCII"] = False
    app.run(port=5000,host="0.0.0.0", debug=True)
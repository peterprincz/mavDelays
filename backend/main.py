from flask import *
from datetime import datetime
import mav
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)



@app.route("/")
def index():
    return "hello world"


@app.route("/counter")
def counter():
    data = {}
    data["start_time"] = datetime.utcnow()
    data["delay_counter"] = get_delays()
    return jsonify(data)

def get_delays():
    result = {}
    vac_to_bp = mav.MavSchedule("vác", "nyugati").trains
    bp_to_vac = mav.MavSchedule("nyugati", "vác").trains
    date_format_string = '%H:%M'

    vac_to_bp_counter = 0
    vac_to_bp_minute_counter = 0
    bp_to_vac_counter = 0
    bp_to_vac_minute_counter = 0

    for train in vac_to_bp:
        if train.origin_arrival != train.real_arrival and train.real_arrival is not "":
            origin = datetime.strptime(train.origin_arrival, date_format_string)
            real = datetime.strptime(train.real_arrival, date_format_string)
            if real > origin:
                vac_to_bp_counter += 1
                vac_to_bp_minute_counter += (real - origin).seconds/60
    for train in bp_to_vac:
        if train.origin_arrival != train.real_arrival and train.real_arrival is not "":
            origin = datetime.strptime(train.origin_arrival, date_format_string)
            real = datetime.strptime(train.real_arrival, date_format_string)
            if real > origin:
                bp_to_vac_counter += 1
                bp_to_vac_minute_counter += (real - origin).seconds / 60
    
    result["vac_to_bp_counter"] = vac_to_bp_counter
    result["vac_to_bp_minutes_counter"] = vac_to_bp_minute_counter
    result["bp_tovac_counter"] = bp_to_vac_counter
    result["bp_tovac_minutes_counter"] = bp_to_vac_minute_counter
    return result
    


if __name__ == "__main__":
    app.run(port=5000, debug=True)
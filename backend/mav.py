from requests_html import HTMLSession
import time
from datetime import datetime
from train import Train
class MavSchedule:

    def __init__(self, from_place, to_place):
        mav_url = self._generate_mav_string(to_place)
        self.trains = self._get_trains_from_url(mav_url)



    def _get_trains_from_url(self, url):
        session = HTMLSession()
        r = session.get(url)
        train_tables = r.html.find(".more")
        trains = []

        for train_table in train_tables:
            train_row_1 = train_table.find("tr")[1].find("td")
            train_row_2 = train_table.find("tr")[2].find("td")
            for index, train in enumerate (list(zip(train_row_1,train_row_2))):
                if index == 1:
                    origin_start = train[0].text
                    origin_arrival = train[1].text
                if index == 2:
                    real_start = train[0].text
                    real_arrival = train[1].text
                if index == 3:
                    rail = train[1].text
            train = Train(origin_start, real_start, origin_arrival, real_arrival, rail)
            trains.append(train)
        return trains

    def _generate_mav_string(self, to):
        current_date = datetime.today().strftime('%y.%m.%d')
        current_time = time.strftime("%H%M", time.gmtime())
        if to.upper() == "NYUGATI":
            return "http://elvira.mav-start.hu/elvira.dll/uf?language=1&i=v%C3%A1c&e=Budapest+Nyugati+%5BBudapest-Nyugati%5D&d="+current_date+".&mikor=-1&u="+current_time+"&go="
        if to.upper() in ["VÁC", "VAC"]:
            return "http://elvira.mav-start.hu/elvira.dll/uf?language=1&i=Budapest+Nyugati+%5BBudapest-Nyugati%5D&e=V%C3%A1c&d="+current_date+".&mikor=-1&u="+current_time+"&go="
        raise ValueError



    def filter_by_time(self, trains, from_time, to_time):
        if is_time_format(self, from_time) and is_time_format(self, to_time):
            result = []
            for train in trains:
                if train.origin_start > from_time and train.origin_arrival < to_time:
                    result.append(train)
            return result
        else:
            raise ValueError

    def is_time_format(self, time_str):
        try:
            time.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False



def main():
    from_place = "nyugati"
    to_place = "vác"
    menetrend = MavSchedule(from_place, to_place)
    print(menetrend.trains)

if __name__ == '__main__':
    main()
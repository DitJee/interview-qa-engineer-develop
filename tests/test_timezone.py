import requests
from dateutil import parser, tz

def test_different_timezone_conversion(api, flight_id, flight_id_2, utc_second_bkk, utc_second_london):
    res = requests.get(f"{api}/flights")
    assert res.status_code == 200
    body = res.json()

    flight_0 = body["flights"][0] # DMK -> HYD
    flight_1 = body["flights"][1] # DMK -> LHR

    assert flight_0["id"] == flight_id
    assert flight_1["id"] == flight_id_2

    dep_time = parser.isoparse(flight_1["departure_time"])
    arr_time = parser.isoparse(flight_1["arrival_time"])

    assert dep_time.tzinfo is not None
    assert arr_time.tzinfo is not None

    assert dep_time.utcoffset().total_seconds() == utc_second_bkk
    assert arr_time.utcoffset().total_seconds() == utc_second_london

def test_same_timezone_conversion(api, flight_id, flight_id_2, utc_second_bkk):
    res = requests.get(f"{api}/flights")
    assert res.status_code == 200
    body = res.json()

    flight_0 = body["flights"][0] # DMK -> HYD
    flight_1 = body["flights"][1] # DMK -> LHR

    assert flight_0["id"] == flight_id
    assert flight_1["id"] == flight_id_2

    dep_time = parser.isoparse(flight_0["departure_time"])
    arr_time = parser.isoparse(flight_0["arrival_time"])

    assert dep_time.tzinfo is not None
    assert arr_time.tzinfo is not None

    assert dep_time.utcoffset().total_seconds() == utc_second_bkk
    assert arr_time.utcoffset().total_seconds() == utc_second_bkk

    assert arr_time > dep_time


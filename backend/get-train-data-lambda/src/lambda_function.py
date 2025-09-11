import os
import csv
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from nyct_gtfs import NYCTFeed, Trip, StopTimeUpdate


def get_arrival_by_id(lines: list, stop_id: str):
    feed: list[Trip] = NYCTFeed("N").filter_trips(line_id=lines)
    stops = {}
    direction = None
    found_stops = False

    if stop_id.endswith("N"):
        direction = "North"
    elif stop_id.endswith("S"):
        direction = "South"
    else:
        return {"error": "Invalid stop_id format. Must end with 'N' or 'S'."}, False

    
    for trip in feed:
        train_letter = trip.route_id
        if train_letter not in stops:
            stops[train_letter] = []
        try:
            stop_times: list[StopTimeUpdate] = trip.stop_time_updates
            for stop_time in stop_times:
                if stop_time.stop_id == stop_id:
                    date_time_est = stop_time.arrival.astimezone(ZoneInfo("America/New_York"))
                    diff = (datetime.now(ZoneInfo("America/New_York")) - date_time_est).total_seconds() / 60
                    diff = abs(int(diff))
                    found_stops = True
                    stops[train_letter].append(diff)
        except Exception as e:
            print("Error in trip:", e)

    return stops, found_stops


def get_stop_id(stop_name: str, direction: str):
    base_dir = os.path.dirname(__file__)
    filename = os.path.join(base_dir, "stops.csv")
    stop_ids = []

    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["stop_name"] == stop_name:
                stop_ids.append(row["stop_id"] + direction)
    return stop_ids


def arrivals(lines, stop_name, stop_direction):
    if not lines or not stop_name or not stop_direction:
        return {"status": "error", "message": "Missing 'lines' or 'stop_id' parameter"}, 400
    if stop_direction not in ["N", "S"]:
        return {"status": "error", "message": "Invalid 'direction' parameter. Must be 'N' or 'S'."}, 400

    stop_id = get_stop_id(stop_name, stop_direction)
    if not stop_id:
        return {"status": "error", "message": f"Stop name '{stop_name}' not found."}, 404

    lines_list = lines.split(",")
    found = False
    result = {}

    for sid in stop_id:
        stops, found_stops = get_arrival_by_id(lines_list, sid)
        if found_stops:
            result.update(stops)
            found = True
            break

    if not found:
        return {"status": "error", "message": f"No arrivals found for {stop_name} ({stop_direction})."}, 404

    return {
        "status": "ok",
        "station": stop_name,
        "direction": stop_direction,
        "lines": result,
        "timestamp": datetime.now(ZoneInfo("America/New_York")).isoformat()
    }, 200


def lambda_handler(event, context):
    print("Event received:", event)

    queryParams = event.get("queryStringParameters") or {}
    lines = queryParams.get("lines", "")
    stop_name = queryParams.get("stop_name", "")
    stop_direction = queryParams.get("direction", "")

    try:
        body, status_code = arrivals(lines, stop_name, stop_direction)
    except Exception as e:
        print("Handler error:", e)
        body = {"status": "error", "message": str(e)}
        status_code = 500

    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


if __name__ == "__main__":
    event = {
        "queryStringParameters": {
            "lines": "N,Q,R",
            "stop_name": "Times Sq-42 St",
            "direction": "N"
        }
    }
    response = lambda_handler(event, None)
    print(response)
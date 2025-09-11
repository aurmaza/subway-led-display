from datetime import datetime
from nyct_gtfs import NYCTFeed, Trip, StopTimeUpdate
from flask import Flask, request, jsonify
import os
from zoneinfo import ZoneInfo
import csv
app = Flask(__name__)
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
        return {"error": "Invalid stop_id format. Must end with 'N' or 'S'."}
    
    
    print(feed)
    for trip in feed:
        # trip.trip_id
        train_letter = trip.route_id
        if trip.route_id not in stops:
            stops[train_letter] = []
        try:
            stop_times:  list[StopTimeUpdate] = trip.stop_time_updates
            for stop_time in stop_times:
                if stop_time.stop_id == stop_id:
                    date_time_est = stop_time.arrival.astimezone(ZoneInfo("America/New_York"))
                    diff = (datetime.now(ZoneInfo("America/New_York")) - date_time_est).total_seconds() / 60
                    diff = int(diff)
                    diff = abs(diff)
                    found_stops = True
                    stops[train_letter].append(diff)       
        except Exception as e:
            print(e)
    return stops, found_stops
def get_stop_id(stop_name: str, direction):
    # Find the directory where this script is located
    base_dir = os.path.dirname(__file__)
    filename = os.path.join(base_dir, "stops.csv")
    stop_ids=[]
    
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if row["stop_name"] == stop_name:
                stop_ids.append(row["stop_id"] + direction)
    return stop_ids
@app.route("/api/arrivals", methods=["GET"])
def arrivals():
    lines = request.args.get("lines", "")
    stop_name = request.args.get("stop_name", "")
    stop_direction = request.args.get("direction", "")
    if not lines or not stop_name or not stop_direction:
        return jsonify({"error": "Missing 'lines' or 'stop_id' parameter"}), 400
    if stop_direction not in ["N", "S"]:
        return jsonify({"error": "Invalid 'direction' parameter. Must be 'N' or 'S'."}), 400
    stop_id = get_stop_id(stop_name, stop_direction)
    if not stop_id:
        return jsonify({"error": f"Stop name '{stop_name}' not found."}), 404
    lines_list = lines.split(",")
    for id in stop_id:
        arrivals = get_arrival_by_id(lines_list, id)
        if arrivals[1]:
            break
    return jsonify(arrivals[0])


@app.route("/test", methods=["GET"])
def test():
    return "Kill yourself!"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)


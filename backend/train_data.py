import datetime
from nyct_gtfs import NYCTFeed, Trip, StopTimeUpdate
from flask import Flask, request, jsonify
import os
app = Flask(__name__)
def get_arrival_by_id(lines: list, stop_id: str):
    feed: list[Trip] = NYCTFeed("N").filter_trips(line_id=lines)  
    stops = {}

    for trip in feed:
        # trip.trip_id
        train_letter = trip.route_id
        if trip.route_id not in stops:
            stops[train_letter] = []
        try:
            stop_times:  list[StopTimeUpdate] = trip.stop_time_updates
            for stop_time in stop_times:
                if stop_time.stop_id == stop_id:
                    stops[train_letter].append(stop_time.arrival)       
        except Exception as e:
            print(e)
    return stops    

@app.route("/api/arrivals", methods=["GET"])
def arrivals():
    lines = request.args.get("lines", "")
    stop_id = request.args.get("stop_id", "")
    if not lines or not stop_id:
        return jsonify({"error": "Missing 'lines' or 'stop_id' parameter"}), 400

    lines_list = lines.split(",")
    arrivals = get_arrival_by_id(lines_list, stop_id)
    return jsonify(arrivals)


@app.route("/test", methods=["GET"])
def test():
    return "Kill yourself!"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)


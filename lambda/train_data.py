import datetime
from nyct_gtfs import NYCTFeed, Trip, StopTimeUpdate
    
def get_arrival_by_id(lines: list, stop_id: str):
    feed: list[Trip] = NYCTFeed("N").filter_trips(line_id=lines)  
    stops = {}
    for trip in feed:
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
    # sorted(stops, key=stops) 
    return stops    
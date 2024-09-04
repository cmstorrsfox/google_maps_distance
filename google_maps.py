import pandas as pd
import numpy as np
import googlemaps
from datetime import datetime
import responses

### pandas dataset
postcodes = pd.read_csv('se_postcodes.csv')

postcode_list = postcodes.Postcode.to_list()


### api info
key = "AIzaSyCGg5xtE2R8HoF25NMRz_HhQyp_OKNbwMs"
client = googlemaps.Client(key)


### function to get distances and times
def get_distances_and_times(origin, destination, mode, units):
  responses.add(
    responses.GET,
    "https://maps.googleapis.com/maps/api/distancematrix/json",
    body='{"status":"OK", "rows":[]}',
    status=200,
    content_type="application/json",
  )


  arrival_time = datetime(2024, 10, 10, 9)




  matrix = client.distance_matrix(origin, destination, mode=mode, units=units, arrival_time=arrival_time)

  distance = matrix.get('rows')[0].get('elements')[0].get('distance').get('text')
  duration = matrix.get('rows')[0].get('elements')[0].get('duration').get('text')

  return {"origin": origin, "distance": distance, "duration": duration}

  

output = get_distances_and_times("GU16 6HA", "TW20 9TR", "transit", "metric")

distance = output.get('rows')[0].get('elements')[0].get('distance').get('text')
duration = output.get('rows')[0].get('elements')[0].get('duration').get('text')

print(duration)

def create_df(address_list, destination, mode, units):
  output_dict = []
  for item in address_list:
    output_dict.append(get_distances_and_times(origin=item, destination=destination, mode=mode, units=units))
  
  df = pd.json_normalize(output_dict)

  return df




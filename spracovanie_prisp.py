#!/usr/bin/python

import json

with open("data_UK.json",'r') as f:
	geo_data={
	        "type": "FeatureCollection",
                "features": []
        }
	for line in f:
		tweet=json.loads(line)
                if tweet['coordinates']:
                	geo_json_feature={
        	                "type": "Feature",
	                        "geometry": tweet['coordinates'],
                       		"properties": {
        		                "text": tweet['text'],
                                	"created_at": tweet['created_at']
                        	}
			}
			geo_data['features'].append(geo_json_feature)
with open("geo_data.json","w") as f_geo:
	f_geo.write(json.dumps(geo_data,indent=4))

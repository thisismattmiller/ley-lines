import csv
from geojson import Feature, Point, FeatureCollection
import geojson
import geopandas
import alphashape
from shapely.geometry import shape


with open('LinkNYC_Locations.csv') as infile:

	reader = csv.DictReader(infile)

	boroughs = {}
	for row in reader:

		if row['Project Status'] == 'Live':


			if row['Borough'] not in boroughs:
				boroughs[row['Borough']] = []

			boroughs[row['Borough']].append(
				Feature(
					geometry=Point((float(row['Longitude']),float(row['Latitude']))), 
					properties={"address": row['Street Address'],"crossStreet1": row['Cross Street 1'],"crossStreet2": row['Cross Street 2'],'blockLocation': row['IxN Corner']}
				)
			)






	for key in boroughs:
		print(key)
		# if key != 'Brooklyn':
		# 	continue

		feature_collection = FeatureCollection(boroughs[key])

		geojson.dump(feature_collection,open(f"nyclink_{key}.geojson",'w'))



		# Define input points
		gdf = geopandas.read_file(f"nyclink_{key}.geojson")

		# Generate the alpha shape
		alpha_shape = alphashape.alphashape(gdf,alpha=25)

		for x in alpha_shape['geometry']:
		    print(x,"<<")

		polygon = alpha_shape.to_crs("EPSG:4326").to_json()

		polygon_data = geojson.loads(polygon)

		print('-----')
		print(polygon_data['features'][0])
		s = shape(polygon_data['features'][0]["geometry"])
		polygon_data['features'][0]['id'] = 'polygon'
		print(s.centroid)
		print(polygon_data)
		polygon_data['features'].append(

			{
			    "geometry": {
			        "coordinates": [
			            s.centroid.x,
			            s.centroid.y
			        ],
			        "type": "Point"
			    },
			    "id": 'centroid',
			    "properties": {			        
			    },
			    "type": "Feature"
			}



		)


		geojson.dump(polygon_data,open(f"nyclink_{key}_final.geojson",'w'))


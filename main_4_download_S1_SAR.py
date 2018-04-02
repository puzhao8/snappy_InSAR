import time, os
import datetime

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

savePath = "D:\\Stockholm\\Ascending\\ASC_orb102_Scene_2_S1_zip\\"
api = SentinelAPI('ahui0911', '19940911', 'https://scihub.copernicus.eu/dhus')

footprint = geojson_to_wkt(read_geojson('stockholm_asc_rorb_102_up_map.geojson'))


# products = api.query(footprint, date=('20170501', '20171031'), platformname = 'Sentinel-1',
#           producttype='SLC', relativeorbitnumber = 102, orbitdirection="DESCENDING")

products = api.query(footprint, date=('20170501', '20171031'), platformname = 'Sentinel-1',
          producttype='SLC', relativeorbitnumber = 102, orbitdirection="ASCENDING", order_by='+beginposition')

print("Total Number of Searched Products:" + str(len(products.keys())))
# api.download_all(products, savePath)

### If a product doesn't exist, then download it.
for key in products.keys():
    filename = products[key]['title']
    # print(savePath + filename + ".zip", os.path.exists(savePath + filename + ".zip"))

    if os.path.exists(savePath + filename + ".zip"):
        print("existed: " + filename)
    else:
        print("Downloading: " + filename)
        api.download(key, savePath)
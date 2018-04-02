import time, os
import datetime


from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

savePath = "F:\\Stockholm_InSAR\\2015_DSC_rorb22_ZIP\\"

api = SentinelAPI('ahui0911', '19940911', 'https://scihub.copernicus.eu/dhus')

footprint = geojson_to_wkt(read_geojson(r'F:\snappy_InSAR_code\GeoJOSN\stockholm_DSC_dw_scene.geojson'))


# products = api.query(footprint, date=('20170501', '20171031'), platformname = 'Sentinel-1',
#           producttype='SLC', relativeorbitnumber = 102, orbitdirection="DESCENDING")


# Launch Date -> S1A: 2014-04-03, S1B: 2016-04-25
### DSC rorb = 22
products = api.query(footprint, date=('20150501', '20151031'), platformname = 'Sentinel-1',
          producttype='SLC',relativeorbitnumber = 22, orbitdirection="DESCENDING", order_by='+beginposition',
                     filename='S1A*')

### ASC rorb = 102
# products = api.query(footprint, date=('20170501', '20171031'), platformname = 'Sentinel-1',
#           producttype='SLC', relativeorbitnumber = 102, orbitdirection="ASCENDING", order_by='+beginposition')

print("Total Number of Searched Products:" + str(len(products.keys())))
# api.download_all(products, savePath)


if not os.path.exists(savePath):
    os.mkdir(savePath)

### If a product doesn't exist, then download it.
for key in products.keys():
    filename = products[key]['title']
    # print(savePath + filename + ".zip", os.path.exists(savePath + filename + ".zip"))

    if os.path.exists(savePath + filename + ".zip"):
        print("existed: " + filename)
    else:
        # print("Downloading: " + filename)
        print(filename)
        # api.download(key, savePath)
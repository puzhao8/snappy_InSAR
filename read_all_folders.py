
import snappy

from snappy import ProductIO
from snappy import HashMap

import os, gc
from snappy import GPF

def read_all_folders_in(path):
    output = []
    sat = [] # # S1A, S1B
    date = []
    # path = "E:\\Fogo Volcano 2014 Eruption\\SENTINEL_zip\\"
    for folder in os.listdir(path):
        gc.enable()

        # output.append(path + folder + "\\")
        output.append(path + folder)
        sat.append(folder.split("_")[0]) # S1A, S1B

        print(folder)
        timestamp = folder.split("_")[5]
        date.append(timestamp[:8])

        # print(folder, timestamp, date)

    # product_t1 = ProductIO.readProduct(output[0] + "\\manifest.safe")
    # product_t2 = ProductIO.readProduct(output[1] + "\\manifest.safe")

    # product_t1 = ProductIO.readProduct(output[0])
    # product_t2 = ProductIO.readProduct(output[1])

    return output

# path = "E:\\Fogo Volcano 2014 Eruption\\SENTINEL_zip\\"
# p1, p2 = read_all_folder(path)
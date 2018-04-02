
import snappy

from snappy import ProductIO
from snappy import HashMap

import os, gc
from snappy import GPF

def read_sorted_fileNamesList_from(path):
    output = []
    dates = []
    date_output_dict = {}
    # path = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\DSC_orb22_Scene_2_S1_zip\\"

    for folder in os.listdir(path):
        gc.enable()

        # output.append(path + folder + "\\")
        output.append(folder)

        # print(folder)
        cur_date = folder.split("_")[5]
        dates.append(cur_date)

        date_output_dict[cur_date] = folder

        # print(folder, timestamp, date)
    dates.sort()
    print(dates)

    filenames = []
    for idx in range(len(dates)):
        name = date_output_dict[dates[idx]]
        filenames.append(name)

    return filenames, dates

### Testing codes
# path = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\DSC_orb22_Scene_2_S1_zip\\"
# filenames, dates = read_all_sorted_folders_in(path)
#
# for i in range(len(filenames)):
#     print(path + filenames[i])

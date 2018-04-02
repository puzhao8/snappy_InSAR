import snappy

from snappy import jpy, ProgressMonitor, ProductIO
from snappy import HashMap

import os, gc
from snappy import GPF
from read_all_sorted_filenames import read_all_sorted_filenames_in
from set_params_4_multi_operations import setParams4MultiOperations

GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
HashMap = snappy.jpy.get_type('java.util.HashMap')


path = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\DSC_orb22_Scene_2_S1_zip\\"
filenames, dates = read_all_sorted_filenames_in(path)

print("The total number of available files is : ", len(filenames))

### Parameters Setting
polarization = 'VV'
subswath = 'IW2'
burstStart = 1
burstEnd = 4
parameters = setParams4MultiOperations(subswath, polarization, burstStart, burstEnd)

for idx in range(3):
    sat1 = filenames[idx][:3]  # obtain sensor name : 'S1A' or 'S1B'
    sat2 = filenames[idx+1][:3]

    product_t1 = ProductIO.readProduct(path + filenames[idx])
    product_t2 = ProductIO.readProduct(path + filenames[idx+1])

    print(product_t1, product_t2)

    print(filenames[idx])
    print(filenames[idx+1])

    roi_name = 'Stockholm'
    t1_info = dates[idx] + "_[" + sat1 + "_" + dates[idx]
    t2_info = sat2 + "_" + dates[idx+1] + "]"

    # SAVE_path = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\InSAR_gpf_results\\"
    SAVE_path = "D:\\Stockholm\\Descending\\DSC_orb22_Scene2_InSAR\\"
    isExist = os.path.exists(SAVE_path)
    if not isExist:
        os.mkdir(SAVE_path)

    TOPSAR_split_param = subswath + '_' + polarization + '_b' + str(burstStart) + '_' + str(burstEnd)
    saveNamePrefix = SAVE_path + roi_name + "_" + t1_info + "_" + t2_info + "_" + TOPSAR_split_param + "_"
    # print(saveNamePrefix)

    t1_spt = GPF.createProduct("TOPSAR-Split", parameters, product_t1)
    # ProductIO.writeProduct(t1_spt, saveNamePrefix + "t1_spt_v1", 'BEAM-DIMAP')

    t1_spt_orb = GPF.createProduct("Apply-Orbit-File", parameters, t1_spt)

    t2_spt = GPF.createProduct("TOPSAR-Split", parameters, product_t2)
    t2_spt_orb = GPF.createProduct("Apply-Orbit-File", parameters, t2_spt)

    prods = []
    prods.append(t1_spt_orb)
    prods.append(t2_spt_orb)

    print("Back-Geocoding...")
    gcd = GPF.createProduct("Back-Geocoding", parameters, prods)
    # ProductIO.writeProduct(gcd, saveNamePrefix + "gcd", 'BEAM-DIMAP')

    print("Interferogram...")
    ifg = GPF.createProduct("Interferogram", parameters, gcd)
    # ProductIO.writeProduct(ifg, saveNamePrefix + "ifg", 'BEAM-DIMAP')

    print("TOPSAR-Deburst...")
    dbt = GPF.createProduct("TOPSAR-Deburst", parameters, ifg)
    # ProductIO.writeProduct(dbt, saveNamePrefix + "dbt", 'BEAM-DIMAP')

    print("TopoPhaseRemoval...")
    tpr = GPF.createProduct("TopoPhaseRemoval", parameters, dbt)
    # ProductIO.writeProduct(tpr, saveNamePrefix + "tpr", 'BEAM-DIMAP')

    print("Multilook...")
    ml = GPF.createProduct("Multilook", parameters, tpr)
    # ProductIO.writeProduct(ml, saveNamePrefix + "ml", 'BEAM-DIMAP')

    # ### ProgressMonitor
    PrintPM = jpy.get_type('com.bc.ceres.core.PrintWriterProgressMonitor')
    ConcisePM = jpy.get_type('com.bc.ceres.core.PrintWriterConciseProgressMonitor')
    System = jpy.get_type('java.lang.System')
    pm = PrintPM(System.out)

    # # ProductIO.writeProduct(TC, terrain, 'GeoTIFF')
    print("GoldsteinPhaseFiltering...")
    flt = GPF.createProduct("GoldsteinPhaseFiltering", parameters, ml)
    ProductIO.writeProduct(flt, saveNamePrefix + "tpr_ml204_flt", 'BEAM-DIMAP', pm)

    ### SUBSET
    WKTReader = snappy.jpy.get_type('com.vividsolutions.jts.io.WKTReader')
    # wkt = "POLYGON((12.76221 53.70951, " \
    #       "12.72085 54.07433, " \
    #       "13.58674 54.07981, " \
    #       "13.59605 53.70875, " \
    #       "12.76221 53.70951))"
    wkt = "POLYGON((19.277 59.113, " \
          "19.277 59.463, " \
          "17.628 59.463, " \
          "17.628 59.113, " \
          "19.277 59.113))"
    geom = WKTReader().read(wkt)

    param_sub = HashMap()
    param_sub.put('geoRegion', geom)
    param_sub.put('outputImageScaleInDb', False)

    print("Subset...")
    sub = GPF.createProduct("Subset", param_sub, flt)
    ProductIO.writeProduct(sub, saveNamePrefix + "tpr_ml204_flt_sub", 'BEAM-DIMAP', pm)

    ### Terrain-Correction
    print("Terrain-Correction...")
    TC = GPF.createProduct("Terrain-Correction", parameters, flt)
    ProductIO.writeProduct(TC, saveNamePrefix + "tpr_ml204_flt_sub_TC80", 'BEAM-DIMAP', pm)

print("================ finished! ==================")
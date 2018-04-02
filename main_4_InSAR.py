import snappy

from snappy import jpy, ProgressMonitor, ProductIO
from snappy import HashMap

import os, gc
from snappy import GPF

GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
HashMap = snappy.jpy.get_type('java.util.HashMap')

output = []
sat = [] # # S1A, S1B
date = []
date_output_dict = {}
path = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\DSC_orb22_Scene_2_S1_zip\\"
# for folder in os.listdir(path):
#     gc.enable()
#
#     # output.append(path + folder + "\\")
#     output.append(path + folder)
#     sat.append(folder.split("_")[0]) # S1A, S1B
#
#     print(folder)
#     timestamp = folder.split("_")[5]
#     date.append(timestamp[:8])

for folder in os.listdir(path):
    gc.enable()

    # output.append(path + folder + "\\")
    output.append(path + folder)
    sat.append(folder.split("_")[0]) # S1A, S1B

    print(folder)
    timestamp = folder.split("_")[5]
    cur_date = timestamp[:8]
    date.append(cur_date)

    date_output_dict[cur_date] = path + folder

    # print(folder, timestamp, date)
date.sort()
print(date)



idx = 0
in1 = date_output_dict[date[idx]]
in2 = date_output_dict[date[idx + 1]]

# print(date[idx], date[idx + 1])
print(in1)
print(in2)

sat1 = in1.split("\\")[3][:3]  # obtain sensor name : 'S1A' or 'S1B'
sat2 = in2.split("\\")[3][:3]

product_t1 = ProductIO.readProduct(in1)
product_t2 = ProductIO.readProduct(in2)


# product_t1 = ProductIO.readProduct(output[0] + "\\manifest.safe")
# product_t2 = ProductIO.readProduct(output[1] + "\\manifest.safe")

# product_t1 = ProductIO.readProduct(output[0])
# product_t2 = ProductIO.readProduct(output[1])

print(product_t1)
print(product_t2)

# print(sat[0], sat[1])
#
# print(date[0])
# print(date[1])

roi_name = 'Stockholm'
t1_info = date[0] + "_[" + sat[0] + "_" + date[0]
t2_info = sat[1] + "_" + date[1] + "]"



# pols = ['VH', 'VV']
# for p in pols:
# p = 'VV'
# polarization = p

polarization = 'VV'
subswath = 'IW2'
burstStart = 1
burstEnd = 4

SAVE_path = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\InSAR_gpf_results\\"
isExist = os.path.exists(SAVE_path)
if not isExist:
    os.mkdir(SAVE_path)

TOPSAR_split_param = subswath + '_' + polarization + '_b' + str(burstStart) + '_' + str(burstEnd)
saveNamePrefix = SAVE_path + roi_name + "_" + t1_info + "_" + t2_info + "_" + TOPSAR_split_param + "_"



### Set Params
params={
    # TOPSAR-split
    "subswath": subswath,
    "selectedPolarisations": polarization,
    "firstBurstIndex": burstStart,
    "lastBurstIndex": burstEnd,

    # Apply-Orbit-File
    "continuteOnFail": True,
    "orbitType" : "Sentinel Precise (Auto Download)",

    # back-Geocoding
    "demResamplingMethod" : "BICUBIC_INTERPOLATION",
    "resamplingType": "BISINC_5_POINT_INTERPOLATION",
    "maskOutAreaWithoutElevation": True,
    "outputDerampDemodPhase": True,

    # Interferogram
    "subtractFlatEarthPhase": True,
    "srpPolynomialDegree" : 5, #Order of 'Flat earth phase' polynomial
    "srpNumberPoints": 501, # Number of points for the 'flat earth phase' polynomial estimation
    "includeCoherence": True,
    "squarePixel": False,
    "Independent Window Sizes": False,
    "cohWinAz": 10, # Size of coherence estimation window in Azimuth direction
    "cohWinRg": 10, # Size of coherence estimation window in Range direction


    # TOPSAR-Deburst

    # TopoPhaseRemoval
    "orbitDegree": 3,
    "tileExtensionPercent": '100',
    "outputTopoPhaseBand=": True, # Output topographic phase band

    # Multilook
    "grSquarePixel": False,
    "nRgLooks": 20, # Number of Range Looks
    "nAzLooks": 4, #Number of Azimuth Looks

    # GoldsteinPhaseFiltering
    "alpha": 1.0, # adaptive filter exponent Valid interval is (0, 1].


    # Terrain-Correction
    "pixelSpacingInMeter": 80.0,
    "outputComplex": True
}

# Parameters Assignments
parameters = HashMap()
for a in params:
    # print(a)
    parameters.put(a, params[a])


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
ProductIO.writeProduct(flt, saveNamePrefix + "tpr_ml_flt", 'BEAM-DIMAP', pm)

print("Terrain-Correction...")
TC = GPF.createProduct("Terrain-Correction", parameters, flt)
ProductIO.writeProduct(TC, saveNamePrefix + "tpr_ml_flt_TC", 'BEAM-DIMAP', pm)
print("================ finished! ==================")
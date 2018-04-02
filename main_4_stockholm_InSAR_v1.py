
import time, datetime
from read_all_sorted_filenames import read_sorted_fileNamesList_from
from InSAR_processing import InSAR_graph_processing_4_two_S1_products


### Load Products
# Stockholm
study_area = "Stockholm"
graphName = "DSC_InSAR_bgd_esd_ifg_dbt_tpr_ML51_flt.xml"
dataPath = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\DSC_orb22_Scene_2_S1_zip\\Stockholm_DSC_S1A_zip"
savePath = "F:\\Stockholm_InSAR\\DSC_rorb22_S1A_12days_InSAR_results\\"
graphPath = "D:\\Stockholm\\snappy_InSAR_code\\" + graphName

dataNamesList, datesList = read_sorted_fileNamesList_from(dataPath)

print("================= " + study_area + ": " + str(len(dataNamesList)) + "products to be processed: ================")
for idx in range(len(dataNamesList)):
    print(dataNamesList[idx])


for idx in range(len(dataNamesList)-1):
    firstDateIndex = idx
    secondDateIndex = idx + 1


    print("====================== InSAR Processing on: ... ========================")
    print(dataNamesList[firstDateIndex])
    print(dataNamesList[secondDateIndex])

    product1_name = dataNamesList[firstDateIndex]
    product2_name = dataNamesList[secondDateIndex]

    TOPSARsplitParamDict = {
        "subswath": "IW2",
        "polarization": "VV",
        "burstStart": "1",
        "burstEnd": "4"
    }
    applyTOPSARsplitFlag = True # Apply specified parameters for TOPSAR_split operation or not

    subswath = TOPSARsplitParamDict["subswath"]
    polarization = TOPSARsplitParamDict["polarization"]
    burstStart = TOPSARsplitParamDict["burstStart"]
    burstEnd = TOPSARsplitParamDict["burstEnd"]

    print("====================== Desired TOPSAR-Split Configuration =========================")
    print(subswath, polarization, burstStart, burstEnd)

    # saveFltPostFix = "_bgd_esd_ifg_dbt_tpr_ML51_flt"
    saveFltPostFix = graphName[:len(graphName)-4]
    print("saveFltPostFix: " + saveFltPostFix)

    start = time.clock()
    # InSAR_graph_processing_4_two_S1_products(study_area, graphPath, dataPath, product1_name, product2_name, savePath, saveFltPostFix,
    #                                          TOPSARsplitParamDict, applyTOPSARsplitFlag)

    elapsed = (time.clock() - start)/60
    print("Time Used: " + str(elapsed) + "m")


print("================================= All processing finished! =======================================")

import time, datetime
from read_all_sorted_filenames import read_sorted_fileNamesList_from
from InSAR_processing_with_sliceAss_multiSwaths import InSAR_graph_processing_for_2_S1_productSets

### Load Products
# Stockholm
study_area = "Stockholm"

printGraphConfigurationFlag = True
executeGraphFlag = True # Execute the specified graph or not
applyTerrainCorrectionFlag = True

graphPath = "F:\\snappy_InSAR_code\\graph_xml\\DSC_InSAR_sliceAss_graph\\"
graph1 = "DSC_InSAR_graph1_sliceAss_IW2_VV_b3_15_bgd_ESD_Ifg_deb.xml"
graph2 = "DSC_InSAR_graph2_sliceAss_IW3_VV_b3_16_bgd_ESD_Ifg_deb.xml"
graph3 = "DSC_InSAR_graph3_sliceAss_IW2_IW3_mrg_tpr_ML204_flt.xml"
graphSet = [graph1, graph2, graph3]

dataPath = "F:\\Stockholm_InSAR\\DSC_rorb22_ZIP\\"
savePath = "F:\\Stockholm_InSAR\\DSC_rorb22_InSAR_sliceAss_results_every12days\\"

dataNamesList, datesList = read_sorted_fileNamesList_from(dataPath)

print("================= " + study_area + ": " + str(len(dataNamesList)) + " products to be processed: ================")
for idx in range(len(dataNamesList)):
    print(dataNamesList[idx])

interval = 12 # interval days
step = interval/6*2
for idx in range(0, len(dataNamesList)-step, step): #(0, 2, 2): # (0, len(dataNamesList)-3, 2) len(dataNamesList)-6
    idxProd1 = idx
    idxProd2 = idxProd1 + 1
    idxProd3 = idx + step
    idxProd4 = idxProd3 + 1
    print("([" + str(idxProd1) + "," + str(idxProd2) + "]->[" + str(idxProd3) + "," + str(idxProd4) + "])")

    print("====================== InSAR Processing on: ... ========================")
    print(dataNamesList[idxProd1])
    print(dataNamesList[idxProd2])
    print(dataNamesList[idxProd3])
    print(dataNamesList[idxProd4])

    t1_product1_name = dataNamesList[idxProd1]
    t1_product2_name = dataNamesList[idxProd2]

    t2_product1_name = dataNamesList[idxProd3]
    t2_product2_name = dataNamesList[idxProd4]

    productSet1 = [t1_product1_name, t1_product2_name]
    productSet2 = [t2_product1_name, t2_product2_name]

    print("========================================================================")
    # saveFltPostFix = "DSC_InSAR_sliceAss_" + "_IW2_VV_b4_16" + "_IW3_VV_b4_18_bgd_ESD_Ifg103_deb" + "_mrg_tpr_ML204_flt"
    saveFltPostFix = "DSC_InSAR_sliceAss_" + graph1[26:len(graph1)-20] + graph2[25:len(graph1)-4] + graph3[33:len(graph3)-4]
    print("saveFltPostFix: " + saveFltPostFix)

    print("========================= Graph Executing Info. ========================")
    if executeGraphFlag:
        print("Executing the given graph...")
    else:
        print("Never Execute the given graph.")

    if applyTerrainCorrectionFlag:
        print("Do Terrain-Correction ...")
    else:
        print("Never Do Terrain-Correction.")
    print("=========================================================================")

    start = time.clock()

    InSAR_graph_processing_for_2_S1_productSets(study_area, graphPath, graphSet, dataPath, productSet1, productSet2,
                                                savePath, saveFltPostFix, executeGraphFlag, printGraphConfigurationFlag, applyTerrainCorrectionFlag)

    elapsed = (time.clock() - start)/60
    print("Total Time Used: " + str(elapsed) + "m")


print("================================= All processing finished! =======================================")
import snappy
import os
from snappy import jpy, ProgressMonitor, ProductIO, HashMap, GPF
# from read_all_folders import read_all_folders_in
from read_all_sorted_filenames import read_sorted_fileNamesList_from
# from snappy_write_image import write_image

def InSAR_graph_processing_4_two_S1_products(study_area, graphName, dataPath, product1_name, product2_name, savePath, TOPSARsplitParamDict, applyTOPSARsplitFlag):
    FileReader = jpy.get_type('java.io.FileReader')
    GraphIO = jpy.get_type('org.esa.snap.core.gpf.graph.GraphIO')
    Graph = jpy.get_type('org.esa.snap.core.gpf.graph.Graph')
    GraphProcessor = jpy.get_type('org.esa.snap.core.gpf.graph.GraphProcessor')
    PrintPM = jpy.get_type('com.bc.ceres.core.PrintWriterProgressMonitor')

    roi_name = study_area

    sat1 = product1_name[:3]
    sat2 = product2_name[:3]

    date1 = product1_name.split("_")[5]
    date2 = product2_name.split("_")[5]


    t1_info = date1 + "_[" + sat1 + "_" + date1
    t2_info = sat2 + "_" + date2 + "]"

    subswath = TOPSARsplitParamDict["subswath"]
    polarization = TOPSARsplitParamDict["polarization"]
    burstStart = TOPSARsplitParamDict["burstStart"]
    burstEnd = TOPSARsplitParamDict["burstEnd"]

    TOPSAR_split_param = subswath + '_' + polarization + '_b' + str(burstStart) + '_' + str(burstEnd)
    saveFileName = roi_name + "_" + t1_info + "_" + t2_info + "_" + TOPSAR_split_param
    print("Prefix of savedFile: " + saveFileName)

    ### Load Graph
    graphFile = FileReader(graphName)
    graph = GraphIO.read(graphFile)

    saveFileName = saveFileName + "_bgd_ifg_dbt_tpr_ml_flt"

    ### Set parameters for TOPSAR-Split operations
    if applyTOPSARsplitFlag:
        topSARsplitParam = [subswath, polarization, burstStart, burstEnd]
        for node_id in ["TOPSAR-Split", "TOPSAR-Split(2)"]:
            for i in range(len(topSARsplitParam)):
                graph.getNode(node_id).getConfiguration().getChild(i).setValue(topSARsplitParam[i])
            # print(node_id, graph.getNode(node_id).getConfiguration().toXml())
    print("======================= Used TOPSAR-Split Configuration ===========================")
    print(graph.getNode("TOPSAR-Split").getConfiguration().toXml())
    print("===================================================================================")

    ###
    # print("====================== Before Configuration ============================")
    # print(graph.getNode("read").getConfiguration().toXml())
    # print(graph.getNode("read(2)").getConfiguration().toXml())
    # print(graph.getNode('write').getConfiguration().toXml())

    graph.getNode("read").getConfiguration().getChild(0).setValue(dataPath + product1_name) #
    graph.getNode("read(2)").getConfiguration().getChild(0).setValue(dataPath + product2_name) # product2_name

    saveFltPath = savePath + "GoldsteinPhaseFiltering_results\\"
    if not os.path.exists(saveFltPath):
        os.makedirs(saveFltPath)
    graph.getNode("write").getConfiguration().getChild(0).setValue(saveFltPath + saveFileName)

    # print("====================== After Configuration ============================")
    # print(graph.getNode("read").getConfiguration().toXml())
    # print(graph.getNode("read(2)").getConfiguration().toXml())
    # print(graph.getNode('write').getConfiguration().toXml())


    ### or a more concise implementation
    ConcisePM = jpy.get_type('com.bc.ceres.core.PrintWriterConciseProgressMonitor')
    System = jpy.get_type('java.lang.System')
    pm = PrintPM(System.out)

    ### Execute Graph
    GraphProcessor = GraphProcessor()
    print("savedFltName:", saveFltPath + saveFileName)
    GraphProcessor.executeGraph(graph, pm) # ============================================== Save "..._Flt.dim"===================

    ### define for writing images
    ImageManager = jpy.get_type('org.esa.snap.core.image.ImageManager')
    JAI = jpy.get_type('javax.media.jai.JAI')

    def write_image(band, filename, format):
        im = ImageManager.getInstance().createColoredBandImage([band], band.getImageInfo(), 0)
        JAI.create("filestore", im, filename, format)

    ### =============== Terrain-Correction ====================
    print("Terrain-Correction...")

    savedFlt = ProductIO.readProduct(saveFltPath + saveFileName + '.dim') # # ================= Read "..._Flt.dim"===================
    write_image(savedFlt.getBandAt(3), saveFltPath + saveFileName + "_phase.png", "PNG")
    write_image(savedFlt.getBandAt(5), saveFltPath + saveFileName + "_coh.png", "PNG")

    params = {
        # Terrain-Correction
        "demName": "SRTM 3Sec",
        "pixelSpacingInMeter": 20.0, # #20
        "outputComplex": True,
        "externalDEMApplyEGM": True,
        "demResamplingMethod": "BILINEAR_INTERPOLATION",
        "imgResamplingMethod": "BILINEAR_INTERPOLATION"
    }

    parameters = HashMap()
    for a in params:
        # print(a)
        parameters.put(a, params[a])

    TC = GPF.createProduct("Terrain-Correction", parameters, savedFlt)
    saveFileName = saveFileName + "_TC"

    ### Write "..._TC.dim"
    # ProductIO.writeProduct(TC, savePath + saveFileName, 'BEAM-DIMAP', pm) # ============== Save "..._Flt_TC.dim"===================

    ### Read " ...TC.dim" and Write coherence band as an image in Tiff format.
    # savedTC = ProductIO.readProduct(savePath + saveFileName + '.dim')
    savedTC = TC

    ### Delete other bands except for coherence band
    for i in range(4):
        # print("Deleted band: ", savedTC.getBandAt(0))
        savedTC.removeBand(savedTC.getBandAt(0))

    saveCohPath = savePath + "Flt_TC_coherence_maps\\"
    if not os.path.exists(saveCohPath):
        os.makedirs(saveCohPath)
    print("savedCohMap: ", saveCohPath + saveFileName + "_coh")
    ProductIO.writeProduct(savedTC, saveCohPath + saveFileName + "_coh", 'GeoTIFF', pm) # =========== Save coherence map =======================
    write_image(savedTC.getBandAt(0), saveCohPath + saveFileName + "_coh.png", "PNG")


### =======================================================================================================
### ============================================= main script =============================================
### =======================================================================================================
### Load Products
# Stockholm
study_area = "Stockholm_city"
dataPath = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\DSC_orb22_Scene_2_S1_zip\\"
savePath = "D:\\Stockholm\\Descending\\DSC_orb22_Scene2_InSAR_ESD\\"
graphName = "D:\\Stockholm\\snappy_InSAR_code\\DSC_TOPSAR_Coreg_Esd_Ifg_wo_TC.xml"

dataNamesList, datesList = read_sorted_fileNamesList_from(dataPath)

print("================= " + study_area + ": data list to be processed: ================")
for idx in range(len(dataNamesList)):
    print(dataNamesList[idx])

# for idx in range(18, len(dataNamesList)-1):
for idx in range(0, 2):
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

    InSAR_graph_processing_4_two_S1_products(study_area, graphName, dataPath, product1_name, product2_name, savePath,
                                             TOPSARsplitParamDict, applyTOPSARsplitFlag)

print("================================= All processing finished! =======================================")

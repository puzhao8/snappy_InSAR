import snappy
import os, time, shutil
from snappy import jpy, ProgressMonitor, ProductIO, HashMap, GPF
# from read_all_folders import read_all_folders_in

# from snappy_write_image import write_image

def InSAR_graph_processing_for_2_S1_productSets(study_area, graphPath, graphSet, dataPath, productSet1, productSet2,
                                                savePath, saveFltPostFix, executeGraphFlag, printGraphConfigurationFlag,
                                                applyTerrainCorrectionFlag):
    FileReader = jpy.get_type('java.io.FileReader')
    GraphIO = jpy.get_type('org.esa.snap.core.gpf.graph.GraphIO')
    Graph = jpy.get_type('org.esa.snap.core.gpf.graph.Graph')
    GraphProcessor = jpy.get_type('org.esa.snap.core.gpf.graph.GraphProcessor')
    PrintPM = jpy.get_type('com.bc.ceres.core.PrintWriterProgressMonitor')

    t1_product1_name = productSet1[0]
    t1_product2_name = productSet1[1]

    t2_product1_name = productSet2[0]
    t2_product2_name = productSet2[1]

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    roi_name = study_area

    sat1 = t1_product1_name[:3]
    sat2 = t2_product1_name[:3]

    date1 = t1_product1_name.split("_")[5][:8]
    date2 = t2_product1_name.split("_")[5][:8]

    t1_info = date1 + "_[" + sat1 + "_" + date1
    t2_info = sat2 + "_" + date2 + "]"


    saveFileName = roi_name + "_" + t1_info + "_" + t2_info + "_"
    print("Prefix of savedFile: " + saveFileName)

    graph1_name = graphSet[0] # IW2...deb
    graph2_name = graphSet[1] # IW3...deb
    graph3_name = graphSet[2] # IW2_IW3_mrg_tpr_ml_flt


    ### load graph1 for processing ProduceSet1
    graphFile1 = FileReader(graphPath + graph1_name)
    graph1 = GraphIO.read(graphFile1)
    saveDeb1Name = saveFileName + graph1_name[26:len(graph1_name)-4]      # IW2_VV_b4_16_bgd_ESD_Ifg103_deb

    ### load graph2 for processing ProduceSet1
    graphFile2 = FileReader(graphPath + graph2_name)
    graph2 = GraphIO.read(graphFile2)
    saveDeb2Name = saveFileName + graph2_name[26:len(graph2_name)-4]      # IW3_VV_b4_18_bgd_ESD_Ifg103_deb

    ### load graph3 for merging debursted products
    graphFile3 = FileReader(graphPath + graph3_name)
    graph3 = GraphIO.read(graphFile3)

    # saveFltPostFix = "_bgd_ifg_dbt_tpr_ml_flt"
    saveFltName = saveFileName + saveFltPostFix

    if printGraphConfigurationFlag:
        print("======================= Used TOPSAR-Split Configuration ===========================")
        print("-------------------------------------------------------")
        print("graph1 TOPSAR-Split Configuration: ")
        print("-------------------------------------------------------")
        print(graph1.getNode("TOPSAR-Split").getConfiguration().toXml())
        print("-------------------------------------------------------")
        print("graph2 TOPSAR-Split Configuration: ")
        print("-------------------------------------------------------")
        print(graph2.getNode("TOPSAR-Split").getConfiguration().toXml())
        print("===================================================================================")

    ###
    # print("====================== Before Configuration ============================")
    # print(graph.getNode("read").getConfiguration().toXml())
    # print(graph.getNode("read(2)").getConfiguration().toXml())
    # print(graph.getNode('write').getConfiguration().toXml())


    saveDebPath = savePath + "TOPSAR_Deburst_results\\"
    if not os.path.exists(saveDebPath):
        os.makedirs(saveDebPath)

    saveFltPath = savePath + "GoldsteinPhaseFiltering_results\\"
    if not os.path.exists(saveFltPath):
        os.makedirs(saveFltPath)

    graph1.getNode("ProductSet-Reader").getConfiguration().getChild(0).setValue(dataPath + t1_product1_name + "," + dataPath + t1_product2_name)  #
    graph1.getNode("ProductSet-Reader(2)").getConfiguration().getChild(0).setValue(dataPath + t2_product1_name + "," + dataPath + t2_product2_name)
    graph1.getNode("Write").getConfiguration().getChild(0).setValue(saveDebPath + saveDeb1Name)

    graph2.getNode("ProductSet-Reader").setConfiguration(graph1.getNode("ProductSet-Reader").getConfiguration())
    graph2.getNode("ProductSet-Reader(2)").setConfiguration(graph1.getNode("ProductSet-Reader(2)").getConfiguration())
    graph2.getNode("Write").getConfiguration().getChild(0).setValue(saveDebPath + saveDeb2Name)

    graph3.getNode("ProductSet-Reader").getConfiguration().getChild(0).setValue(saveDebPath + saveDeb1Name +".dim,"+ saveDebPath + saveDeb2Name + ".dim")
    graph3.getNode("Write").getConfiguration().getChild(0).setValue(saveFltPath + saveFltName)

    # print("====================== After Configuration ============================")
    # print(graph.getNode("read").getConfiguration().toXml())
    # print(graph.getNode("read(2)").getConfiguration().toXml())
    # print(graph.getNode('write').getConfiguration().toXml())

    if printGraphConfigurationFlag:
        print("======================= Used ProductSet-Reader and Write Configuration ===========================")
        print("-------------------------------------------------------")
        print("graph1: ")
        print("-------------------------------------------------------")
        print(graph1.getNode("ProductSet-Reader").getConfiguration().toXml())
        print(graph1.getNode("ProductSet-Reader(2)").getConfiguration().toXml())
        print(graph1.getNode("Write").getConfiguration().toXml())

        print("-------------------------------------------------------")
        print("graph2: ")
        print("-------------------------------------------------------")
        print(graph2.getNode("ProductSet-Reader").getConfiguration().toXml())
        print(graph2.getNode("ProductSet-Reader(2)").getConfiguration().toXml())
        print(graph2.getNode("Write").getConfiguration().toXml())

        print("-------------------------------------------------------")
        print("graph3: ")
        print("-------------------------------------------------------")
        print(graph3.getNode("ProductSet-Reader").getConfiguration().toXml())
        print(graph3.getNode("Write").getConfiguration().toXml())


    ### or a more concise implementation
    ConcisePM = jpy.get_type('com.bc.ceres.core.PrintWriterConciseProgressMonitor')
    System = jpy.get_type('java.lang.System')
    pm = PrintPM(System.out)

    ### Execute Graph
    GraphProcessor = GraphProcessor()
    print("savedFltName:", saveFltPath + saveFltName)

    # executeGraphFlag = True
    if executeGraphFlag:
        # if not os.path.exists(saveDebPath + saveDeb1Name + ".dim"):
        print("Start to execute graph1 ...")
        start = time.clock()
        GraphProcessor.executeGraph(graph1, pm) # ============================================== Save "..._Flt.dim"===================
        elapsed = (time.clock() - start) / 60
        print("Time Used by graph1: " + str(elapsed) + "m")
        print("-------------------------------------------------------")

        # if not os.path.exists(saveDebPath + saveDeb2Name + ".dim"):
        print("Start to execute graph2 ...")
        start = time.clock()
        GraphProcessor.executeGraph(graph2, pm)
        elapsed = (time.clock() - start) / 60
        print("Time Used by graph2: " + str(elapsed) + "m")
        print("-------------------------------------------------------")

        # if not os.path.exists(saveFltPath + saveFltName + ".dim"):
        print("Start to execute graph3 ...")
        start = time.clock()
        GraphProcessor.executeGraph(graph3, pm)
        elapsed = (time.clock() - start) / 60
        print("Time Used by graph3: " + str(elapsed) + "m")
        print("-------------------------------------------------------")

    ### define for writing images
    ImageManager = jpy.get_type('org.esa.snap.core.image.ImageManager')
    JAI = jpy.get_type('javax.media.jai.JAI')

    def write_image(band, filename, format):
        im = ImageManager.getInstance().createColoredBandImage([band], band.getImageInfo(), 0)
        JAI.create("filestore", im, filename, format)


    # applyTerrainCorrectionflag = False
    if applyTerrainCorrectionFlag:
        ### =============== Terrain-Correction ====================
        print("Terrain-Correction...")

        savedFlt = ProductIO.readProduct(saveFltPath + saveFltName + '.dim')  # # ================= Read "..._Flt.dim"===================
        write_image(savedFlt.getBandAt(3), saveFltPath + saveFltName + "_phase.png", "PNG")
        write_image(savedFlt.getBandAt(5), saveFltPath + saveFltName + "_coh.png", "PNG")



        pixelSpacing = 80
        params = {
            # Terrain-Correction
            "demName": "SRTM 3Sec",
            "pixelSpacingInMeter": float(pixelSpacing),
            "outputComplex": False,
            "externalDEMApplyEGM": True,
            "demResamplingMethod": "BILINEAR_INTERPOLATION",
            "imgResamplingMethod": "BILINEAR_INTERPOLATION",
            "nodataValueAtSea": False
        }

        parameters = HashMap()
        for a in params:
            # print(a)
            parameters.put(a, params[a])

        TC = GPF.createProduct("Terrain-Correction", parameters, savedFlt)
        saveTCname = saveFltName + "_TC" + str(pixelSpacing)

        ### Write "..._TC.dim"
        # ProductIO.writeProduct(TC, savePath + saveFileName, 'BEAM-DIMAP', pm) # ============== Save "..._Flt_TC.dim"===================

        ### Read " ...TC.dim" and Write coherence band as an image in Tiff format.
        # savedTC = ProductIO.readProduct(savePath + saveFileName + '.dim')
        savedTC = TC

        ### Delete other bands except for coherence band
        for i in range(savedTC.getNumBands()-1):
            # print("Deleted band: ", savedTC.getBandAt(0))
            savedTC.removeBand(savedTC.getBandAt(0))

        saveCohPath = savePath + "Flt_TC_coherence_maps\\"
        if not os.path.exists(saveCohPath):
            os.makedirs(saveCohPath)

        print("savedCohMap: ", saveCohPath + saveTCname + "_coh")
        ProductIO.writeProduct(savedTC, saveCohPath + saveTCname + "_coh", 'GeoTIFF', pm)  # =========== Save coherence map =======================
        write_image(savedTC.getBandAt(0), saveCohPath + saveTCname + "_coh.png", "PNG")

    # shutil.rmtree(saveDebPath)  # Delete Intermediate Data
    # os.system("rd/s/q " + saveDebPath)
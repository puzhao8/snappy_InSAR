import snappy
from snappy import jpy, ProgressMonitor, ProductIO
from read_all_folders import read_all_folders_in


FileReader = jpy.get_type('java.io.FileReader')
GraphIO = jpy.get_type('org.esa.snap.core.gpf.graph.GraphIO')
Graph = jpy.get_type('org.esa.snap.core.gpf.graph.Graph')
GraphProcessor = jpy.get_type('org.esa.snap.core.gpf.graph.GraphProcessor')
PrintPM = jpy.get_type('com.bc.ceres.core.PrintWriterProgressMonitor')

### Load Products
path = "D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\DSC_orb22_Scene_2_S1_zip\\"
folders = read_all_folders_in(path)
print(folders)

product_t1 = ProductIO.readProduct(folders[0])
product_t2 = ProductIO.readProduct(folders[1])

### Load Graph
graphFile = FileReader("D:\\Stockholm\\Descending\\DSC_orb22_Scene_2\\stockholm_DSC_TOPSAR_Coreg_Ifg_wo_TC.xml")


graph = GraphIO.read(graphFile)

# graph('sourceProducts', [product_t1, product_t2])
# graph(targetProduct', path + 'target')


### Execute Graph
GraphProcessor = GraphProcessor()


### or a more concise implementation
ConcisePM = jpy.get_type('com.bc.ceres.core.PrintWriterConciseProgressMonitor')
System = jpy.get_type('java.lang.System')
pm = PrintPM(System.out)
# ProductIO.writeProduct(resultProduct, outPath, "NetCDF-CF", pm)

# GraphProcessor.executeGraph(graph, ProgressMonitor.NULL)
GraphProcessor.executeGraph(graph, pm)
# GraphProcessor.executeGraph(graph)


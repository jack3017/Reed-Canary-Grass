ROI_PLOT_LIST = [2,5,8,23,19,10,34]
#shape = iface.addVectorLayer("C:/Users/Mason/reed/shapes/treatment_areas/DT_TreatmentAreas_2913_20201029.shp",'','ogr')
#print('\n')
root_dir = r'C:\Users\Mason\reed\matrix_tif_data'
from osgeo import gdal
gdal.AllRegister()

#    Flyover will need to be changed manually (or commented/uncommented) based off of the current date being viewed in the GIS
flyover = '2019-04-03'
#flyover = '2019-04-17'
#flyover = '2019-05-01'
#flyover = '2019-05-17'
#flyover = '2019-05-29'
#flyover = '2019-06-12'
#flyover = '2019-07-24'
#flyover = '2019-08-08'
#flyover = '2019-08-22'
#flyover = '2019-09-04'
#flyover = '2019-09-19'
#flyover = '2019-10-09'
#flyover = '2019-10-23'

dir = root_dir+'\\'+flyover+'\\'

fp = 'Plot_'
fs = '_check.tif'

tfws = '_check.tfw'
#This had to be run a few times for each flyover to get the size adjustment to line up correctly, current_size_offset will have to be updated based off of the print on line 70 until average_size_discrepency (printed on line 69) is exactly 1
current_size_offset = 0.08460646493111128
tfwsize = str(current_size_offset)
#This will read in all the tifs in the PNGS folder and place them in the QGIS project, using .tifw files so that they line up perfectly
layers = QgsProject.instance().mapLayers().values()
average_size_discrepency = 0
for layer in layers:
    print(layer.name())
    if layer.name() == "DT_TreatmentAreas_2913_20201029":
        for feature in layer.getFeatures():
            attrs = feature.attributes()
            bbox = feature.geometry().boundingBox()
            id = str(feature.id())
            x_min = bbox.xMinimum()
            y_min = bbox.yMinimum()
            x_max = bbox.xMaximum()
            y_max = bbox.yMaximum()
            infile = dir+fp+id+fs
                        
            if feature.id() in ROI_PLOT_LIST:
                f = open(dir+fp+id+tfws,"w")
                f.write(tfwsize+"\n0\n0\n-"+tfwsize+"\n"+str(x_min)+'\n'+str(y_min+(y_max-y_min)))
                f.close()
                
                tif = iface.addRasterLayer(infile,id)
                tif.setCrs(QgsCoordinateReferenceSystem('EPSG:2913'))
                rasterTransparency = tif.renderer().rasterTransparency()
                listPixels = []
                pixel = QgsRasterTransparency.TransparentThreeValuePixel()
                pixel.red = 0
                pixel.green = 0
                pixel.blue = 0
                pixel.percentTransparent = 100
                listPixels.append(pixel)
                rasterTransparency.setTransparentThreeValuePixelList(listPixels)
                tif.triggerRepaint()
                size_discrepency = (y_max-y_min)/(tif.extent().yMaximum()-tif.extent().yMinimum())
                average_size_discrepency = average_size_discrepency + size_discrepency
                #print(size_discrepency)
average_size_discrepency = average_size_discrepency/7
print(average_size_discrepency)
print(current_size_offset/(1/average_size_discrepency))

#CHANGE current_size_offset based off of this print ^ on line 70
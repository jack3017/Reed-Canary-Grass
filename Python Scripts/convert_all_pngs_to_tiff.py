#CHANGE root_dir IN mle_data.py before running anything!
import os
from PIL import Image

#CHANGE root_dir IN mle_data.py before running anything!
import mle_data.py
root_dir = mle_data.root_dir

#this converts all pngs from the MLE,py output into tifs to be imported into gis for the confusion matrix data collection

for flyover in os.listdir(root_dir):
	suffix = str(flyover).strip('\n')
	dir = root_dir + '\\' + suffix
	print(str(flyover))
	print(str(dir))
	
	for plot in os.listdir(dir):		
		if plot.endswith("_check.png"):
			plot_dir_in = dir+'\\'+plot
			infile = plot
			outfile = infile.replace('.png','.tif')
			plot_dir_out = dir+'\\'+outfile
			plot_dir_out = plot_dir_out.replace('PNGs','matrix_tif_data')
			print(plot_dir_out)
			
			image = Image.open(plot_dir_in)
			image.thumbnail(image.size)
			image = image.convert('RGB')
			image.save(plot_dir_out,'TIFF',quality=100)
import os
from PIL import Image

#By Jack McConnell
#This script is a derivation of the "first" script, print_all_tifs.py
#This script replaces the printing with converting, when ran in the home directory of this project it converts every .tif to a .jpg
#The naming convention is weird (".tif.jpg" is the new name, but i will keep this because it makes it more obvious they are conversions)
#This script does not delete the old .tif files so it is safe to run
#I haven't tested this script running multiple times I'm not 100% sure it is a good idea

#save root directory to revert to in loop
root_dir = r'C:\Users\jackm\Desktop\Capstone\tifs'

for flyover in os.listdir(root_dir):
	#save name of next (flyover) directory, remove trailing newline
	suffix = str(flyover).strip('\n')
	#save the flyover directory to go into
	dir = root_dir + '\\' + suffix
	#print the name of the flyover
	print(str(flyover))
	
	#in each flyover directory...
	for wavelength in os.listdir(dir):
		#save the name of the next (wavelength) directory, remove trailing newline
		suffix = str(wavelength).strip('\n') + '\\Plots'
		#save the wavelength directory to go into
		subdir = dir + '\\' + suffix
		#print the name of the wavelength
		print('\t' + str(wavelength))
		
		#for each plot in 
		for plot in os.listdir(subdir):
			#if it is a .tif file...
			if plot.endswith(".tif"):
				#make file name without extension (.tif)
				file = os.path.splitext(str(subdir) + '\\' + str(plot))[0]
				#with .tif extension
				infile = file + '.tif'
				#with .jpg extension
				outfile = infile + '.jpg'
				#print that file is being converted
				print("\t\tgenerating jpg of: " + infile + "...")
				
				#open image
				image = Image.open(infile)
				#thumbnail
				image.thumbnail(image.size)
				#convert to RBG
				image = image.convert('RGB')
				#save as .jpg
				image.save(outfile, 'JPEG', quality=100)
				#print success
				print("\t\t\tgenerated: " + outfile)
				
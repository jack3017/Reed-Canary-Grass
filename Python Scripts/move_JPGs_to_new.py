import os
from shutil import copyfile

#By Jack McConnell
#This script moves all of the JPG images generated with convert_all_tifs_to_jpg.py to the folders created by copy_folder_structure.py

#save root directory to revert to in loop
root_dir = r'C:\Users\jackm\Desktop\Capstone\tifs'
jpgs = root_dir + '\\JPGs'

for flyover in os.listdir(root_dir):
	#save name of next (flyover) directory, remove trailing newline
	suffix = str(flyover).strip('\n')
	#save the flyover directory to go into
	dir = root_dir + '\\' + suffix
	#save the jpg directory version of the flyover directory to go into
	dirjpg = jpgs + '\\' + suffix
	#print the name of the flyover
	print(str(flyover))
	
	#in each flyover directory...
	for wavelength in os.listdir(dir):
		#save the name of the next (wavelength) directory, remove trailing newline
		suffix1 = str(wavelength).strip('\n') + '\\Plots'
		suffix2 = str(wavelength).strip('\n')

		#save the wavelength directory to go into
		subdir = dir + '\\' + suffix1
		#save the corresponding jpg wavelength directory to go into
		subdirjpg = dirjpg + '\\' + suffix2
		#print the name of the wavelength
		print('\t' + str(wavelength))
		
		#for each plot in 
		for plot in os.listdir(subdir):
			#if it is a .jpg file...
			if plot.endswith(".jpg"):
				#save path of source jpg
				plotsrc = subdir + '\\' + plot
				#save path of dest
				plotdst = subdirjpg + '\\' + plot
				
				copyfile(plotsrc, plotdst)
				
				print("\t\t\tmoved: " + plotsrc + " to: " + plotdst)
				
import os

#By Jack McConnell
#This script, when ran in the base directory it is found in, prints the name of every .tif file in the subdirectories
#This script is functionally pretty useless but we can replace the name printing with actually useful code, like converting or analyzing 

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
				#print the name
				print("\t\t" + str(plot))
				
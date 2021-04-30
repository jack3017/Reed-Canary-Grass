import os

#By Jack McConnell
#This script, when ran in the base directory it is found in, takes all the flyover folders (and their sub-folders)
#and copies them to another JPG directory, so I can copy all the JPGs over with the copy_JPGs script

#save root directory to revert to in loop
root_dir = r'C:\Users\jackm\Desktop\Capstone\tifs'
jpgs = root_dir + '\\PNGs'

for flyover in os.listdir(root_dir):
	#save name of next (flyover) directory, remove trailing newline
	suffix = str(flyover).strip('\n')
	#save the flyover directory to go into
	dir = root_dir + '\\' + suffix
	#flyover directory name to create
	created_dir = jpgs + '\\' + suffix
	#make new directory in JPGs folder
	os.mkdir(created_dir)
	
	
	#in each flyover directory...
	for wavelength in os.listdir(dir):
		#save the name of the next (wavelength) directory, remove trailing newline
		suffix = str(wavelength).strip('\n')
		#save the wavelength directory to go into
		subdir = dir + '\\' + suffix
		#save the JPG\Flyover\Wavelength to copy 
		second_created_dir = created_dir + '\\' + suffix
		#make new directory in JPGs\Flyover folder
		os.mkdir(second_created_dir)
	
		

				
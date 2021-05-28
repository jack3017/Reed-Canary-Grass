from PIL import Image as im
import urllib.request
import random
import numpy as np
from matplotlib.pyplot import imshow
import os
import math

#CHANGE root_dir IN mle_data.py before running anything!
import mle_data.py
root_dir = mle_data.root_dir
ROI_STATS = mle_data.ROI_STATS
R05_C = mle_data.R05_C
R05_C_K = mle_data.R05_C_K
R1_C = mle_data.R1_C
R1_C_K = mle_data.R1_C_K
R2_C = mle_data.R2_C
R2_C_K = mle_data.R2_C_K
XX = mle_data.XX
tgs = mle_data.tgs

euler = math.e
pi = math.pi

#main function for MLE caclculation
def MLE(GREEN,RED,REDGE,NIR,flight,tg):
	#initalize the highest likelihood to 0
	max_likelihood = 0.0
	#initalize the ID of the class to -1
	max_likelilood_id = -1
	#loop over all 4 classes
	for i in range(0,4):
		#ROI_STATS dictionary si indexed from 1
		roi = i+1
		
		#The denominators for the new bands, calculated from the 4 bands passed into the function
		NDVI_D = NIR+RED
		GDVI_D = NIR+GREEN
		
		#Set the denominator to a really small number to avoid divide by zero error
		if NDVI_D == 0:
			NDVI_D = 0.00000000001
		if GDVI_D == 0:
			GDVI_D = 0.00000000001
		
		#actual values for new bands
		NDVI = (NIR-RED)/(NDVI_D)
		GDVI = (NIR-GREEN)/(GDVI_D)
		
		#Find the mean and STD DEV for each band, as read from the ROI_STATS table
		MEAN_GREEN = ROI_STATS[flight][550][roi][0]
		STD_GREEN = ROI_STATS[flight][550][roi][1]
		
		MEAN_RED = ROI_STATS[flight][650][roi][0]
		STD_RED = ROI_STATS[flight][650][roi][1]
		
		MEAN_REDGE = ROI_STATS[flight][710][roi][0]
		STD_REDGE = ROI_STATS[flight][710][roi][1]
		
		MEAN_NIR = ROI_STATS[flight][850][roi][0]
		STD_NIR = ROI_STATS[flight][850][roi][1]
		
		#calculate the mean dn stddev's denominators for the new bands from the stats of the other bands
		MEAN_NDVI_D = MEAN_NIR+MEAN_RED
		STD_NDVI_D = STD_NIR+STD_RED
		
		MEAN_GDVI_D = MEAN_NIR+MEAN_GREEN
		STD_GDVI_D = STD_NIR+STD_GREEN
		
		#again,avoid divide by zero error in denominators
		if MEAN_NDVI_D == 0:
			MEAN_NDVI_D = 0.00000000001
		if STD_NDVI_D == 0:
			STD_NDVI_D = 0.00000000001
		if MEAN_GDVI_D == 0:
			MEAN_GDVI_D = 0.00000000001
		if STD_GDVI_D == 0:
			STD_GDVI_D = 0.00000000001
		
		#Finally, the actual stats for the new bands
		MEAN_NDVI = (MEAN_NIR-MEAN_RED)/(MEAN_NDVI_D)
		STD_NDVI = (STD_NIR-STD_RED)/(STD_NDVI_D)
		
		MEAN_GDVI = (MEAN_NIR-MEAN_GREEN)/(MEAN_GDVI_D)
		STD_GDVI = (STD_NIR-STD_GREEN)/(STD_GDVI_D)
		
		#Probablities that the pixel(passed into the function via its 4 bands) is in this class (i+1) based off of each band
		prob_GREEN = MLE_band(GREEN,MEAN_GREEN,STD_GREEN)
		prob_RED = MLE_band(RED,MEAN_RED,STD_RED)
		prob_REDGE = MLE_band(REDGE,MEAN_REDGE,STD_REDGE)
		prob_NIR = MLE_band(NIR,MEAN_NIR,STD_NIR)
		prob_NDVI = MLE_band(NDVI,MEAN_NDVI,STD_NDVI)
		prob_GDVI = MLE_band(NDVI,MEAN_GDVI,STD_GDVI)
		
		#multiply all probabilities together to get total probability that this pixels is in the class i+1
		prob_set = prob_GREEN*prob_RED*prob_REDGE*prob_NIR*prob_NDVI*prob_GDVI
		
		#if this probability is greater than the highest probability for any previous class, then update the return value to that class
		if prob_set > max_likelihood:
			max_likelihood = prob_set
			max_likelilood_id = i
		
	return max_likelilood_id

#Actual equation for probability of a particular variable (band) for a given item (pixel). Probably the only part of the code that has no problems
def MLE_band(x,mean,sd):
	return (1/(sd*(math.pow(2*pi,0.5))))*math.pow(euler,(-1/2)*math.pow(((x-mean)/(sd)),2))

#Loop over every flyover 
for flyover in os.listdir(root_dir):
	print(str(flyover)+":")
	#We skipped 2019-08-08 because we never fully compiled the data for this step as this date was orignally missing the 850nm band
	if flyover != "2019-08-08":
		dir = str(root_dir)+"/"+str(flyover)
		#this is still just to access the files based off of the folder structure
		dir_550 = dir+"/w550n/"
		dir_650 = dir+"/w650n/"
		dir_710 = dir+"/w710n/"
		dir_850 = dir+"/w850n/"
		
		#there were 38 plots, and 1 image for each
		for i in range(0,38):
			print("\t Plot "+str(i)+":")
			file_550 = dir_550+"Plot_"+str(i)+".tif.png"
			file_650 = dir_650+"Plot_"+str(i)+".tif.png"
			file_710 = dir_710+"Plot_"+str(i)+".tif.png"
			file_850 = dir_850+"Plot_"+str(i)+".tif.png"
			
			#initialize number of pixels in the image
			num_pixels = 0
			
			#only one open needs to be saved for later to get the height and width
			#this is because we only get the width and height if they all match anyways
			img_550 = im.open(file_550,"r")
			width,height = img_550.size
			
			#create tables (arrays?,lists?) for each band in the image 
			val_550 = list(img_550.getdata())
			val_650 = list(im.open(file_650,"r").getdata())
			val_710 = list(im.open(file_710,"r").getdata())
			val_850 = list(im.open(file_850,"r").getdata())
			
			#check that the size of each table is the same, if not, we had an error
			if len(val_550) == len(val_650) == len(val_710) == len(val_850):
				num_pixels = len(val_550)
				
				#THE NAMES GRASS,SOIL,TREE,SHRUB WERE ARBITRARY, AS WE DIDN'T ACTUALLY KNOW WHAT THESE CLASSES WERE
				grass_pixels = []
				soil_pixels = []
				tree_pixels = []
				shrub_pixels = []
				black_pixels = []

				num_unknown_pixels = num_pixels
				num_other_pixels = 0
				num_border_pixels = 0
				
				num_grass_pixels = 0
				num_soil_pixels = 0
				num_tree_pixels = 0
				num_shrub_pixels = 0
				num_black_pixels = 0

				#Average reflectance of grass pixels (with class id of 0)
				avg_550 = 0
				avg_650 = 0
				avg_710 = 0
				avg_850 = 0
				
				#initialize an array to place the data for the visual results into, this was not really necessary, but let us view the output and make sure it was working
				visual_img_data = np.zeros((height,width,3),dtype=np.uint8)
				max_550 = 0
				max_650 = 0
				max_710 = 0
				max_850 = 0
				
				#we already checked that the number of pixels in each array was the same, so we can loop through all these pixels
				for j in range(0,num_pixels):
					_550 = val_550[j][0]
					_650 = val_650[j][0]
					_710 = val_710[j][0]
					_850 = val_850[j][0]
					
					#this loop is just to find the highest value at each band, but I think this may be unnecessary at this point in time
					if _550 > max_550:
						max_550 = _550
					if _650 > max_650:
						max_650 = _650
					if _710 > max_710:
						max_710 = _710
					if _850 > max_850:
						max_850 = _850
				#loop over all pixels again	
				for j in range(0,num_pixels):
					_550 = val_550[j][0]
					_650 = val_650[j][0]
					_710 = val_710[j][0]
					_850 = val_850[j][0]
					
					#if the value at all 4 bands is 0, then we know we're looking at a pixel on the border (created by the fact that the actual plot was a rotated rectangle inside a rectangular image)
					if _550 + _650 + _710 + _850 == 0:
						num_border_pixels += 1
						continue
					
					#now we actually run the MLE function on this pixel to get the id of the class that the pixel (most likely) belongs to
					category_id = MLE(_550,_650,_710,_850,flyover,tgs[i]*4-3)
					
					if category_id == -1:
						num_black_pixels += 1
						black_pixels.append(j)
					
					#We only add the values to the average if the class id is 0 because these are (porbably) grass pixels
					if category_id == 0:
						avg_550 += _550
						avg_650 += _650
						avg_710 += _710
						avg_850 += _850
						num_grass_pixels += 1
						grass_pixels.append(j)
					elif category_id == 1:
						num_soil_pixels += 1
						soil_pixels.append(j)
					elif category_id == 2:
						num_tree_pixels += 1
						tree_pixels.append(j)
					elif category_id == 3:
						num_shrub_pixels += 1
						shrub_pixels.append(j)
					else:
						num_other_pixels +=1
					num_unknown_pixels -= 1
					#Number of other pixels and number of unknown pixels should both be 0
				#save the visual image(this is again only to look at, not used in any further calculations, can be removed to save run time)
				visual_img = im.fromarray(visual_img_data,'RGB')
				visual_img_dir = dir+"/"+"Plot_"+str(i)+"_visual.png"
				visual_img.save(visual_img_dir,'JPEG',quality=100)
				print("\t\tSaved Image as "+visual_img_dir)
				#number of grass pixels should pretty much always be more than 0, if we really did have 0 grass pixels than the herbicide worked way too well
				if num_grass_pixels > 0:
					avg_550 /= num_grass_pixels
					avg_650 /= num_grass_pixels
					avg_710 /= num_grass_pixels
					avg_850 /= num_grass_pixels
				else:
					avg_550 = 0
					avg_650 = 0
					avg_710 = 0
					avg_850 = 0

				#Check image was actually used for the confusion matrix. there exists a python script for qgis in the repo to import these to the GIS
				check_img_data = np.zeros((height,width,3),dtype=np.uint8)
				grass_pixel_index = 0
				soil_pixel_index = 0
				tree_pixel_index = 0
				shrub_pixel_index = 0
				black_pixel_index = 0
				#Loop through all pixels in the 1 dimensional list
				for h in range(0,height):
					for w in range(0,width):
						#assign current pixel based off of height and width values
						cur_pixel = width*h+w
						visual_img_data[h,w] = [val_550[cur_pixel][0]*(255/max_550),val_650[cur_pixel][0]*(255/max_650),val_850[cur_pixel][0]*(255/max_850)]
						if grass_pixel_index < len(grass_pixels) and cur_pixel == grass_pixels[grass_pixel_index]:
							check_img_data[h,w] = [64,255,64]
							grass_pixel_index += 1
						if soil_pixel_index < len(soil_pixels) and cur_pixel == soil_pixels[soil_pixel_index]:
							check_img_data[h,w] = [16,128,16]
							soil_pixel_index += 1
						if tree_pixel_index < len(tree_pixels) and cur_pixel == tree_pixels[tree_pixel_index]:
							check_img_data[h,w] = [255,128,255]
							tree_pixel_index += 1
						if shrub_pixel_index < len(shrub_pixels) and cur_pixel == shrub_pixels[shrub_pixel_index]:
							check_img_data[h,w] = [96,32,96]
							shrub_pixel_index += 1
						if black_pixel_index < len(black_pixels) and cur_pixel == black_pixels[black_pixel_index]:
							check_img_data[h,w] = [0,0,0]
							black_pixel_index += 1
				#We don't want to count the black border pixels in the image corners in any calculations
				num_real_pixels = num_pixels-num_border_pixels
				print("\t\tNumber of real pixels (not counting black corners: "+str(num_real_pixels)+"\n")
				print("\t\t\tNumber of light green (probably grass) pixels: "+str(num_grass_pixels)+" ("+str(num_grass_pixels/num_real_pixels*100)+" %)")
				print("\t\t\tNumber of dark green pixels: "+str(num_soil_pixels)+" ("+str(num_soil_pixels/num_real_pixels*100)+" %)")
				print("\t\t\tNumber of light purple pixels: "+str(num_tree_pixels)+" ("+str(num_tree_pixels/num_real_pixels*100)+" %)")
				print("\t\t\tNumber of dark purple pixels: "+str(num_shrub_pixels)+" ("+str(num_shrub_pixels/num_real_pixels*100)+" %)")
				print(" ")
				print("\t\t\tAverage Reflectance of 550nm (out of 255): "+str(avg_550))
				print("\t\t\tAverage Reflectance of 650nm (out of 255): "+str(avg_650))
				print("\t\t\tAverage Reflectance of 710nm (out of 255): "+str(avg_710))
				print("\t\t\tAverage Reflectance of 850nm (out of 255): "+str(avg_850))
				
				#save the image to be imported to the gis for the confusion matrix
				check_img = im.fromarray(check_img_data,'RGB')
				check_img_dir = dir+"/"+"Plot_"+str(i)+"_check.png"
				check_img.save(check_img_dir,'PNG',quality=100)
				
				#save the visual image (again, probably can be removed)
				visual_img = im.fromarray(visual_img_data,'RGB')
				visual_img_dir = dir+"/"+"Plot_"+str(i)+"_visual.png"
				visual_img.save(visual_img_dir,'PNG',quality=100)
				print("\t\tSaved Image as "+check_img_dir)
			else:
				print("\t\tSkipped due to mismatched pixels counts between bands")
	else:
		print("\tSkipped Flyover")
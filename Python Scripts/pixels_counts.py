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
R05_C = mle_data.R05_C
R05_C_K = mle_data.R05_C_K
R1_C = mle_data.R1_C
R1_C_K = mle_data.R1_C_K
R2_C = mle_data.R2_C
R2_C_K = mle_data.R2_C_K
XX = mle_data.XX
tgs = mle_data.tgs

#Just a trimmed down MLE.py to only count the pixels in the resulting images, without recreating the images
for flyover in os.listdir(root_dir):
	print(str(flyover)+":")
	if flyover != "2019-08-08":
		dir = str(root_dir)+"/"+str(flyover)+"/"

		for i in range(0,38):
			print("\t Plot "+str(i)+":")
			img_file = dir+"Plot_"+str(i)+"_check.png"
			
			num_pixels = 0
			
			img = im.open(img_file,"r")
			width,height = img.size
			img_val = list(img.getdata())
			
			num_pixels = len(img_val)
	
			num_light_green_pixels = 0
			num_dark_green_pixels = 0
			num_light_purple_pixels = 0
			num_dark_purple_pixels = 0
			num_black_pixels = 0
			
			
			for j in range(0,num_pixels):
				red = img_val[j][0]
				if red == 64:
					num_light_green_pixels += 1
				elif red == 16:
					num_dark_green_pixels += 1
				elif red == 255:
					num_light_purple_pixels += 1
				elif red == 96:
					num_dark_purple_pixels += 1
				elif red == 0:
					num_black_pixels += 1
				else:
					print("ERROR UNEXPECTED RED VALUE AT PIXEL "+str(j)+"!!!")
			
			num_real_pixels = num_pixels - num_black_pixels
			
			print("\t\tLight Green Pixels: "+str(100*num_light_green_pixels/num_real_pixels)+" %")
			print("\t\tDark Green Pixels: "+str(100*num_dark_green_pixels/num_real_pixels)+" %")
			print("\t\tLight Purple Pixels: "+str(100*num_light_purple_pixels/num_real_pixels)+" %")
			print("\t\tDark Purple Pixels: "+str(100*num_dark_purple_pixels/num_real_pixels)+" %")
	else:
		print("\tSkipped Flyover")
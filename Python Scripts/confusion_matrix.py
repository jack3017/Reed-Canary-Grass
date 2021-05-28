from PIL import Image as im
import urllib.request
import random
import numpy as np
from matplotlib.pyplot import imshow
import os
import math

#CHANGE root_dir IN mle_data.py before running anything!
import mle_data.py
CM_STATS = mle_data.CM_STATS
cat_names = mle_data.cat_names

total_accuracy = 0
total_counted_pixels = 0
total_correct_pixels = 0
for flyover in CM_STATS:
	print("\t"+str(flyover)+":")
	flyover_accuracy = 0
	flyover_counted_pixels = 0
	flyover_correct_pixels = 0
	flyover_matrix = {
		1: [0,0,0,0],
		2: [0,0,0,0],
		3: [0,0,0,0],
		4: [0,0,0,0]
	}
	for tbl in CM_STATS[flyover]:
		for i in range(0,4):
			actual_column = -1
			if i == 0:
				actual_column = 1
			elif i == 1:
				actual_column = 0
			elif i == 2:
				actual_column = 3
			elif i == 3:
				actual_column = 2
			flyover_matrix[tbl[0]][actual_column] += tbl[i+1]
	for i in range(1,5):
		cat_total = 0
		cat_accuracy = 0
		row = ""
		for j in range(0,4):
			count = flyover_matrix[i][j]
			count_string = str(count)
			for k in range(0,5-len(count_string)):
				if k%2 == 1:
					count_string = count_string+" "
				else:
					count_string = " "+count_string
			row = row+"["+count_string+"]"
			cat_total = cat_total + count
		cat_correct = flyover_matrix[i][i-1]
		cat_accuracy = cat_correct/cat_total
		flyover_counted_pixels = flyover_counted_pixels + cat_total
		flyover_correct_pixels = flyover_correct_pixels + cat_correct
		print("\t\t"+str(i)+" ("+cat_names[i]+"):\t"+row+"\tcategory accuracy: "+str(cat_accuracy*100)+"%")
	
	total_counted_pixels = total_counted_pixels + flyover_counted_pixels
	total_correct_pixels = total_correct_pixels + flyover_correct_pixels
	flyover_accuracy = flyover_correct_pixels/flyover_counted_pixels	
	p0 = flyover_accuracy

	row_1_sum = 0
	row_2_sum = 0
	row_3_sum = 0
	row_4_sum = 0
	
	for i in range(0,4):
		row_1_sum = row_1_sum + flyover_matrix[1][i]
	for i in range(0,4):
		row_2_sum = row_2_sum + flyover_matrix[2][i]
	for i in range(0,4):
		row_3_sum = row_3_sum + flyover_matrix[3][i]
	for i in range(0,4):
		row_4_sum = row_4_sum + flyover_matrix[4][i]
	
	# print(row_1_sum,row_2_sum,row_3_sum,row_4_sum)
	
	column_1_sum = 0
	column_2_sum = 0
	column_3_sum = 0
	column_4_sum = 0
	
	for i in range(1,5):
		column_1_sum = column_1_sum + flyover_matrix[i][0]
	for i in range(1,5):
		column_2_sum = column_2_sum + flyover_matrix[i][1]
	for i in range(1,5):
		column_3_sum = column_3_sum + flyover_matrix[i][2]
	for i in range(1,5):
		column_4_sum = column_4_sum + flyover_matrix[i][3]
	
	pe = (row_1_sum*column_1_sum + row_2_sum*column_2_sum + row_3_sum*column_3_sum + row_4_sum*column_4_sum)/(flyover_counted_pixels*flyover_counted_pixels)
	
	_k = (p0-pe)/(1-pe)
	
	# print("\n\t\tflyover p0: "+str(flyover_accuracy))
	# print("\t\tflyover pe: "+str(pe))
	print("\n\t\tK: "+str(_k)+"\n")	
total_accuracy = total_correct_pixels/total_counted_pixels
# print("TOTAL ACCURACY: "+str(total_accuracy*100)+"%")
import pandas as pd
import numpy as np
import os
import cmath 
import skrf as rf
import matplotlib.pyplot as plt
import cv2

def process_mdf_file(mdf_file):

	data_file_mdf = pd.read_csv(mdf_file, sep=" ", header=None,  names=[" ", "FILENAME(string)", "Temp_C(real)", "Vd(real)","Id(real)", "Vg(real)" ])
	data_file_mdf.drop(data_file_mdf.head(2).index,inplace=True)
	data_file_mdf.drop(data_file_mdf.tail(1).index,inplace=True)
	data_file_mdf.drop(data_file_mdf.columns[[0]], axis=1, inplace=True )
	# data_file_mdf
	tabledata = np.asarray(data_file_mdf)
	for rows in range(tabledata.shape[0]):
		tabledata[rows][0] = os.path.split(tabledata[rows][0] .replace("\\","/"))[1]

	return tabledata

def get_data(tabledata):

	transistor_on = []# vg >= -2.35.
	transistor_off = []# vg < -2.35.

	for i in range(len(tabledata)):
	#     print(tabledata[i][4])
		if (float(tabledata[i][4])) < -2.35:
			transistor_off.append(tabledata[i][0])
		else:
			transistor_on.append(tabledata[i][0])

	return transistor_on, transistor_off

def plot_s21(files, graphs_path, dir_name):
	for file in files:
		data_s2p = pd.read_table(os.path.join(dir_name, file), sep=" ", header=None,  names=["Frequency ", "S11 real", "S11 imaginary", "S12 real", "S12 imaginary",  "S21 real", "S21 imaginary",  "S22 real", "S22 imaginary" ])
		data_s2p.drop(data_s2p.head(3).index,inplace=True)

		s2p_data_array = np.asarray(data_s2p)
		s2p_data_array = s2p_data_array.astype('float32')

		s21 = [None] * len(s2p_data_array)
		s21_mag = [None] * len(s2p_data_array)
		s21_phase = [None] * len(s2p_data_array)

		for i in range(len(s2p_data_array)):

			s21[i] = complex(s2p_data_array[i][5] , s2p_data_array[i][6])
			s21_mag[i] = rf.mathFunctions.complex_2_db(s21[i])
			s21_phase[i] = rf.mathFunctions.complex_2_degree(s21[i])

		#         s21_title = head_tail[0] + f'_s21  with  vd: {file[1]} and vg: {file[2]}'
		head_tail = os.path.splitext(file)
		s21_title = head_tail[0] + '_s21.png'

		rf.plotting.plot_polar(s21_mag, s21_phase, x_label=None, y_label=None)#, title=s21_title, show_legend=True)
		rf.plotting.save_all_figs(graphs_path, format=['png'])
		plt.close()

		os.rename(os.path.join(graphs_path,'unnamedPlot.png'),os.path.join(graphs_path,s21_title))



if __name__ == '__main__':


	'''
	mdf_file: Give the mdf file path
	process_mdf_file: processes the mdf file and gives back data in numpy array
	get_data: sorts the data into classes.
	plot_s21: Generates the plots for the given class
	'''


	mdf_file = 'C:/Users/Dell/Desktop/EE work/s2p/SEI_VGQ0VDQ000_T25_s2p/SEI_VGQ0VDQ000_T25.mdf'
	dir_name = os.path.dirname(mdf_file)
	data_folder = dir_name + '_s21'
	if not os.path.exists(data_folder):
		os.makedirs(data_folder)

	on_path = data_folder + '/transistor_on'
	off_path = data_folder + '/transistor_off'

	if not os.path.exists(on_path):
		os.makedirs(on_path)

	if not os.path.exists(off_path):
		os.makedirs(off_path)

	array_data = process_mdf_file(mdf_file)
	transistor_on, transistor_off = get_data(array_data)

	plot_s21(transistor_on, on_path, dir_name)
	plot_s21(transistor_off, off_path, dir_name)
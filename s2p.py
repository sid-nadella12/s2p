import os, sys
import skrf as rf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cmath

# Enter the .s2p data files path here
file_path = 'C:/Users/Dell/Desktop/EE work/s2p/SEI_VGQ0VDQ000_T25_s2p/'

# Give the path where you want the generated graphs to be saved
graphs_path = 'C:/Users/Dell/Desktop/EE work/s2p/SEI_VGQ0VDQ000_T25_s2p_s12_s21/'

# count = 0

# for files in os.listdir(file_path):
# 	head_tail = os.path.splitext(files)
# 	# head_tail[0], head_tail[1]
# 	if head_tail[1] == ".s2p":
# 		ntwk = rf.Network(os.path.join(file_path, files))
# 		plt.title(head_tail[0])
# 		ntwk.plot_s_smith()
# 		rf.plotting.save_all_figs(graphs_path, format=['png'])
# 		plt.close()

def polar_plot(s2p_file):

	data_s2p = pd.read_table(s2p_file, sep=" ", header=None,  names=["Frequency ", "S11 real", "S11 imaginary", "S12 real", "S12 imaginary",  "S21 real", "S21 imaginary",  "S22 real", "S22 imaginary" ])
	data_s2p.drop(data_s2p.head(3).index,inplace=True)

	s2p_data_array = np.asarray(data_s2p)
	s2p_data_array = s2p_data_array.astype('float32')

	s12 = [None] * len(s2p_data_array)
	s12_mag = [None] * len(s2p_data_array)
	s12_phase = [None] * len(s2p_data_array)

	s21 = [None] * len(s2p_data_array)
	s21_mag = [None] * len(s2p_data_array)
	s21_phase = [None] * len(s2p_data_array)

	for i in range(len(s2p_data_array)):

		s12[i] = complex(s2p_data_array[i][3] , s2p_data_array[i][4])
		s12_mag[i] = abs(s12[i])
		s12_phase[i] = cmath.phase(s12[i])

		s21[i] = complex(s2p_data_array[i][5] , s2p_data_array[i][6])
		s21_mag[i] = abs(s21[i])
		s21_phase[i] = cmath.phase(s21[i])

	file_name = os.path.basename(s2p_file)
	head_tail = os.path.splitext(file_name)

	s12_title = head_tail[0] + '_s12'
	rf.plotting.plot_polar(s12_mag, s12_phase, x_label=None, y_label=None, title=s12_title, show_legend=True)
	rf.plotting.save_all_figs(graphs_path, format=['png'])
	plt.close()

	s21_title = head_tail[0] + '_s21'
	rf.plotting.plot_polar(s21_mag, s21_phase, x_label=None, y_label=None, title=s21_title, show_legend=True)
	rf.plotting.save_all_figs(graphs_path, format=['png'])
	plt.close()	





for files in os.listdir(file_path):
	polar_plot(os.path.join(file_path, files))


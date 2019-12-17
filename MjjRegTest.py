

from root_pandas import read_root
import os
import xgboost as xgb
import argparse
import warnings
import pickle
warnings.simplefilter(action='ignore', category=FutureWarning)
from matplotlib import pyplot
import ROOT
import numpy as np

#Library with input variables and booster configuration
import MjjRegConf 
#Library with auxiliary functions
import MjjRegLib



#***Test function***
def test(raw_test_dataset, cut, output_dataset, path2tree, tree_name, year):
	test_dataset = os.getcwd() + '/dataset/' + 'test_tree.root'
	MjjRegLib.prepare_dataset(raw_test_dataset, test_dataset, path2tree, tree_name, cut)
	input_arr = read_root(test_dataset, columns = MjjRegConf.get_features(), key = path2tree + tree_name)
	
	test_first_ev = 0
	test_last_ev = 	input_arr.shape[0]-1
	
	test_arr = input_arr.loc[test_first_ev:test_last_ev,'leadingJet_pt':]

	reg_model = loaded_model = pickle.load(open(os.getcwd() + '/dataset/XGB_Mjj_Reg_model_' + year + '.xgb', "rb"))
	reg_C_arr = reg_model.predict(data = test_arr)
	
	MjjRegLib.make_output_file(test_dataset, path2tree, tree_name, reg_C_arr, output_dataset)
	print ('Testing successfully compleated!')

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('filename', help = 'use the name of the file to perform mjj regression')
	parser.add_argument('year', help = 'year for train datasets of run2')
	parser.add_argument('--data', help="use <data> file format",action="store_true")
	args = parser.parse_args()


	cut = 'Mjj < 200'
	if args.data:
		path2tree = '/tagsDumper/trees/'
		tree_name = 'bbggSelectionTree'
	else:
		path2tree = ''
		tree_name = 'bbggSelectionTree'
	
	filename = args.filename
	path2data = '/afs/cern.ch/user/s/stzakhar/public/mjj_input/' + args.year + '/'
	raw_test_dataset = path2data + filename
	path2output = '/afs/cern.ch/user/s/stzakhar/public/mjj_output/' + args.year + '/'
	output_dataset = path2output + filename
	
	
	test(raw_test_dataset, cut, output_dataset, path2tree, tree_name, args.year)
	
	MjjRegLib.plot_mjj_bkg(0, 250,100000, path2output, filename, path2tree, tree_name)
#	MjjRegLib.plot_reg_res(output_dataset, path2tree, tree_name)

if __name__ == "__main__":
	main()



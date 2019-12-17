#This file contains functions for configuring regressor input variables & parameters of the model

# get_features() returns a list of the regressor variables for configuring of the input files 
def get_features(key = ''):
	f_list = []
	if key == 'for_train':
		f_list.extend(['mbbNu'])

	f_list.extend([
	'Mjj',
	'leadingJet_pt',
	'leadingJet_eta',
	'leadingJet_mass',
	'leadingJet_e',
	'leadingJet_phi',

	'subleadingJet_pt',
	'subleadingJet_eta',
	'subleadingJet_mass',
	'subleadingJet_e',
	'subleadingJet_phi',

	'ttH_MET',
	'ttH_phiMET',
	'MjjReg_phi12',
	'MjjReg_phi1M',
	'MjjReg_phi2M',
	'leadingJet_DeepCSV',
	'subleadingJet_DeepCSV',
	'rho',
	'nvtx',
	'diHiggs_mass'
	])
	return f_list

#get_booster_params() returns a dictionary of names: key is for old name, value is for new name
def get_new_names():
	new_name = {}	
	new_name['reg_reco_mjj'] 			= 'Mjj'
	new_name['reg_recoJet_1_pt'] 		= 'leadingJet_pt'
	new_name['reg_recoJet_1_eta'] 		= 'leadingJet_eta'
	new_name['reg_recoJet_1_mass'] 		= 'leadingJet_mass'
	new_name['reg_recoJet_1_e']			= 'leadingJet_e'
	new_name['reg_recoJet_1_phi']		= 'leadingJet_phi'

	new_name['reg_recoJet_2_pt']		= 'subleadingJet_pt'
	new_name['reg_recoJet_2_eta']		= 'subleadingJet_eta'
	new_name['reg_recoJet_2_mass']		= 'subleadingJet_mass'
	new_name['reg_recoJet_2_e']			= 'subleadingJet_e'
	new_name['reg_recoJet_2_phi']		= 'subleadingJet_phi'

	new_name['Met_CorPt']				= 'ttH_MET'
	new_name['Met_CorPhi']				= 'ttH_phiMET'
	new_name['reg_recoJet_phi12']		= 'MjjReg_phi12'
	new_name['reg_recoJet_phi1M']		= 'MjjReg_phi1M'
	new_name['reg_recoJet_phi2M']		= 'MjjReg_phi2M'
	new_name['reg_recoJet_1_DeepCSV']	= 'leadingJet_DeepCSV'
	new_name['reg_recoJet_2_DeepCSV']	= 'subleadingJet_DeepCSV'
	new_name['rho']						= 'rho'
	new_name['nvtx']					= 'nvtx'
	new_name['reg_reco_Mbbgg']			= 'diHiggs_mass'
	return new_name

	
#get_booster_params() returns a dictionary of booster parameters 
def get_booster_params():
	params = {}

	params['base_score'] 		=0.5
	params['booster']			='gbtree'
	params['colsample_bylevel']	=1
	params['gamma']				=1
	params['importance_type']	='gain'
	params['learning_rate']		=0.05
	params['max_delta_step']	=0
	params['max_depth']			=15
	params['min_child_weight']	=1
	params['n_estimators']		=100
	params['n_jobs']			=8
	params['nthread']			=None
	params['objective']			='reg:linear'
	params['random_state']		=0
	params['reg_alpha']			=0
	params['reg_lambda']		=1
	params['scale_pos_weight']	=1
	params['silent']			=False
	params['verbosity']			=1
	params['subsample']			=1
	return params



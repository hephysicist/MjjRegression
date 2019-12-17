import os
import numpy as np
from ROOT import TCanvas, TFile, TDirectory, TH1D, TColor, gStyle, TLegend, TLatex, TPad, TF1, TMath, TTree, gDirectory, gPad
import ROOT
import MjjRegConf


def rename_vars(input_tree):
	
	new_name = MjjRegConf.get_new_names()
	
	linkdict = {}
	branch = {}
	input_tree.SetBranchStatus('*', 1)
	for var in new_name.keys():
		input_tree.SetBranchStatus(var, 0)
	output_tree = input_tree.CopyTree('')
	for var in new_name.keys():
		input_tree.SetBranchStatus(var, 1)
		linkdict[var] = np.empty(1, dtype='float32')  
		input_tree.SetBranchAddress(var, linkdict[var])
		branch[var] = output_tree.Branch(new_name[var]	, linkdict[var]	, new_name[var] + '/F')
	
	n_events = input_tree.GetEntries()
	for event in range (0, n_events):
		input_tree.GetEntry(event)
		for var in new_name.keys():
			branch[var].Fill()
		if event % 1000 == 0:
			print('Renaming event {}'.format(event))
	output_tree.Write()
	return output_tree
	


#Makes a copy of the input .root file and puts there additional variables for the regression
def prepare_dataset_train(path2input, path2output, path2tree, tree_name, cut):
	
	input_file = TFile(path2input, 'READ')
	input_tree = input_file.Get(path2tree + tree_name)	
	out_file = TFile(path2output, 'RECREATE')
	
	output_tree = input_tree.CopyTree(cut)
	output_tree.SetName(tree_name)
	output_tree.SetTitle(tree_name)

	reg_recoJet_1_phi  = np.empty(1, dtype='float32')  
	reg_recoJet_2_phi  = np.empty(1, dtype='float32')  
	Met_CorPhi         = np.empty(1, dtype='float32')   
	
	reg_recoJet_phi12 	= np.empty(1, dtype='float32')
	reg_recoJet_phi1M	= np.empty(1, dtype='float32')
	reg_recoJet_phi2M	= np.empty(1, dtype='float32')
	

	output_tree.SetBranchAddress("reg_recoJet_1_phi"	, reg_recoJet_1_phi	)
	output_tree.SetBranchAddress("reg_recoJet_2_phi"	, reg_recoJet_2_phi	)
	output_tree.SetBranchAddress("Met_CorPhi"			, Met_CorPhi		)

	phi12_br = output_tree.Branch("reg_recoJet_phi12"	, reg_recoJet_phi12	, "reg_recoJet_phi12/F"	)
	phi1M_br = output_tree.Branch("reg_recoJet_phi1M"	, reg_recoJet_phi1M	, "reg_recoJet_phi1M/F"	)
	phi2M_br = output_tree.Branch("reg_recoJet_phi2M"	, reg_recoJet_phi2M	, "reg_recoJet_phi2M/F"	)

	n_events = output_tree.GetEntries()
	for event in range (0, n_events):
		output_tree.GetEntry(event)
		
		reg_recoJet_phi12[0] = ROOT.TVector2.Phi_mpi_pi(reg_recoJet_1_phi[0] - reg_recoJet_2_phi[0])
		reg_recoJet_phi12[0] = abs(reg_recoJet_phi12[0])
		
		reg_recoJet_phi1M[0] = ROOT.TVector2.Phi_mpi_pi(reg_recoJet_1_phi[0] - Met_CorPhi[0])
		reg_recoJet_phi1M[0] = abs(reg_recoJet_phi1M[0])
		
		reg_recoJet_phi2M[0] = ROOT.TVector2.Phi_mpi_pi(reg_recoJet_2_phi[0] - Met_CorPhi[0])
		reg_recoJet_phi2M[0] = abs(reg_recoJet_phi2M[0])
	
		phi12_br.Fill()
		phi1M_br.Fill()
		phi2M_br.Fill()
		if event % 1000 == 0:
			print ('event {}'.format(event))
	output_tree =  rename_vars(output_tree)
	output_tree.AutoSave()
	out_file.Close()
	print ('Prepared {} events with <{}> cut'.format( n_events, cut))
	print ('Path to the file: {}'.format(path2output))

#Makes a copy of the input .root file and puts there additional variables for the regression
def prepare_dataset(path2input, path2output, path2tree, tree_name, cut):
	
	input_file = TFile(path2input, 'READ')
	input_tree = input_file.Get(path2tree + tree_name)
	output_file = TFile(path2output, 'RECREATE')
	output_file.mkdir(path2tree)
	output_file.cd(path2tree)
	
	output_tree = input_tree.CopyTree(cut)
	output_tree.SetName(tree_name)
	output_tree.SetTitle(tree_name)

	
	leadingJet_pt		= np.empty(1, dtype='float32')  
	leadingJet_eta		= np.empty(1, dtype='float32') 
	leadingJet_phi		= np.empty(1, dtype='float32')   
	leadingJet_mass		= np.empty(1, dtype='float32')
	leadingJet_e		= np.empty(1, dtype='float32')
	
	
	subleadingJet_pt	= np.empty(1, dtype='float32')
	subleadingJet_eta	= np.empty(1, dtype='float32')
	subleadingJet_phi	= np.empty(1, dtype='float32')  
	subleadingJet_mass	= np.empty(1, dtype='float32')   
	subleadingJet_e		= np.empty(1, dtype='float32')
	   
	ttH_phiMET			= np.empty(1, dtype='float32')   
	
	MjjReg_phi12 	= np.empty(1, dtype='float32')
	MjjReg_phi1M	= np.empty(1, dtype='float32')
	MjjReg_phi2M	= np.empty(1, dtype='float32')

	output_tree.SetBranchAddress("subleadingJet_pt"		, subleadingJet_pt)
	output_tree.SetBranchAddress("subleadingJet_eta"	, subleadingJet_eta)
	output_tree.SetBranchAddress("subleadingJet_phi"	, subleadingJet_phi)
	output_tree.SetBranchAddress("subleadingJet_mass"	, subleadingJet_mass)
	
	output_tree.SetBranchAddress("leadingJet_pt"		, leadingJet_pt)
	output_tree.SetBranchAddress("leadingJet_eta"		, leadingJet_eta)
	output_tree.SetBranchAddress("leadingJet_phi"		, leadingJet_phi)
	output_tree.SetBranchAddress("leadingJet_mass"		, leadingJet_mass)
	

	output_tree.SetBranchAddress("ttH_phiMET", ttH_phiMET)

	phi12_br = output_tree.Branch("MjjReg_phi12"	, MjjReg_phi12	, "MjjReg_phi12/F"	)
	phi1M_br = output_tree.Branch("MjjReg_phi1M"	, MjjReg_phi1M	, "MjjReg_phi1M/F"	)
	phi2M_br = output_tree.Branch("MjjReg_phi2M"	, MjjReg_phi2M	, "MjjReg_phi2M/F"	)

	leadingJet_e_br 	= output_tree.Branch("leadingJet_e"	, leadingJet_e	, "leadingJet_e/F"	)
	subleadingJet_e_br	= output_tree.Branch("subleadingJet_e"	, subleadingJet_e	, "subleadingJet_e/F"	)

	n_events = output_tree.GetEntries()
	for event in range (0, n_events):
		if event % 1000 == 0:
			print('event {}'.format(event))
		output_tree.GetEntry(event)
		
		MjjReg_phi12[0] = ROOT.TVector2.Phi_mpi_pi(leadingJet_phi[0] - subleadingJet_phi[0])
		MjjReg_phi12[0] = abs(MjjReg_phi12[0])
		
		MjjReg_phi1M[0] = ROOT.TVector2.Phi_mpi_pi(leadingJet_phi[0] - ttH_phiMET[0])
		MjjReg_phi1M[0] = abs(MjjReg_phi1M[0])
		
		MjjReg_phi2M[0] = ROOT.TVector2.Phi_mpi_pi(subleadingJet_phi[0] - ttH_phiMET[0])
		MjjReg_phi2M[0] = abs(MjjReg_phi2M[0])

		p1 = leadingJet_pt[0]*np.cosh(leadingJet_eta[0])
		m1 = leadingJet_mass[0]
		leadingJet_e[0] = np.sqrt(p1*p1 + m1*m1)

		p2 = subleadingJet_pt[0]*np.cosh(subleadingJet_eta[0])
		m2 = leadingJet_mass[0]
		subleadingJet_e[0] = np.sqrt(p2*p2 + m2*m2)
		phi12_br.Fill()
		phi1M_br.Fill()
		phi2M_br.Fill()
		
		leadingJet_e_br.Fill()
		subleadingJet_e_br.Fill()

		
	output_tree.AutoSave()
	output_file.Close()
	print ('Prepared {} events with <{}> cut'.format( n_events, cut))
	print ('Path to the file: {}'.format(path2output))

#Makes a tree from the regression results. That is needed for RooFitMjj function
def make_output_file(test_dataset, path2tree, tree_name, reg_C_arr, path2output):

	input_file = ROOT.TFile.Open(test_dataset, 'READ')
	input_tree = input_file.Get(path2tree + tree_name)

	Mjj	= np.empty(1, dtype = 'float32')
	input_tree.SetBranchAddress('Mjj', Mjj)

	output_file = ROOT.TFile(path2output ,'RECREATE')	
	output_file.mkdir(path2tree)
	output_file.cd(path2tree)

	output_tree = input_tree.CloneTree(0)
	output_tree.SetName(tree_name)
	output_tree.SetTitle(tree_name)
	
	MjjReg_mjj	= np.empty(1, dtype = 'float32')
	MjjReg_mjj_br = output_tree.Branch('MjjReg_mjj', MjjReg_mjj	, 'MjjReg_mjj/F')
	MjjReg_corr = np.empty(1, dtype = 'float32')
	MjjReg_corr_br = output_tree.Branch('MjjReg_corr', MjjReg_corr , 'MjjReg_corr/F')
	
	n_events = input_tree.GetEntries()
	for i in range(0, n_events):
		input_tree.GetEntry(i)
		MjjReg_mjj[0] = reg_C_arr[i] * Mjj[0]
		MjjReg_corr[0] = reg_C_arr[i]
		output_tree.Fill()
	output_tree.Write()
	print ('Output file is: {}'.format(path2output))

# Performs the unbinned fit of 'branch_name' variable from 'input_tree' with 'cut' appied 
def RooFitMjj(input_tree, branch_name, cut, marker_color):
	
	ROOT.gROOT.cd()
	buf_tree = input_tree.CopyTree(cut)
	buf_tree.SetBranchStatus('*', 0)
	buf_tree.SetBranchStatus(branch_name, 1)	
	data_tree = buf_tree.CopyTree('')
	data_tree.GetBranch(branch_name).SetTitle('x')
	data_tree.GetBranch(branch_name).SetName('x')
	buf_tree.Delete()
	x = ROOT.RooRealVar('x','x',0,300)
	
	data = ROOT.RooDataSet("data","data",data_tree,ROOT.RooArgSet(x))

	mean = ROOT.RooRealVar("mean","Mean of Gaussian",120,100,140)
	sigma = ROOT.RooRealVar("sigma","Width of Gaussian",15,5,30)
	gauss_raw = ROOT.RooGaussian("gauss_raw","gauss(x,mean,sigma)",x,mean,sigma)
	
	meanCBF = ROOT.RooRealVar("meanCBF","mean of CBF",125,100,140)
	sigmaCBF = ROOT.RooRealVar("sigmaCBF","sigma of CBF",15,10,30)
	alpha = ROOT.RooRealVar("alpha","alpha of CBF",1,0,10)
	n = ROOT.RooRealVar("n","n of CBF",1.,1.,10)
	model = ROOT.RooCBShape('CBShape', 'Cystal Ball Function', x, meanCBF, sigmaCBF, alpha, n)
	
	gauss_raw.fitTo(data,ROOT.RooFit.Range(80,160),ROOT.RooFit.PrintLevel(1))
	mean_val = mean.getValV()
	sigma_val = sigma.getValV()

	model.fitTo(data,ROOT.RooFit.Range(mean_val - 1.5 * sigma_val,mean_val + 1.5 * sigma_val),ROOT.RooFit.PrintLevel(1))

	mean_valCBF		= meanCBF.getValV()
	mean_errCBF		= meanCBF.getAsymErrorHi()
	sigma1_valCBF	= sigmaCBF.getValV()
	sigma1_errCBF	= sigmaCBF.getAsymErrorHi()
	alpha_val		= alpha.getValV()
	n_val			= n.getValV()

	frame =x.frame(50,200)
	frame.SetName('')
	data.plotOn(frame,ROOT.RooFit.Binning(100),ROOT.RooFit.MarkerColor(marker_color))
	model.plotOn(frame,ROOT.RooFit.LineColor(marker_color))
	frame.GetXaxis().SetTitle('M_{jj} [GeV]')
	
	chi2_text = ROOT.TLatex()  		
	chi2_text.SetNDC()
	chi2_var = frame.chiSquare()
	chi2_text.SetTextSize(0.04)
	chi2_text.DrawLatex(0.7,0.8,'#chi^{2}/NDF' + ' = {:2.2f}'.format(chi2_var))
	return frame, [mean_valCBF, mean_errCBF, sigma1_valCBF, sigma1_errCBF, chi2_var]

def plot_reg_res(path2input, path2tree, tree_name):
	current_dir  = os.getcwd()
	input_file = TFile(path2input, 'READ')
	input_tree = input_file.Get(path2tree + tree_name)	
	mjj_frame, mjj_fitres = RooFitMjj(input_tree, 'Mjj', '',ROOT.kRed)
	mjj_reg_frame, mjj_reg_fitres = RooFitMjj(input_tree, 'MjjReg_mjj', '',ROOT.kBlue)
	mjj_reg_frame.Draw()
	mjj_frame.Draw('same')
	print(mjj_fitres)
	print(mjj_reg_fitres)
	s2m_impr = 100. * (1. - mjj_reg_fitres[2]/mjj_fitres[2]*mjj_fitres[0]/mjj_reg_fitres[0])
	s_impr = 100. * (1. - mjj_reg_fitres[2]/mjj_fitres[2])
	print ('sigma2mean impr.: {:3.2f}%\tsigma impr.: {:3.2f}%'.format(s2m_impr, s_impr))

	stat_res = ROOT.TLatex()		
	stat_res.SetNDC()
	stat_res.SetTextSize(0.05)
	stat_res.SetTextAlign(13)
	stat_res.SetTextFont(42)
	stat_res.SetTextColor(ROOT.kRed)
	stat_res.DrawLatex(0.15,.86,'#mu = '		+ '{:3.2f}'.format(mjj_fitres[0]))
	stat_res.SetTextColor(ROOT.kBlue)
	stat_res.DrawLatex(0.15,.80,'#mu = '		+ '{:3.2f}'.format(mjj_reg_fitres[0]))
	stat_res.SetTextColor(ROOT.kRed)
	stat_res.DrawLatex(0.15,.74,'#sigma  = '	+ '{:3.2f}'.format(mjj_fitres[2]))
	stat_res.SetTextColor(ROOT.kBlue)
	stat_res.DrawLatex(0.15,.68,'#sigma  = '	+ '{:3.2f}'.format(mjj_reg_fitres[2]))
#	stat_res.SetTextColor(ROOT.kRed)
#	stat_res.DrawLatex(0.65,.84,'#minus#minus')
#	stat_res.SetTextColor(ROOT.kBlack)
#	stat_res.DrawLatex(0.7,.86,'no regression')
#	stat_res.SetTextColor(ROOT.kBlue)
#	stat_res.DrawLatex(0.65,.78,'#minus#minus')
#	stat_res.SetTextColor(ROOT.kBlack)
#	stat_res.DrawLatex(0.7,.80,'m_{jj} regression')		
	
	stat_res.SetTextColor(ROOT.kRed)
	stat_res.DrawLatex(0.6,.84,'#minus#minus')
	stat_res.SetTextColor(ROOT.kBlack)
	stat_res.DrawLatex(0.65,.86,'pt regression')
	stat_res.SetTextColor(ROOT.kBlue)
	stat_res.DrawLatex(0.6,.78,'#minus#minus')
	stat_res.SetTextColor(ROOT.kBlack)
	stat_res.DrawLatex(0.65,.80,'pt+m_{jj} regression')		
	text = input()

def plot_mjj_bkg(m_low, m_up,n_entries, path2file, filename, path2tree, tree):
	current_dir = os.getcwd()	
	
	input_file = TFile.Open(path2file + filename, 'READ')
	tree = input_file.Get(path2tree+tree)

	Mjj			= np.empty(1, dtype='float32')  
	MjjReg_mjj	= np.empty(1, dtype='float32')  
	MjjReg_corr		= np.empty(1, dtype='float32')

	tree.SetBranchAddress('Mjj'			, Mjj )
	tree.SetBranchAddress('MjjReg_mjj'	, MjjReg_mjj	)
	tree.SetBranchAddress('MjjReg_corr'	, MjjReg_corr	)
	
	n_points = 100

	h_mjj		= TH1D('h_reco_mjj'			,';m_{jj} [GeV];Events;'	,n_points, 50, m_up)
	h_mjj_reg	= TH1D('h_reco_mjj_reg'		,';m_{jj} [GeV];Events;'	,n_points, 50, m_up)

	event_count = 0
	for i in range(0, tree.GetEntries()):
		tree.GetEntry(i)
		if Mjj[0] <= m_up  and Mjj[0] > m_low: 
			h_mjj.Fill(Mjj[0])
			h_mjj_reg.Fill(MjjReg_mjj[0])
			event_count +=1
			if event_count == n_entries:
				break
			

	c1 = TCanvas('c1','m_jj',1200,900)
	gStyle.SetOptStat(0)
	h_mjj_reg.SetLineColor(4)
	h_mjj_reg.GetXaxis().SetTitle('M_{jj}, [GeV]')
	h_mjj_reg.GetXaxis().SetRangeUser(m_low, m_up)
	h_mjj_reg.GetYaxis().SetTitle('')
	h_mjj.Draw()
	h_mjj.SetLineColor(2)
	h_mjj_reg.Draw("same")
	
	mjj_leg = TLegend(0.6,0.7,0.8,0.8)
	mjj_leg.SetBorderSize(0)
	mjj_leg.AddEntry(h_mjj,'no regression','l')
	mjj_leg.AddEntry(h_mjj_reg,'m_{jj} regression','l')
	mjj_leg.SetTextSize(.04)
	mjj_leg.Draw()
	
	mjj_entries = h_mjj.GetEntries()
	mjj_reg_entries = h_mjj_reg.GetEntries()
	
	stat_mjj = TLatex()	
	stat_mjj.SetNDC()
	stat_mjj.SetTextSize(0.04)
	stat_mjj.SetTextAlign(13)
	stat_mjj.SetTextFont(42)
	stat_mjj.SetTextColor(ROOT.kRed)
	stat_mjj.DrawLatex(0.15,.60,'Evt = ' + '{:5.0f}'.format(mjj_entries))
	stat_mjj.SetTextColor(ROOT.kBlue)
	stat_mjj.DrawLatex(0.15,.54,'Evt = ' + '{:5.0f}'.format(mjj_reg_entries))


#	const = 1e3
#	res_fitf = TF1('res_fitf','gaus(0)')
#	res_fitf.SetParameters(const, pref_mean, pref_rms)
#	h_mjjres.Fit(res_fitf,'','', pref_mean - pref_rms,  pref_mean + pref_rms)
#	
#	mjjres_reg_mean		= res_fitf.GetParameter(1)
#	mjjres_reg_mean_e	= res_fitf.GetParError(1)
#	mjjres_reg_sigma	= res_fitf.GetParameter(2)
#	mjjres_reg_sigma_e	= res_fitf.GetParError(2)
#	mjjres_reg_Chi2		= res_fitf.GetChisquare()
#	mjjres_reg_NDF 		= res_fitf.GetNDF()
#	
#	res_fitf = TF1('res_fitf','gaus')
#	res_fitf.SetParameters(const, pref_mean_reg, pref_mean_reg, pref_rms_reg)
#	h_mjjres_reg.Fit(res_fitf,'','', pref_mean_reg - pref_rms_reg, pref_mean_reg + pref_rms_reg)
#	
#	mjjres_mean		= res_fitf.GetParameter(1)
#	mjjres_mean_e	= res_fitf.GetParError(1)
#	mjjres_sigma	= res_fitf.GetParameter(2)
#	mjjres_sigma_e	= res_fitf.GetParError(2)
#	mjjres_Chi2		= res_fitf.GetChisquare()
#	mjjres_NDF 		= res_fitf.GetNDF()

#	stat_res.DrawLatex(0.65,.70,'#mu = '	+ '{:1.3f}#pm{:1.3f}'.format(mjjres_mean, mjjres_mean_e))
#	stat_res.SetTextColor(ROOT.kBlue)
#	stat_res.DrawLatex(0.65,.64,'#mu = '	+ '{:1.3f}#pm{:1.3f}'.format(mjjres_reg_mean, mjjres_reg_mean_e))
#	stat_res.SetTextColor(ROOT.kRed)
#	stat_res.DrawLatex(0.65,.58,'#sigma  = ' + '{:1.3f}#pm{:1.3f}'.format(mjjres_sigma, mjjres_sigma_e))
#	stat_res.SetTextColor(ROOT.kBlue)
#	stat_res.DrawLatex(0.65,.52,'#sigma  = ' + '{:1.3f}#pm{:1.3f}'.format(mjjres_reg_sigma, mjjres_reg_sigma_e))
#	stat_res.SetTextColor(ROOT.kRed)
#	stat_res.DrawLatex(0.65,.46,'#chi^{2}/NDF = ' + '{:3.1f}/{:2.0f}'.format(mjjres_Chi2,mjjres_NDF))
#	stat_res.SetTextColor(ROOT.kBlue)
#	stat_res.DrawLatex(0.65,.40,'#chi^{2}/NDF = ' + '{:3.1f}/{:2.0f}'.format(mjjres_reg_Chi2,mjjres_reg_NDF))
	text = input()


import ROOT
import numpy as np
import sys
import os
import glob

''' 
Read the data and print the maximum and minimum values stored in the TBranches for interesting quantities.
Use it to specify the boundaries of the histograms.
Recommended: Use the data with higher statistics to set the boundaries. It will run longer, but you will have the highest probabilty to get extreme bins. 

TODO: Achtung! Raffiniert! Define a function which does the whole stuff without reading the whole chain everytime to make the code modular. 
'''

infile = sys.argv[1]

f = ROOT.TFile(infile)

infiles = sys.argv[1:]
if len(infiles)>1: True
elif len(infiles)==1: infiles=glob.glob(infiles[0])

chain=ROOT.TChain("MVATree")
for inpath in infiles:
    inpath = os.path.abspath(inpath)
    chain.Add(inpath)
print chain.GetNtrees()


# read the data and write into lists

def makeListOfHistoBinning(chain, additionalvetoes = [],jetordered = True):
	'''
	Generate list of interesting TBranch in TChain and initialize corresponding histograms with Sumw2 called.
	If there is a GenJet_Pt branch, optionally make also pT ordered histograms.
	Veto for uninteresting quantities to reduce dimensionality.
	'''
	vetoes = ["GenCJet", "GenHiggs", "CHadron", "Q1", "Q2", "_W_", "_Nu_", "_Lep_", 
	"PDGID", "Idx", "Evt_ID", "GenEvt", "Reco", "Tags",
	"Trigger", "SF", "Weight_CSV", "Weight_LHA", "Weight_PU", "Weight_pu", "GenWeight", "variation"]

	for addveto in additionalvetoes:
		vetoes.append(addveto)

	# make a list of branch names
	lBranches = chain.GetListOfBranches()
	branchnames = []
	for branch in lBranches:
		branchnames.append(branch.GetName())

	Histos = []
	for bname in branchnames:
		# perform vetoes
		if any(x in bname for x in vetoes): 
			# print str(bname) + " vetoed"
			continue
		#print str(bname) + " keeped"

		# set the binning of the histograms
		if "_Pt" in bname or "HadronPt" in bname:
			xmin = 0.0
			xmax = 2500.0
			nbins = int(ceil((xmax-xmin)/10))
		elif "_E" in bname:
			xmin = 0.0
			xmax = 4200.0
			nbins = int(ceil((xmax-xmin)/10))
		elif "_Dr" in bname:
			xmin = 0.0
			xmax = 12.0
			nbins = int(ceil((xmax-xmin)/0.01))
		elif "_M" in bname:
			xmin = 0.0
			xmax = 2000.0
			nbins = int(ceil((xmax-xmin)/10))
		elif "_Phi" in bname:
			xmin = -3.5
			xmax = 3.5
			nbins = int(ceil((xmax-xmin)/0.01))
		elif "_Eta" in bname:
			if "Hadron" in bname:
				xmax = 8.0
			elif "Jet" in bname:
				xmax = 3.0
			xmin = -xmax
			nbins = int(ceil((xmax-xmin)/0.01))
		elif "Weight" in bname:
			if "GenValue" in bname or "GEN_nom" in bname:
				xmin = -500
				xmax = -xmin
				nbins =int(ceil((xmax-xmin)/1))
			else:
				xmin = 0.0
				xmax = 1.0
				nbins = int(ceil((xmax-xmin)/0.001))
		elif "N_" in bname or "NHadrons" in bname:
			xmin = -0.5
			xmax = 30.5
			nbins = int(ceil((xmax-xmin)/1))
		else:
			xmin = chain.GetMinimum(bname)
			xmax = chain.GetMaximum(bname)
			nbins = 300

		# if the flag jetordered is set True, make additional six Pt ordered GenJet_Pt histograms
		# declare the histograms and set the bins
		if jetordered:
			if bname == "GenJet_Pt" or bname == "Jet_Pt":
				names = ["_", "_1st_","_2nd_","_3rd_","_4th_","_5th_", "_6th_"]
				for x in names:
					nbname = x.join(bname.rsplit("_", 1))
					h = ROOT.TH1D()
					h.SetName(nbname)
					h.SetTitle(nbname)
					h.SetBins(nbins, xmin, xmax)
					#h.SetMinimum(xmin)
					#h.SetMaximum(xmax)
					h.Sumw2()
					Histos.append(h)
			else:
				h = ROOT.TH1D()
				h.SetName(bname)
				h.SetTitle(bname)
				h.SetBins(nbins, xmin, xmax)
				#h.SetMinimum(xmin)
				#h.SetMaximum(xmax)
				h.Sumw2()
				Histos.append(h)

		else:
			h = ROOT.TH1D()
			h.SetName(bname)
			h.SetTitle(bname)
			h.SetBins(nbins, xmin, xmax)
			#h.SetMinimum(xmin)
			#h.SetMaximum(xmax)
			h.Sumw2()
			Histos.append(h)

	print "You have chosen " + str(len(Histos)) + " physical quantities from originally " + str(len(branchnames)) + " available."
	#print "The corresponding histograms are: \n" + str(Histos)	
	return Histos



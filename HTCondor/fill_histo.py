import ROOT
import sys
import os
import glob
from array import array
from numpy import ceil
from optparse import OptionParser

def parse_args():
	usage = '%prog [options] path/to/ntuples\n' 
	parser = OptionParser(usage = usage)

	parser.add_option( 
		"-l", "--lowerEdge",
		help = "Start at this event",
		dest = "low_edge",
		type = "int"
		)
	parser.add_option( 
		"-u", "--upperEdge",
		help = "End with this event",
		dest = "up_edge",
		type = "int"
		)
	parser.add_option( 
		"-n", "--batch-number",
		help = "Specify the batch number of these histograms, which corresponds to the event range given. ",
		dest = "n_batch",
		type = "int"
		)

	options, args = parser.parse_args()
	
	return options, args



def main ():
	''' 
	read files and write ttbb event data into histograms
	use data generated by different generators respectively
	execute with "python read.py <PATH/TO/NTUPLES/*.root>"
	'''
	options, infiles = parse_args()

	# specify the suffix for the .root file which contains the histograms, default: ""
	n_batch = options.n_batch
	suffix = ""
	if n_batch != None:
		suffix = str(n_batch)

	onlyone = True
	if len(infiles)>1: 
		True
	elif len(infiles)==1 and not onlyone: 
		datadir = os.path.dirname(os.path.abspath(infiles[0]))
		infiles=glob.glob(datadir+"/"+os.path.basename(datadir) + '*.root')
	elif onlyone:
		infiles = os.path.abspath(infiles[0])
		infiles = [infiles]

	for infile in infiles:
		infile = os.path.abspath(infile)

	chain = getChain(infiles = infiles)
	# chain.SetBranchStatus("*", 1)
	origin = os.path.dirname(os.path.abspath(infiles[0]))

	# set which events should be filled, default: fill all
	low_edge = options.low_edge
	up_edge = options.up_edge
	if low_edge == None:
		low_edge = 0
	if up_edge == None:
		up_edge = chain.GetEntries()

	Histos = makeListOfHistos(chain = chain, additionalvetoes = [],jetordered = True)
	Histos_ttbb = Histos
	Histos_ttb = Histos
	fillHistos(Histos = Histos, chain = chain, low_edge = low_edge, up_edge = up_edge ,cuts = ["GenEvt_I_TTPlusBB > 0"]) 
	fillHistos(Histos = Histos_ttbb, chain = chain, low_edge = low_edge, up_edge = up_edge, cuts = ["GenEvt_I_TTPlusBB == 3"])
	fillHistos(Histos = Histos_ttb, chain = chain, low_edge = low_edge, up_edge = up_edge, cuts = ["GenEvt_I_TTPlusBB < 3"])
	writeHistos(Histos = Histos, origin =  origin, suffix = suffix)
	writeHistos(Histos = Histos_ttbb, origin = origin, suffix = suffix + "_ttbb-cuts")
	writeHistos(Histos = Histos_ttb, origin = origin, suffix = suffix + "_ttb-cuts")



def getChain(infiles):
	'''
	read all the .root files and add the corresponding tree (here: MVATree) into a TChain
	'''
	chain=ROOT.TChain("MVATree")
	for inpath in infiles:
		inpath = os.path.abspath(inpath)
		# print "checking file", inpath
		f = ROOT.TFile(inpath)
		if f.IsOpen():
			if not f.IsZombie() and not f.TestBit(ROOT.TFile.kRecovered):
				chain.Add(inpath)
				continue
			else:
				f.Close()
		print "file '%s' is broken!" % inpath
	print "Read in " + str(chain.GetNtrees()) + " files."
	return chain



def makeListOfHistos(chain, additionalvetoes = [],jetordered = True):
	'''
	Generate list of interesting TBranch in TChain and initialize corresponding histograms with Sumw2 called.
	If there is a GenJet_Pt branch, optionally make also pT ordered histograms.
	Veto for uninteresting quantities to reduce dimensionality.
	'''

	vetoes = ["GenCJet", "GenHiggs", "CHadron", "Q1", "Q2", "_W_", "_Nu_", "_Lep_", "fromTTH", "FromTopType", "TopPt",
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
			#chain.SetBranchStatus(bname, 0)
			# print str(bname) + " vetoed"
			continue
		#print str(bname) + " keeped"

		xmin = xmax = None
		nbins = None

		# set the binning of the histograms
		if bname.endswith("_Pt") or bname.endswith("HadronPt"):
			xmin = 0.0
			xmax = 2500.0
			nbins = int(ceil((xmax-xmin)/10))
		elif bname.endswith("_Eta"):
			if "Hadron" in bname:
				xmax = 8.0
			elif "Jet" in bname:
				xmax = 3.0
			else:
				xmax = 4.0
			xmin = -xmax
			nbins = int(ceil((xmax-xmin)/0.01))
		elif bname.endswith("_E"):
			xmin = 0.0
			xmax = 4200.0
			nbins = int(ceil((xmax-xmin)/10))
		elif bname.endswith("_Dr") or bname.endswith("_DeltaR"):
			xmin = 0.0
			xmax = 12.0
			nbins = int(ceil((xmax-xmin)/0.01))
		elif bname.endswith("_M"):
			xmin = 0.0
			xmax = 2000.0
			nbins = int(ceil((xmax-xmin)/10))
		elif bname.endswith("_Phi"):
			xmin = -3.5
			xmax = 3.5
			nbins = int(ceil((xmax-xmin)/0.01))
		elif bname.startswith("Weight"):
			if bname.endswith("GenValue") or bname.endswith("GEN_nom"):
				xmin = -500
				xmax = -xmin
				nbins =int(ceil((xmax-xmin)/1))
			else:
				xmin = 0.0
				xmax = 1.0
				nbins = int(ceil((xmax-xmin)/0.001))
		elif bname.startswith("N_") or bname.endswith("NHadrons"):
			xmin = -0.5
			xmax = 30.5
			nbins = int(ceil((xmax-xmin)/1))
		else:
			print "Warning: Selection fails for ", bname
			continue
			# xmin = chain.GetMinimum(bname)
			# xmax = chain.GetMaximum(bname)
			# nbins = 300

		# if the flag jetordered is set True, make additional six Pt ordered GenJet_Pt histograms
		# declare the histograms and set the bins
		if jetordered:
			if bname.startswith("GenJet_Pt") and  bname.endswith("_Pt"):
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
			elif bname.startswith("AdditionalGenBJet") and bname.endswith("_Pt"):
				names = ["_", "_1st_", "_2nd_"]
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
			elif bname.startswith("AdditionalLightGenJet") and bname.endswith("_Pt"):
				names = ["_", "_1st_", "_2nd_"]
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



def fillHistos(chain, Histos, low_edge, up_edge, cuts = None):
	''' 
	Fill the weighted data into the histos if the event is a tt+b-jets event.
	'''
	for ievt, e in enumerate(chain):
		# skip all events with eventnumber smaller than low_edge
		if ievt+1 < low_edge:
			continue
		# don't exceed the maximum eventnumber
		if ievt+1 <= up_edge:

			if (ievt+1)%5000==0:
				print "at event", ievt+1

			if not e.GenEvt_I_TTPlusBB > 0: continue    # GenEvt_I_TTPlusBB =1 for ttb =2 for tt2b =3 for ttbb

			if cuts != None:
				for cut in cuts:
					if cut.split()[1] == ">": 
						condition = getattr(e, cut.split()[0]) > cut.split()[-1]
					elif cut.split()[1] == "<":
						condition = getattr(e, cut.split()[0]) < cut.split()[-1]
					else:
						condition = getattr(e, cut.split()[0]) == cut.split()[-1]

					if not condition: continue


			for ih,h in enumerate(Histos):
				# for the first, second, ... leading jet histogram: fill it
				names = ["1st_Pt","2nd_Pt","3rd_Pt","4th_Pt","5th_Pt", "6th_Pt"]
				if any( x in h.GetName() for x in names):
					# loop over all possible histograms and fill them with the according jet pT
					for istr, string in enumerate(["1st", "2nd", "3rd", "4th", "5th", "6th"]):
						istr += 1
						if ("GenJet_" in h.GetName() and string in h.GetName()):
							# convert the read-write buffer ptr into a list
							dummy = e.GenJet_Pt
							if len(dummy)>=istr:
								b = []
								for i in range(len(dummy)):
									b.append(dummy[i])
								# sort it
								if len(b)==0: continue
								b.sort()
								# fill the histograms
								h.Fill(b[-istr], e.Weight_GEN_nom*e.Weight_XS)
						elif ("AdditionalGenBJet" in h.GetName() and string in h.GetName()):
							dummy = e.AdditionalGenBJet_Pt
							if len(dummy)>=istr:
								b = []
								for i in range(len(dummy)):
									b.append(dummy[i])
								# sort it
								if len(b)==0: continue
								b.sort()
								# fill the histograms
								h.Fill(b[-istr], e.Weight_GEN_nom*e.Weight_XS)
						elif ("AdditionalLightGenJet" in h.GetName() and string in h.GetName()):
							dummy = e.AdditionalLightGenJet_Pt
							if len(dummy)>=istr:
								b = []
								for i in range(len(dummy)):
									b.append(dummy[i])
								# sort it
								if len(b)==0: continue
								b.sort()
								# fill the histograms
								h.Fill(b[-istr], e.Weight_GEN_nom*e.Weight_XS)
						else:
							continue
				else:
					# fill the histograms for all other quantities
					# convert the read-write buffer ptr into a python list
					dummy = getattr(e, h.GetName())
					b = []
					if isinstance(dummy, (int, long, float)):
						dummy = [dummy]
					for i in range(len(dummy)):
						b.append(dummy[i])
					# fill the histogram
					for l in range(len(b)):
						h.Fill(b[l], e.Weight_GEN_nom*e.Weight_XS)
		# if the eventnumber gets higher than the upper limit: break
		else:
			break



def writeHistos(Histos, origin, suffix = ""):
	''' 
	Write the histos into a new root file depending on the type of generated data used. 
	'''
	name = '%s'
	if suffix != "":
		name += "_" + suffix
	name += ".root"

	if all(x in origin for x in ["ttbb", "amcatnlo"]):
		f = ROOT.TFile(name % "ttbb_4FS_amcatnlo_Histos","update")    
	elif all(x in origin for x in ["TTbb", "Powheg", "Openloops"]):
		f = ROOT.TFile(name % "ttbb_4FS_Powheg_OL_Histos","update")
	elif all(x in origin for x in ["TTbb", "Powheg", "Helac"]):
		f = ROOT.TFile(name % "ttbb_4FS_PowHel_Histos","update")
	elif all(x in origin for x in ["TTJets", "amcatnlo"]):
		f = ROOT.TFile(name % "ttjets_Histos","update")
	elif "TTToSemi" in origin:
		f = ROOT.TFile(name % "tt_semileptonic_Histos","update")
	else:
		print "Error: Couldn't find the data origin of the histograms. Abort!"
		exit(0)

	for h in Histos:
		h.Write()
	f.Close()



if __name__ == '__main__':
	main()
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

	# set which events should be filled, default: fill all
	low_edge = options.low_edge
	up_edge = options.up_edge
	if low_edge == None:
		low_edge = 0
	if up_edge == None:
		up_edge = chain.GetEntries()

	Histos = makeListOfHistos(chain = chain, additionalvetoes = [],jetordered = True)
	fillHistos(Histos = Histos, chain = chain, low_edge = low_edge, up_edge = up_edge) 
	writeHistos(Histos = Histos, origin = os.path.dirname(os.path.abspath(infiles[0])), suffix = suffix)



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

	for ibname1,bname1 in enumerate(branchnames):
		# perform vetoes
		if any(x in bname1 for x in vetoes): 
			# print str(bname) + " vetoed"
			continue
		#print str(bname) + " keeped"

		# set the binning of the histograms
		xmin1 = xmin2 = xmax1 = xmax2 = None
		nbins1 = nbins2 = None

		if bname1.endswith("_Pt") or bname1.endswith("HadronPt"):
			xmin1 = 0.0
			xmax1 = 2500.0
			nbins1 = int(ceil((xmax1-xmin1)/10))
		elif bname1.endswith("_Eta"):
			if "Hadron" in bname1 or "B" in bname1:
				xmax1 = 8.0
			elif "Jet" in bname1:
				xmax1 = 3.0
			else:
				xmax1 = 4.0
			xmin1 = -xmax1
			nbins1 = int(ceil((xmax1-xmin1)/0.01))
		elif bname1.endswith("_E"):
			xmin1 = 0.0
			xmax1 = 4200.0
			nbins1 = int(ceil((xmax1-xmin1)/10))
		elif bname1.endswith("_Dr") or bname1.endswith("_DeltaR"):
			xmin1 = 0.0
			xmax1 = 12.0
			nbins1 = int(ceil((xmax1-xmin1)/0.01))
		elif bname1.endswith("_M"):
			xmin1 = 0.0
			xmax1 = 2000.0
			nbins1 = int(ceil((xmax1-xmin1)/10))
		elif bname1.endswith("_Phi"):
			xmin1 = -3.5
			xmax1 = 3.5
			nbins1 = int(ceil((xmax1-xmin1)/0.01))
		elif bname1.startswith("Weight"):
			if bname1.endswith("GenValue") or bname1.endswith("GEN_nom"):
				xmin1 = -500
				xmax1 = -xmin1
				nbins1 =int(ceil((xmax1-xmin1)/1))
			else:
				xmin1 = 0.0
				xmax1 = 1.0
				nbins1 = int(ceil((xmax1-xmin1)/0.001))
		elif bname1.startswith("N_") or bname1.endswith("_NHadrons"):
			xmin1 = -0.5
			xmax1 = 30.5
			nbins1 = int(ceil((xmax1-xmin1)/1))
		else:
			print "Warning: Selection fails for ", bname1
			continue
			# xmin1 = chain.GetMinimum(bname1)
			# xmax1 = chain.GetMaximum(bname1)
			# nbins1 = 300

		for ibname2 in range(ibname1):
			bname2 = branchnames[ibname2]
			# perform vetoes
			if any(x in bname2 for x in vetoes): 
				# print str(bname) + " vetoed"
				continue
			#print str(bname) + " keeped"

			# set the binning of the histograms
			if bname2.endswith("_Pt") or bname2.endswith("HadronPt"):
				xmin2 = 0.0
				xmax2 = 2500.0
				nbins2 = int(ceil((xmax2-xmin2)/10))
			elif bname2.endswith("_Eta"):
				if "Hadron" in bname2 or "B" in bname2:
					xmax2 = 8.0
				elif "Jet" in bname2:
					xmax2 = 3.0
				else:
					xmax2 = 4.0
				xmin2 = -xmax2
				nbins2 = int(ceil((xmax2-xmin2)/0.01))
			elif bname2.endswith("_E"):
				xmin2 = 0.0
				xmax2 = 4200.0
				nbins2 = int(ceil((xmax2-xmin2)/10))
			elif bname2.endswith("_Dr") or bname2.endswith("_DeltaR"):
				xmin2 = 0.0
				xmax2 = 12.0
				nbins2 = int(ceil((xmax2-xmin2)/0.01))
			elif bname2.endswith("_M"):
				xmin2 = 0.0
				xmax2 = 2000.0
				nbins2 = int(ceil((xmax2-xmin2)/10))
			elif bname2.endswith("_Phi"):
				xmin2 = -3.5
				xmax2 = 3.5
				nbins2 = int(ceil((xmax2-xmin2)/0.01))
			elif bname2.startswith("Weight"):
				if bname2.endswith("GenValue") or bname2.endswith("GEN_nom"):
					xmin2 = -500
					xmax2 = -xmin2
					nbins2 =int(ceil((xmax2-xmin2)/1))
				else:
					xmin2 = 0.0
					xmax2 = 1.0
					nbins2 = int(ceil((xmax2-xmin2)/0.001))
			elif bname2.startswith("N_") or bname2.endswith("NHadrons"):
				xmin2 = -0.5
				xmax2 = 30.5
				nbins2 = int(ceil((xmax2-xmin2)/1))
			else:
				print "Warning: Selection fails for ", bname2
				continue
				# xmin2 = chain.GetMinimum(bname2)
				# xmax2 = chain.GetMaximum(bname2)
				# nbins2 = 300


			# Pick out only ""sensefull" 2D histograms
			# list of conditions for "sensefull" 2D histograms
			lconditions = [
			bname1.split("_")[:-1]==bname2.split("_")[:-1] and any(s.endswith(x) for x in ["_Pt", "_E", "_Phi", "_Eta", "DeltaR", "_Dr"] for s in [bname1, bname2]), # Internal combinatorical kinematics' comparisons
			any(s.startswith("Weight") for s in [bname1, bname2]) and any(s.endswith(x) for x in ["_Pt", "_E", "_Phi", "_Eta", "_Dr"] for s in [bname1, bname2]), # Weight plots
			any(all(s.startswith(x) for s in [bname1, bname2]) for x in ["Additional", "GenTopHad_B", "GenTopLep_B"]) and all("B" in s for s in [bname1, bname2]) and any(all(s.endswith(x) for s in [bname1, bname2]) for x in ["_Pt", "_E", "_Phi", "_Eta", "_Dr"] ) and (("Hadron" in bname1 and "Jet" in bname2) or ("Jet" in bname1 and "Hadron" in bname2)), # B-Hadron <-> B-Jet comparison
			]

			if not any(lconditions):
				# print "!"*130
				# print bname1 +"-"+ bname2, " doesn't fullfill conditions! Skipped!"
				# print "!"*130
				# exit(0)
				continue

			nbins1 = int(nbins1)
			nbins2 = int(nbins2)
			xmin1 = ROOT.Double(xmin1)
			xmin2 = ROOT.Double(xmin2)
			xmax1 = ROOT.Double(xmax1)
			xmax2 = ROOT.Double(xmax2)

			# if the flag jetordered is set True, make additional six Pt ordered GenJet_Pt histograms
			# declare the histograms and set the bins
			if jetordered:
				if bname1 == "GenJet_Pt" or bname1 == "Jet_Pt":
					names = ["_", "_1st_","_2nd_","_3rd_","_4th_","_5th_", "_6th_"]
					for x in names:
						nbname1 = x.join(bname1.rsplit("_", 1))
						if bname2 == "GenJet_Pt" or bname1 == "Jet_Pt":
							for x in names:
								nbname2 = x.join(bname2.rsplit("_", 1))
								nbname = nbname1 + "-" + nbname2
								h = ROOT.TH2D()
								h.SetName(nbname)
								h.SetTitle(nbname)
								print "-"*130
								print "Histo: ", nbname
								print "nbins1: %s (type: %s)" % (str(nbins1), str(type(nbins1)))
								print "xmin1: %s (type: %s)" % (str(xmin1), str(type(xmin1)))
								print "xmax1: %s (type: %s)" % (str(xmax1), str(type(xmax1)))
								print "nbins2: %s (type: %s)" % (str(nbins2), str(type(nbins2)))
								print "xmin2: %s (type: %s)" % (str(xmin2), str(type(xmin2)))
								print "xmax2: %s (type: %s)" % (str(xmax2), str(type(xmax2)))
								print "-"*130
								h.SetBins(nbins1, xmin1, xmax1, nbins2, xmin2, xmax2)
								#h.SetMinimum(xmin1)
								#h.SetMaximum(xmax1)
								h.Sumw2()
								Histos.append(h)
						else:
							nbname = nbname1 + "-" + bname2
							h = ROOT.TH2D()
							h.SetName(nbname)
							h.SetTitle(nbname)
							# print "-"*130
							# print "Histo: ", nbname
							# print "nbins1: %s (type: %s)" % (str(nbins1), str(type(nbins1)))
							# print "xmin1: %s (type: %s)" % (str(xmin1), str(type(xmin1)))
							# print "xmax1: %s (type: %s)" % (str(xmax1), str(type(xmax1)))
							# print "nbins2: %s (type: %s)" % (str(nbins2), str(type(nbins2)))
							# print "xmin2: %s (type: %s)" % (str(xmin2), str(type(xmin2)))
							# print "xmax2: %s (type: %s)" % (str(xmax2), str(type(xmax2)))
							# print "-"*130


							h.SetBins(nbins1, xmin1, xmax1, nbins2, xmin2, xmax2)
							#h.SetMinimum(xmin1)
							#h.SetMaximum(xmax1)
							h.Sumw2()
							Histos.append(h)
				else:
					h = ROOT.TH2D()
					nbname = bname1 + "-" + bname2
					h.SetName(nbname)
					h.SetTitle(nbname)
					# print "-"*130
					# print "Histo: ", nbname
					# print "nbins1: %s (type: %s)" % (str(nbins1), str(type(nbins1)))
					# print "xmin1: %s (type: %s)" % (str(xmin1), str(type(xmin1)))
					# print "xmax1: %s (type: %s)" % (str(xmax1), str(type(xmax1)))
					# print "nbins2: %s (type: %s)" % (str(nbins2), str(type(nbins2)))
					# print "xmin2: %s (type: %s)" % (str(xmin2), str(type(xmin2)))
					# print "xmax2: %s (type: %s)" % (str(xmax2), str(type(xmax2)))
					# print "-"*130
					h.SetBins(nbins1, xmin1, xmax1, nbins2, xmin2, xmax2)
					#h.SetMinimum(xmin1)
					#h.SetMaximum(xmax1)
					h.Sumw2()
					Histos.append(h)

			else:
				h = ROOT.TH2D()
				nbname = bname1 + "-" + bname2
				h.SetName(nbname)
				h.SetTitle(nbname)
				h.SetBins(nbins1, xmin1, xmax1, nbins2, xmin2, xmax2)
				#h.SetMinimum(xmin1)
				#h.SetMaximum(xmax1)
				h.Sumw2()
				Histos.append(h)

	print "You have chosen " + str(len(Histos)) + " combinations from originally " + str(len(branchnames)) + " physical quantities available."
	#print "The corresponding histograms are: \n" + str(Histos)	
	return Histos



def fillHistos(chain, Histos, low_edge, up_edge):
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

			for ih,h in enumerate(Histos):
				hname = h.GetName()
				hname1 = hname.split("-")[0]
				hname2 = hname.split("-")[1]

				# for the first, second, ... leading jet histogram: fill it
				names = ["1st_Pt","2nd_Pt","3rd_Pt","4th_Pt","5th_Pt", "6th_Pt"]
				if any( name1 in hname1 for name1 in names):
					# loop over all possible histograms and fill them with the according jet pT
					for istr1, string1 in enumerate(["1st", "2nd", "3rd", "4th", "5th", "6th"]):
						if "GenJet_" in hname1 and string1 in hname1:
							# convert the read-write buffer ptr into a list
							istr1 += 1
							dummy1 = e.GenJet_Pt
							if len(dummy1)>=istr1:
								b1 = []
								for i1 in range(len(dummy1)):
									b1.append(dummy1[i1])
								# sort it
								if len(b1)==0: continue
								b1.sort()
								# the same for the second dimension
								if any(y in hname2 for y in names):
									for istr2, string2 in enumerate(["1st", "2nd", "3rd", "4th", "5th", "6th"]):
										istr2 += 1
										if "GenJet_" in hname2 and string2 in hname2:
											dummy2 = e.GenJet_Pt
											if len(dummy2)>=istr2:
												b2 = []
												for i2 in range(len(dummy2)):
													b2.append(dummy2[i2])
												if len(b2)==0: continue
												b2.sort()
												# fill the histograms
												h.Fill(b1[-istr1], b2[-istr2], e.Weight_GEN_nom*e.Weight_XS,)
								else:
									dummy2 = getattr(e, hname2)
									b2 =[]
									if isinstance(dummy2, (int, long, float)):
										dummy2 = [dummy2]
									for i2 in range(len(dummy2)):
										b2.append(dummy2[i2])
									# fill the histograms
									for l in range(len(b2)):
										h.Fill(b1[-istr1], b2[l], e.Weight_GEN_nom*e.Weight_XS)
						# cross check if it's really the GenJet_Pt histogram
						else:
							continue

				# fill the histograms for all other quantities
				else:
					# convert the read-write buffer ptrs into python lists
					dummy1 = getattr(e, hname1)
					b1 = []
					if isinstance(dummy1, (int, long, float)):
						dummy1 = [dummy1]
					for i1 in range(len(dummy1)):
						b1.append(dummy1[i1])
					dummy2 = getattr(e, hname2)
					b2 = []
					if isinstance(dummy2, (int, long, float)):
						dummy2 = [dummy2]
					for i2 in range(len(dummy2)):
						b2.append(dummy2[i2])

					# fill the histograms
					if len(b1)==len(b2):
						for l in range(len(b1)):
							h.Fill(b1[l], b2[l], e.Weight_GEN_nom*e.Weight_XS)
					else:
						for l1 in range(len(b1)):
							for l2 in range(len(b2)):
								h.Fill(b1[l1], b2[l2], e.Weight_GEN_nom*e.Weight_XS)
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
		f = ROOT.TFile(name % "ttbb_4FS_amcatnlo_Histos","recreate")
		for h in Histos:
			h.Write()
		f.Close()
	    
	    
	elif all(x in origin for x in ["TTbb", "Powheg"]):
		f = ROOT.TFile(name % "ttbb_4FS_Powheg_OL_Histos","recreate")
		for h in Histos:
			h.Write()
		f.Close()

	elif all(x in origin for x in ["TTJets", "amcatnlo"]):
		f = ROOT.TFile(name % "ttjets_Histos","recreate")
		for h in Histos:
			h.Write()
		f.Close()

	elif "TTToSemi" in origin:
		f = ROOT.TFile(name % "tt_semileptonic_Histos","recreate")
		for h in Histos:
			h.Write()
		f.Close()



if __name__ == '__main__':
	main()
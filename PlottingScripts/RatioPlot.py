import numpy as np
import sys
import os
import ROOT
from decimal import Decimal
from array import array
from numpy import ceil


ROOT.gStyle.SetPaintTextFormat("4.2f")
ROOT.gROOT.SetBatch(1)
ROOT.gDirectory.cd('PyROOT:/')

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)



# def getVariables( data ):
#     return data.columns



def canvasStyle(canvas):
	canvas.Divide(1,2)
	canvas.cd(1).SetPad(0.,0.3,1.0,1.0);
	canvas.cd(1).SetBottomMargin(0.0);
	canvas.cd(2).SetPad(0.,0.0,1.0,0.3);
	canvas.cd(2).SetTopMargin(0.0);
	canvas.cd(1).SetTopMargin(0.07);
	canvas.cd(2).SetBottomMargin(0.4);
	canvas.cd(1).SetRightMargin(0.05);
	canvas.cd(1).SetLeftMargin(0.15);
	canvas.cd(2).SetRightMargin(0.05);
	canvas.cd(2).SetLeftMargin(0.15);
	canvas.cd(2).SetTicks(1,1)
	canvas.cd(1).SetTicks(1,1)


# def calcNorm( variable ):
# 	print("norming values:")
# 	allValues = []
# 	for key in dataDict:
# 		allValues+= list(dataDict[key].eval(variable))

# 	mu = np.mean(allValues)
# 	sig = np.std(allValues)
# 	print("mu  = "+str(mu))
# 	print("std = "+str(sig))
# 	return mu, sig



def setupStyle(graph):
	graph.GetXaxis().SetTitleSize(3*graph.GetXaxis().GetTitleSize())
	# graph.GetXaxis().SetTitleOffset(1.3*graph.GetXaxis().GetTitleOffset())
	graph.GetXaxis().SetLabelSize(2.4*graph.GetXaxis().GetLabelSize())
	
	# graph.GetYaxis().SetTitleSize(2.4*graph.GetXaxis().GetTitleSize())
	# graph.GetYaxis().SetTitleOffset(1.3*graph.GetXaxis().GetTitleOffset())
	# graph.GetYaxis().SetLabelSize(2.4*graph.GetXaxis().GetLabelSize())
	return graph



# def getlow(l):
# 	low = 0
# 	if len(l) != 0:
# 		low = l[-1]
# 	return low


# def GetArray_rebinHisto(histo, smallbin = 10, middlebin = 20, endbin = 100):
# 	nbins = histo.GetNbinsX() # number of bins of the original histo
# 	norm = histo.Integral() # norm of the original histo

# 	# calculate the old average binwidth
# 	oldbinwidth = 0
# 	for i in range(nbins):
# 		oldbinwidth += histo.GetBinWidth(i)
# 	oldbinwidth = oldbinwidth/nbins

# 	# fill xbins for new binning
# 	xbins = [] # list of new low edges of the histogram with ngroup+1 elements

# 	smallbinRange = histo.GetBinLowEdge(1) + histo.GetBinWidth(1)
# 	middlebinRange = smallbinRange
# 	endbinRange = middlebinRange

# 	for i in range(1, nbins+1):
# 		integral = histo.Integral(1, i) 
# 		if integral < 0.1 * norm:
# 			smallbinRange = histo.GetBinLowEdge(i) + histo.GetBinWidth(i)
# 		if integral < 0.99 *norm:
# 			middlebinRange = histo.GetBinLowEdge(i) + histo.GetBinWidth(i)
# 		if integral < 1.0 *norm:
# 			endbinRange = histo.GetBinLowEdge(i) + histo.GetBinWidth(i)

# 	print smallbinRange, middlebinRange, endbinRange

# 	for i in range(int(np.ceil(smallbinRange/smallbin))):
# 		xbins.append(smallbin*i)
	
# 	for i in range(int(np.ceil((middlebinRange-smallbinRange)/middlebin))):
# 		low = getlow(xbins)
# 		xbins.append(middlebin + low)
# 	for i in range(int(np.ceil((endbinRange-middlebinRange)/endbin))):
# 		low = getlow(xbins)
# 		xbins.append(endbin + low)

# 	ngroup = len(xbins) - 1
# 	xarray = array("d", xbins)

# 	return ngroup, xarray



# def dump_histo(histo):
# 	for i in range(1, histo.GetNbinsX()+1):
# 		print "bin {0} = {1} (width = {2}".format(i, histo.GetBinCenter(i), histo.GetBinWidth(i))



def shapePlots( histos, savename="",normed = True, rebinned = True):
	'''
	Function which creates RatioPlots from a list of histograms. It always uses the first histogram in the list as a reference to the others.
	'''

	# mkdir
	if normed and rebinned:
		shapePath = "./RatioPlots_normed_rebinned"
	elif normed:
		shapePath = "./RatioPlots_normed"
	elif rebinned:
		shapePath = "./RatioPlots_rebinned"
	else:
	shapePath = "./RatioPlots"
	if not os.path.exists( shapePath ):
		os.makedirs(shapePath)

	
	# Create a list of histos and normalize them if normed = True and rebin if rebin = True
	Histos = histos
	print Histos
	# also set the legend according to their origin
	legends = {}
	for i, histo in enumerate(Histos):
		#if i == 0:
			#ngroup, xarray = GetArray_rebinHisto(histo)
		hname = histo.GetName()

		# if rebinned = True, rebin the histograms for a better overview
		if rebinned:
			newname = hname + "_rebinned"
			xarray = 0
			ngroup = 5
			xbins = []
			if "_Pt" in hname or "HadronPt" in hname:
				# xmin = 0.0
				# xmax = 2500.0
				# nbins = int(ceil((xmax-xmin)/10))
				xbins = [0, 10, 20, 40 ,60, 80, 100, 120, 140, 160, 180, 200, 220, 250, 300, 350, 400, 450, 500, 600, 1000, 2000, 3000]
				#print "histo at", histo
			elif "_Eta" in hname:
				if "Hadron" in hname:
					softbin = 3.0
					xbins = [-8.0, -4.0, -softbin]
					newbin = 50
					for n in range(newbin-1):
						xbins.append(xbins[-1] + (2*softbin/newbin))
					xbins = xbins + [softbin, 4.0, 8.0]
				elif "Jet" in hname:
					xmax = 3.0
					xmin = -xmax
					nbins = int(ceil((xmax-xmin)/0.01))
					ngroup = nbins/50
			elif "_E" in hname:
				# xmin = 0.0
				# xmax = 4200.0
				# nbins = int(ceil((xmax-xmin)/10))
				xbins = [0, 10, 20, 40 ,60, 80, 100, 120, 140, 160, 180, 200, 220, 250, 300, 350, 400, 450, 500, 600, 1000, 2000, 3000]
			elif "_Dr" in hname:
				xmin = 0.0
				xmax = 12.0
				nbins = int(ceil((xmax-xmin)/0.01))
				ngroup = nbins/50
			elif "_M" in hname:
				# xmin = 0.0
				# xmax = 2000.0
				# nbins = int(ceil((xmax-xmin)/10))
				xbins = [0, 10, 20, 40 ,60, 80, 100, 120, 140, 160, 180, 200, 220, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1500]
			elif "_Phi" in hname:
				xmin = -3.5
				xmax = 3.5
				nbins = int(ceil((xmax-xmin)/0.01))
				ngroup = nbins/50
			elif "Weight" in hname:
				if "GenValue" in hname or "GEN_nom" in hname:
					xmin = -500
					xmax = -xmin
					nbins =int(ceil((xmax-xmin)/1))
					ngroup = nbins/200
				else:
					xmin = 0.0
					xmax = 1.0
					nbins = int(ceil((xmax-xmin)/0.001))
					ngroup = nbins/200
			elif "N_" in hname or "NHadrons" in hname:
				# xmin = -0.5
				# xmax = 30.5
				# nbins = int(ceil((xmax-xmin)/1))
				ngroup = 1
			else:
				# xmin = chain.GetMinimum(hname)
				# xmax = chain.GetMaximum(hname)
				nbins = 300
				ngroup = nbins/50

			# actually rebin the histogram
			if len(xbins)>0:
				xarray = array("d", xbins)
				ngroup = len(xbins)-1
				histo = histo.Rebin(ngroup, newname, xarray)
			else:
				histo = histo.Rebin(ngroup, newname)
			print str(hname) + ' rebinned for a better overview.'


		else:
			print 'Binning maintained for ' + str(histo.GetName()) + '.'

		if normed:
			norm = histo.Integral()
			if not norm == 0:
				histo.Scale(1.0/norm)
				print str(histo.GetName()) + ' normalized to 1.\n'
			else:
				print "WARNING: histo '%s' has zero integral" % histo.GetName()
		else:
			print 'Norm maintained for ' + str(histo.GetName()) + '.\n'

		legends[histo.GetName()+'_'+str(i)] = Histos[i].GetDirectory().GetName()
		Histos[i] = histo

	print legends

	##Calc Kolmogorov-Smirnov p value
	#ksScore = Histos[0].KolmogorovTest(Histos[1])
	#print ksScore
	#print "KS Score = {}".format(ksScore)
	
	#Make a nice canavas
	canvas=ROOT.TCanvas("canvas"+savename,"canvas"+savename,1500,1200)
	canvasStyle(canvas)
	
	
	#Calc maximum y values for both histos
	maxYvalue=0
	for ikey,key in enumerate(Histos):
		maxYvalue=max(maxYvalue,Histos[ikey].GetMaximum())
	#Scaling the maxY for more room
	maxYvalue=maxYvalue*1.1
	canvas.cd(1)
	
	#Set X-axis title
	Histos[0].GetXaxis().SetTitle(savename)
	
	for ikey, key in enumerate(Histos):
		#Set color and y-axis scale
		key.SetLineColor(ikey+2)
		key.SetMinimum(0.0)
		key.SetMaximum(maxYvalue)

		#Draw histos in same canvas
		if ikey==0:
			key.Draw("HIST E")
		else:
			key.Draw("HIST E SAME")

	#Add legend
	T = ROOT.TLegend(0.2,0.8,0.45,0.9)
	#Label every histo according to the file they came from
	for ih, h in enumerate(Histos):
		legend_entry = legends[h.GetName() + '_' + str(ih)]
		legend_entry = ".".join(legend_entry.split('.')[:-1])
		legend_entry = legend_entry.split('_')
		legend_entry = legend_entry[:-1]
		legend_entry = ' '.join(legend_entry)
		T.AddEntry(Histos[ih], legend_entry, 'l')
	##Create entry for Kolmogorov-Smirnov value
	#dummy_Histo = ROOT.TH1D("Dummy","Dummy",10,0,1)
	#dummy_Histo.SetLineColor(0)
	#dummy_Histo.SetFillColor(0)
	#T.AddEntry(dummy_Histo,"ksScore: %.2E" % Decimal(ksScore) ,"")
	T.Draw("SAME")
	
	#Change canvas
	canvas.cd(2)
	
	# Ratioplot
	ratioclone=Histos[0].Clone()
	canvas.cd(2)
	ratioclones=[]
	for ih, h in enumerate(Histos):
		ratioclones.append(Histos[0].Clone())
		#print ratioclones[ih].GetName(), ratioclones[ih].GetLineColor()
		ratioclones[ih].Divide(Histos[ih],Histos[0])
		#print ratioclones[ih].GetName()
		ratioclones[ih].SetMinimum(0.0)
		ratioclones[ih].SetMaximum(2.0)
		ratioclones[ih].GetYaxis().SetTitle("Ratio")
		ratioclones[ih].GetYaxis().SetTitleSize(2*ratioclones[ih].GetYaxis().GetTitleSize())
		ratioclones[ih].GetXaxis().SetTitle(savename)
		ratioclones[ih].SetLineColor(ih+2)
		setupStyle(ratioclones[ih])
		if ih == 0:
			#Make black line in ratio plot for y=1
			raticlone_dummy = ratioclones[ih].Clone()
			for iBin in range(raticlone_dummy.GetNbinsX()):
					raticlone_dummy.SetBinContent(iBin+1,1.)
			
			#ratioclone.SetLineColor(ROOT.kBlue)    
			raticlone_dummy.SetLineColor(1)
			raticlone_dummy.Draw("HIST E5")
		#if ih == 0:            
		 #   ratioclone.Draw("HIST E3 SAME")
		else:
			ratioclones[ih].Draw("HIST E SAME")
		
	canvas.Update()
	#Save canvas
	canvas.SaveAs(shapePath+"/"+savename+".pdf")
	canvas.SaveAs(shapePath+"/"+savename+".png")





def main(args = sys.argv[1:]):
	''' 
	read in the histos and create plots
	infiles should be .root files filled with the desired histograms 
	'''
	infiles = args
	for infile in infiles:
		infile = os.path.basename(infile)

	print 'Making Ratioplots with ' + str(infiles[0]) + ' as reference file ... \n' 

	# read the input TFiles and append them to a list
	tfs=[]
	for file in infiles:
		tfs.append(ROOT.TFile(file,"READ"))

	# get a list of all keys stored in the TFiles (assuming all TFiles contain the same key content) and write a list of these keys
	kl=None
	for ifile, file in enumerate(tfs):
		tmp = [x.GetName() for x in file.GetListOfKeys()]
		if kl is None:
			kl = tmp
		kl = [x for x in tmp if x in kl]
		# if tfs[0].GetListOfKeys().GetSize() == tfs[ifile].GetListOfKeys().GetSize(): 
		#     continue
		# else:
		#     print 'The given ROOT file ' + str(file) + ' is not compatible. Make sure to forward only ROOT::TFile arguments which contain histograms of the same quantities. \n' + 'Abort!'
		#     exit(0)
	# for key in tfs[0].GetListOfKeys():
	#     kl.append(key.GetName())
	# kl = [x.GetName() for x in tfs[0].GetListOfKeys()]

	# for every key in the keylist get the according histogram
	for k in kl:
		histos=[]
		for f in tfs:
			tmp = f.Get(k)
			if isinstance(tmp, ROOT.TH1):
				histos.append(tmp)
				print histos[-1].GetDirectory().GetName()
				print tmp.GetDirectory().GetName()
		shapePlots(histos = histos, savename = histos[0].GetName())
			
	for f in tfs:
		f.Close()
	


if __name__ == '__main__':
	main()

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

# MCMatchVarProcessor
l_GenTopHad_Eta = []
l_GenTopHad_Phi = []
l_GenTopHad_Pt = []
l_GenTopLep_Eta = []
l_GenTopLep_Phi = []
l_GenTopLep_Pt = []

l_GenTopHad_B_GenJet_Eta = []
l_GenTopHad_B_GenJet_Phi = []
l_GenTopHad_B_GenJet_Pt = []
l_GenTopLep_B_GenJet_Eta = []
l_GenTopLep_B_GenJet_Phi = []
l_GenTopLep_B_GenJet_Pt = []

l_GenTopHad_B_Hadron_Eta = []
l_GenTopHad_B_Hadron_Phi = []
l_GenTopHad_B_Hadron_Pt = []
l_GenTopLep_B_Hadron_Eta = []
l_GenTopLep_B_Hadron_Phi = []
l_GenTopLep_B_Hadron_Pt = []


# AdditionalJetProcessor
l_AdditionalGenBJet_Eta = []
l_AdditionalGenBJet_Phi = []
l_AdditionalGenBJet_Pt = []

l_AdditionalBHadron_Eta = []
l_AdditionalBHadron_Phi = []
l_AdditionalBHadron_Pt = []


ievt=0
for e in chain:
    ievt+=1
    if ievt%5000==0:
        print "at event", ievt
    if not e.GenEvt_I_TTPlusBB > 0: continue
    #branchtitle=t.GetBranch(Electron_Pt).GetTitle()
    #if ("[" in branchtitle):
        #countvariable=branchtitle.rsplit("]",1)[0].split("[")[-1]
    for i in e.GenTopHad_Eta: l_GenTopHad_Eta.append(i)
    for i in e.GenTopHad_Phi: l_GenTopHad_Phi.append(i)
    for i in e.GenTopHad_Pt: l_GenTopHad_Pt.append(i)
    for i in e.GenTopLep_Eta: l_GenTopLep_Eta.append(i)
    for i in e.GenTopLep_Phi: l_GenTopLep_Phi.append(i)
    for i in e.GenTopLep_Pt: l_GenTopLep_Pt.append(i)

    for i in e.GenTopHad_B_GenJet_Eta: l_GenTopHad_B_GenJet_Eta.append(i)
    for i in e.GenTopHad_B_GenJet_Phi: l_GenTopHad_B_GenJet_Phi.append(i)
    for i in e.GenTopHad_B_GenJet_Pt: l_GenTopHad_B_GenJet_Pt.append(i)
    for i in e.GenTopLep_B_GenJet_Eta: l_GenTopLep_B_GenJet_Eta.append(i)
    for i in e.GenTopLep_B_GenJet_Phi: l_GenTopLep_B_GenJet_Phi.append(i)
    for i in e.GenTopLep_B_GenJet_Pt: l_GenTopLep_B_GenJet_Pt.append(i)

    for i in e.GenTopHad_B_Hadron_Eta: l_GenTopHad_B_Hadron_Eta.append(i)
    for i in e.GenTopHad_B_Hadron_Phi: l_GenTopHad_B_Hadron_Phi.append(i)
    for i in e.GenTopHad_B_Hadron_Pt: l_GenTopHad_B_Hadron_Pt.append(i)
    for i in e.GenTopLep_B_Hadron_Eta: l_GenTopLep_B_Hadron_Eta.append(i)
    for i in e.GenTopLep_B_Hadron_Phi: l_GenTopLep_B_Hadron_Phi.append(i)
    for i in e.GenTopLep_B_Hadron_Pt: l_GenTopLep_B_Hadron_Pt.append(i)

    for i in e.AdditionalGenBJet_Eta: l_AdditionalGenBJet_Eta.append(i)
    for i in e.AdditionalGenBJet_Phi: l_AdditionalGenBJet_Phi.append(i)
    for i in e.AdditionalGenBJet_Pt: l_AdditionalGenBJet_Pt.append(i)

    for i in e.AdditionalBHadron_Eta: l_AdditionalBHadron_Eta.append(i)
    for i in e.AdditionalBHadron_Phi: l_AdditionalBHadron_Phi.append(i)
    for i in e.AdditionalBHadron_Pt: l_AdditionalBHadron_Pt.append(i)
    
    

# set histogram boundaries
xmin_GenTopHad_Eta = min(l_GenTopHad_Eta)
xmax_GenTopHad_Eta = max(l_GenTopHad_Eta)
xmin_GenTopHad_Phi = min(l_GenTopHad_Phi)
xmax_GenTopHad_Phi = max(l_GenTopHad_Phi)
xmin_GenTopHad_Pt = min(l_GenTopHad_Pt)
xmax_GenTopHad_Pt = max(l_GenTopHad_Pt)
xmin_GenTopLep_Eta = min(l_GenTopLep_Eta)
xmax_GenTopLep_Eta = max(l_GenTopLep_Eta)
xmin_GenTopLep_Phi = min(l_GenTopLep_Phi)
xmax_GenTopLep_Phi = max(l_GenTopLep_Phi)
xmin_GenTopLep_Pt = min(l_GenTopLep_Pt)
xmax_GenTopLep_Pt = max(l_GenTopLep_Pt)

xmin_GenTopHad_B_Hadron_Eta = min(l_GenTopHad_B_Hadron_Eta)
xmax_GenTopHad_B_Hadron_Eta = max(l_GenTopHad_B_Hadron_Eta)
xmin_GenTopHad_B_Hadron_Phi = min(l_GenTopHad_B_Hadron_Phi)
xmax_GenTopHad_B_Hadron_Phi = max(l_GenTopHad_B_Hadron_Phi)
xmin_GenTopHad_B_Hadron_Pt = min(l_GenTopHad_B_Hadron_Pt)
xmax_GenTopHad_B_Hadron_Pt = max(l_GenTopHad_B_Hadron_Pt)
xmin_GenTopLep_B_Hadron_Eta = min(l_GenTopLep_B_Hadron_Eta)
xmax_GenTopLep_B_Hadron_Eta = max(l_GenTopLep_B_Hadron_Eta)
xmin_GenTopLep_B_Hadron_Phi = min(l_GenTopLep_B_Hadron_Phi)
xmax_GenTopLep_B_Hadron_Phi = max(l_GenTopLep_B_Hadron_Phi)
xmin_GenTopLep_B_Hadron_Pt = min(l_GenTopLep_B_Hadron_Pt)
xmax_GenTopLep_B_Hadron_Pt = max(l_GenTopLep_B_Hadron_Pt)

xmin_GenTopHad_B_GenJet_Eta = min(l_GenTopHad_B_GenJet_Eta)
xmax_GenTopHad_B_GenJet_Eta = max(l_GenTopHad_B_GenJet_Eta)
xmin_GenTopHad_B_GenJet_Phi = min(l_GenTopHad_B_GenJet_Phi)
xmax_GenTopHad_B_GenJet_Phi = max(l_GenTopHad_B_GenJet_Phi)
xmin_GenTopHad_B_GenJet_Pt = min(l_GenTopHad_B_GenJet_Pt)
xmax_GenTopHad_B_GenJet_Pt = max(l_GenTopHad_B_GenJet_Pt)
xmin_GenTopLep_B_GenJet_Eta = min(l_GenTopLep_B_GenJet_Eta)
xmax_GenTopLep_B_GenJet_Eta = max(l_GenTopLep_B_GenJet_Eta)
xmin_GenTopLep_B_GenJet_Phi = min(l_GenTopLep_B_GenJet_Phi)
xmax_GenTopLep_B_GenJet_Phi = max(l_GenTopLep_B_GenJet_Phi)
xmin_GenTopLep_B_GenJet_Pt = min(l_GenTopLep_B_GenJet_Pt)
xmax_GenTopLep_B_GenJet_Pt = max(l_GenTopLep_B_GenJet_Pt)

xmin_AdditionalGenBJet_Eta = min(l_AdditionalGenBJet_Eta)
xmax_AdditionalGenBJet_Eta = max(l_AdditionalGenBJet_Eta)
xmin_AdditionalGenBJet_Phi = min(l_AdditionalGenBJet_Phi)
xmax_AdditionalGenBJet_Phi = max(l_AdditionalGenBJet_Phi)
xmin_AdditionalGenBJet_Pt = min(l_AdditionalGenBJet_Pt)
xmax_AdditionalGenBJet_Pt = max(l_AdditionalGenBJet_Pt)

xmin_AdditionalBHadron_Eta = min(l_AdditionalBHadron_Eta)
xmax_AdditionalBHadron_Eta = max(l_AdditionalBHadron_Eta)
xmin_AdditionalBHadron_Phi = min(l_AdditionalBHadron_Phi)
xmax_AdditionalBHadron_Phi = max(l_AdditionalBHadron_Phi)
xmin_AdditionalBHadron_Pt = min(l_AdditionalBHadron_Pt)
xmax_AdditionalBHadron_Pt = max(l_AdditionalBHadron_Pt)



#h_GenTopHad_Eta = f.Get("GenTopHad_Eta")
#h_GenTopHad_Phi = f.Get("GenTopHad_Phi")
#h_GenTopHad_Pt = f.Get("GenTopHad_Pt")
#h_GenTopLep_Eta = f.Get("GenTopLep_Eta")
#h_GenTopLep_Phi = f.Get("GenTopLep_Phi")
#h_GenTopLep_Pt = f.Get("GenTopLep_Pt")
boundaryfile = os.path.join(os.getcwd(), 'bound_hists.dat')
with open(boundaryfile, 'wb') as textfile:

	textfile.write("GenTopHad_Eta MaxBin = "+ str(xmax_GenTopHad_Eta) + '\n')
	textfile.write("GenTopHad_Eta MinBin = "+ str(xmin_GenTopHad_Eta)+ '\n')

	textfile.write("GenTopHad_Phi MaxBin = "+ str(xmax_GenTopHad_Phi)+ '\n')
	textfile.write("GenTopHad_Phi MinBin = "+ str(xmin_GenTopHad_Phi)+ '\n')
	textfile.write("GenTopHad_Pt MaxBin = "+ str(xmax_GenTopHad_Pt)+ '\n')
	textfile.write("GenTopHad_Pt MinBin = "+ str(xmin_GenTopHad_Pt)+ '\n')

	textfile.write("GenTopLep_Eta MaxBin = "+ str(xmax_GenTopLep_Eta)+ '\n')
	textfile.write("GenTopLep_Eta MinBin = "+ str(xmin_GenTopLep_Eta)+ '\n')

	textfile.write("GenTopLep_Phi MaxBin = "+ str(xmax_GenTopLep_Phi+ '\n')
	textfile.write("GenTopLep_Phi MinBin = "+ str(xmin_GenTopLep_Phi+ '\n')

	textfile.write("GenTopLep_Pt MaxBin = "+ str(xmax_GenTopLep_Pt)+ '\n')
	textfile.write("GenTopLep_Pt MinBin = "+ str(xmin_GenTopLep_Pt)+ '\n')

	textfile.write("\n")


	textfile.write("GenTopHad_BHadron_Eta MaxBin = "+ str(xmax_GenTopHad_B_Hadron_Eta)+ '\n')
	textfile.write("GenTopHad_BHadron_Eta MinBin = "+ str(xmin_GenTopHad_B_Hadron_Eta)+ '\n')

	textfile.write("GenTopHad_BHadron_Phi MaxBin = "+ str(xmax_GenTopHad_B_Hadron_Phi)+ '\n')
	textfile.write("GenTopHad_BHadron_Phi MinBin = "+ str(xmin_GenTopHad_B_Hadron_Phi)+ '\n')

	textfile.write("GenTopHad_BHadron_Pt MaxBin = "+ str(xmax_GenTopHad_B_Hadron_Pt)+ '\n')
	textfile.write("GenTopHad_BHadron_Pt MinBin = "+ str(xmin_GenTopHad_B_Hadron_Pt)+ '\n')

	textfile.write("GenTopLep_BHadron_Eta MaxBin = "+ str(xmax_GenTopLep_B_Hadron_Eta)+ '\n')
	textfile.write("GenTopLep_BHadron_Eta MinBin = "+ str(xmin_GenTopLep_B_Hadron_Eta)+ '\n')

	textfile.write("GenTopLep_BHadron_Phi MaxBin = "+ str(xmax_GenTopLep_B_Hadron_Phi)+ '\n')
	textfile.write("GenTopLep_BHadron_Phi MinBin = "+ str(xmin_GenTopLep_B_Hadron_Phi)+ '\n')

	textfile.write("GenTopLep_BHadron_Pt MaxBin = "+ str(xmax_GenTopLep_B_Hadron_Pt)+ '\n')
	textfile.write("GenTopLep_BHadron_Pt MinBin = "+ str(xmin_GenTopLep_B_Hadron_Pt)+ '\n')
	textfile.write("\n")


	textfile.write("GenTopHad_B_GenJet_Eta MaxBin = "+ str(xmax_GenTopHad_B_GenJet_Eta)+ '\n')
	textfile.write("GenTopHad_B_GenJet_Eta MinBin = "+ str(xmin_GenTopHad_B_GenJet_Eta)+ '\n')

	textfile.write("GenTopHad_B_GenJet_Phi MaxBin = "+ str(xmax_GenTopHad_B_GenJet_Phi)+ '\n')
	textfile.write("GenTopHad_B_GenJet_Phi MinBin = "+ str(xmin_GenTopHad_B_GenJet_Phi)+ '\n')

	textfile.write("GenTopHad_B_GenJet_Pt MaxBin = "+ str(xmax_GenTopHad_B_GenJet_Pt)+ '\n')
	textfile.write("GenTopHad_B_GenJet_Pt MinBin = "+ str(xmin_GenTopHad_B_GenJet_Pt)+ '\n')

	textfile.write("GenTopLep_B_GenJet_Eta MaxBin = "+ str(xmax_GenTopLep_B_GenJet_Eta)+ '\n')
	textfile.write("GenTopLep_B_GenJet_Eta MinBin = "+ str(xmin_GenTopLep_B_GenJet_Eta)+ '\n')

	textfile.write("GenTopLep_B_GenJet_Phi MaxBin = "+ str(xmax_GenTopLep_B_GenJet_Phi)+ '\n')
	textfile.write("GenTopLep_B_GenJet_Phi MinBin = "+ str(xmin_GenTopLep_B_GenJet_Phi)+ '\n')

	textfile.write("GenTopLep_B_GenJet_Pt MaxBin = "+ str(xmax_GenTopLep_B_GenJet_Pt)+ '\n')
	textfile.write("GenTopLep_B_GenJet_Pt MinBin = "+ str(xmin_GenTopLep_B_GenJet_Pt)+ '\n')

	textfile.write("\n")


	textfile.write("AdditionalGenBJet_Eta MaxBin = "+ str(xmax_AdditionalGenBJet_Eta)+ '\n')
	textfile.write("AdditionalGenBJet_Eta MinBin = "+ str(xmin_AdditionalGenBJet_Eta)+ '\n')

	textfile.write("AdditionalGenBJet_Phi MaxBin = "+ str(xmax_AdditionalGenBJet_Phi)+ '\n')
	textfile.write("AdditionalGenBJet_Phi MinBin = "+ str(xmin_AdditionalGenBJet_Phi)+ '\n')

	textfile.write("AdditionalGenBJet_Pt MaxBin = "+ str(xmax_AdditionalGenBJet_Pt)+ '\n')
	textfile.write("AdditionalGenBJet_Pt MinBin = "+ str(xmin_AdditionalGenBJet_Pt)+ '\n')

	textfile.write("\n")


	textfile.write("AdditionalBHadron_Eta MaxBin = "+ str(xmax_AdditionalBHadron_Eta)+ '\n')
	textfile.write("AdditionalBHadron_Eta MinBin = "+ str(xmin_AdditionalBHadron_Eta)+ '\n')

	textfile.write("AdditionalBHadron_Phi MaxBin = "+ str(xmax_AdditionalBHadron_Phi)+ '\n')
	textfile.write("AdditionalBHadron_Phi MinBin = "+ str(xmin_AdditionalBHadron_Phi)+ '\n')

	textfile.write("AdditionalBHadron_Pt MaxBin = "+ str(xmax_AdditionalBHadron_Pt)+ '\n')
	textfile.write("AdditionalBHadron_Pt MinBin = "+ str(xmin_AdditionalBHadron_Pt)+ '\n')




import ROOT
import sys
import os
import glob
from array import array


''' 
read files and write ttbb event data into histograms
use data generated by different generators respectively
execute with "python read.py <PATH/TO/NTUPLES/*.root>"
'''

# read all the .root files and pu the corresponding tree (here: MVATree) into a TChain
infiles = sys.argv[1:]
if len(infiles)>1: True
elif len(infiles)==1: infiles=glob.glob(infiles[0])

chain=ROOT.TChain("MVATree")
for inpath in infiles:
    inpath = os.path.abspath(inpath)
    chain.Add(inpath)
print chain.GetNtrees()

# define and generate histos
nbins = 50
nbins_pT = 251
# Optional: You can get xmin and xmax from a scan of the data. See: askforbins.py
h_N_GenJets = ROOT.TH1D("N_GenJets", "N_GenJets", 40, -10.0, 30.0)
h_GenJet_Pt = ROOT.TH1D("GenJet_Pt", "GenJet_Pt", nbins_pT, -10.0, 2500.0)
h_GenJet_1st_Pt = ROOT.TH1D("GenJet_1st_Pt", "GenJet_1st_Pt", nbins_pT, -10.0, 2500.0)
h_GenJet_2nd_Pt = ROOT.TH1D("GenJet_2nd_Pt", "GenJet_2nd_Pt", nbins_pT, -10.0, 2500.0)
h_GenJet_3rd_Pt = ROOT.TH1D("GenJet_3rd_Pt", "GenJet_3rd_Pt", nbins_pT, -10.0, 2500.0)
h_GenJet_4th_Pt = ROOT.TH1D("GenJet_4th_Pt", "GenJet_4th_Pt", nbins_pT, -10.0, 2500.0)
h_GenJet_5th_Pt = ROOT.TH1D("GenJet_5th_Pt", "GenJet_5th_Pt", nbins_pT, -10.0, 2500.0)
h_GenJet_6th_Pt = ROOT.TH1D("GenJet_6th_Pt", "GenJet_6th_Pt", nbins_pT, -10.0, 2500.0)

h_GenTopHad_Eta = ROOT.TH1D("GenTopHad_Eta", "GenTopHad_Eta", nbins, -12.0, 12.0)
h_GenTopHad_Phi = ROOT.TH1D("GenTopHad_Phi", "GenTopHad_Phi", nbins, -9.0, 3.5)
h_GenTopHad_Pt = ROOT.TH1D("GenTopHad_Pt", "GenTopHad_Pt", nbins_pT, -10.0, 2500.0)
h_GenTopLep_Eta = ROOT.TH1D("GenTopLep_Eta", "GenTopLep_Eta", nbins, -12.0, 12.0)
h_GenTopLep_Phi = ROOT.TH1D("GenTopLep_Phi", "GenTopLep_Phi", nbins, -9.0, 3.5)
h_GenTopLep_Pt = ROOT.TH1D("GenTopLep_Pt", "GenTopLep_Pt", nbins_pT, -10.0, 2500.0)

h_GenTopHad_B_GenJet_Eta = ROOT.TH1D("GenTopHad_B_GenJet_Eta", "GenTopHad_B_GenJet_Eta", nbins, -9.0, 2.5)
h_GenTopHad_B_GenJet_Phi = ROOT.TH1D("GenTopHad_B_GenJet_Phi", "GenTopHad_B_GenJet_Phi", nbins, -9.0, 3.5)
h_GenTopHad_B_GenJet_Pt = ROOT.TH1D("GenTopHad_B_GenJet_Pt", "GenTopHad_B_GenJet_Pt", nbins_pT, -10.0, 2500.0)
h_GenTopLep_B_GenJet_Eta = ROOT.TH1D("GenTopLep_B_GenJet_Eta", "GenTopLep_B_GenJet_Eta", nbins, -9.0, 2.5)
h_GenTopLep_B_GenJet_Phi = ROOT.TH1D("GenTopLep_B_GenJet_Phi", "GenTopLep_B_GenJet_Phi", nbins, -9.0, 3.5)
h_GenTopLep_B_GenJet_Pt = ROOT.TH1D("GenTopLep_B_GenJet_Pt", "GenTopLep_B_GenJet_Pt", nbins_pT, -10.0, 2500.0)

h_GenTopHad_B_Hadron_Eta = ROOT.TH1D("GenTopHad_B_Hadron_Eta", "GenTopHad_B_Hadron_Eta", nbins, -9.0, 6.5)
h_GenTopHad_B_Hadron_Phi = ROOT.TH1D("GenTopHad_B_Hadron_Phi", "GenTopHad_B_Hadron_Phi", nbins, -9.0, 3.5)
h_GenTopHad_B_Hadron_Pt = ROOT.TH1D("GenTopHad_B_Hadron_Pt", "GenTopHad_B_Hadron_Pt", nbins_pT, -10.0, 2500.0)
h_GenTopLep_B_Hadron_Eta = ROOT.TH1D("GenTopLep_B_Hadron_Eta", "GenTopLep_B_Hadron_Eta", nbins, -9.0, 7.0)
h_GenTopLep_B_Hadron_Phi = ROOT.TH1D("GenTopLep_B_Hadron_Phi", "GenTopLep_B_Hadron_Phi", nbins, -9.0, 3.5)
h_GenTopLep_B_Hadron_Pt = ROOT.TH1D("GenTopLep_B_Hadron_Pt", "GenTopLep_B_Hadron_Pt", nbins_pT, -10.0, 2500.0)

h_AdditionalGenBJet_Eta = ROOT.TH1D("AdditionalGenBJet_Eta", "AdditionalGenBJet_Eta", nbins, -2.5, 2.5)
h_AdditionalGenBJet_Phi = ROOT.TH1D("AdditionalGenBJet_Phi", "AdditionalGenBJet_Phi", nbins, -3.5, 3.5)
h_AdditionalGenBJet_Pt = ROOT.TH1D("AdditionalGenBJet_Pt", "AdditionalGenBJet_Pt", nbins_pT, -10.0, 2500.0)

h_AdditionalBHadron_Eta = ROOT.TH1D("AdditionalBHadron_Eta", "AdditionalBHadron_Eta", nbins, -12.0, 12.0)
h_AdditionalBHadron_Phi = ROOT.TH1D("AdditionalBHadron_Phi", "AdditionalBHadron_Phi", nbins, -3.5, 3.5)
h_AdditionalBHadron_Pt = ROOT.TH1D("AdditionalBHadron_Pt", "AdditionalBHadron_Pt", nbins_pT, -10.0, 2500.0)

h_Weight_GEN_nom = ROOT.TH1D("Weight_GEN_nom", "Weight_GEN_nom", nbins, chain.GetMinimum("Weight_GEN_nom"), chain.GetMaximum("Weight_GEN_nom"))



# make sure, that Histo and Variable correspond
Histos = [
h_N_GenJets, h_GenJet_Pt, h_GenJet_1st_Pt, h_GenJet_2nd_Pt, h_GenJet_3rd_Pt, h_GenJet_4th_Pt, h_GenJet_5th_Pt, h_GenJet_6th_Pt,
h_GenTopHad_Eta, h_GenTopHad_Phi, h_GenTopHad_Pt, 
h_GenTopLep_Eta, h_GenTopLep_Phi, h_GenTopLep_Pt,
h_GenTopHad_B_GenJet_Eta, h_GenTopHad_B_GenJet_Phi, h_GenTopHad_B_GenJet_Pt, 
h_GenTopLep_B_GenJet_Eta, h_GenTopLep_B_GenJet_Phi, h_GenTopLep_B_GenJet_Pt, 
h_GenTopHad_B_Hadron_Eta, h_GenTopHad_B_Hadron_Phi, h_GenTopHad_B_Hadron_Pt, 
h_GenTopLep_B_Hadron_Eta, h_GenTopLep_B_Hadron_Phi, h_GenTopLep_B_Hadron_Pt, 
h_AdditionalGenBJet_Eta, h_AdditionalGenBJet_Phi, h_AdditionalGenBJet_Pt, 
h_AdditionalBHadron_Eta, h_AdditionalBHadron_Phi, h_AdditionalBHadron_Pt, 
]
Variables = []
for h in Histos:
    h.Sumw2()
    Variables.append(h.GetName())
Histo_Variable=zip(Histos,Variables)
#print Histo_Variable

# fill the data into the histos, if the event is a tt+b-jets event, weight the events and call Sumw2 for uncertainties
ievt=0
for e in chain:
    ievt+=1
    if ievt%5000==0:
        print "at event", ievt

    if not e.GenEvt_I_TTPlusBB > 0: continue    # GenEvt_I_TTPlusBB =1 for ttb =2 for tt2b =3 for ttbb
    
    for ih,h in enumerate(Histos):
        # for the first, second, ... leading jet histogram: fill it
        names = ["1st_Pt","2nd_Pt","3rd_Pt","4th_Pt","5th_Pt", "6th_Pt"]
        if any( x in h.GetName() for x in names):
            # loop over all possible histograms and fill them with the according jet pT
            for istr, string in enumerate(["1st", "2nd", "3rd", "4th", "5th", "6th"]):
                if "GenJet_" + string in Variables[ih]:
                    dummy = e.GenJet_Pt
                    if len(dummy)>=istr:
                        b = []
                        for i in range(len(dummy)):
                            b.append(dummy[i])

                        if isinstance(b, (long, int, float)): 
                            b = [b]
                        b.sort()
                        h.Fill(b[-istr], e.Weight_GEN_nom*e.Weight_XS)
                else:
                    continue
        else:
            # fill the histograms for all other quantities
            b = getattr(e,Variables[ih])
            #title = b.GetTitle()
    #       if len(b) != 1:
            if isinstance(b, (long, int, float)):
                b = [b]
            for l in range(len(b)):
                    h.Fill(b[l], e.Weight_GEN_nom*e.Weight_XS)
            #else:
             #   h.Fill(b[0], e.Weight_GEN_nom)
    

''' write the histos into a new root file depending on the type of generated data used '''
if "ttbb" and "amcatnlo" in infiles[0]:
    f = ROOT.TFile("ttbb_4FS_amcatnlo_Histos.root","recreate")
    for h in Histos:
        h.Write()
    f.Close()
    
    
elif "TTbb" and "Powheg" in infiles[0]:
    f = ROOT.TFile("ttbb_4FS_Powheg_OL_Histos.root","recreate")
    for h in Histos:
        h.Write()
    f.Close()

elif "TTJets" and "amcatnlo" in infiles[0]:
    f = ROOT.TFile("ttjets_Histos.root","recreate")
    for h in Histos:
        h.Write()
    f.Close()

elif "TTToSemi" in infiles[0]:
    f = ROOT.TFile("tt_semileptonic_Histos.root","recreate")
    for h in Histos:
        h.Write()
    f.Close()


    

import numpy as np
import sys
import os
import ROOT
from decimal import Decimal


ROOT.gStyle.SetPaintTextFormat("4.2f")
ROOT.gROOT.SetBatch(1)
ROOT.gDirectory.cd('PyROOT:/')

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


def getVariables( data ):
    return data.columns


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
    

def calcNorm( variable ):
    print("norming values:")
    allValues = []
    for key in dataDict:
        allValues+= list(dataDict[key].eval(variable))

    mu = np.mean(allValues)
    sig = np.std(allValues)
    print("mu  = "+str(mu))
    print("std = "+str(sig))
    return mu, sig


def setupStyle(graph):
    graph.GetXaxis().SetTitleSize(3*graph.GetXaxis().GetTitleSize())
    # graph.GetXaxis().SetTitleOffset(1.3*graph.GetXaxis().GetTitleOffset())
    graph.GetXaxis().SetLabelSize(2.4*graph.GetXaxis().GetLabelSize())
    
    # graph.GetYaxis().SetTitleSize(2.4*graph.GetXaxis().GetTitleSize())
    # graph.GetYaxis().SetTitleOffset(1.3*graph.GetXaxis().GetTitleOffset())
    # graph.GetYaxis().SetLabelSize(2.4*graph.GetXaxis().GetLabelSize())
    return graph

'''
Function which creates RatioPlots from a list of histograms. It always uses the first histogram in the list as a reference to the others.
'''
def shapePlots( histos, savename="",normed = True ):
    # mkdir
    if normed:
    	shapePath = "./RatioPlots_normed"
    else:
	shapePath = "./RatioPlots"
    if not os.path.exists( shapePath ):
        os.makedirs(shapePath)

    # loop over variables
    
    #create list of histos and normalize them if normed = True
    Histos = histos
    print Histos
    for histo in Histos:
        print histo
        if normed:
            histo.Scale(1.0/histo.Integral())
            print str(histo) + ' normalized to 1 \n'
        else:
            print str(histo) + ' not normalized'

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
        legend_entry = h.GetDirectory().GetName()
        legend_entry = legend_entry.split('.')
        legend_entry = legend_entry[0].split('_')
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



''' read in the histos and create plots
    infiles should be: Powheg_Histos_binned.root, Sherpa_Histos_binned.root '''

def main(args = sys.argv[1:]):
    infiles = args
    for infile in infiles:
        infile = os.path.basename(infile)

    print 'Making Ratioplots with ' + str(infiles[0]) + ' as reference file ... \n' 

    # read the input TFiles and append them to a list
    tfs=[]
    for file in infiles:
        tfs.append(ROOT.TFile(file,"READ"))

    # get a list of all keys stored in the TFiles (assuming all TFiles contain the same key content) and write a list of these keys
    kl=[]
    for ifile, file in enumerate(tfs):
        if tfs[0].GetListOfKeys().GetSize() == tfs[ifile].GetListOfKeys().GetSize(): 
            continue
        else:
            print 'The given ROOT file ' + str(file) + ' is not compatible. Make sure to forward only ROOT::TFile arguments which contain histograms of the same quantities. \n' + 'Abort!'
            exit(0)
    for key in tfs[0].GetListOfKeys():
        kl.append(key.GetName())

    # for every key in the keylist get the according histogram
    for k in kl:
        histos=[]
        for f in tfs:
            histos.append(f.Get(k))
        shapePlots(histos = histos, savename = histos[0].GetName())
            
    for f in tfs:
        f.Close()
    

if __name__ == '__main__':
    main()
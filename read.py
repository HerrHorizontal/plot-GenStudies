import ROOT
import sys
import os
import glob
import subprocess
from array import array
from numpy import ceil
from optparse import OptionParser

classdir = os.path.join(os.getcwd(), "base", "classes")
if not classdir in sys.path:
	sys.path.append(classdir)
from batchConfig_base import batchConfig_base

def parse_args():
	usage = '%prog [options] path/to/ntuples\n' 

	parser = OptionParser(usage = usage)

	parser.add_option( "-p", "--parallel",
					help = "do calculations of the histograms in parallel on batch system (default: False)",
					action = "store_true",
					default = False,
					dest = "run_on_batch"
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

	# make directory system
	workdir = os.getcwd()
	# directory for the finished Histograms
	histdir = os.path.join(workdir,'Histograms')
	if not os.path.exists(histdir):
			os.mkdir(histdir)
	# directory for the finished batches
	batchdir = os.path.join(histdir,'batches')
	if not os.path.exists(batchdir):
			os.mkdir(batchdir)
	# directory for the runscripts
	scriptdir = os.path.join(batchdir,'runscripts')
	if not os.path.exists(scriptdir):
		os.mkdir(scriptdir)

	for infile in infiles:
		infile = os.path.abspath(infile)

	chain = getChain(infiles = infiles)
	low_edges, up_edges = getListOfEdges(chain = chain)
	infiledir = os.path.dirname(infiles[0])
	scriptdir, scriptfiles = makeShellScripts(low_edges = low_edges, up_edges = up_edges, infiledir = infiledir)
	run_ShellScripts(scriptfiles = scriptfiles)
	


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



def getListOfEdges(chain, batchsize = 50000):
	'''
	cut the chain in smaller batches, which can be submitted afterwards and run in parallel
	'''
	nentries = chain.GetEntries()
	chain_cuts = []
	ncuts = nentries/batchsize
	print "Cutting the TChain in " + str(ncuts) + " batches"
	for i in range(ncuts):
		chain_cuts.append(i*batchsize)
	chain_cuts.append(nentries)

	low_edges = chain_cuts[:-1]
	up_edges = chain_cuts[1:]

	return low_edges, up_edges



def makeShellScripts(low_edges, up_edges, infiledir):

	if len(low_edges) != len(up_edges):
		print "Error: Number of low and upper batch boundaries doesn't correspond! Abort!"
		exit()

	edges = zip(low_edges, up_edges)

	datadir = infiledir
	datadir = os.path.abspath(datadir)

	workdir = os.getcwd()
	histdir = os.path.join(workdir, 'Histograms')
	batchdir = os.path.join(histdir, 'batches')
	scriptdir = os.path.join(batchdir, 'runscripts')

	files = []
	for iedge, edge in enumerate(edges):
		batch = str(iedge+1)
		filename = os.path.join(scriptdir, os.path.basename(datadir)+'_batch'+batch+'.sh')
		with open(filename, 'wb') as scriptfile:
			scriptfile.writelines(['# set the CMSSW environment and load all needed modules\n', 
									'#module use -a /afs/desy.de/group/cms/modulefiles/\n', 
									'export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n', 
									'source $VO_CMS_SW_DIR/cmsset_default.sh\n', 
									'export CMSSW_GIT_REFERENCE=/nfs/dust/cms/user/mhorzela/.cmsgit-cache\n', 
									'alias cd=\'cd -P\'\n', 
									'myvarcwd=$PWD\n', 
									'cd /nfs/dust/cms/user/mhorzela/CMSSW_9_4_9/src\n', 
									'eval `scramv1 runtime -sh`\n', 
									'cd ~\n', 
									'echo "setup CMSSW_949 and stuff"\n', 
									'cd $myvarcwd\n\n', 
									])
			scriptfile.writelines(['# fill histo with batch number ' + str(batch) + '\n',
								   'cd ' + str(batchdir) + '\n'])
			scriptfile.writelines(['python ../../fill_histo.py -n ' + batch + ' -l ' + str(edge[0]) + ' -u ' + str(edge[1]) + ' ' + datadir+"/"+os.path.basename(datadir) + '*.root\n'])
			scriptfile.write('cd ' + str(workdir))
		files.append(filename)

	os.chdir(workdir)

	return scriptdir, files

def run_ShellScripts(scriptfiles):

	workdir = os.getcwd()
	histdir = os.path.join(workdir, 'Histograms')
	batchdir = os.path.join(histdir, 'batches')
	scriptdir = os.path.join(batchdir, 'runscripts')

	# check if the scripts are in the right directory
	if scriptdir != os.path.dirname(scriptfiles[0]):
		print "Error: The scriptfiles' are in the wrong directory! They should be in ./Histograms/batches/runscripts ! Abort!"
		exit()

	# set the job properties
	jobids =[]
	print 'Setting job porperties ... \n'
	bc = batchConfig_base()
	bc.diskspace = 3000000
	bc.runtime = 3600 

	# submit the batches in the current stage as an arrayjob to the cluster
	print 'Submitting jobs ... \n'
	arrayscriptpath = os.path.join(scriptdir, os.path.basename(scriptfiles[0]).rsplit('_',1)[0]+'_array.sh')
	jobids += bc.submitArrayToBatch(scripts = scriptfiles, arrayscriptpath = arrayscriptpath)
	print 'Jobs submitted!\n'

	# wait till the jobs are finished, before the next stage is started
	print 'Waiting for jobs to finish ... \n'
	bc.do_qstat(jobids)
	print 'Reading step finished.'

	os.chdir(workdir)



def haddBatches(histfiles):

	workdir = os.getcwd()
	histdir = os.path.join(workdir, 'Histograms')
	batchdir = os.path.join(histdir, 'batches')
	scriptdir = os.path.join(batchdir, 'runscripts')

	histname = os.path.basename(histfiles[0]).split('.')[0].rsplit('_',1)[0]
	haddprocess = 'hadd -k ' +os.path.join(histdir, histname) + ' ' + histfiles
	subprocess.check_call(haddprocess)






if __name__ == '__main__':
	main()
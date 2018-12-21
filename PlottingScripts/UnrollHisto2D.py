from sys import argv, path as spath
from os import path as opath
import ROOT
thisdir = opath.realpath(opath.dirname(__file__))
basedir = opath.join(thisdir, "..", "base")
if not basedir in spath:
    spath.append(basedir)

def cross_check(orig, unrolled):
	bins = unrolled.GetNbinsX()
	x = ROOT.Long(0)
	y = ROOT.Long(0)
	z = ROOT.Long(0)
	for b in range(1, bins+1):
		unrolled.GetBinXYZ(b, x, y, z)
		orig_val = orig.GetBinContent(x, y)
		unrolled_val = unrolled.GetBinContent(b)
		print "origval({2},{3}) = {0}\tunrolled val({4}) = {1}".format(orig_val, unrolled_val, x, y, b)

def do_unrolling(h):
	bins_x = h.GetNbinsX()+2 #also count over and underflow bins
	bins_y = h.GetNbinsY()+2
	allbins = bins_x*bins_y
	hist = ROOT.TH1D("unrolled_" + h.GetName(), "", allbins, 0, allbins)
	hist.Sumw2()
	hist.SetDirectory(0)
	bins = []
	for x in range(0, bins_x):
		for y in range(0, bins_y):
			# print "x={0}\ty={1}".format(x, y)
			current_bin = h.GetBin(x, y)
			bins.append(current_bin)
			current_val = h.GetBinContent(current_bin)
			current_error = h.GetBinError(current_bin)
			# print "bin = {0}\tval = {1}\terr = {2}".format(current_bin, current_val, current_error)
			if current_bin > allbins:
				print "WARNING: global bin is in overflow of unrolled histo", hist.GetName()
			hist.SetBinContent(current_bin, current_val)
			hist.SetBinError(current_bin, current_error)
	norm = hist.Integral()
	if norm < 0:
		print "WARNING: THERE IS SOMETHING STRANGE IN THE NEIGHBORHOOD! Will skip", h.GetName()
		return None
	# print "allbins = {0}\tcounted bins = {1}".format(allbins, len(bins))
	# cross_check(orig = h, unrolled = hist)
	return hist

def unroll_histos(path_to_file):
	infile = ROOT.TFile.Open(path_to_file)
	if f.IsZombie() or f.TestBit(ROOT.TFile.kRecovered):
		print "file '%s' is broken!" % path_to_file
		return None
	hists = []
	keys = infile.GetListOfKeys()
	broken = []
	for key in keys:
		keyname = key.GetName()
		h = infile.Get(keyname)
		if isinstance(h, ROOT.TH2):
			tmp = do_unrolling(h)
			if not tmp is None: 
				hists.append(tmp)
			else:
				broken.append(keyname)


	infile.Close()
	dirname = opath.dirname(path_to_file)
	filename = opath.basename(path_to_file)
	newfilename = opath.join(dirname, "unrolled_" + filename)
	outfile = ROOT.TFile.Open(newfilename, "RECREATE")
	print outfile
	for h in hists:
		print h
		outfile.WriteTObject(h)
	outfile.Close()
	with open("broken_histograms.txt","w") as f:
		f.write("\n".join(broken))

def main(args = argv[1:]):
	
	for path in args:
		if not opath.exists(path):
			print "ERROR: path '%s' does not exist!" % path
			continue
		path = opath.abspath(path)

		unroll_histos(path)





if __name__ == '__main__':
	main()

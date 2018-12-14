import ROOT
import json
import os
import shutil
import fnmatch

class helperClass_base(object):

	def __init__(self):
		print "initializing helperClass"

	def is_number(self, s):
		s.replace("p", ".")
		try:
			float(s)
			return True
		except ValueError:
			print "{0} is not a number!".format(s)
			return False

	def intact_root_file(self, f):

		if f and isinstance(f, ROOT.TFile):
			if f.IsOpen() and not f.IsZombie() and not f.TestBit(ROOT.TFile.kRecovered):
				return True
		return False
	
	def is_good_fit(self, result):
		if result.status() == 0 and result.covQual() == 3:
			return True
		print "WARNING: This is not a good fit!"
		print "\tStatus: {0}\tQuality: {1}".format(result.status(), result.covQual())
		return False

	def load_roofitresult(self, rfile):
		result = rfile.Get("fit_s")
		if not isinstance(result, ROOT.RooFitResult):
			result = rfile.Get("fit_mdf")
			if not isinstance(result, ROOT.RooFitResult):
				result = None
		if result and not self.is_good_fit(result):
			result = None
		
		return result


	def load_variable(self, result, parname):
		var = result.floatParsFinal().find(parname)
		if isinstance(var, ROOT.RooRealVar):
			return var

	def load_postfit_uncert_from_variable(self, filename, parname):
		f = ROOT.TFile(filename)
		error = None
		if self.intact_root_file(f):
			result = self.load_roofitresult(rfile = f)
			if result:
				var = self.load_variable(result = result, parname = parname)
				if var:
					error = var.getError()
		if f.IsOpen(): f.Close()
		return error

	def load_postfit_uncert(self, filename, parname):
		vals = self.load_asym_postfit(filename = filename, parname = parname)
		if vals:
			value = (vals[1] + vals[2])/2
			if value != 0:
				return value
			else:
				return self.load_postfit_uncert_from_variable(filename = filename, parname = parname)


	def load_asym_postfit(self, filename, parname):
		f = ROOT.TFile.Open(filename)
		if self.intact_root_file(f):
			result = self.load_roofitresult(rfile = f)
			if result:
				var = self.load_variable(result = result, parname = parname)
				if var:
					value = var.getVal()
					errorhi = var.getErrorHi()
					errorlo = var.getErrorLo()
					f.Close()
					return value, errorhi, abs(errorlo)
				else:
					print "Could not load RooRealVar %s from %s" % (parname, filename)
			else:
				print "Could not load RooFitResult from %s" % (filename)
		else:
			print "File %s is not intact!" % filename
		if f.IsOpen(): f.Close()
		return None

	def load_correlation(self, filename, par1, par2):
		f = ROOT.TFile.Open(filename)
		correlation = None
		if self.intact_root_file(f):
			result = self.load_roofitresult(rfile = f)
			if result:
				parts = result.floatParsFinal().contentsString().split(",")
				if par1 in parts:
					if par2 in parts:
						correlation = result.correlation(par1, par2)
					else:
						print "Parameter %s is not part of this fit model! Skipping" % par2
				else:
					print "Parameter %s is not part of this fit model! Skipping" % par1
		else:
			print "File %s is not intact!" % filename
		if f.IsOpen(): f.Close()
		return correlation


	def dump_json(self, outname, allvals):
		if len(allvals) > 0:
			print "opening file", outname
			with open(outname, "w") as outfile:
				json.dump(allvals, outfile, indent = 4, separators = (',', ': '))

	def get_lumi_from_filename(self, filename):
		temp = "_".join(filename.split(".")[:-1])
		parts = temp.split("_")
		lumistring = ""
		for i, part in enumerate(parts):
			print i,part

			if i != len(parts) and part == "lumi" and self.is_number(parts[i+1].replace("p", ".")):
				return float(parts[i+1].replace("p", "."))
		return None

	def insert_values(self, cmds, keyword, toinsert, joinwith=","):
		if keyword in cmds:
			i = cmds.index(keyword)
			if joinwith == "replace":
				cmds[i+1] = toinsert
			elif joinwith == "insert":
				pass
			elif joinwith == "remove":
				print "removing",keyword, toinsert
				print "index:", cmds.index(keyword)
				# cmds = [x for j, x in enumerate(cmds) if j != i or j!= i+1]
				cmds = cmds[:i] + cmds[i+2:]
				print cmds
			else:
				cmds[i+1] = joinwith.join([cmds[i+1],toinsert])
		else:
			if not joinwith == "remove":
				cmds += [keyword, toinsert]
		return cmds

	def save_canvas(self, c, outname):
		outname = self.treat_special_chars(outname)
		c.SaveAs(outname + ".pdf")
		c.SaveAs(outname + ".png")
		c.SaveAs(outname + ".root")

	def treat_special_chars(self, string):
	    string = string.replace("#", "")
	    string = string.replace(" ", "_")
	    string = string.replace("{", "")
	    string = string.replace("}", "")
	    string = string.replace("?", "X")
	    string = string.replace("*", "X")
	    return string

  	def create_folder(self, folder, reset = False):
		if reset:
			if os.path.exists(folder):
				shutil.rmtree(folder)

		if not os.path.exists(folder):
			os.makedirs(folder)	

	def lsDirectory(self, fullpath, filewildcard = "*.root"):
		print "checking path", fullpath
		filelist = []
		epath = ROOT.gSystem.ExpandPathName(fullpath)
		dirpointer = ROOT.gSystem.OpenDirectory(epath)
		if dirpointer: 
			file = ROOT.gSystem.GetDirEntry(dirpointer)
			while file: 
				# print file
				fnames = fnmatch.filter([file], filewildcard)
				if len(fnames) == 1:
					fname = os.path.join(fullpath, fnames[0])
					filelist.append(fname)
				file = ROOT.gSystem.GetDirEntry(dirpointer)
		# print filelist
		return filelist

	def generate_file(self, code, outpath):
		print "creating file", outpath
		with open(outpath, "w") as f:
			f.write(code)
		if os.path.exists(outpath):
			return outpath
		return None
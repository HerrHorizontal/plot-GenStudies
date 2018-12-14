from sys import argv
from os import path as opath, getcwd
from glob import glob

def load_classes():
	thisdir = opath.dirname(opath.realpath(__file__))
	thisdir = opath.abspath(thisdir)
	classdir = opath.join(thisdir, "classes")
	return glob(opath.join(classdir, "*.py"))

def gen_code(subclassname, classname, parentdir):
	lines = ['from sys import path as spath']
	lines += ['baserepodir = "%s"' % parentdir]
	lines += ['if not baserepodir in spath:']
	lines += ['\tspath.append(baserepodir)']
	lines += ['from {0} import {0}'.format(classname)]
	lines += ['class {0}({1}):'.format(subclassname, classname)]
	lines += ['\tdef __init__(self):']
	lines += ['\t\tsuper(%s, self).__init__()' % subclassname]
	return "\n".join(lines)

def init_class(targetpath, classfile):
	filename = opath.basename(classfile)
	parentdir = opath.dirname(classfile)
	classname = ".".join(filename.split(".")[:-1])
	subclassname = classname.replace("_base", "")
	code = gen_code(subclassname = subclassname, classname = classname, parentdir = parentdir)
	scriptpath = opath.join(targetpath, subclassname+".py")
	if not opath.exists(scriptpath):
		with open(scriptpath,"w") as f:
			f.write(code)
		print "initialized subclass {0} in {1}".format(subclassname, scriptpath)
		print "IMPORTANT: Please do not forget to check the '__init__' function (created class with default)!"
	else:
		print "script already exists: %s! If you want to reinitialize please remove that file" % scriptpath

def main(args = argv):
	targetpath = args[1]
	classes = []
	if len(args)>2:
		for arg in args[2:]:
			if opath.exists(arg):
				arg = opath.abspath(arg)
				classes.append(arg)
			else:
				print "%s does not exist, skipping" % arg

	if len(classes) == 0:
		classes = load_classes()

	if opath.exists(targetpath):
		for cl in classes:
			init_class(targetpath = targetpath, classfile = cl)
	else:
		print "%s does not exist!" % targetpath

if __name__ == '__main__':
	main(argv)

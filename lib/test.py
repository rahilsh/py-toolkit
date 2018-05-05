import sys
#import glob
#for name in sorted(glob.glob('/Users/rahil.r/Documents/repo/local/reports/1/*.jrxml')):
#	print(name)

#from lxml import etree
#tree = etree.parse("/Users/rahil.r/Documents/repo/local/reports/1/actor/actor.jrxml")
#root = tree.getroot()
#print(root.tag)
#import pdb; pdb.set_trace()
#for country in root.findall("{"+root.nsmap.get(None)+"}"+"property"):
#	value = country.get("value")
#	name  = country.get("name")
#	print(name+" : "+value)

#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument('--environment', help='Enter environment', default='local')
#parser.add_argument('--dry-run', action="store_true", default=False)
#args = parser.parse_args()
#print args.environment
#print args.dry_run




#def file_get_contents(filename):
#    with open(filename) as f:
#        return f.read()


#print file_get_contents("/Users/rahil.r/Documents/repo/analytics-infra/src/main/python/jasper-deployment/LastProcessedCommit.txt")
print sys.path[0]

#!/usr/bin/env python3
import sys
import numpy as np
import pandas as pd
import argparse
import sys

class HelpfulParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = HelpfulParser(description=__doc__,
    epilog="""Johannes Buchner (C) 2020-2021 <johannes.buchner.acad@gmx.com>""",
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--samples", type=int, default=1000,
                    help="Number of samples to use")
parser.add_argument('--parameter', type=str, required=True,
                    help="Name of the fitting parameter to extract")
parser.add_argument('paths', type=str, nargs='+',
                    help="Folders of UltraNest runs")
parser.add_argument('--out', '-o', type=str, required=True,
                    help="Output file name")
parser.add_argument('--verbose', '-v', help="Show progress", action='store_true')

args = parser.parse_args()

paramname = args.parameter
num_samples = args.samples
dirnames = args.paths

print("columns: %s" % (pd.read_csv(dirnames[0] + 'chains/equal_weighted_post.txt', sep=' ').columns.tolist()))

results = np.empty((len(dirnames), num_samples))

if args.verbose:
	import tqdm
	dirnames = tqdm.tqdm(dirnames)

for i, dirname in enumerate(dirnames):
	df = pd.read_csv(dirname + 'chains/equal_weighted_post.txt', sep=' ', usecols=(paramname,))
	if len(df) > num_samples:
		results[i] = df[paramname].values[:num_samples]
	else:
		print("padding %s" % dirname)
		results[i] = np.hstack(tuple([df[paramname].values] * 10))[:num_samples]

if args.verbose:
	print("writing to '%s' ... " % args.out)
np.savetxt(args.out, results)

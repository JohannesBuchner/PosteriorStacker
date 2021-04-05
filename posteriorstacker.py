#!/usr/bin/env python3
"""
Posterior stacking tool.

Johannes Buchner (C) 2020-2021

Given posterior distributions of some parameter from many objects,
computes the sample distribution, using a simple hierarchical model.

The method is described in Baronchelli, Nandra & Buchner (2020)
https://ui.adsabs.harvard.edu/abs/2020MNRAS.498.5284B/abstract
Two computations are performed with this tool:

- Gaussian model (as in the paper)
- Histogram model (using a Dirichlet prior distribution)

The histogram model is non-parametric and more flexible.
Both models are computed using UltraNest.
The output is plotted.
"""

import numpy as np
import matplotlib.pyplot as plt
import ultranest, ultranest.stepsampler
import scipy.stats
import argparse

class HelpfulParser(argparse.ArgumentParser):
	def error(self, message):
		sys.stderr.write('error: %s\n' % message)
		self.print_help()
		sys.exit(2)

parser = HelpfulParser(description=__doc__,
	epilog="""Johannes Buchner (C) 2020 <johannes.buchner.acad@gmx.com>""",
	formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('filename', type=str, 
                    help="Filename containing posterior samples, one object per line")
parser.add_argument("low", type=float,
					help="Lower end of the distribution")
parser.add_argument("high", type=float,
					help="Upper end of the distribution")
parser.add_argument('nbins', type=int,
					help="Number of histogram bins")
parser.add_argument('--verbose', type=bool, help="Show progress")
parser.add_argument('--name', type=str, default="Parameter", help="Parameter name (for plot)")

args = parser.parse_args()
filename = args.filename

data = np.loadtxt(filename)
Nobj, Nsamples = data.shape
minval = args.low
maxval = args.high
ndim = args.nbins
viz_callback = 'auto' if args.verbose else None

bins = np.linspace(minval, maxval, ndim+1)
bins_lo = bins[:-1]
bins_hi = bins[1:]

binned_data = np.array([np.histogram(row, bins=bins)[0] for row in data])

print("fitting histogram model...")

param_names = ['bin%d' % (i+1) for i in range(ndim)]

def likelihood(params):
	return np.log((binned_data * params).sum(axis=1) / Nsamples * ndim + 1e-300).sum()

def transform_dirichlet(quantiles):
    # https://en.wikipedia.org/wiki/Dirichlet_distribution#Random_number_generation
    # first inverse transform sample from Gamma(alpha=1,beta=1), which is Exponential(1)
    gamma_quantiles = -np.log(quantiles)
    # dirichlet variables
    return gamma_quantiles / gamma_quantiles.sum()

sampler = ultranest.ReactiveNestedSampler(param_names, likelihood, transform_dirichlet, 
	log_dir=filename + '_out_flex%d' % ndim, resume=True)
sampler.stepsampler = ultranest.stepsampler.RegionBallSliceSampler(40, region_filter=False)
result = sampler.run(frac_remain=0.5, viz_callback=viz_callback)
sampler.print_results()
sampler.plot()

print("fitting gaussian model...")

gparam_names = ['mean', 'std']

def glikelihood(params):
	mean, std = params
	return np.log(scipy.stats.norm(mean, std).pdf(data).mean(axis=1) + 1e-300).sum()

def gtransform(cube):
	params = cube.copy()
	params[0] = 3 * (maxval - minval) * cube[0] + minval
	params[1] = cube[1] * (maxval - minval) * 3
	return params

gsampler = ultranest.ReactiveNestedSampler(gparam_names, glikelihood, gtransform, 
	log_dir=filename + '_out_gauss', resume=True, vectorized=False)
gresult = gsampler.run(frac_remain=0.5, viz_callback=viz_callback)
gsampler.print_results()
gsampler.plot()

print("plotting results ...")

from ultranest.plot import PredictionBand

plt.errorbar(
	x=(bins_hi+bins_lo)/2,
	xerr=(bins_hi-bins_lo)/2,
	y=binned_data.mean(axis=0) / Nsamples / (bins_hi-bins_lo),
	yerr=binned_data.std(axis=0) / Nsamples / (bins_hi-bins_lo),
	linestyle=' ', color='lightgray',
	label='Averaged Posteriors')

x = np.linspace(minval, maxval, 400)
band = PredictionBand(x)

for mean, std in gresult['samples']:
	band.add(scipy.stats.norm(mean, std).pdf(x))
band.line(color='r', label='Gaussian model')
band.shade(alpha=0.5, color='r')

plt.errorbar(
	x=(bins_hi+bins_lo)/2,
	xerr=(bins_hi-bins_lo)/2,
	y=result['samples'].mean(axis=0) / (bins_hi-bins_lo),
	yerr=result['samples'].std(axis=0) / (bins_hi-bins_lo),
	marker='o', linestyle=' ', color='k',
	label='Histogram model')

plt.xlabel(args.name)
plt.ylabel('Probability density')
plt.legend(loc='best')
plt.savefig(filename + '_out.pdf', bbox_inches='tight')
plt.close()

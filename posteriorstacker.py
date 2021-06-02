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
import argparse
import sys

__version__ = '0.6.1'

class HelpfulParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = HelpfulParser(description=__doc__,
    epilog="""Johannes Buchner (C) 2020-2021 <johannes.buchner.acad@gmx.com>""",
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

# compute KL for each object:
prior = (1. / ndim)
density = (binned_data + 0.1) / ((binned_data + 0.1).sum(axis=1)).reshape((-1, 1))
KL = (density * np.log2((density / prior))).sum(axis=1)
for i in np.argsort(KL):
    plt.plot(
        bins[:-1], binned_data[i] / binned_data[i].sum(),
        drawstyle='steps-pre',
        alpha=0.25 if KL[i] < 2 else None,
        color='gray' if KL[i] < 1 else 'k' if KL[i] < 2 else None,
        label=None if KL[i] < 2 else i
    )
plt.xlabel(args.name)
plt.ylabel('Probability density')
plt.legend(loc='best', title='Input row', prop=dict(size=6))
plt.savefig(filename + '_hists.pdf', bbox_inches='tight')
plt.close()

print("fitting histogram model...")

param_names = ['bin%d' % (i+1) for i in range(ndim)]

def likelihood(params):
    """Histogram model"""
    return np.log(np.dot(binned_data, params) / Nsamples + 1e-300).sum()

def transform_dirichlet(quantiles):
    """Histogram distribution priors"""
    # https://en.wikipedia.org/wiki/Dirichlet_distribution#Random_number_generation
    # first inverse transform sample from Gamma(alpha=1,beta=1), which is Exponential(1)
    gamma_quantiles = -np.log(quantiles)
    # dirichlet variables
    return gamma_quantiles / gamma_quantiles.sum()

sampler = ultranest.ReactiveNestedSampler(
    param_names, likelihood, transform_dirichlet,
    log_dir=filename + '_out_flex%d' % ndim, resume=True)
sampler.stepsampler = ultranest.stepsampler.RegionBallSliceSampler(40, region_filter=False)
result = sampler.run(frac_remain=0.5, viz_callback=viz_callback)
sampler.print_results()
sampler.plot()

print("fitting gaussian model...")

gparam_names = ['mean', 'std']

def normal_pdf(x, mean, std):
    """Same as scipy.stats.norm(norm, std).pdf(x), but faster."""
    return np.exp(-0.5 * ((x - mean) / std)**2) / (std * (2 * np.pi)**0.5)

def glikelihood(params):
    """Gaussian sample distribution"""
    mean, std = params
    return np.log(normal_pdf(data, mean, std).mean(axis=1) + 1e-300).sum()

def gtransform(cube):
    """Gaussian sample distribution priors"""
    params = cube.copy()
    params[0] = 3 * (maxval - minval) * cube[0] + minval
    params[1] = cube[1] * (maxval - minval) * 3
    return params

gsampler = ultranest.ReactiveNestedSampler(
    gparam_names, glikelihood, gtransform,
    log_dir=filename + '_out_gauss', resume=True)
gresult = gsampler.run(frac_remain=0.5, viz_callback=viz_callback)
gsampler.print_results()


avg_mean, avg_std = gresult['samples'].mean(axis=0)
N_resolved = np.logical_and(data > avg_mean - 5 * avg_std, data < avg_mean + 5 * avg_std).sum(axis=1)
import warnings
N_undersampled = (N_resolved < 20).sum()
if N_undersampled > 0:
    warnings.warn("std may be over-estimated: too few samples to resolve the distribution in %d objects." % N_undersampled)

print()
print("Vary the number of samples to check numerical stability!")

print("plotting results ...")
gsampler.plot()


plt.figure(figsize=(5,3))
from ultranest.plot import PredictionBand

lo_data = np.quantile(binned_data, 0.15865525393145707, axis=0)
mid_data = np.quantile(binned_data, 0.5, axis=0)
hi_data = np.quantile(binned_data, 0.8413447460685429, axis=0)

"""
plt.errorbar(
    x=(bins_hi+bins_lo)/2,
    xerr=(bins_hi-bins_lo)/2,
    y=mid_data / Nsamples / (bins_hi-bins_lo),
    yerr=[
        (mid_data - lo_data) / Nsamples / (bins_hi-bins_lo), 
        (hi_data - mid_data) / Nsamples / (bins_hi-bins_lo)
    ],
    linestyle=' ', color='lightgray',
    label='Averaged Posteriors')
"""

x = np.linspace(minval, maxval, 400)
band = PredictionBand(x)

for mean, std in gresult['samples']:
    band.add(normal_pdf(x, mean, std))
band.line(color='r', label='Gaussian model')
band.shade(alpha=0.5, color='r')

lo_hist = np.quantile(result['samples'], 0.15865525393145707, axis=0)
mid_hist = np.quantile(result['samples'], 0.5, axis=0)
hi_hist = np.quantile(result['samples'], 0.8413447460685429, axis=0)

plt.errorbar(
    x=(bins_hi+bins_lo)/2,
    xerr=(bins_hi-bins_lo)/2,
    y=result['samples'].mean(axis=0) / (bins_hi-bins_lo),
    yerr=[
        (mid_hist - lo_hist) / (bins_hi-bins_lo), 
        (hi_hist - mid_hist) / (bins_hi-bins_lo)
    ],
    marker='o', linestyle=' ', color='k',
    label='Histogram model', capsize=2)

plt.xlabel(args.name)
plt.ylabel('Probability density')
plt.legend(loc='best')
plt.savefig(filename + '_out.pdf', bbox_inches='tight')
plt.close()

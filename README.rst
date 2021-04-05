PosteriorStacker
==================

Combines Bayesian analyses from many datasets.

Introduction
-------------------

Fitting a model to a data set gives 
posterior probability distributions for a parameter of 
interest. But how do you combine such probability
distributions if you have many datasets?

This question arises frequently in astronomy when
analysing samples, and trying to infer sample
distributions of some quantity.

PosteriorStacker allows deriving sample
distributions from posterior distributions from a number of objects.

Method
-------------------

The method is described in 
`Baronchelli, Nandra & Buchner (2020) <https://ui.adsabs.harvard.edu/abs/2020MNRAS.498.5284B/abstract>`_

The hierarchical Bayesian model models a Gaussian sample distribution
(with unknown mean and standard deviation). The per-object
parameters are also unknown, but integrated out numerically using
the posterior samples.

Additional to the Gaussian model (as in the paper), 
a histogram model (using a Dirichlet prior distribution) is computed,
which is non-parametric and more flexible.
Both models are inferred using `UltraNest <https://johannesbuchner.github.io/UltraNest/>`_.

The output is plotted.

Getting started
-------------------

0. Install the required libraries (scipy, matplotlib, ultranest) with pip or similar.

1. Prepare an ascii file with each row containing one object's posterior samples.
   The file should be readable with numpy.loadtxt.

2. run for usage instructions::

	$ python3 posteriorstacker.py --help
	usage: posteriorstacker.py [-h] [--verbose VERBOSE] [--name NAME] filename low high nbins

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

	positional arguments:
	  filename           Filename containing posterior samples, one object per line
	  low                Lower end of the distribution
	  high               Upper end of the distribution
	  nbins              Number of histogram bins

	optional arguments:
	  -h, --help         show this help message and exit
	  --verbose VERBOSE  Show progress
	  --name NAME        Parameter name (for plot)

	Johannes Buchner (C) 2020 <johannes.buchner.acad@gmx.com>

   for example::

	$ python3 posteriorstacker.py NH_posteriors.txt.gz 20 26 10 --name '$\log(N_H/\mathrm{cm}^2)$"

3. analyse output files: 

  * filename.txt_out.pdf contains a plot, 
  * filename.txt_out_gauss contain the ultranest analyses output assuming a Gaussian distribution.
  * filename.txt_out_flexN contain the ultranest analyses output assuming a histogram model.
  * The directories include diagnostic plots, corner plots and posterior samples of the distribution parameters.

With these output files, you can:

* plot the sample parameter distribution
* report the mean and spread, and their uncertainties
* split the sample by some parameter, and plot the sample mean as a function of that parameter.

If you want to adjust the parameter plot, just edit the script.

Licence
--------
AGPLv3 (see COPYING file). Contact me if you need a different licence.

PosteriorStacker
==================

Combines Bayesian analyses from many datasets.

* `Introduction <#introduction>`_
* `Method <#method>`_
* `Tutorial <#tutorial>`_
* `Output plot <#visualising-the-results>`_ and files

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

The method is described in Appendix A of
`Baronchelli, Nandra & Buchner (2020) <https://ui.adsabs.harvard.edu/abs/2020MNRAS.498.5284B/abstract>`_.

.. image:: hbm.png

The inputs are posterior samples of a single parameter,
for a number of objects. These need to come from pre-existing analyses,
under a flat parameter prior.

The hierarchical Bayesian model (illustrated above) models the sample distribution
as a Gaussian with unknown mean and standard deviation. The per-object
parameters are also unknown, but integrated out numerically using
the posterior samples.

Additional to the Gaussian model (as in the paper), 
a histogram model (using a flat Dirichlet prior distribution) is computed,
which is non-parametric and more flexible.
Both models are inferred using `UltraNest <https://johannesbuchner.github.io/UltraNest/>`_.

The output is visualised in a publication-ready plot.

Synopsis of the program::

	$ posteriorstacker.py --help
	usage: posteriorstacker.py [-h] [--verbose VERBOSE] [--name NAME]
	                           filename low high nbins
	
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
	
	Johannes Buchner (C) 2020-2021 <johannes.buchner.acad@gmx.com>

Licence
--------
AGPLv3 (see COPYING file). Contact me if you need a different licence.

Install
--------

.. image:: https://img.shields.io/pypi/v/PosteriorStacker.svg
        :target: https://pypi.python.org/pypi/PosteriorStacker

.. image:: https://travis-ci.com/JohannesBuchner/PosteriorStacker.svg?branch=main
    :target: https://travis-ci.com/JohannesBuchner/PosteriorStacker

Install as usual::

	pip install posteriorstacker

This also installs the required `ultranest <https://johannesbuchner.github.io/UltraNest/>`_
python package.

Tutorial
=================================

In this tutorial you will learn:

* How to find a intrinsic distribution from data with asymmetric error bars and upper limits
* How to use PosteriorStacker

Lets say we want to find the intrinsic velocity dispersion given some noisy data points.

Our data are velocity measurements of a few globular cluster velocities in a dwarf galaxy,
fitted with some model.

Preparing the inputs
---------------------

For generating the demo input files and plots, run::

	$ python3 tutorial/gendata.py

You can also import posterior points from ultranest output folders::

	$ load_ultranest_outputs.py --help
	usage: load_ultranest_outputs.py [-h] [--samples SAMPLES] --parameter
	                                 PARAMETER --out OUT [--verbose]
	                                 paths [paths ...]
	
	Built-in functions, exceptions, and other objects.
	
	Noteworthy: None is the `nil' object; Ellipsis represents `...' in slices.
	
	positional arguments:
	  paths                 Folders of UltraNest runs
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --samples SAMPLES     Number of samples to use
	  --parameter PARAMETER
	                        Name of the fitting parameter to extract
	  --out OUT, -o OUT     Output file name
	  --verbose, -v         Show progress
	
	Johannes Buchner (C) 2020-2021 <johannes.buchner.acad@gmx.com>

Visualise the data
----------------------

Lets plot the data first to see what is going on:

.. image:: example.png

**Caveat on language**: These are not actually "the data" (which are counts on a CCD).
Instead, this is a intermediate representation of a posterior/likelihood,
assuming flat priors on velocity.

Data properties
-----------------

This scatter plot shows:

* large, sometimes asymmetric error bars
* intrinsic scatter

Resampling the data
--------------------

We could also represent each data point by a cloud of samples. Each point represents a possible true solution of that galaxy.

.. image:: example-samples.png

Running PosteriorStacker
=========================

We run the script with a range limit of +-100 km/s::

	$ python3 posteriorstacker.py posteriorsamples.txt -80 +80 11 --name="Velocity [km/s]"
	fitting histogram model...
	[ultranest] Sampling 400 live points from prior ...
	[ultranest] Explored until L=-1e+01  
	[ultranest] Likelihood function evaluations: 112359
	[ultranest] Writing samples and results to disk ...
	[ultranest] Writing samples and results to disk ... done
	[ultranest]   logZ = -20.46 +- 0.06632
	[ultranest] Effective samples strategy satisfied (ESS = 779.4, need >400)
	[ultranest] Posterior uncertainty strategy is satisfied (KL: 0.46+-0.06 nat, need <0.50 nat)
	[ultranest] Evidency uncertainty strategy is satisfied (dlogz=0.15, need <0.5)
	[ultranest]   logZ error budget: single: 0.08 bs:0.07 tail:0.41 total:0.41 required:<0.50
	[ultranest] done iterating.
	
	logZ = -20.442 +- 0.431
	  single instance: logZ = -20.442 +- 0.075
	  bootstrapped   : logZ = -20.458 +- 0.146
	  tail           : logZ = +- 0.405
	insert order U test : converged: False correlation: 394.0 iterations
	
	    bin1                0.047 +- 0.045
	    bin2                0.056 +- 0.051
	    bin3                0.067 +- 0.056
	    bin4                0.061 +- 0.058
	    bin5                0.105 +- 0.083
	    bin6                0.32 +- 0.14
	    bin7                0.16 +- 0.10
	    bin8                0.052 +- 0.051
	    bin9                0.045 +- 0.043
	    bin10               0.046 +- 0.046
	    bin11               0.044 +- 0.043
	fitting gaussian model...
	[ultranest] Sampling 400 live points from prior ...
	[ultranest] Explored until L=-4e+01  
	[ultranest] Likelihood function evaluations: 4584
	[ultranest] Writing samples and results to disk ...
	[ultranest] Writing samples and results to disk ... done
	[ultranest]   logZ = -47.35 +- 0.1094
	[ultranest] Effective samples strategy satisfied (ESS = 1026.2, need >400)
	[ultranest] Posterior uncertainty strategy is satisfied (KL: 0.46+-0.06 nat, need <0.50 nat)
	[ultranest] Evidency uncertainty strategy is satisfied (dlogz=0.28, need <0.5)
	[ultranest]   logZ error budget: single: 0.13 bs:0.11 tail:0.41 total:0.42 required:<0.50
	[ultranest] done iterating.
	
	logZ = -47.358 +- 0.491
	  single instance: logZ = -47.358 +- 0.125
	  bootstrapped   : logZ = -47.351 +- 0.276
	  tail           : logZ = +- 0.405
	insert order U test : converged: False correlation: 3.0 iterations
	
	    mean                -0.5 +- 4.8
	    std                 11.9 +- 5.2
	
	Vary the number of samples to check numerical stability!
	plotting results ...

Notice the parameters of the fitted gaussian distribution above.
The standard deviation is quite small (which was the point of the original paper).
A corner plot is at posteriorsamples.txt_out_gauss/plots/corner.pdf


Visualising the results
-----------------------

Here is the output plot, converted to png for this tutorial with::

	$ convert -density 100 posteriorsamples.txt_out.pdf out.png

.. image:: out.png

In black, we see the non-parametric fit.
The red curve shows the gaussian model.

The histogram model indicates that a more heavy-tailed distribution
may be better.

The error bars in gray is the result of naively averaging the posteriors.
This is not a statistically meaningful procedure,
but it can give you ideas what models 
you may want to try for the sample distribution.

Output files
------------

* posteriorsamples.txt_out.pdf contains a plot, 
* posteriorsamples.txt_out_gauss contain the ultranest analyses output assuming a Gaussian distribution.
* posteriorsamples.txt_out_flexN contain the ultranest analyses output assuming a histogram model.
* The directories include diagnostic plots, corner plots and posterior samples of the distribution parameters.
* posteriorsamples.txt_hists.pdf shows the input histograms, and highlights the most informative ones.

With these output files, you can:

* plot the sample parameter distribution
* report the mean and spread, and their uncertainties
* split the sample by some parameter, and plot the sample mean as a function of that parameter.

If you want to adjust the plot, just edit the script.

If you want to try a different distribution, adapt the script.
It uses `UltraNest <https://johannesbuchner.github.io/UltraNest/>`_
for the inference.

Take-aways
-----------

* PosteriorStacker computed a intrinsic distribution from a set of uncertain measurements
* This tool can combine arbitrarily pre-existing analyses.
* No assumptions about the posterior shapes were necessary -- multi-modal and asymmetric works fine.

## pRF_sim

Here is a repository that uses 'Shablona' as a template (https://github.com/uwescience/shablona). As a result, there are things in here we may not need and a few things that will need to be populated with the relevant info for this package.

## Installation.

1. Git clone
2. python setup.py develop.

## Structure.

1. Scripts that drive everything are in /pRF_sim
2. Notebooks are in /notebooks.
3. I have included some data in /pRF_sim/data.
4. A yaml file that can be used to define parameters is in /pRF_sim/data.

## Notebooks.

1. prfpy_API_example: A minimal example of prfpy usage. 
2. Prepare_retinotopy_prior. Here I prepare a retinotopy 'prior' of prf estimates throughout the brain. This may be useful for simulations.

## Scripts.

1. stim.py Here, for convenience, I borrow a set of functions from 'popeye' for defining simple bar stimuli - for the purpose of an example. Functions for defining different design matrices could go here. 
2. utils.py. A set of utlitiies. Loads the package yaml into memory - as well as the Glasser cortical parcellaion and retinotopy prior. 
3. vis.py. A set of plotting functions that use pycortex. 












# pylook

Data analysis tools for rock mechanics experiments in the spirit of the legacy XLook tool.

We follow the [semantic versioning](https://semver.org/) practice. That means that while the
package is 0.X (as it is currently) we may be changing the API as design constraints and
decisions are reached. We won't break your code for fun, but we also won't burden users for
the next decade to maintain a bad design decision that was made. When you see a version
number like 0.a.b it means that a is a feature release and b is a bug fix only release.

We only support Python 3 and you should too! It's not hard to switch from Python 2, has
massive performance improvements, and is regularly updated.

## Kick the tires
Currently pylook is in a pre-release state - we haven't settled on things enough to make a
release yet, so you'll need to install directly from the repo you're viewing here. If you
want to help develop, see the instructions in the
[Contributing Guide](https://github.com/LeemanGeophysicalLLC/pylook/blob/master/CONTRIBUTING.md)
for help setting up a development environment and the process of submitting a pull
request.

Just want to grab the current version and play? Great! Make sure you've got 
[Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed (or Anaconda if you
prefer). First create the pylook environment by downloading our
[environment file](https://github.com/LeemanGeophysicalLLC/pylook/blob/master/environment.yml)
and creating the environment via `conda env create`.

Then install the latest from this repo:
```
pip install git+https://github.com/LeemanGeophysicalLLC/pylook
```

## When will this be released?
We'll be releasing a package on pypi and conda forge by the end of 2020. We want to ensure that
a suitable level of base functionality and test occurs before release to bring a solid
and reliable product to you from the beginning!

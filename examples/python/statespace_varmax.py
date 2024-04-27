#!/usr/bin/env python

# DO NOT EDIT
# Autogenerated from the notebook statespace_varmax.ipynb.
# Edit the notebook and then sync the output with this file.
#
# flake8: noqa
# DO NOT EDIT

# # VARMAX models
#
# This is a brief introduction notebook to VARMAX models in statsmodels.
# The VARMAX model is generically specified as:
# $$
# y_t = \nu + A_1 y_{t-1} + \dots + A_p y_{t-p} + B x_t + \epsilon_t +
# M_1 \epsilon_{t-1} + \dots M_q \epsilon_{t-q}
# $$
#
# where $y_t$ is a $\text{k_endog} \times 1$ vector.

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

dta = sm.datasets.webuse('lutkepohl2', 'https://www.stata-press.com/data/r12/')
dta.index = dta.qtr
dta.index.freq = dta.index.inferred_freq
endog = dta.loc['1960-04-01':'1978-10-01',
                ['dln_inv', 'dln_inc', 'dln_consump']]

# ## Model specification
#
# The `VARMAX` class in statsmodels allows estimation of VAR, VMA, and
# VARMA models (through the `order` argument), optionally with a constant
# term (via the `trend` argument). Exogenous regressors may also be included
# (as usual in statsmodels, by the `exog` argument), and in this way a time
# trend may be added. Finally, the class allows measurement error (via the
# `measurement_error` argument) and allows specifying either a diagonal or
# unstructured innovation covariance matrix (via the `error_cov_type`
# argument).

# ## Example 1: VAR
#
# Below is a simple VARX(2) model in two endogenous variables and an
# exogenous series, but no constant term. Notice that we needed to allow for
# more iterations than the default (which is `maxiter=50`) in order for the
# likelihood estimation to converge. This is not unusual in VAR models which
# have to estimate a large number of parameters, often on a relatively small
# number of time series: this model, for example, estimates 27 parameters
# off of 75 observations of 3 variables.

exog = endog['dln_consump']
mod = sm.tsa.VARMAX(endog[['dln_inv', 'dln_inc']],
                    order=(2, 0),
                    trend='n',
                    exog=exog)
res = mod.fit(maxiter=1000, disp=False)
print(res.summary())

# From the estimated VAR model, we can plot the impulse response functions
# of the endogenous variables.

ax = res.impulse_responses(10, orthogonalized=True,
                           impulse=[1, 0]).plot(figsize=(13, 3))
ax.set(xlabel='t', title='Responses to a shock to `dln_inv`')

# ## Example 2: VMA
#
# A vector moving average model can also be formulated. Below we show a
# VMA(2) on the same data, but where the innovations to the process are
# uncorrelated. In this example we leave out the exogenous regressor but now
# include the constant term.

mod = sm.tsa.VARMAX(endog[['dln_inv', 'dln_inc']],
                    order=(0, 2),
                    error_cov_type='diagonal')
res = mod.fit(maxiter=1000, disp=False)
print(res.summary())

# ## Caution: VARMA(p,q) specifications
#
# Although the model allows estimating VARMA(p,q) specifications, these
# models are not identified without additional restrictions on the
# representation matrices, which are not built-in. For this reason, it is
# recommended that the user proceed with error (and indeed a warning is
# issued when these models are specified). Nonetheless, they may in some
# circumstances provide useful information.

mod = sm.tsa.VARMAX(endog[['dln_inv', 'dln_inc']], order=(1, 1))
res = mod.fit(maxiter=1000, disp=False)
print(res.summary())

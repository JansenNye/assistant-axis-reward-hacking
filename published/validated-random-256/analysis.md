# Random-vector reward-hacking control

Coverage: {'expected': 824, 'complete': 824, 'error_oom': 0}

Random directions are independent isotropic unit vectors. Two-sided extremeness uses |AUROC − 0.5|.

Baselines need no direction: the region's token count and the norm of its mean residual.

| Region | Grouping | Pairs | AA AUROC | Random AUROC 2.5/50/97.5% | Tail fraction | Token-count AUROC | Residual-norm AUROC |
|---|---|---:|---:|---|---:|---:|---:|
| prompt | problem | 4872 | 0.5401 | 0.420 / 0.498 / 0.576 | 0.4358 | 0.462 | 0.457 |
| prompt | problem_family_turn | 868 | 0.5248 | 0.426 / 0.498 / 0.563 | 0.4981 | 0.487 | 0.497 |
| cot | problem | 4866 | 0.6880 | 0.344 / 0.514 / 0.691 | 0.0467 | 0.485 | 0.505 |
| cot | problem_family_turn | 867 | 0.6955 | 0.319 / 0.520 / 0.710 | 0.0545 | 0.442 | 0.565 |
| final | problem | 4872 | 0.7605 | 0.147 / 0.486 / 0.860 | 0.2140 | 0.513 | 0.121 |
| final | problem_family_turn | 868 | 0.7143 | 0.140 / 0.485 / 0.868 | 0.3035 | 0.544 | 0.116 |

## Per-direction uncertainty

95% percentile intervals from 1000 whole-problem bootstrap draws, shared across directions.

A random direction counts as predictive when its CI lies strictly above or below 0.5; touching 0.5 does not count.
These intervals describe uncertainty for each fixed direction, not the spread across random directions.

| Region | Grouping | AA 95% CI | Random CI above 0.5 | Random CI below 0.5 | Random CI excludes 0.5 | Fraction |
|---|---|---|---:|---:|---:|---:|
| prompt | problem | 0.5015–0.5804 | 39 | 37 | 76 / 256 | 29.7% |
| prompt | problem_family_turn | 0.4849–0.5676 | 32 | 38 | 70 / 256 | 27.3% |
| cot | problem | 0.6028–0.7698 | 62 | 47 | 109 / 256 | 42.6% |
| cot | problem_family_turn | 0.6076–0.7809 | 70 | 53 | 123 / 256 | 48.0% |
| final | problem | 0.6631–0.8117 | 83 | 86 | 169 / 256 | 66.0% |
| final | problem_family_turn | 0.6087–0.7984 | 83 | 88 | 171 / 256 | 66.8% |

Negative labels are unflagged, not judge-confirmed non-hacks.
Random-direction tail fractions describe axis specificity, not a causal or label-permutation test.
Exact turn matching does not equal exact token-length matching; partial-rank adjustment is a sensitivity analysis.
Problem-only comparison uses this same strictly selected cohort, not the original broader cohort.
Bootstrap resamples whole base problems, keeping repeated episodes and turns together.
Per-direction 95% CIs are pointwise, not simultaneous across directions or analysis cells.
The fraction of random-direction CIs excluding 0.5 is descriptive, not a p-value for Assistant-Axis specificity.
Bare legacy axis artifact has matching dimensions but cannot authenticate model provenance.
Incomplete/OOM or empty-region cases may bias complete-case results.

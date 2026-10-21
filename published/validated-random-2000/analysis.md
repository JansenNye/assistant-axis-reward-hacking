# Random-vector reward-hacking control

Coverage: {'expected': 824, 'complete': 824, 'error_oom': 0}

Random directions are independent isotropic unit vectors. Two-sided extremeness uses |AUROC − 0.5|.

Baselines need no direction: the region's token count and the norm of its mean residual.

| Region | Grouping | Pairs | AA AUROC | Random AUROC 2.5/50/97.5% | Tail fraction | Token-count AUROC | Residual-norm AUROC |
|---|---|---:|---:|---|---:|---:|---:|
| prompt | problem | 4872 | 0.5401 | 0.419 / 0.501 / 0.581 | 0.4403 | 0.462 | 0.457 |
| prompt | problem_family_turn | 868 | 0.5248 | 0.430 / 0.499 / 0.571 | 0.5407 | 0.487 | 0.497 |
| cot | problem | 4866 | 0.6880 | 0.331 / 0.500 / 0.669 | 0.0255 | 0.485 | 0.505 |
| cot | problem_family_turn | 867 | 0.6955 | 0.311 / 0.504 / 0.691 | 0.0440 | 0.442 | 0.565 |
| final | problem | 4872 | 0.7605 | 0.148 / 0.503 / 0.853 | 0.1869 | 0.513 | 0.121 |
| final | problem_family_turn | 868 | 0.7143 | 0.145 / 0.504 / 0.849 | 0.2894 | 0.544 | 0.116 |

## Per-direction uncertainty

95% percentile intervals from 1000 whole-problem bootstrap draws, shared across directions.

A random direction counts as predictive when its CI lies strictly above or below 0.5; touching 0.5 does not count.
These intervals describe uncertainty for each fixed direction, not the spread across random directions.

| Region | Grouping | AA 95% CI | Random CI above 0.5 | Random CI below 0.5 | Random CI excludes 0.5 | Fraction |
|---|---|---|---:|---:|---:|---:|
| prompt | problem | 0.5015–0.5804 | 335 | 306 | 641 / 2000 | 32.0% |
| prompt | problem_family_turn | 0.4849–0.5676 | 291 | 268 | 559 / 2000 | 28.0% |
| cot | problem | 0.6028–0.7698 | 453 | 448 | 901 / 2000 | 45.1% |
| cot | problem_family_turn | 0.6076–0.7809 | 508 | 523 | 1031 / 2000 | 51.5% |
| final | problem | 0.6631–0.8117 | 634 | 627 | 1261 / 2000 | 63.0% |
| final | problem_family_turn | 0.6087–0.7984 | 673 | 666 | 1339 / 2000 | 67.0% |

Negative labels are unflagged, not judge-confirmed non-hacks.
Random-direction tail fractions describe axis specificity, not a causal or label-permutation test.
Exact turn matching does not equal exact token-length matching; partial-rank adjustment is a sensitivity analysis.
Problem-only comparison uses this same strictly selected cohort, not the original broader cohort.
Bootstrap resamples whole base problems, keeping repeated episodes and turns together.
Per-direction 95% CIs are pointwise, not simultaneous across directions or analysis cells.
The fraction of random-direction CIs excluding 0.5 is descriptive, not a p-value for Assistant-Axis specificity.
Bare legacy axis artifact has matching dimensions but cannot authenticate model provenance.
Incomplete/OOM or empty-region cases may bias complete-case results.

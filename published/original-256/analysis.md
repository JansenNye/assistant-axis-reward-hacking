# Random-vector reward-hacking control

Coverage: {'expected': 824, 'complete': 824, 'error_oom': 0}

Random directions are independent isotropic unit vectors. Two-sided extremeness uses |AUROC − 0.5|.

| Region | Grouping | Pairs | AA AUROC | Random AUROC 2.5/50/97.5% | Tail fraction |
|---|---|---:|---:|---|---:|
| prompt | problem | 4872 | 0.5365 | [0.42016882183908044, 0.4970751231527094, 0.5753284072249589] | 0.5097 |
| prompt | problem_family_turn | 868 | 0.5150 | [0.42669930875576034, 0.49798387096774194, 0.5648761520737328] | 0.6732 |
| cot | problem | 4866 | 0.6880 | [0.3441224825318537, 0.5140772708590218, 0.6908651870119195] | 0.0467 |
| cot | problem_family_turn | 867 | 0.6955 | [0.3187716262975778, 0.5196078431372548, 0.7097750865051904] | 0.0545 |
| final | problem | 4872 | 0.7605 | [0.14711617405582922, 0.4861453201970444, 0.8603499589490969] | 0.2140 |
| final | problem_family_turn | 868 | 0.7143 | [0.13983294930875576, 0.48502304147465436, 0.867655529953917] | 0.3035 |

Negative labels are unflagged, not judge-confirmed non-hacks.
Random-direction tail fractions describe axis specificity, not a causal or label-permutation test.
Exact turn matching does not equal exact token-length matching; partial-rank adjustment is a sensitivity analysis.
Problem-only comparison uses this same strictly selected cohort, not the original broader cohort.
Bootstrap resamples whole base problems, keeping repeated episodes and turns together.
Bare legacy axis artifact has matching dimensions but cannot authenticate model provenance.
Incomplete/OOM or empty-region cases may bias complete-case results.

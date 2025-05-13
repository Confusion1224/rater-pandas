# Rater-Pandas

A Python package for calculating inter-rater reliability statistics (Kappa, Agreement, ICC) using pandas DataFrames.

## Installation

```bash
pip install rater-pandas
```

## Load Data
Use pandas to load your rating data into a DataFrame before calculating statistics.
All functions in this library use pandas DataFrames as input. Here's the example dataframe we'll use to demonstrate all functionality:

```python
import pandas as pd

# Example rating data - wide format (common for kappa statistics)
ratings_wide = pd.DataFrame({
    'PatientID': [101, 102, 103, 104, 105],
    'RaterA': [3, 2, 4, 3, 2],          # 1-5 severity scale
    'RaterB': [4, 2, 4, 3, 3],          # 1-5 severity scale
    'RaterC': [3, 3, 4, 2, 2]           # 1-5 severity scale
}).set_index('PatientID')  # Using PatientID as index

# Example rating data - long format (common for ICC)
ratings_long = pd.DataFrame({
    'PatientID': [101, 101, 101, 102, 102, 102, 103, 103, 103],
    'Rater': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'],
    'Score': [3.2, 3.5, 3.4, 4.1, 4.2, 4.0, 2.8, 2.9, 3.1]  # Continuous scores
})
```

## Statistical Measures
This package provides three categories of inter-rater reliability statistics:

1. Kappa Statistics: For categorical data (nominal/ordinal)
    - Cohen's Kappa (2 raters)
    - Fleiss' Kappa (2+ raters)

2. Agreement Measures
    - Krippendorff Alpha
    - Scott's Pi
    - Spearman's Intrarater Correlation
    - Cronbach's Alpha

3. Intraclass Correlation (ICC)
    - ICC1, ICC2, ICC3, ICC1k, ICC2k, ICC3k

##  Inter-Rater Reliability Metrics Comparison

| Metric                  | Description                                                                 | Raters | Missing Data | Output Statistics                          | Data Format          |
|-------------------------|-----------------------------------------------------------------------------|--------|--------------|--------------------------------------------|----------------------|
| **Cohen's Kappa**       | Agreement between 2 raters (nominal/ordinal)                                | 2      | ❌           | κ, p-value, z-score, CI, etc                             | Wide only            |
| **Fleiss' Kappa**       | Agreement for multiple raters (nominal/ordinal)                             | 2+     | ✅           | κ                                          | Wide only            |
| **Krippendorff's Alpha**| Flexible reliability coefficient (nominal, ordinal, interval, ratio)                           | 2+     | ✅           | α                            | Wide only            |
| **Scott's Pi**          | Agreement accounting for chance (nominal)                                   | 2      | ❌           | π                                      | Wide only            |
| **Spearman Correlation**| Consistency between raters                         | 2      | ❌           | r, p-value                                 | Wide only            |
| **Cronbach's Alpha**    | Internal consistency of raters (interval/ratio)                             | 2+     | ✅           | α, item variance, total variance                    | Wide only            |
| **ICC**                 | Consistency/absolute agreement (interval/ratio)                             | 2+     | ✅           | ICC (A-1, C-1, etc.), F-test, CI           | Wide + Long          |

## Implementation Notes

```python
# Wide format example (all metrics)
wide_data = pd.DataFrame({
    'rater1': [1, 2, 3],
    'rater2': [1, 3, 3],
    'rater3': [2, 3, 3]
})

# Long format (ICC only)
long_data = pd.DataFrame({
    'subject': [1,1,1,2,2,2],
    'rater': ['A','B','C','A','B','C'],
    'score': [1,2,2,3,3,3]
})
```

## Kappa Statistics
Kappa statistics measure agreement between raters while accounting for chance agreement. Values range from -1 (perfect disagreement) to 1 (perfect agreement), with 0 indicating chance agreement.

Interpretation Guide for Cohen Kappa and Fleiss Kappa:

≤ 0: No agreement

0.01-0.20: Slight agreement

0.21-0.40: Fair agreement

0.41-0.60: Moderate agreement

0.61-0.80: Substantial agreement

0.81-1.00: Almost perfect agreement

1. <b>Cohen's Kappa</b>

Use for 2 raters with categorical data (nominal or ordinal). Return all statistical results by setting return_results=True.
```python
from rater_pandas.kappa import cohens_kappa_from_df

kappa = cohens_kappa_from_df(
    df=ratings_wide,
    rater_a='Clinician',
    rater_b='Researcher',
    return_results=False  # Set True for detailed output
)

print(f"Cohen's Kappa: {kappa:.3f}")
```

<b>2. Fleiss Kappa</b>

Use for 2+ raters with categorical data (nominal or ordinal).
```python
from rater_pandas.kappa import fleiss_kappa_from_df

kappa = fleiss_kappa_from_df(df=ratings_wide)
print(f"Cohen's Kappa: {kappa:.3f}")
```

## Agreement Measures
Agreement measures assess the consistency between raters. These can be used for both categorical and continuous data, depending on the measure.

## Reliability Metrics Comparison

This table summarizes various reliability metrics and their interpretations.

| Range         | Scott's Pi              | Krippendorff's Alpha    | Spearman's Intrarater Correlation | Cronbach's Alpha               |
|---------------|-------------------------|--------------------------|-----------------------------------|---------------------------------|
| **≤ 0**       | No agreement            | Poor reliability         | No correlation                    | Poor reliability            |
| **0.01 - 0.20** | Slight agreement        | Weak reliability         | Weak correlation                  | Poor reliability            |
| **0.21 - 0.40** | Fair agreement          | Moderate reliability     | Moderate correlation               | Poor reliability      |
| **0.41 - 0.60** | Moderate agreement      | Acceptable reliability   | Fair correlation                  | Poor reliability      |
| **0.61 - 0.80** | Substantial agreement    | Strong reliability       | Strong correlation                | Moderate reliability               |
| **0.81 - 1.00** | Almost perfect agreement | Almost perfect reliability | Perfect correlation               | Strong reliability               |

<b>1. Krippendorff's Alpha</b>

A robust measure for any number of raters, works with nominal, ordinal, interval, or ratio data.

```python
from rater_pandas.agreement import krippendorff_alpha_from_df

alpha = krippendorff_alpha_from_df(
    df=ratings_long,
    unit_col='PatientID',
    rater_col='Rater',
    score_col='Score',
    level_of_measurement='interval'  # or 'nominal', 'ordinal', 'ratio'
)

print(f"Krippendorff's Alpha: {alpha:.3f}")
```

<b>2. Scott's Pi</b>

Similar to Cohen's Kappa but assumes equal marginal distributions.

```python
from rater_pandas.agreement import scotts_pi_from_df

pi = scotts_pi_from_df(
    df=ratings_wide[['RaterA', 'RaterB']],  # For 2 raters
    return_results=False
)

print(f"Scott's Pi: {pi:.3f}")
```

<b>3. Spearman's Intrarater Correlation</b>
Measures consistency of a single rater's scores over time (test-retest reliability).

```python
from rater_pandas.agreement import spearman_corr_from_df

corr = spearman_intrarater_from_df(
    df=ratings_wide,
    rater_cols=['RaterA', 'RaterB', 'RaterC'],
    patient_id_col='PatientID'
)

print(f"Spearman's Intrarater Correlation: {corr:.3f}")
```
<b>4. Cronbach's Alpha</b>

Measures internal consistency between multiple raters.

```python
from rater_pandas.agreement import cronbachs_alpha_from_df

alpha = cronbach_alpha_from_df(
    df=ratings_wide,
    rater_cols=['RaterA', 'RaterB', 'RaterC']
)

print(f"Cronbach's Alpha: {alpha:.3f}")
```

## Intraclass Correlation (ICC)
ICC measures reliability for continuous data. Six forms are available (ICC1, ICC2, ICC3 and their k-rater versions).

```python
from rater_pandas.icc import icc_from_df

icc_results = icc_from_df(
    df=ratings_long,
    unit_col='PatientID',
    rater_col='Rater',
    score_col='Score',
    model='two-way',  # 'one-way', 'two-way', or 'three-way'
    type='agreement',  # 'consistency' or 'agreement'
    unit='single'      # 'single' or 'average'
)

print("ICC Results:")
print(f"ICC Value: {icc_results['icc']:.3f}")
print(f"95% CI: ({icc_results['ci_lower']:.3f}, {icc_results['ci_upper']:.3f})")
print(f"F-test: F({icc_results['df1']},{icc_results['df2']})={icc_results['F']:.3f}, p={icc_results['p']:.4f}")
```

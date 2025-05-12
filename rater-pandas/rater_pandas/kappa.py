import pandas as pd
import numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa
from statsmodels.stats.inter_rater import cohens_kappa

def cohens_kappa_from_df(
    df: pd.DataFrame, 
    rater_a: str, 
    rater_b: str, 
    categories: list = None,
    return_results: bool = False
):
    """
    Compute Cohen's Kappa directly from a pandas DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing ratings from two raters.
    rater_a, rater_b : str
        Column names of the two raters.
    categories : list, optional
        List of all possible categories. If None, inferred from the data.
    return_results : bool, default False
        If True, returns the full results object (including standard error).
        If False, returns only the Kappa point estimate.

    Returns:
    --------
    float or namedtuple
        Cohen's Kappa statistic (float if return_results=False).
        Full results (namedtuple with `kappa` and `std_err`) if return_results=True.

    Example:
    --------
    >>> df = pd.DataFrame({
    ...     "Rater1": [1, 2, 3, 1, 2],
    ...     "Rater2": [1, 2, 3, 1, 3]
    ... })
    >>> cohens_kappa_from_df(df, "Rater1", "Rater2", return_results=False)
    0.6363636363636364  # Just the Kappa value
    >>> cohens_kappa_from_df(df, "Rater1", "Rater2", return_results=True)
    KappaResults(kappa=0.6363636363636364, std_err=0.22188005018839622)  # Full results
    """
    # Extract ratings
    ratings_a = df[rater_a]
    ratings_b = df[rater_b]
    
    # Get unique categories if not provided
    if categories is None:
        categories = sorted(set(ratings_a).union(set(ratings_b)))
    
    # Create contingency matrix
    contingency = pd.crosstab(
        ratings_a, 
        ratings_b, 
        rownames=[rater_a], 
        colnames=[rater_b]
    ).reindex(index=categories, columns=categories, fill_value=0)
    
    # Compute Cohen's Kappa using statsmodels
    results = cohens_kappa(contingency.values)
    
    return results if return_results else results.kappa

def fleiss_kappa_from_df(df: pd.DataFrame, categories: list = None) -> float:
    """
    Compute Fleiss' Kappa directly from a pandas DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame where rows are subjects and columns are raters.
        Each cell contains the category assigned by a rater to a subject.
    categories : list, optional
        List of all possible categories. If None, inferred from the data.

    Returns:
    --------
    float
        Fleiss' Kappa statistic (between -1 and 1).

    Example:
    --------
    >>> df = pd.DataFrame({
    ...     "Rater1": [1, 2, 3, 1, 2],
    ...     "Rater2": [1, 2, 3, 1, 3],
    ...     "Rater3": [1, 2, 3, 1, 2]
    ... })
    >>> fleiss_kappa_from_df(df)
    0.7986577181208053
    """
    # Get unique categories if not provided
    if categories is None:
        categories = np.unique(df.values)
    
    n_subjects, n_raters = df.shape
    n_categories = len(categories)
    
    # Initialize an empty matrix (subjects × categories)
    agg = np.zeros((n_subjects, n_categories), dtype=int)
    
    # Count how many raters assigned each category per subject
    for i, subject in df.iterrows():
        for category_idx, category in enumerate(categories):
            agg[i, category_idx] = (subject == category).sum()
    
    # Compute Fleiss' Kappa using statsmodels
    return fleiss_kappa(agg)
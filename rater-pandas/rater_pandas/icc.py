import pandas as pd
import pingouin as pg

def icc_from_df(
    df: pd.DataFrame,
    targets: str,
    raters: list,
    model: str = "ICC3k",
    return_df: bool = False,
):
    """
    Compute ICC from a DataFrame (wide or long format).
    Handles both single and average measures (e.g., ICC1, ICC1k, ICC2, ICC2k).

    Parameters:
    -----------
    df : pd.DataFrame
        Wide format: Columns = [targets, rater1, rater2, ...].
        Long format: Columns = [targets, rater, score].
    targets : str
        Column name for subjects/targets (e.g., "Subject").
    raters : list or str
        For wide format: List of rater columns (e.g., ["Rater1", "Rater2"]).
        For long format: Single rater column name (e.g., "Rater").
    model : str, optional
        ICC model ("ICC1", "ICC2", "ICC3", "ICC1k", "ICC2k", "ICC3k").
    return_df : bool, optional
        If True, returns full results (DataFrame). If False, returns ICC value.

    Returns:
    --------
    float or pd.DataFrame
    """
    # Check if wide format (multiple rater columns)
    if isinstance(raters, list) and len(raters) > 1:
        df_long = df.melt(
            id_vars=[targets],
            value_vars=raters,
            var_name="rater",
            value_name="score",
        )
        targets_col = targets
        raters_col = "rater"
        ratings_col = "score"
    else:
        df_long = df.copy()
        targets_col = targets
        raters_col = raters[0] if isinstance(raters, list) else raters
        ratings_col = "score" if "score" in df.columns else df.columns[2]  # Guess ratings column

    # Compute ICC
    icc_results = pg.intraclass_corr(
        data=df_long,
        targets=targets_col,
        raters=raters_col,
        ratings=ratings_col,
    )

    # Return results
    return icc_results if return_df else icc_results.set_index("Type").loc[model, "ICC"]
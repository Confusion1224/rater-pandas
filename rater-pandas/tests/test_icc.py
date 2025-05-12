from rater_pandas.icc import icc_from_df
import pandas as pd

# Example wide format data
data = {
    'Subject': [1, 2, 3, 4],
    'Rater1': [3.4, 5.1, 2.8, 6.2],
    'Rater2': [3.6, 5.3, 2.9, 6.0],
    'Rater3': [3.5, 5.0, 3.1, 6.1]
}
df_wide = pd.DataFrame(data)

# Calculate ICC
icc_value = icc_from_df(
    df=df_wide,
    targets="Subject",  # column with subject IDs
    raters=["Rater1", "Rater2", "Rater3"],  # list of rater columns
    model="ICC3k"  # choose ICC model (default is ICC3k)
)

print(f"ICC value: {icc_value}")

# Example long format data
data = {
    'Subject': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'Rater': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'],
    'Score': [3.4, 3.6, 3.5, 5.1, 5.3, 5.0, 2.8, 2.9, 3.1]
}
df_long = pd.DataFrame(data)

# Calculate ICC
icc_value = icc_from_df(
    df=df_long,
    targets="Subject",  # column with subject IDs
    raters="Rater",    # column with rater IDs
    model="ICC2k"      # choose ICC model
)

print(f"ICC value: {icc_value}")

full_results = icc_from_df(
    df=df_wide,  # or df_long
    targets="Subject",
    raters=["Rater1", "Rater2", "Rater3"],  # or "Rater" for long format
    return_df=True  # returns full results DataFrame
)

print(full_results)
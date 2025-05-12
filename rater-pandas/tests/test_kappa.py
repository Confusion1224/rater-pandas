from rater_pandas.kappa import cohens_kappa_from_df
from rater_pandas.kappa import fleiss_kappa_from_df
import pandas as pd

data = {
    'Rater1': [1, 2, 3, 4, 5],
    'Rater2': [2, 3, 3, 4, 5],
    'Rater3': [3, 4, 5, 2, 5]
}
df = pd.DataFrame(data)

results = cohens_kappa_from_df(df, 'Rater1', 'Rater2', return_results=False)
print(results)

results = fleiss_kappa_from_df(df)
print(results)


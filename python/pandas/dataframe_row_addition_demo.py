# %%

import pandas as pd
import time

df: pd.DataFrame = pd.util.testing.makeDataFrame()[0:0].reset_index(drop=True)
time_start = time.perf_counter()
for i in range(10000):
    dummy_result_row = (0, 0, 0, 0)
    df.loc[len(df)] = dummy_result_row
total_time = time.perf_counter() - time_start
print(total_time)
# %%

import pandas as pd
import time

df: pd.DataFrame = pd.util.testing.makeDataFrame()[0:0].reset_index(drop=True)
time_start = time.perf_counter()
results: list = []
for i in range(10000):
    dummy_result_row = (0, 0, 0, 0)
    results.append(dummy_result_row)
df = pd.DataFrame(results, columns=df.columns)
total_time = time.perf_counter() - time_start
print(total_time)

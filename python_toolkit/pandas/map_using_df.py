"""Using a Dataframe as a mapping table."""

import pandas as pd

# Sample DataFrame
data = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
df = pd.DataFrame(data)

# Set column 'a' as the index
df.set_index('a', inplace=True)

# Function to get values from columns 'b' and 'c' based on the value in column 'a'
def get_mapped_values(df, index_value):
    try:
        result = df.loc[index_value, ['b', 'c']]
        return result.to_dict()
    except KeyError:
        return None

# Example usage
value_in_a = 2
mapped_values = get_mapped_values(df, value_in_a)
print(mapped_values)

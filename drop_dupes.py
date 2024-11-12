import pandas as pd

# Sample DataFrame
data = {
    'a': [1, 2, 3, 4, 5, 6],
    'b': ['A', 'A', 'B', 'B', 'C', 'C'],
    'c': ['X', 'X', 'Y', 'Y', 'Z', 'Z'],
    'd': ['P', 'P', 'Q', 'Q', 'R', 'R'],
    'e': [10, 20, 30, 40, 50, 60],
    'f': [100, 200, 300, 400, 500, 600]
}

df = pd.DataFrame(data)

# Find duplicated rows based on columns b, c, d (keep only the first occurrence)
duplicate_mask = df.duplicated(subset=['b', 'c', 'd'])

# Clear the duplicated values for columns b, c, and d in all but the first occurrence
df.loc[duplicate_mask, ['b', 'c', 'd']] = ""

print(df)

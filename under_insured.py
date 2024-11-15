import pandas as pd

# Sample DataFrame
data = {
    'zip': ['12345', '12367', '12389', '12400', '12456', '12500', '22345', '22367'],
    'city': ['CityA', 'CityA', 'CityB', 'CityB', 'CityC', 'CityC', 'CityD', 'CityD'],
    'county': ['CountyX', 'CountyX', 'CountyY', 'CountyY', 'CountyZ', 'CountyZ', 'CountyW', 'CountyW'],
    'cost_sqft': [100, 120, 80, 85, 150, 300, 50, 55]
}
df = pd.DataFrame(data)

# Extract first three digits of ZIP code
df['zip_prefix'] = df['zip'].str[:3]

# Overall average
overall_avg = df['cost_sqft'].mean()

# Compute averages by group
grouped_averages = {
    'zip': df.groupby('zip_prefix')['cost_sqft'].mean(),
    'city': df.groupby('city')['cost_sqft'].mean(),
    'county': df.groupby('county')['cost_sqft'].mean()
}

# Function to find underinsured properties
def find_underinsured(group_col, threshold=0.75):
    group_avg = df.groupby(group_col)['cost_sqft'].transform('mean')
    return df[df['cost_sqft'] < group_avg * threshold]

# Identify underinsured properties
underinsured_zip = find_underinsured('zip_prefix')
underinsured_city = find_underinsured('city')
underinsured_county = find_underinsured('county')

# Lowest n insured properties
n = 5
lowest_n_insured = df.nsmallest(n, 'cost_sqft')

# Summary Output
summary = {
    'overall_avg': overall_avg,
    'lowest_n_insured': lowest_n_insured,
    'grouped_averages': grouped_averages,
    'underinsured_by_zip': underinsured_zip,
    'underinsured_by_city': underinsured_city,
    'underinsured_by_county': underinsured_county
}

# Display the results
for key, value in summary.items():
    print(f"\n--- {key.upper()} ---")
    print(value)

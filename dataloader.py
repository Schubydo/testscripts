import pandas as pd

# Load the Excel file into a DataFrame
file_path = 'your_excel_file.xlsx'
df = pd.read_excel(file_path)

# Initialize an empty list to store the stacked data
stacked_data = []

# Iterate over the columns in groups of 5
for i in range(0, len(df.columns), 5):
    # Extract the relevant columns for the current group
    policy_col = df.iloc[:, i]
    pc_col = df.iloc[:, i + 1]
    earned_col = df.iloc[:, i + 2]
    ep_col = df.iloc[:, i + 3]
    delta_col = df.iloc[:, i + 4]

    # Extract the mm/yy part from the column headers
    date_mm_yy = df.columns[i].split('/')[-1]

    # Stack the columns into a temporary DataFrame
    temp_df = pd.DataFrame({
        'Policy': policy_col,
        'PC': pc_col,
        'Earned': earned_col,
        'EP': ep_col,
        'Delta': delta_col,
        'Date': date_mm_yy
    })

    # Append the temporary DataFrame to the stacked_data list
    stacked_data.append(temp_df)

# Concatenate all the temporary DataFrames into a single DataFrame
final_df = pd.concat(stacked_data, ignore_index=True)

# Optionally, save the final stacked DataFrame to a new Excel file
final_df.to_excel('stacked_output.xlsx', index=False)

# Print the final DataFrame for verification
print(final_df)

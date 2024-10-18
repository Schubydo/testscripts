import pandas as pd

# Load the Excel file with all sheets
file_path = 'your_excel_file.xlsx'  # Update with your actual file path

# Read all sheets into a dictionary of DataFrames
sheets_dict = pd.read_excel(file_path, sheet_name=None)  # sheet_name=None reads all sheets

# Initialize an empty list to store the stacked DataFrames from all sheets
all_data = []

# Iterate over each sheet
for sheet_name, df in sheets_dict.items():
    # Initialize an empty list to store the stacked data for this sheet
    stacked_data = []

    # Iterate over the columns in groups of 5 for the current sheet
    for i in range(0, len(df.columns), 5):
        # Extract the relevant columns for the current group
        policy_col = df.iloc[:, i]
        pc_col = df.iloc[:, i + 1]
        earned_col = df.iloc[:, i + 2]
        ep_col = df.iloc[:, i + 3]
        delta_col = df.iloc[:, i + 4]

        # Extract the mm/yy part from the column headers
        date_str = df.columns[i].split('/')[-1]  # This gets the 'mm/yy' part
        month, year = date_str.split('/')  # Split into month and year

        # Stack the columns into a temporary DataFrame
        temp_df = pd.DataFrame({
            'Policy': policy_col,
            'PC': pc_col,
            'Earned': earned_col,
            'EP': ep_col,
            'Delta': delta_col,
            'Month': month,
            'Year': year
        })

        # Append the temporary DataFrame to the stacked_data list for this sheet
        stacked_data.append(temp_df)

    # Concatenate all the stacked DataFrames for this sheet into one DataFrame
    sheet_df = pd.concat(stacked_data, ignore_index=True)

    # Drop rows where all of 'Policy', 'PC', 'EP', and 'Delta' are NaN or empty
    sheet_df_cleaned = sheet_df.dropna(subset=['Policy', 'PC', 'EP', 'Delta'], how='all')

    # Append the cleaned DataFrame for this sheet to the all_data list
    all_data.append(sheet_df_cleaned)

# Concatenate the cleaned DataFrames from all sheets into a single DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Optionally, save the final stacked DataFrame to a new Excel file
final_df.to_excel('final_stacked_output.xlsx', index=False)

# Print the final DataFrame for verification
print(final_df)

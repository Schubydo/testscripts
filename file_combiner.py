import os
import pandas as pd

# Define a function to standardize column names
def clean_column_names(col_name):
    """Cleans column names by stripping whitespace and converting to lowercase."""
    return col_name.strip().lower()

# Define a function to map columns to the template
def map_columns_to_template(df, column_mapping):
    """
    This function maps the columns of a dataframe to match the template based on column_mapping.
    df: The dataframe to clean.
    column_mapping: A dictionary where the keys are template column names and the values are possible variants in the files.
    """
    # Create an empty dictionary to store renamed columns
    new_columns = {}
    
    # Loop through the current dataframe columns and map to template
    for col in df.columns:
        cleaned_col = clean_column_names(col)
        for template_col, possible_names in column_mapping.items():
            if cleaned_col in possible_names:
                new_columns[col] = template_col  # Map to template column name
    
    # Rename columns in the dataframe
    df = df.rename(columns=new_columns)
    
    # Filter only template columns, add missing columns if necessary
    for template_col in column_mapping.keys():
        if template_col not in df.columns:
            df[template_col] = pd.NA  # Add missing columns with empty values
    
    return df[column_mapping.keys()]  # Return only template columns

# Path to the directory containing the Excel files
directory_path = '/path/to/your/excel/files'

# Load the template (assuming it's in Excel format)
template_df = pd.read_excel('/path/to/your/template.xlsx')

# Define your column mapping (keys are the template columns, values are possible column name variations in the files)
column_mapping = {
    'name': ['name', 'full_name', 'customer_name'],
    'email': ['email', 'email_address', 'mail'],
    'phone': ['phone', 'phone_number', 'contact_number'],
    # Add all the other relevant columns for your use case
}

# Create an empty list to store the cleaned dataframes
cleaned_dataframes = []

# Loop over all files in the directory
for file_name in os.listdir(directory_path):
    if file_name.endswith('.xlsx'):  # Process only Excel files
        file_path = os.path.join(directory_path, file_name)
        
        # Read all sheets in the current Excel file
        sheets_dict = pd.read_excel(file_path, sheet_name=None)  # `sheet_name=None` loads all sheets into a dictionary
        
        # Loop through each sheet
        for sheet_name, df in sheets_dict.items():
            print(f"Processing sheet: {sheet_name} from file: {file_name}")
            
            # Clean and map the columns to the template
            df_cleaned = map_columns_to_template(df, column_mapping)
            
            # Append the cleaned dataframe to the list
            cleaned_dataframes.append(df_cleaned)

# Combine all cleaned dataframes into one
combined_df = pd.concat(cleaned_dataframes, ignore_index=True)

# Export the final combined dataframe to Excel
output_path = '/path/to/output/combined_data.xlsx'
combined_df.to_excel(output_path, index=False)

print(f"Combined data saved to {output_path}")

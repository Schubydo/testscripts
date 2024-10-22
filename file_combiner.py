import os
import pandas as pd

# Define a function to standardize column names
def clean_column_names(col_name):
    """Cleans column names by stripping whitespace and converting to lowercase."""
    return col_name.strip().lower()

# Define a function to map columns to the template
def map_columns_to_template(df, column_mapping):
    """
    This function maps the columns of a dataframe to match the template based on partial matches in column_mapping.
    df: The dataframe to clean.
    column_mapping: A dictionary where the keys are template column names and the values are possible variants in the files.
    """
    # Create an empty dictionary to store renamed columns
    new_columns = {}
    
    # Loop through the current dataframe columns
    for col in df.columns:
        cleaned_col = clean_column_names(col)
        
        # Try to map to the correct template column using partial matches
        for template_col, possible_names in column_mapping.items():
            # If any part of the cleaned column contains a substring from the possible names, map it
            if any(possible_name in cleaned_col for possible_name in possible_names):
                new_columns[col] = template_col  # Map to template column name
                break  # Stop searching after finding a match
    
    # Rename columns in the dataframe
    df = df.rename(columns=new_columns)
    
    # Filter only template columns, add missing columns if necessary
    for template_col in column_mapping.keys():
        if template_col not in df.columns:
            df[template_col] = pd.NA  # Add missing columns with empty values
    
    return df[column_mapping.keys()]  # Return only template columns


# Function to remove nuisance rows based on defined rules
def remove_nuisance_rows(df, min_populated_ratio=0.2):
    """
    This function removes unwanted rows from the dataframe based on specific rules:
    - Removes rows with all NaN values.
    - Removes repeated header rows.
    - Removes rows with unwanted placeholder values like 'N/A', 'None', etc.
    - Removes rows that are less than `min_populated_ratio` populated (default is 20%).
    """
    # Rule 1: Remove completely empty rows (where all values are NaN)
    df = df.dropna(how='all')
    
    # Rule 2: Remove rows with repeated headers (check if column names exist in the data)
    # Example: if 'name' appears in the data (indicating a repeated header row)
    header_keywords = list(column_mapping.keys())  # You can also define more keywords to identify header rows
    df = df[~df.apply(lambda row: any([col_name in str(row).lower() for col_name in header_keywords]), axis=1)]
    
    # Rule 3: Remove rows with placeholder values (e.g., 'N/A', 'None', etc.)
    placeholders = ['n/a', 'none', '', 'nan']  # Add more placeholder values as needed
    df = df.replace(placeholders, pd.NA).dropna(how='all')  # Replace and remove rows with placeholders
    
    # Rule 4: Drop rows that are less than `min_populated_ratio` populated
    threshold = int(min_populated_ratio * len(df.columns))  # Calculate the minimum number of non-NaN values needed
    df = df.dropna(thresh=threshold)  # Only keep rows with at least 'threshold' non-NaN values

    return df


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
            
            # Step 1: Remove nuisance rows before column mapping
            df_cleaned = remove_nuisance_rows(df)
            
            # Step 2: Clean and map the columns to the template
            df_cleaned = map_columns_to_template(df_cleaned, column_mapping)
            
            # Append the cleaned dataframe to the list
            cleaned_dataframes.append(df_cleaned)

# Combine all cleaned dataframes into one
combined_df = pd.concat(cleaned_dataframes, ignore_index=True)

# Export the final combined dataframe to Excel
output_path = '/path/to/output/combined_data.xlsx'
combined_df.to_excel(output_path, index=False)

print(f"Combined data saved to {output_path}")

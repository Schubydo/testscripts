import os
import pandas as pd

# Define a function to standardize column names
def clean_column_names(col_name):
    """Cleans column names by stripping whitespace and converting to lowercase."""
    return col_name.strip().lower()

# Function to add suffix to duplicate columns
def make_column_names_unique(columns):
    """
    Appends a suffix (e.g., .1, .2, etc.) to duplicate column names to make them unique.
    """
    seen = {}
    new_columns = []
    for col in columns:
        if col in seen:
            # If duplicate, increment the suffix number
            seen[col] += 1
            new_columns.append(f"{col}.{seen[col]}")
        else:
            seen[col] = 0
            new_columns.append(col)
    return new_columns

# Define a function to map columns to the template with partial matching
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
    
    # Make sure columns are unique by adding suffixes to duplicates
    df.columns = make_column_names_unique(df.columns)

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
    header_keywords = list(column_mapping.keys())  # You can also define more keywords to identify header rows
    df = df[~df.apply(lambda row: any([col_name in str(row).lower() for col_name in header_keywords]), axis=1)]
    
    # Rule 3: Remove rows with placeholder values (e.g., 'N/A', 'None', etc.)
    placeholders = ['n/a', '

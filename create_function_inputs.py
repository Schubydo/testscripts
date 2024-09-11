import pandas as pd
import ast  # To safely evaluate string representations of lists

# Function to process row data and handle conversion of string representations of lists and file paths
def process_row(*args):
    cleaned_args = []
    
    for arg in args:
        if isinstance(arg, str):
            # Remove extra quotes around the string
            arg = arg.replace('"', '')

            # Check if the string looks like a list and try to convert it to a real list
            if arg.startswith('[') and arg.endswith(']'):
                try:
                    # Use ast.literal_eval to convert string representations of lists to actual lists
                    evaluated_arg = ast.literal_eval(arg)
                    if isinstance(evaluated_arg, list):
                        cleaned_args.append(evaluated_arg)
                    else:
                        cleaned_args.append(arg)  # If not a list, keep as string
                except (ValueError, SyntaxError):
                    cleaned_args.append(arg)  # If not evaluable, append as string
            else:
                # Handle raw file paths starting with r' and ending with '
                if arg.startswith("r'") and arg.endswith("'"):
                    # Reconstruct the raw string by removing 'r' and ensuring it's treated as raw
                    raw_string = arg[2:-1]  # Remove the r' and '
                    cleaned_args.append(rf"{raw_string}")  # Append as raw string
                else:
                    cleaned_args.append(arg)  # Append regular strings
        else:
            cleaned_args.append(arg)  # Non-string values remain unchanged
    
    # Convert cleaned_args to a tuple
    cleaned_args_tuple = tuple(cleaned_args)

# Function to load and parse data from an Excel file
def load_and_parse_excel(file_path, sheet_name=None):
    
    data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')  # Use openpyxl for .xlsm files

    
    if isinstance(data, pd.DataFrame):
        # Iterate over each row in the DataFrame
        for index, row in data.iterrows():
            process_row(*row)  # Do the function here #

    elif isinstance(data, dict):
        for sheet, df in data.items():
            print(f"Processing sheet: {sheet}")
            for index, row in df.iterrows():
                process_row(*row) # Do the function #
    else:
        print("Unexpected data format")


if __name__ == '__main__':
    
    file_path = "TestExcel.xlsx"  # Path to Excel file, python file and excel sheet will have to be in the same directory 
    load_and_parse_excel(file_path, sheet_name="Sheet1")  # You can also use sheet_name=None to load all sheets

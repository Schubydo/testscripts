import pandas as pd 

def process_row(*args):
    cleaned_args = []
    
    for arg in args:
        if isinstance(arg, str):
            # Remove quotes around the string
            arg = arg.replace('"', '')
            
            # Check if the string looks like a list and try to convert it to a real list
            try:
                # Use ast.literal_eval to convert string representations of lists to actual lists
                evaluated_arg = ast.literal_eval(arg)
                if isinstance(evaluated_arg, list):  # Ensure it converted to a list
                    cleaned_args.append(evaluated_arg)
                else:
                    cleaned_args.append(arg)  # If not a list, keep as string
            except (ValueError, SyntaxError):
                # If it's not a list or can't be evaluated, just append the cleaned string
                cleaned_args.append(arg)
        else:
            cleaned_args.append(arg)  # Non-string values remain unchanged
    
    # Process the cleaned row data (print for demonstration)
    print("Cleaned row data:", cleaned_args)

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

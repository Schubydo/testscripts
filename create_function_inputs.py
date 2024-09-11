import pandas as pd 

def process_row(*args):
    # Process the row data, placeholder
    print(args)

# Function to load and parse data from an Excel file
def load_and_parse_excel(file_path, sheet_name=None):
    
    data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')  # Use openpyxl for .xlsm files

    
    if isinstance(data, pd.DataFrame):
        # Iterate over each row in the DataFrame
        for index, row in data.iterrows():
            process_row(*row)

    elif isinstance(data, dict):
        for sheet, df in data.items():
            print(f"Processing sheet: {sheet}")
            for index, row in df.iterrows():
                process_row(*row)
    else:
        print("Unexpected data format")

# Example usage
file_path = "TestExcel.xlsx"  # Path to Excel file
load_and_parse_excel(file_path, sheet_name="Sheet1")  # You can also use sheet_name=None to load all sheets

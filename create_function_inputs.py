import pandas as pd 




def load_and_parse_excel(file_path, sheet_name=None):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Convert the row into a list of values and pass it as arguments to `process_row`
        email_function(*row)


if __name__ == '__main__':

    load_and_parse_excel('TestExcel',sheet_name=None)
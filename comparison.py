import pandas as pd

def compare_excel_sheets(file1, file2, sheet_name1=0, sheet_name2=0):
    """
    Compare two Excel sheets and return a summary of differences.
    
    Parameters:
    - file1: str : Path to the first Excel file.
    - file2: str : Path to the second Excel file.
    - sheet_name1: str or int : Name or index of the sheet in file1 to compare (default is first sheet).
    - sheet_name2: str or int : Name or index of the sheet in file2 to compare (default is first sheet).
    
    Returns:
    - A DataFrame summarizing the differences.
    """
    # Read the two Excel sheets
    df1 = pd.read_excel(file1, sheet_name=sheet_name1)
    df2 = pd.read_excel(file2, sheet_name=sheet_name2)
    
    # Ensure the shapes are identical before comparing
    if df1.shape != df2.shape:
        raise ValueError(f"Excel sheets have different shapes: {df1.shape} vs {df2.shape}")
    
    # Create a DataFrame to store the differences
    diff_df = pd.DataFrame(index=df1.index, columns=df1.columns)
    
    # Iterate over each cell and check if it's different
    for row in df1.index:
        for col in df1.columns:
            value1 = df1.at[row, col]
            value2 = df2.at[row, col]
            
            # If the values are different, store the difference
            if value1 != value2:
                diff_df.at[row, col] = f"{value1} → {value2}"
            else:
                diff_df.at[row, col] = "No Change"
    
    # Filter out rows/columns where there are no changes (optional)
    diff_summary = diff_df[(diff_df != "No Change").any(axis=1)]
    
    return diff_summary

# Example usage
# differences = compare_excel_sheets("forecast_jan.xlsx", "forecast_feb.xlsx")
# print(differences)

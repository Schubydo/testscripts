import openpyxl

def update_excel_files(file1_path, file2_path):
    # Load the first workbook (source file) and get data from B16 and B19
    wb1 = openpyxl.load_workbook(file1_path)
    sheet1 = wb1.active
    value_b16 = sheet1['B16'].value
    value_b19 = sheet1['B19'].value
    
    # Load the second workbook (target file)
    wb2 = openpyxl.load_workbook(file2_path)
    sheet2 = wb2.active
    
    # Find the first blank cell in columns I and J
    row_i = 1
    row_j = 1
    while sheet2[f'I{row_i}'].value is not None:
        row_i += 1
    while sheet2[f'J{row_j}'].value is not None:
        row_j += 1

    # Insert values into the first blank cells in columns I and J
    sheet2[f'I{row_i}'] = value_b16
    sheet2[f'J{row_j}'] = value_b19

    # Save the changes to the second file
    wb2.save(file2_path)
    print(f"Values {value_b16} and {value_b19} added to columns I and J of {file2_path}")

# Usage
# update_excel_files('source_file.xlsx', 'target_file.xlsx')

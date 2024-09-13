import xlwings as xw
import os

# Define a function to save PDF with different filter views
def save_filtered_excel_to_pdf(file_path, output_dir, filter_column, filter_values):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the Excel file
    app = xw.App(visible=False)  # Make Excel run in the background
    wb = app.books.open(file_path)

    # Reference the 'Overview' sheet
    sheet = wb.sheets['Overview']

    # Loop through the list of filter values
    for filter_value in filter_values:
        # Apply the filter to the specified column
        sheet.range(filter_column).api.AutoFilter(Field=1, Criteria1=filter_value)

        # Define the output file path (PDF)
        output_pdf = os.path.join(output_dir, f"{filter_value}.pdf")

        # Export the filtered sheet as PDF
        sheet.api.ExportAsFixedFormat(0, output_pdf)

    # Close the workbook and quit Excel
    wb.close()
    app.quit()

# Usage example
if __name__ == "__main__":
    # File paths
    excel_file = 'path_to_your_excel_file.xlsx'
    output_folder = 'path_to_save_pdfs'

    # Filter configuration: specify the column (e.g., "A1" for column A) and the values to filter on
    filter_column = 'A1'  # Adjust this to the header of the column you want to filter
    filter_values = ['FilterValue1', 'FilterValue2', 'FilterValue3']  # List of values to filter on

    # Call the function
    save_filtered_excel_to_pdf(excel_file, output_folder, filter_column, filter_values)

import xlwings as xw
import os

def save_filtered_excel_to_pdf(file_path, output_dir, dropdown_cell, filter_values):
    app = None
    wb = None
    try:
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open the Excel file
        app = xw.App(visible=False)  # Make Excel run in the background
        wb = app.books.open(file_path)

        # Reference the sheet with the dropdown list
        main_sheet = wb.sheets[0]  # Adjust as necessary, e.g., use wb.sheets['SheetName']

        # Loop through the list of filter values
        for filter_value in filter_values:
            try:
                # Set the dropdown cell value
                main_sheet.range(dropdown_cell).value = filter_value

                # Allow Excel to recalculate and update (optional sleep may be needed in some cases)
                app.api.Wait()  # Ensure Excel updates before saving

                # Define the output file path (PDF)
                output_pdf = os.path.join(output_dir, f"{filter_value}.pdf")

                # Save the updated sheet as PDF (assume we want to save the same sheet)
                main_sheet.api.ExportAsFixedFormat(0, output_pdf)
                print(f"Saved updated view for '{filter_value}' as PDF: {output_pdf}")

            except Exception as e:
                print(f"Error saving PDF for filter '{filter_value}': {e}")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Ensure the workbook and Excel application are closed
        if wb:
            try:
                wb.close()
            except Exception as e:
                print(f"Error closing workbook: {e}")
        if app:
            try:
                app.quit()
            except Exception as e:
                print(f"Error quitting Excel application: {e}")

# Usage example
if __name__ == "__main__":
    excel_file = 'path_to_your_excel_file.xlsx'
    output_folder = 'path_to_save_pdfs'
    dropdown_cell = 'A1'  # Cell address of the dropdown list
    filter_values = ['Value1', 'Value2', 'Value3']  # List of values to select from the dropdown

    save_filtered_excel_to_pdf(excel_file, output_folder, dropdown_cell, filter_values)

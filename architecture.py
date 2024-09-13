import xlwings as xw
import os
import time

def save_filtered_excel_to_pdf(file_path, dropdown_cell, filter_values):
    app = None
    wb = None
    try:
        # Get the current working directory
        output_dir = os.getcwd()

        # Open the Excel file
        app = xw.App(visible=False)  # Make Excel run in the background
        wb = app.books.open(file_path)

        # Reference the sheet with the dropdown list
        main_sheet = wb.sheets[0]  # Adjust as necessary, e.g., use wb.sheets['SheetName']

        for filter_value in filter_values:
            try:
                # Set the dropdown cell value
                main_sheet.range(dropdown_cell).value = filter_value

                # Allow Excel to process the change
                time.sleep(2)  # Wait for 2 seconds to allow Excel to update; adjust if needed

                # Set the print area to cover the entire used range of the sheet
                main_sheet.api.PageSetup.PrintArea = main_sheet.api.UsedRange.Address

                # Set orientation to landscape
                main_sheet.api.PageSetup.Orientation = 2  # 2 for landscape

                # Adjust scaling to fit the sheet on one page if necessary
                main_sheet.api.PageSetup.FitToPagesTall = False
                main_sheet.api.PageSetup.FitToPagesWide = 1

                # Define the output file path (PDF) in the working directory
                sanitized_filter_value = "".join(char for char in filter_value if char.isalnum() or char in " _-")
                output_pdf = os.path.join(output_dir, f"{sanitized_filter_value}.pdf")

                # Export the updated sheet as PDF
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
    dropdown_cell = 'A1'  # Cell address of the dropdown list
    filter_values = ['Value1', 'Value2', 'Value3']  # List of values to select from the dropdown

    save_filtered_excel_to_pdf(excel_file, dropdown_cell, filter_values)

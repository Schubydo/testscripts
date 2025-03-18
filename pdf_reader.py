import os
import pandas as pd
import PyPDF2

class PDFExtractor:
    def __init__(self, fields=None):
        self.data = []  # Stores extracted data before converting to DataFrame
        self.fields = fields if fields else ["Maximum Limit", "Coverholder Commission", "Earthquake Conditions"]

    def process_pdf(self, file_path):
        """Determines file type and calls the corresponding extraction function."""
        filename = os.path.basename(file_path)
        if filename.endswith("_CA.pdf"):
            self.extract_ca(file_path)
        elif filename.endswith("_INT.pdf"):
            self.extract_int(file_path)
        elif filename.endswith("_US.pdf"):
            self.extract_us(file_path)
        elif filename.endswith("_FL.pdf"):
            self.extract_fl(file_path)
        else:
            print(f"Unknown file type: {filename}")

    def extract_relevant_pages(self, file_path, field):
        """Extracts only the pages that contain the specified field."""
        relevant_text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if field in page_text:
                    relevant_text += page_text + "\n"
        return relevant_text
    
    def parse_relevant_data(self, file_path, filename):
        """Finds key fields and extracts relevant information using GPT."""
        extracted_data = {"Filename": filename}
        
        for field in self.fields:
            text = self.extract_relevant_pages(file_path, field)
            if text:
                prompt_text = f"Extract only the relevant details for {field} from the following text: {text}"
                extracted_data[field] = self.prompt_gpt(prompt_text)  # Simulated GPT call
            else:
                extracted_data[field] = "Not Found"
                
        self.data.append(extracted_data)
    
    def extract_ca(self, file_path):
        self.parse_relevant_data(file_path, os.path.basename(file_path))
    
    def extract_int(self, file_path):
        self.parse_relevant_data(file_path, os.path.basename(file_path))
    
    def extract_us(self, file_path):
        self.parse_relevant_data(file_path, os.path.basename(file_path))
    
    def extract_fl(self, file_path):
        self.parse_relevant_data(file_path, os.path.basename(file_path))
    
    def save_to_excel(self, output_file="extracted_data.xlsx"):
        """Saves extracted data to an Excel file."""
        df = pd.DataFrame(self.data)
        df.to_excel(output_file, index=False)
        print(f"Data saved to {output_file}")
    
    def prompt_gpt(self, prompt_text):
        """Simulated GPT function to process extracted text."""
        return "Extracted Data (GPT response)"  # Replace with actual GPT integration

# Example usage
fields_to_extract = ["Maximum Limit", "Coverholder Commission", "Earthquake Conditions"]
extractor = PDFExtractor(fields=fields_to_extract)
extractor.process_pdf("sample_CA.pdf")
extractor.process_pdf("sample_INT.pdf")
extractor.process_pdf("sample_US.pdf")
extractor.process_pdf("sample_FL.pdf")
extractor.save_to_excel()

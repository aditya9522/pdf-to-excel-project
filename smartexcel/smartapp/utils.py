import io
import fitz  # PyMuPDF
from openpyxl import Workbook

def convert_pdf_to_excel(pdf_file):
    # Create a new Excel workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "PDF Data"

    # Open the PDF file with PyMuPDF
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    # Extract data assuming the format matches your form fields
    data = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        lines = text.splitlines()
        for line in lines:
            if ":" in line:
                field, value = line.split(":", 1)
                data.append([field.strip(), value.strip()])

    # Write data to Excel starting from row 2 (1st row reserved for headers)
    for index, row_data in enumerate(data, start=2):
        worksheet.cell(row=index, column=1, value=row_data[0])  # Field
        worksheet.cell(row=index, column=2, value=row_data[1])  # Value

    # Set headers
    worksheet.cell(row=1, column=1, value="Field")
    worksheet.cell(row=1, column=2, value="Value")

    # Adjust column width
    worksheet.column_dimensions['A'].width = 30
    worksheet.column_dimensions['B'].width = 60

    # Save the workbook to a BytesIO object
    excel_file = io.BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)

    return excel_file

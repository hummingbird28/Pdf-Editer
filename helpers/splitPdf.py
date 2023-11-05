import os
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

def split_pdf(input_file, output_directory, start=None, end=None, output_format='pdf', password=None):
    os.makedirs(output_directory, exist_ok=True)
    if output_format == "image":
#        convert_from_path(input_file, output_directory)
        return

    with open(input_file, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        pages = pdf_reader.pages
        if start and not end:
            try:
                pages = pages[start]
            except IndexError:
                pass
        else:
            if end:
                pages = pages[:end]
            if start:
                pages = pages[start:]

        for page_num, page in enumerate(pages, 1):
            if output_format == 'pdf':
                output_file = os.path.join(output_directory, f"page_{page_num}.pdf")
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)
                if password:
                    pdf_writer.encrypt(password)
                with open(output_file, "wb") as output_pdf:
                    pdf_writer.write(output_pdf)
            else:
                raise ValueError("Invalid output format. Supported formats: 'pdf', 'image'.")
    return output_directory

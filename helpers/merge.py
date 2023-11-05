import os
from PyPDF2 import PdfReader, PdfWriter, PageObject
from PIL import Image


def write_file(pdf_path, pdf_writer):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])


def mergeFiles(input_files, output_file, password=None):
    pdf_writer = PdfWriter()

    for file_path in input_files:
        if file_path.lower().endswith(".pdf"):
            write_file(file_path, pdf_writer)
        elif file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            image = Image.open(file_path)
            pdf_path = file_path + ".pdf"
            image.save(pdf_path, "PDF", resolution=100.0)
            write_file(pdf_path, pdf_writer)
            os.remove(pdf_path)  # Remove the temporary PDF file
        else:
            print(f"Warning: File '{file_path}' is not a supported format. Skipping.")
            return
    if password:
        pdf_writer.encrypt(password)
    with open(output_file, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
    return output_file

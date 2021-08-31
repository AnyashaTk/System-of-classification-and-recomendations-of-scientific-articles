from PyPDF2 import PdfFileWriter, PdfFileReader
import os

for file in os.listdir(
        "/home/stork/PycharmProjects/System-of-classification-and-recomendations-of-scientific-articles/PDF_data/astro-ph")[
            :10]:
    file_path = "/home/stork/PycharmProjects/System-of-classification-and-recomendations-of-scientific-articles/PDF_data/astro-ph/" + file
    input_PDF = PdfFileReader(open(file_path,
                                   'rb'))
    output = PdfFileWriter()
    new_File_PDF = input_PDF.getPage(0)
    output.addPage(new_File_PDF)
    output_Name_File = "./pdf_first_pages" + file
    outputStream = open(output_Name_File, 'wb')
    output.write(outputStream)
    outputStream.close()

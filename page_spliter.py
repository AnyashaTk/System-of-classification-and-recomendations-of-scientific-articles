from PyPDF2 import PdfFileWriter, PdfFileReader
import os
file_names=os.listdir("/home/stork/PycharmProjects/ClsRecArticles/PDF_data/astro-ph")
for file in file_names[:10]:
    file_path = "/home/stork/PycharmProjects/ClsRecArticles/PDF_data/astro-ph/" + file
    with open('/home/stork/PycharmProjects/ClsRecArticles/PDF_data/astro-ph/2101.02454.pdf', 'rb') as f:
        input_PDF = PdfFileReader(f)
        output = PdfFileWriter()
        new_File_PDF = input_PDF.getPage(0)
        output.addPage(new_File_PDF)
        output_Name_File = "./pdf_first_pages" + file
        outputStream = open(output_Name_File, 'wb')
        output.write(outputStream)
        outputStream.close()

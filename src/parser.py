from base64 import b64decode
from PyPDF2 import PdfFileWriter, PdfFileReader


class PdfParser:

    @staticmethod
    def parse(base64: str):
        pdf_bytes = b64decode(base64, validate=True)
        if pdf_bytes[0:4] != b'%PDF':
            return None
        return pdf_bytes

    @staticmethod
    def split_pdf(base_path: str, split_at_page: int = 0, end_fix: str = "-mix") -> [str]:
        if split_at_page == 0:
            return [base_path]

        # Read file:
        input_pdf = PdfFileReader(open(base_path, "rb"))

        # Check range:
        if split_at_page > input_pdf.numPages:
            print("Could split this pdf, there a less pages then splitted index")
            return [base_path]

        # Create a splitted output file:
        output_splitted = PdfFileWriter()
        for i in range(split_at_page):
            output_splitted.addPage(input_pdf.getPage(i))

        output_path = base_path.replace(".pdf", end_fix + ".pdf")
        with open(output_path, "wb") as outputStream:
            output_splitted.write(outputStream)

        # Update base item:
        output_base = PdfFileWriter()
        output_pages = 0
        for i in range(input_pdf.numPages):
            if i > split_at_page - 1:
                output_pages = output_pages + 1
                output_base.addPage(input_pdf.getPage(i))

        # update base path file if any pages left, otherwise return None
        if output_pages <= 0:
            base_path = None
        else:
            with open(base_path.replace(".pdf", "-items.pdf"), "wb") as outputStream:
                print(output_pages)
                output_base.write(outputStream)

        path = base_path.replace(".pdf", "-items.pdf")
        return [path, output_path]


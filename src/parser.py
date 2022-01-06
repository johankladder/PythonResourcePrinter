from base64 import b64decode


class PdfParser:

    @staticmethod
    def parse(base64: str):
        pdf_bytes = b64decode(base64, validate=True)
        if pdf_bytes[0:4] != b'%PDF':
            return None
        return pdf_bytes


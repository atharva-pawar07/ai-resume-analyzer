import pymupdf
from fastapi import HTTPException, status


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    """

    try:
        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        extracted_text = ""

        for page in document:
            extracted_text += page.get_text()

        document.close()

        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No readable text found in PDF"
            )

        return extracted_text.strip()

    except Exception as error:
        if isinstance(error, HTTPException):
            raise error

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or corrupted PDF file"
        )
from io import BytesIO

import pdfplumber


class PdfParseError(RuntimeError):
    pass


def parse_pdf_bytes(pdf_bytes: bytes) -> str:
    try:
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            content = "\n".join((page.extract_text() or "") for page in pdf.pages).strip()
    except Exception:
        # For MVP fixtures and tests we allow plain-text fallback.
        content = pdf_bytes.decode("utf-8", errors="ignore").strip()

    if not content:
        raise PdfParseError("empty text extracted from pdf")
    return content

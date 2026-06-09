"""Pitch Master — PDF Text Extraction."""

from __future__ import annotations

import io
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes.

    Args:
        file_bytes: Raw PDF content as bytes.

    Returns:
        Extracted text from the PDF.

    Raises:
        ValueError: If PDF cannot be read.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n\n".join(pages)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")


def get_pdf_info(file_bytes: bytes) -> dict:
    """Get PDF metadata.

    Args:
        file_bytes: Raw PDF content as bytes.

    Returns:
        Dictionary with page count and metadata.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        info = reader.metadata
        return {
            "page_count": len(reader.pages),
            "title": info.title if info else None,
            "author": info.author if info else None,
        }
    except Exception:
        return {"page_count": 0, "title": None, "author": None}

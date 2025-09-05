"""Custom element classes related to text runs (CT_FtnEdnRef)."""

from __future__ import annotations

from docx.oxml.simpletypes import ST_DecimalNumber
from docx.oxml.xmlchemy import BaseOxmlElement, RequiredAttribute


class CT_FtnEdnRef(BaseOxmlElement):
    """`<w:footnoteReference>` and `<w:endnoteReference>` elements."""
    id = RequiredAttribute("w:id", ST_DecimalNumber)

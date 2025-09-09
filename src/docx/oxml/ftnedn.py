from __future__ import annotations

from typing import TYPE_CHECKING, List

from docx.oxml.simpletypes import ST_DecimalNumber
from docx.oxml.xmlchemy import BaseOxmlElement, RequiredAttribute, ZeroOrMore

if TYPE_CHECKING:
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.block import CT_Sdt
    from docx.oxml.text.paragraph import CT_P

class CT_Footnotes(BaseOxmlElement):
    footnote = ZeroOrMore("w:footnote")

class CT_Endnotes(BaseOxmlElement):
    endnote = ZeroOrMore("w:endnote")

class CT_FtnEdn(BaseOxmlElement):
    id = RequiredAttribute("w:id", ST_DecimalNumber)
    p = ZeroOrMore("w:p")
    tbl = ZeroOrMore("w:tbl")

    @property
    def inner_content_elements(self) -> List[CT_P | CT_Tbl | CT_Sdt]:
        """Generate all `w:p`, `w:tbl` and `w:sdt` elements in this document-body.

        Elements appear in document order. Elements shaded by nesting in a `w:ins` or
        other "wrapper" element will not be included.
        """
        return self.xpath("./w:p | ./w:tbl | ./w:sdt")

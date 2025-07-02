# pyright: reportPrivateUsage=false

"""Custom element classes related to sdt blocks (CT_Sdt)."""

from __future__ import annotations

from typing import List

from docx.oxml.shared import CT_String
from docx.oxml.text.paragraph import CT_P
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OneAndOnlyOne,
    ZeroOrMore,
    ZeroOrOne,
)


class CT_Sdt(BaseOxmlElement):
    """`<w:sdt>` element."""

    content = OneAndOnlyOne("w:sdtContent")
    sdtPr: CT_SdtPr | None = ZeroOrOne("w:sdtPr") # pyright: ignore[reportAssignmentType]


class CT_SdtContent(BaseOxmlElement):
    """`<w:sdtContent>` element."""

    p_lst = List[CT_P]
    p = ZeroOrMore("w:p")

    @property
    def inner_content_elements(self) -> List[CT_P]:
        """Paragraph children of the `w:sdt` element, in document order."""
        return self.xpath("./w:p")


class CT_SdtPr(BaseOxmlElement):
    """`<w:sdtPr>` element."""
    
    docPartObj: CT_SdtDocPart | None = ZeroOrOne("w:docPartObj") # pyright: ignore[reportAssignmentType]
    id_attr = ZeroOrOne("w:id")


class CT_SdtDocPart(BaseOxmlElement):
    """`<w:docPartObj>` element."""
    
    docPartGallery: CT_String | None = ZeroOrOne("w:docPartGallery") # pyright: ignore[reportAssignmentType]

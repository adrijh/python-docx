"""Custom element classes related to fields (CT_AlternateContent)."""

from __future__ import annotations

from docx.oxml.drawing import CT_Drawing, CT_Pict
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    ZeroOrMore,
)


class CT_Choice(BaseOxmlElement):
    """
    `<mc:Choice>` element within AlternateContent.
    Contains content for applications that support the specified requirements.
    """
    drawing = ZeroOrMore("w:drawing")
    pict = ZeroOrMore("w:pict")

    @property
    def inner_content_items(self) -> list[CT_Drawing | CT_Pict]:
        """Text of run, possibly punctuated by `w:lastRenderedPageBreak` elements."""
        return self.xpath("w:drawing | w:pict")
    

class CT_Fallback(BaseOxmlElement):
    """
    `<mc:Fallback>` element within AlternateContent.
    Contains fallback content for applications that don't support the Choice requirements.
    """
    pict = ZeroOrMore("w:pict")
    drawing = ZeroOrMore("w:drawing")

    @property
    def inner_content_items(self) -> list[CT_Drawing | CT_Pict]:
        """Text of run, possibly punctuated by `w:lastRenderedPageBreak` elements."""
        return self.xpath("w:drawing | w:pict")


class CT_AlternateContent(BaseOxmlElement):
    """`<mc:AlternateContent>` element, containing the text for a field."""
    choice: CT_Choice = ZeroOrMore("mc:Choice")
    fallback: CT_Fallback = ZeroOrMore("mc:Fallback")

"""Custom element classes related to fields (CT_FldSimple)."""

from __future__ import annotations

from typing import List

from docx.oxml.text.run import CT_R
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    ZeroOrMore,
)


class CT_FldSimple(BaseOxmlElement):
    """`<w:fldSimple>` element, containing the text for a field."""

    r_lst: List[CT_R]
    r = ZeroOrMore("w:r")

    @property
    def text(self) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        """The textual content of this hyperlink.

        `CT_FldSimple` can store text as one or more `w:r` children.
        """
        return "".join(r.text for r in self.xpath("w:r"))

    @property
    def inner_content_elements(self) -> List[CT_R]:
        """Run children of the `w:fldSimple` element, in document order."""
        return self.xpath("./w:r")

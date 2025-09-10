"""Sdt block-related proxy types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from docx.oxml.text.block import CT_Sdt
from docx.shared import StoryChild

if TYPE_CHECKING:
    import docx.types as t
    from docx.table import Table
    from docx.text.paragraph import Paragraph


class SdtBlock(StoryChild):
    """Proxy object wrapping a `<w:sdt>` element."""

    def __init__(self, sdt: CT_Sdt, parent: t.ProvidesStoryPart):
        super(SdtBlock, self).__init__(parent)
        self._sdt = self._element = sdt

    @property
    def text(self) -> str:
        return self._sdt.text

    @property
    def paragraphs(self) -> list[Paragraph]:
        from docx.text.paragraph import Paragraph

        return [Paragraph(p, self) for p in self._sdt.content.p_lst]

    @property
    def tables(self) -> list[Table]:
        from docx.table import Table

        return [Table(t, self) for t in self._sdt.content.tbl_lst]

    @property
    def sdt_blocks(self) -> list[SdtBlock]:
        return [SdtBlock(s, self) for s in self._sdt.content.sdt_lst]

    @property
    def gallery(self) -> str | None:
        obj = self._sdt.sdtPr.docPartObj if self._sdt.sdtPr is not None else None
        if obj is None:
            return None

        return obj.docPartGallery.val if obj.docPartGallery is not None else None

    def iter_inner_content(self) -> Iterator[Paragraph | Table | SdtBlock]:
        """Generate each `Paragraph`, `Table` or `SdtBlock` in this container in document order."""
        from docx.oxml.table import CT_Tbl
        from docx.oxml.text.paragraph import CT_P
        from docx.table import Table
        from docx.text.paragraph import Paragraph
        
        for elem in self._element.content.inner_content_elements:
            if isinstance(elem, CT_P):
                yield Paragraph(elem, self)
            if isinstance(elem, CT_Tbl):
                yield Table(elem, self)
            if isinstance(elem, CT_Sdt):
                yield SdtBlock(elem, self)

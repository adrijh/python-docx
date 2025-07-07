"""Sdt block-related proxy types."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docx.oxml.text.block import CT_Sdt
from docx.shared import StoryChild
from docx.text.paragraph import Paragraph

if TYPE_CHECKING:
    import docx.types as t


class SdtBlock(StoryChild):
    """Proxy object wrapping a `<w:sdt>` element."""

    def __init__(self, sdt: CT_Sdt, parent: t.ProvidesStoryPart):
        super(SdtBlock, self).__init__(parent)
        self._sdt = self._element = sdt

    @property
    def paragraphs(self) -> list[Paragraph]:
        return [Paragraph(p, self) for p in self._sdt.content.p_lst]

    @property
    def gallery(self) -> str | None:
        obj = self._sdt.sdtPr.docPartObj if self._sdt.sdtPr is not None else None
        if obj is None:
            return None

        return obj.docPartGallery.val if obj.docPartGallery is not None else None

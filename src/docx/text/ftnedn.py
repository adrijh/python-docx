"""Footnotes and Endnotes objects, container for all objects in the footnotes/endnotes parts."""
from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from docx.blkcntnr import BlockItemContainer
from docx.shared import ElementProxy
from docx.table import Table
from docx.text.paragraph import Paragraph

if TYPE_CHECKING:
    from docx.oxml.ftnedn import CT_Endnotes, CT_Footnotes, CT_FtnEdn
    from docx.parts.ftnedn import EndnotesPart, FootnotesPart


class Footnote(BlockItemContainer):
    def __init__(self, footnote: CT_FtnEdn, parent: FootnotesPart) -> None:
        super().__init__(footnote, parent)
        self._element = footnote

    @property
    def id(self) -> int:
        return int(self._element.id)

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        """Generate each `Paragraph` or `Table` in this container in document order."""
        from docx.oxml.table import CT_Tbl
        from docx.oxml.text.paragraph import CT_P
        
        for elem in self._element.inner_content_elements:
            if isinstance(elem, CT_P):
                yield Paragraph(elem, self)
            if isinstance(elem, CT_Tbl):
                yield Table(elem, self)


class Footnotes(ElementProxy):
    def __init__(self, footnotes: CT_Footnotes, parent: FootnotesPart) -> None:
        super().__init__(footnotes)
        self._element = footnotes
        self._parent = parent

    def __iter__(self) -> Iterator[Footnote]:
        for footnote in self._element.footnote_lst:
            yield Footnote(footnote, self._parent)

    def __len__(self) -> int:
        return len(self._element.footnote_lst)


class Endnote(BlockItemContainer):
    def __init__(self, endnote: CT_FtnEdn, parent: EndnotesPart) -> None:
        super().__init__(endnote, parent)
        self._element = endnote

    @property
    def part(self):
        """Return the document part for hyperlink resolution."""
        return self._parent.package.main_document_part

    @property
    def id(self) -> int:
        return int(self._element.id)

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        """Generate each `Paragraph` or `Table` in this container in document order."""
        from docx.oxml.table import CT_Tbl
        from docx.oxml.text.paragraph import CT_P
        
        for elem in self._element.inner_content_elements:
            if isinstance(elem, CT_P):
                yield Paragraph(elem, self)
            if isinstance(elem, CT_Tbl):
                yield Table(elem, self)


class Endnotes(ElementProxy):
    def __init__(self, endnotes: CT_Endnotes, parent: EndnotesPart) -> None:
        super().__init__(endnotes)
        self._element = endnotes
        self._parent = parent

    def __iter__(self) -> Iterator[Endnote]:
        for endnote in self._element.endnote_lst:
            yield Endnote(endnote, self._parent)

    def __len__(self) -> int:
        return len(self._element.endnote_lst)

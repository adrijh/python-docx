"""Footnotes and Endnotes objects, container for all objects in the footnotes/endnotes parts."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from docx.oxml.ftnedn import CT_Endnotes, CT_Footnotes, CT_FtnEdn
from docx.oxml.text.run import CT_FtnEdnRef
from docx.shared import ElementProxy, StoryChild

if TYPE_CHECKING:
    import docx.types as t


class Footnote(ElementProxy):
    def __init__(self, footnote: CT_FtnEdn) -> None:
        super().__init__(footnote)
        self._element = footnote

    @property
    def id(self) -> int:
        return int(self._element.id)


class Footnotes(ElementProxy):
    def __init__(self, footnotes: CT_Footnotes) -> None:
        super().__init__(footnotes)
        self._element = footnotes

    def __iter__(self) -> Iterator[Footnote]:
        for footnote in self._element.footnote_lst:
            yield Footnote(footnote)

    def __len__(self) -> int:
        return len(self._element.footnote_lst)


class Endnote(ElementProxy):
    def __init__(self, endnote: CT_FtnEdn) -> None:
        super().__init__(endnote)
        self._element = endnote

    @property
    def id(self) -> int:
        return int(self._element.id)


class Endnotes(ElementProxy):
    def __init__(self, footnotes: CT_Endnotes) -> None:
        super().__init__(footnotes)
        self._element = footnotes

    def __iter__(self) -> Iterator[Endnote]:
        for endnote in self._element.endnote_lst:
            yield Endnote(endnote)

    def __len__(self) -> int:
        return len(self._element.endnote_lst)

    def add_endnote(self, endnote: Endnote) -> None:
        return self._element._insert_endnote(endnote._element)


class FootnoteReference(StoryChild):
    def __init__(self, ref: CT_FtnEdnRef, parent: t.ProvidesStoryPart) -> None:
        super().__init__(parent)
        self._ref = self._element = self.element = ref

    @property
    def id(self) -> int:
        return int(self._ref.id)

    @property
    def footnote(self) -> Footnote | None:
        for footnote in self.part.footnotes:
            if footnote.id == self.id:
                return footnote

        return None


class EndnoteReference(StoryChild):
    def __init__(self, ref: CT_FtnEdnRef, parent: t.ProvidesStoryPart) -> None:
        super().__init__(parent)
        self._ref = self._element = self.element = ref

    @property
    def id(self) -> int:
        return int(self._ref.id)

    @property
    def endnote(self) -> Footnote | None:
        for endnote in self.part.endnotes:
            if endnote.id == self.id:
                return endnote

        return None

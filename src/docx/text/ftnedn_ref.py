"""FootnoteReference and EndnoteReference objects."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docx.oxml.text.run import CT_FtnEdnRef
from docx.shared import StoryChild

if TYPE_CHECKING:
    import docx.types as t
    from docx.text.ftnedn import Endnote, Footnote


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
    def endnote(self) -> Endnote | None:
        for endnote in self.part.endnotes:
            if endnote.id == self.id:
                return endnote

        return None

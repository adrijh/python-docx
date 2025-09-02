"""AlternateContent related objects."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from docx.drawing import Drawing, Picture
from docx.oxml.alternate import CT_AlternateContent, CT_Choice, CT_Fallback
from docx.oxml.drawing import CT_Drawing, CT_Pict
from docx.shared import Parented

if TYPE_CHECKING:
    import docx.types as t


class AlternateContent(Parented):
    """Container for a AlternateContent object."""

    def __init__(self, alt: CT_AlternateContent, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._alt = self._element = alt

    @property
    def choices(self) -> list[Choice]:
        return [Choice(choice, self) for choice in self._alt.choice_lst] 

    @property
    def fallback(self) -> Choice | None:
        return Choice(self._alt.fallback, self)


class Choice(Parented):
    """Container for a Choice or Fallback object."""

    def __init__(self, choice: CT_Choice | CT_Fallback, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._choice = self._element = choice


    def iter_inner_content(self) -> Iterator[Drawing | Picture]:
        for elem in self._choice.inner_content_items:
            if isinstance(elem, CT_Drawing):
                yield Drawing(elem, self)
            if isinstance(elem, CT_Pict):
                yield Picture(elem, self)

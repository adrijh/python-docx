"""Field-related proxy objects for python-docx, Field in particular."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from docx.oxml.text.field import CT_FldSimple
from docx.oxml.text.run import CT_R
from docx.shared import StoryChild
from docx.text.run import Run

if TYPE_CHECKING:
    import docx.types as t


class Field(StoryChild):
    """Proxy object wrapping `<w:fldSimple>` element."""

    def __init__(self, fld: CT_FldSimple, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._fld = self._element = self.element = fld


    def iter_inner_content(self) -> Iterator[Run]:
        """Generate the content-items in this field in the order they appear."""
        for item in self._fld.inner_content_elements:
            if isinstance(item, CT_R):  # pyright: ignore[reportUnnecessaryIsInstance]
                yield Run(item, self)

    @property
    def text(self) -> str:
        """String formed by concatenating the text equivalent of its runs."""
        return self._fld.text

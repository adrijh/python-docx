from __future__ import annotations

from typing import TYPE_CHECKING

from docx.oxml.text.symbol import CT_Sym
from docx.shared import Parented

if TYPE_CHECKING:
    import docx.types as t

class Symbol(Parented):
    """Container for a DrawingML object."""

    def __init__(self, sym: CT_Sym, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._sym = self._element = sym

    @property
    def text(self) -> str:
        return self._sym.text

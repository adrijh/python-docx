"""DrawingML-related objects are in this subpackage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docx.enum.shape import WD_ANCHORED_SHAPE, WD_INLINE_SHAPE
from docx.oxml.drawing import CT_Drawing, CT_Pict
from docx.shape import AnchoredShape, InlineShape
from docx.shared import Parented

if TYPE_CHECKING:
    import docx.types as t


class Drawing(Parented):
    """Container for a DrawingML object."""

    def __init__(self, drawing: CT_Drawing, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._drawing = self._element = drawing


    @property
    def shape(self) -> InlineShape | AnchoredShape:
        if self._drawing.inline is not None:
            return InlineShape(self._drawing.inline)

        if self._drawing.anchor is not None:
            return AnchoredShape(self._drawing.anchor)

        raise ValueError("Drawing does not contain inline or anchor attributes")


    @property
    def type(self) -> WD_INLINE_SHAPE | WD_ANCHORED_SHAPE:
        return self.shape.type

    @property
    def is_inline(self) -> bool:
        return isinstance(self.shape.type, WD_INLINE_SHAPE)


class Picture(Parented):
    """Container for a Picture object."""

    def __init__(self, pict: CT_Pict, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._pict = self._element = pict

"""Math-related objects are in this subpackage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docx.oxml.math import CT_OMath, CT_OMathPara
from docx.shared import Parented

if TYPE_CHECKING:
    import docx.types as t

class MathPara(Parented):
    """Container for a DrawingML object."""

    def __init__(self, math_para: CT_OMathPara, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._math_para = self._element = math_para

class Math(Parented):
    """Container for a DrawingML object."""

    def __init__(self, math: CT_OMath, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._math = self._element = math

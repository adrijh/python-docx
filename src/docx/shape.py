"""Objects related to shapes.

A shape is a visual object that appears on the drawing layer of a document.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

from docx.enum.shape import (
    WD_ANCHORED_SHAPE_TYPE,
    WD_INLINE_SHAPE_TYPE,
)
from docx.oxml.ns import nsmap
from docx.oxml.shape import CT_Anchor, CT_GraphicalObjectData
from docx.shared import Parented

if TYPE_CHECKING:
    from docx.oxml.document import CT_Body
    from docx.oxml.shape import CT_Inline
    from docx.parts.story import StoryPart
    from docx.shared import Length


T = TypeVar("T", WD_ANCHORED_SHAPE_TYPE, WD_INLINE_SHAPE_TYPE)

def get_drawing_type(graphic_data: CT_GraphicalObjectData, enum_type: Type[T]) -> T:
    uri = graphic_data.uri

    if uri == nsmap["pic"]:
        blip = graphic_data.pic.blipFill.blip
        if blip.link is not None:
            return enum_type.LINKED_PICTURE

        return enum_type.PICTURE

    if uri == nsmap["c"]:
        return enum_type.CHART
    if uri == nsmap["dgm"]:
        return enum_type.SMART_ART
    if uri == nsmap["wps"]:
        return enum_type.SHAPE
    if uri == nsmap["wpg"]:
        return enum_type.SHAPE_GROUP

    return enum_type.NOT_IMPLEMENTED


class InlineShapes(Parented):
    """Sequence of |InlineShape| instances, supporting len(), iteration, and indexed access."""

    def __init__(self, body_elm: CT_Body, parent: StoryPart):
        super(InlineShapes, self).__init__(parent)
        self._body = body_elm

    def __getitem__(self, idx: int):
        """Provide indexed access, e.g. 'inline_shapes[idx]'."""
        try:
            inline = self._inline_lst[idx]
        except IndexError:
            msg = "inline shape index [%d] out of range" % idx
            raise IndexError(msg)

        return InlineShape(inline)

    def __iter__(self):
        return (InlineShape(inline) for inline in self._inline_lst)

    def __len__(self):
        return len(self._inline_lst)

    @property
    def _inline_lst(self):
        body = self._body
        xpath = "//w:p/w:r/w:drawing/wp:inline"
        return body.xpath(xpath)


class InlineShape:
    """Proxy for an ``<wp:inline>`` element, representing the container for an inline
    graphical object."""

    def __init__(self, inline: CT_Inline):
        super(InlineShape, self).__init__()
        self._inline = inline

    @property
    def height(self) -> Length:
        """Read/write.

        The display height of this inline shape as an |Emu| instance.
        """
        return self._inline.extent.cy

    @height.setter
    def height(self, cy: Length):
        self._inline.extent.cy = cy
        self._inline.graphic.graphicData.pic.spPr.cy = cy

    @property
    def type(self):
        """The type of this inline shape as a member of
        ``docx.enum.shape.WD_INLINE_SHAPE``, e.g. ``LINKED_PICTURE``.

        Read-only.
        """
        return get_drawing_type(
            graphic_data=self._inline.graphic.graphicData,
            enum_type=WD_INLINE_SHAPE_TYPE,
        )

    @property
    def width(self):
        """Read/write.

        The display width of this inline shape as an |Emu| instance.
        """
        return self._inline.extent.cx

    @width.setter
    def width(self, cx: Length):
        self._inline.extent.cx = cx
        self._inline.graphic.graphicData.pic.spPr.cx = cx


class AnchoredShape:
    """Proxy for an ``<wp:anchor>`` element, representing the container for an inline
    graphical object."""

    def __init__(self, anchor: CT_Anchor):
        super(AnchoredShape, self).__init__()
        self._anchor = anchor

    @property
    def height(self) -> Length:
        """Read/write.

        The display height of this inline shape as an |Emu| instance.
        """
        return self._anchor.extent.cy

    @height.setter
    def height(self, cy: Length):
        self._anchor.extent.cy = cy
        self._anchor.graphic.graphicData.pic.spPr.cy = cy

    @property
    def type(self) -> WD_ANCHORED_SHAPE_TYPE:
        """The type of this inline shape as a member of
        ``docx.enum.shape.WD_ANCHORED_SHAPE``, e.g. ``LINKED_PICTURE``.

        Read-only.
        """
        return get_drawing_type(
            graphic_data=self._anchor.graphic.graphicData,
            enum_type=WD_ANCHORED_SHAPE_TYPE,
        )

    @property
    def width(self):
        """Read/write.

        The display width of this inline shape as an |Emu| instance.
        """
        return self._anchor.extent.cx

    @width.setter
    def width(self, cx: Length):
        self._anchor.extent.cx = cx
        self._anchor.graphic.graphicData.pic.spPr.cx = cx

    def to_inline(self) -> InlineShape:
        return InlineShape(self._anchor.to_inline())

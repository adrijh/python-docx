"""Enumerations related to DrawingML shapes in WordprocessingML files."""

import enum


class WD_INLINE_SHAPE_TYPE(enum.Enum):
    """Corresponds to WdInlineShapeType enumeration.

    http://msdn.microsoft.com/en-us/library/office/ff192587.aspx.
    """

    CHART = 12
    SHAPE_GROUP = 8
    SHAPE = 7
    LINKED_PICTURE = 4
    PICTURE = 3
    SMART_ART = 15
    NOT_IMPLEMENTED = -6


WD_INLINE_SHAPE = WD_INLINE_SHAPE_TYPE


class WD_ANCHORED_SHAPE_TYPE(enum.Enum):
    """Corresponds to WdInlineShapeType enumeration.

    http://msdn.microsoft.com/en-us/library/office/ff192587.aspx.
    """

    CHART = 12
    SHAPE_GROUP = 8
    SHAPE = 7
    LINKED_PICTURE = 4
    PICTURE = 3
    SMART_ART = 15
    NOT_IMPLEMENTED = -6


WD_ANCHORED_SHAPE = WD_ANCHORED_SHAPE_TYPE

"""Custom element-classes for DrawingML-related elements like `<w:drawing>`.

For legacy reasons, many DrawingML-related elements are in `docx.oxml.shape`. Expect
those to move over here as we have reason to touch them.
"""

from docx.oxml.xmlchemy import BaseOxmlElement, ZeroOrOne


class CT_Drawing(BaseOxmlElement):
    """`<w:drawing>` element, containing a DrawingML object like a picture or chart."""
    anchor = ZeroOrOne("wp:anchor")
    inline = ZeroOrOne("wp:inline")

class CT_Pict(BaseOxmlElement):
    """`<w:pict>` element, containing a DrawingML object like a picture or chart."""

from docx.oxml.simpletypes import ST_DecimalNumber
from docx.oxml.xmlchemy import BaseOxmlElement, RequiredAttribute, ZeroOrMore


class CT_Footnotes(BaseOxmlElement):
    footnote = ZeroOrMore("w:footnote")

class CT_Endnotes(BaseOxmlElement):
    endnote = ZeroOrMore("w:endnote")

class CT_FtnEdn(BaseOxmlElement):
    id = RequiredAttribute("w:id", ST_DecimalNumber)
    p = ZeroOrMore("w:p")
    tbl = ZeroOrMore("w:tbl")

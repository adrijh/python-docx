from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OneAndOnlyOne,
    OneOrMore,
    ZeroOrMore,
    ZeroOrOne,
)


class CT_OMathPara(BaseOxmlElement):
    """
    `<m:oMathPara>` element, containing a paragraph-level math zone.
    """
    oMathParaPr = ZeroOrOne("m:oMathParaPr")
    oMath = OneOrMore("m:oMath")
    
    r = ZeroOrMore("w:r")


class CT_OMath(BaseOxmlElement):
    """
    `<m:oMath>` element, containing Office Math Markup Language content.
    Corrected implementation with proper cardinality.
    """
    f = ZeroOrOne("m:f")
    func = ZeroOrOne("m:func")
    sSub = ZeroOrOne("m:sSub")
    sSup = ZeroOrOne("m:sSup")
    sSubSup = ZeroOrOne("m:sSubSup")
    rad = ZeroOrOne("m:rad")
    e = ZeroOrOne("m:e")
    num = ZeroOrOne("m:num")
    den = ZeroOrOne("m:den")
    sub = ZeroOrOne("m:sub")
    sup = ZeroOrOne("m:sup")
    deg = ZeroOrOne("m:deg")
    
    r = ZeroOrMore("m:r")
    t = ZeroOrMore("m:t")
    
    d = ZeroOrOne("m:d")
    m = ZeroOrOne("m:m")
    mr = ZeroOrMore("m:mr")
    me = ZeroOrMore("m:me")
    
    acc = ZeroOrOne("m:acc")
    bar = ZeroOrOne("m:bar")
    box = ZeroOrOne("m:box")
    borderBox = ZeroOrOne("m:borderBox")
    eqArr = ZeroOrOne("m:eqArr")
    nary = ZeroOrOne("m:nary")
    phant = ZeroOrOne("m:phant")
    
    fPr = ZeroOrOne("m:fPr")
    sSubPr = ZeroOrOne("m:sSubPr")
    sSupPr = ZeroOrOne("m:sSupPr")
    radPr = ZeroOrOne("m:radPr")
    rPr = ZeroOrOne("m:rPr")
    ctrlPr = ZeroOrOne("m:ctrlPr")


class CT_Fraction(BaseOxmlElement):
    """
    `<m:f>` element, representing a fraction.
    Has exactly one numerator and one denominator.
    """
    fPr = ZeroOrOne("m:fPr")
    num = OneAndOnlyOne("m:num")
    den = OneAndOnlyOne("m:den")


class CT_Subscript(BaseOxmlElement):
    """
    `<m:sSub>` element, representing subscript.
    Has a base element and subscript content.
    """
    sSubPr = ZeroOrOne("m:sSubPr")
    e = OneAndOnlyOne("m:e")
    sub = OneAndOnlyOne("m:sub")


class CT_MathRun(BaseOxmlElement):
    """
    `<m:r>` element, a run within math content.
    """
    rPr = ZeroOrOne("m:rPr")
    w_rPr = ZeroOrOne("w:rPr")
    t = ZeroOrOne("m:t")

    
class CT_MathElement(BaseOxmlElement):
    """
    `<m:e>` element, base element that can contain math content.
    Can contain multiple runs or other math structures.
    """
    r = ZeroOrMore("m:r")
    
    f = ZeroOrOne("m:f")
    sSub = ZeroOrOne("m:sSub")
    sSup = ZeroOrOne("m:sSup")

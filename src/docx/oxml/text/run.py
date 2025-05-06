"""Custom element classes related to text runs (CT_R)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterator, List

from docx.oxml.drawing import CT_Drawing
from docx.oxml.ns import qn
from docx.oxml.simpletypes import ST_BrClear, ST_BrType, ST_String
from docx.oxml.text.font import CT_RPr
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrMore,
    ZeroOrOne,
)
from docx.shared import TextAccumulator

if TYPE_CHECKING:
    from docx.oxml.shape import CT_Anchor, CT_Inline
    from docx.oxml.text.pagebreak import CT_LastRenderedPageBreak
    from docx.oxml.text.parfmt import CT_TabStop

# ------------------------------------------------------------------------------------
# Run-level elements


class CT_R(BaseOxmlElement):
    """`<w:r>` element, containing the properties and text for a run."""

    add_br: Callable[[], CT_Br]
    add_tab: Callable[[], CT_TabStop]
    get_or_add_rPr: Callable[[], CT_RPr]
    _add_drawing: Callable[[], CT_Drawing]
    _add_t: Callable[..., CT_Text]
    _add_sym: Callable[..., CT_Sym]

    rPr: CT_RPr | None = ZeroOrOne("w:rPr")  # pyright: ignore[reportAssignmentType]
    br = ZeroOrMore("w:br")
    cr = ZeroOrMore("w:cr")
    drawing = ZeroOrMore("w:drawing")
    t = ZeroOrMore("w:t")
    tab = ZeroOrMore("w:tab")
    sym: CT_Sym | None = ZeroOrOne("w:sym") # pyright: ignore[reportAssignmentType]

    def add_t(self, text: str) -> CT_Text:
        """Return a newly added `<w:t>` element containing `text`."""
        t = self._add_t(text=text)
        if len(text.strip()) < len(text):
            t.set(qn("xml:space"), "preserve")
        return t

    def add_drawing(self, inline_or_anchor: CT_Inline | CT_Anchor) -> CT_Drawing:
        """Return newly appended `CT_Drawing` (`w:drawing`) child element.

        The `w:drawing` element has `inline_or_anchor` as its child.
        """
        drawing = self._add_drawing()
        drawing.append(inline_or_anchor)
        return drawing

    def clear_content(self) -> None:
        """Remove all child elements except a `w:rPr` element if present."""
        # -- remove all run inner-content except a `w:rPr` when present. --
        for e in self.xpath("./*[not(self::w:rPr)]"):
            self.remove(e)

    @property
    def inner_content_items(self) -> List[str | CT_Drawing | CT_LastRenderedPageBreak]:
        """Text of run, possibly punctuated by `w:lastRenderedPageBreak` elements."""
        from docx.oxml.text.pagebreak import CT_LastRenderedPageBreak

        accum = TextAccumulator()

        def iter_items() -> Iterator[str | CT_Drawing | CT_LastRenderedPageBreak]:
            for e in self.xpath(
                "w:br"
                " | w:cr"
                " | w:drawing"
                " | w:lastRenderedPageBreak"
                " | w:noBreakHyphen"
                " | w:ptab"
                " | w:t"
                " | w:tab"
            ):
                if isinstance(e, (CT_Drawing, CT_LastRenderedPageBreak)):
                    yield from accum.pop()
                    yield e
                else:
                    accum.push(str(e))

            # -- don't forget the "tail" string --
            yield from accum.pop()

        return list(iter_items())

    @property
    def lastRenderedPageBreaks(self) -> List[CT_LastRenderedPageBreak]:
        """All `w:lastRenderedPageBreaks` descendants of this run."""
        return self.xpath("./w:lastRenderedPageBreak")

    @property
    def style(self) -> str | None:
        """String contained in `w:val` attribute of `w:rStyle` grandchild.

        |None| if that element is not present.
        """
        rPr = self.rPr
        if rPr is None:
            return None
        return rPr.style

    @style.setter
    def style(self, style: str | None):
        """Set character style of this `w:r` element to `style`.

        If `style` is None, remove the style element.
        """
        rPr = self.get_or_add_rPr()
        rPr.style = style

    @property
    def text(self) -> str:
        """The textual content of this run, with Symbol font mapping if needed."""
        raw_text = "".join(
            str(e) for e in self.xpath("w:br | w:cr | w:noBreakHyphen | w:ptab | w:t | w:tab")
        )

        font = self.rPr.rFonts_ascii if self.rPr is not None else None
        if self.sym is not None:
            return self.sym.text

        if font == "Symbol":
            return "".join(CT_Sym.utf8_to_unicode(c) for c in raw_text)

        return raw_text

    @text.setter
    def text(self, text: str):  # pyright: ignore[reportIncompatibleMethodOverride]
        self.clear_content()
        _RunContentAppender.append_to_run_from_text(self, text)

    def _insert_rPr(self, rPr: CT_RPr) -> CT_RPr:
        self.insert(0, rPr)
        return rPr

    @property
    def symbol(self) -> str | None:
        return self.sym.code if self.sym is not None else None

    @symbol.setter
    def symbol(self, code: str) -> CT_Sym:
        sym = self._add_sym()
        sym.val = code
        sym.font = "Symbol"
        return sym
        


# ------------------------------------------------------------------------------------
# Run inner-content elements


class CT_Br(BaseOxmlElement):
    """`<w:br>` element, indicating a line, page, or column break in a run."""

    type: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:type", ST_BrType, default="textWrapping"
    )
    clear: str | None = OptionalAttribute("w:clear", ST_BrClear)  # pyright: ignore

    def __str__(self) -> str:
        """Text equivalent of this element. Actual value depends on break type.

        A line break is translated as "\n". Column and page breaks produce the empty
        string ("").

        This allows the text of run inner-content to be accessed in a consistent way
        for all run inner-context text elements.
        """
        return "\n" if self.type == "textWrapping" else ""


class CT_Cr(BaseOxmlElement):
    """`<w:cr>` element, representing a carriage-return (0x0D) character within a run.

    In Word, this represents a "soft carriage-return" in the sense that it does not end
    the paragraph the way pressing Enter (aka. Return) on the keyboard does. Here the
    text equivalent is considered to be newline ("\n") since in plain-text that's the
    closest Python equivalent.

    NOTE: this complex-type name does not exist in the schema, where `w:tab` maps to
    `CT_Empty`. This name was added to give it distinguished behavior. CT_Empty is used
    for many elements.
    """

    def __str__(self) -> str:
        """Text equivalent of this element, a single newline ("\n")."""
        return "\n"


class CT_NoBreakHyphen(BaseOxmlElement):
    """`<w:noBreakHyphen>` element, a hyphen ineligible for a line-wrap position.

    This maps to a plain-text dash ("-").

    NOTE: this complex-type name does not exist in the schema, where `w:noBreakHyphen`
    maps to `CT_Empty`. This name was added to give it behavior distinguished from the
    many other elements represented in the schema by CT_Empty.
    """

    def __str__(self) -> str:
        """Text equivalent of this element, a single dash character ("-")."""
        return "-"


class CT_PTab(BaseOxmlElement):
    """`<w:ptab>` element, representing an absolute-position tab character within a run.

    This character advances the rendering position to the specified position regardless
    of any tab-stops, perhaps for layout of a table-of-contents (TOC) or similar.
    """

    def __str__(self) -> str:
        """Text equivalent of this element, a single tab ("\t") character.

        This allows the text of run inner-content to be accessed in a consistent way
        for all run inner-context text elements.
        """
        return "\t"


# -- CT_Tab functionality is provided by CT_TabStop which also uses `w:tab` tag. That
# -- element class provides the __str__() method for this empty element, unconditionally
# -- returning "\t".


class CT_Text(BaseOxmlElement):
    """`<w:t>` element, containing a sequence of characters within a run."""

    def __str__(self) -> str:
        """Text contained in this element, the empty string if it has no content.

        This property allows this run inner-content element to be queried for its text
        the same way as other run-content elements are. In particular, this never
        returns None, as etree._Element does when there is no content.
        """
        return self.text or ""


class CT_Sym(BaseOxmlElement):
    val = RequiredAttribute("w:char", ST_String)
    font = RequiredAttribute("w:font", ST_String)

    @property
    def code(self) -> str:
        return str(self.val)

    @property
    def text(self) -> str:
        """The textual content Symbol in standard unicode."""
        return SYMBOL_MAP.get(str(self.val), "")

    @text.setter
    def text(self, _: str):  # pyright: ignore[reportIncompatibleMethodOverride]
        pass

    @staticmethod
    def utf8_to_symbol_code(char: str) -> str:
        hex_code = f"{ord(char):04X}"
        return f"F0{hex_code[-2:]}"

    @staticmethod
    def utf8_to_unicode(char: str) -> str:
        return SYMBOL_MAP.get(CT_Sym.utf8_to_symbol_code(char), char)

    @staticmethod
    def symbol_code_from_unicode(unicode: str) -> str:
        return SYMBOL_MAP_INV.get(unicode)


# ------------------------------------------------------------------------------------
# Utility


class _RunContentAppender:
    """Translates a Python string into run content elements appended in a `w:r` element.

    Contiguous sequences of regular characters are appended in a single `<w:t>` element.
    Each tab character ('\t') causes a `<w:tab/>` element to be appended. Likewise a
    newline or carriage return character ('\n', '\r') causes a `<w:cr>` element to be
    appended.
    """

    def __init__(self, r: CT_R):
        self._r = r
        self._bfr: List[str] = []

    @classmethod
    def append_to_run_from_text(cls, r: CT_R, text: str):
        """Append inner-content elements for `text` to `r` element."""
        appender = cls(r)
        appender.add_text(text)

    def add_text(self, text: str):
        """Append inner-content elements for `text` to the `w:r` element."""
        for char in text:
            self.add_char(char)
        self.flush()

    def add_char(self, char: str):
        """Process next character of input through finite state maching (FSM).

        There are two possible states, buffer pending and not pending, but those are
        hidden behind the `.flush()` method which must be called at the end of text to
        ensure any pending `<w:t>` element is written.
        """
        if char == "\t":
            self.flush()
            self._r.add_tab()
        elif char in "\r\n":
            self.flush()
            self._r.add_br()
        else:
            self._bfr.append(char)

    def flush(self):
        text = "".join(self._bfr)
        if text:
            self._r.add_t(text)
        self._bfr.clear()



SYMBOL_MAP = {
    "F020": "\u0020",
    "F021": "\u0021",
    "F022": "\u2200",
    "F023": "\u0023",
    "F024": "\u2203",
    "F025": "\u0025",
    "F026": "\u0026",
    "F027": "\u220d",
    "F028": "\u0028",
    "F029": "\u0029",
    "F02A": "\u002a",
    "F02B": "\u002b",
    "F02C": "\u002c",
    "F02D": "\u002d",
    "F02E": "\u002e",
    "F02F": "\u002f",
    "F030": "\u0030",
    "F031": "\u0031",
    "F032": "\u0032",
    "F033": "\u0033",
    "F034": "\u0034",
    "F035": "\u0035",
    "F036": "\u0036",
    "F037": "\u0037",
    "F038": "\u0038",
    "F039": "\u0039",
    "F03A": "\u003a",
    "F03B": "\u003b",
    "F03C": "\u003c",
    "F03D": "\u003d",
    "F03E": "\u003e",
    "F03F": "\u003f",
    "F040": "\u0040",
    "F041": "\u0391",
    "F042": "\u0392",
    "F043": "\u03a7",
    "F044": "\u2206",
    "F045": "\u0395",
    "F046": "\u03a6",
    "F047": "\u0393",
    "F048": "\u0397",
    "F049": "\u0399",
    "F04A": "\u03d1",
    "F04B": "\u039a",
    "F04C": "\u039b",
    "F04D": "\u039c",
    "F04E": "\u039d",
    "F04F": "\u039f",
    "F050": "\u03a0",
    "F051": "\u0398",
    "F052": "\u03a1",
    "F053": "\u03a3",
    "F054": "\u03a4",
    "F055": "\u03a5",
    "F056": "\u03c2",
    "F057": "\u03a9",
    "F058": "\u039e",
    "F059": "\u03a8",
    "F05A": "\u005a",
    "F05B": "\u005b",
    "F05C": "\u2234",
    "F05D": "\u005d",
    "F05E": "\u22a5",
    "F05F": "\u005f",
    "F060": "",
    "F061": "\u03b1",
    "F062": "\u03b2",
    "F063": "\u03c7",
    "F064": "\u03b4",
    "F065": "\u03b5",
    "F066": "\u03c6",
    "F067": "\u03b3",
    "F068": "\u03b7",
    "F069": "\u03b9",
    "F06A": "",
    "F06B": "\u03ba", ## i think wrong kappa
    "F06C": "\u03bb",
    "F06D": "\u03bc",
    "F06E": "\u03bd",
    "F06F": "\u03bf",
    "F070": "\u03c0",
    "F071": "\u03b8",
    "F072": "\u03c1", # i think wrong rho
    "F073": "\u03c3",
    "F074": "\u03c4",
    "F075": "\u03c5",
    "F076": "\u03d6",
    "F077": "\u03c9",
    "F078": "\u03be",
    "F079": "\u03a8", # perhaps lowercase psi?
    "F07A": "\u03b6",
    "F07B": "\u007b",
    "F07C": "\u007c",
    "F07D": "\u007d",
    "F07E": "\u007e",
    "F07F": "\u007f",
    "F080": "",
    "F081": "",
    "F082": "",
    "F083": "",
    "F084": "",
    "F085": "",
    "F086": "",
    "F087": "",
    "F088": "",
    "F089": "",
    "F08A": "",
    "F08B": "",
    "F08C": "",
    "F08D": "",
    "F08E": "",
    "F08F": "",
    "F090": "",
    "F091": "",
    "F092": "",
    "F093": "",
    "F094": "",
    "F095": "",
    "F096": "",
    "F097": "",
    "F098": "",
    "F099": "",
    "F09A": "",
    "F09B": "",
    "F09C": "",
    "F09D": "",
    "F09E": "",
    "F09F": "",
    "F0A0": "",
    "F0A1": "",
    "F0A2": "",
    "F0A3": "\u2264",
    "F0A4": "\u2215",
    "F0A5": "\u221e",
    "F0A6": "",
    "F0A7": "",
    "F0A8": "",
    "F0A9": "",
    "F0AA": "",
    "F0AB": "",
    "F0AC": "",
    "F0AD": "",
    "F0AE": "",
    "F0AF": "",
    "F0B0": "",
    "F0B1": "",
    "F0B2": "",
    "F0B3": "\u2265",
    "F0B4": "",
    "F0B5": "\u221d",
    "F0B6": "\u2202",
    "F0B7": "", # important
    "F0B8": "", # important
    "F0B9": "\u2260",
    "F0BA": "\u2261",
    "F0BB": "\u2248",
    "F0BC": "\u22ef", # should not be midline
    "F0BD": "\u2223",
    "F0BE": "",
    "F0BF": "",
    "F0C0": "",
    "F0C1": "",
    "F0C2": "",
    "F0C3": "",
    "F0C4": "\u2297",
    "F0C5": "\u2295",
    "F0C6": "\u2205",
    "F0C7": "\u22c2",
    "F0C8": "\u22c3",
    "F0C9": "\u2283",
    "F0CA": "\u2287",
    "F0CB": "\u2284",
    "F0CC": "\u2282",
    "F0CD": "\u2286",
    "F0CE": "\u2208",
    "F0CF": "\u2209",
    "F0D0": "\u2220",
    "F0D1": "\u2207",
    "F0D2": "",
    "F0D3": "",
    "F0D4": "",
    "F0D5": "\u220f",
    "F0D6": "\u221a",
    "F0D7": "\u2219",
    "F0D8": "\u00ac",
    "F0D9": "\u22c0",
    "F0DA": "\u22c1",
    "F0DB": "",
    "F0DC": "",
    "F0DD": "",
    "F0DE": "",
    "F0DF": "",
    "F0E0": "",
    "F0E1": "",
    "F0E2": "",
    "F0E3": "",
    "F0E4": "",
    "F0E5": "\u2211",
    "F0E6": "",
    "F0E7": "",
    "F0E8": "",
    "F0E9": "",
    "F0EA": "",
    "F0EB": "",
    "F0EC": "",
    "F0ED": "",
    "F0EE": "",
    "F0EF": "",
    "F0F0": "",
    "F0F1": "",
    "F0F2": "",
    "F0F3": "",
    "F0F4": "",
    "F0F5": "",
    "F0F6": "",
    "F0F7": "",
    "F0F8": "",
    "F0F9": "",
    "F0FA": "",
    "F0FB": "",
    "F0FC": "",
    "F0FD": "",
    "F0FE": "",
    "F0FF": "",
}

SYMBOL_IGNORE = [
    "F020",
    "F021",
    "F028",
    "F029",
    "F02A",
    "F02B",
    "F02C",
    "F02D",
    "F02E",
    "F02F",
    "F030",
    "F031",
    "F032",
    "F033",
    "F034",
    "F035",
    "F036",
    "F037",
    "F038",
    "F039",
    "F03A",
    "F03B",
    "F03C",
    "F03D",
    "F03E",
    "F03F",
    "F041",
    "F042",
    "F043",
    "F045",
    "F048",
    "F049",
    "F04B",
    "F04D",
    "F04E",
    "F04F",
    "F052",
    "F054",
    "F055",
    "F05A",
    "F07B",
    "F07C",
    "F07D",
    "F07E",
    "F07F",
    "F0B2",
]

SYMBOL_MAP_INV = {
    v:k for k, v
    in SYMBOL_MAP.items()
    if v and k not in SYMBOL_IGNORE
}

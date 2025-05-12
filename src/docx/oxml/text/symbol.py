"""Custom element class related to symbols (CT_Sym)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from docx.enum.text import WD_UNDERLINE
from docx.oxml.simpletypes import ST_String
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    RequiredAttribute,
)

if TYPE_CHECKING:
    from docx.oxml.text.font import CT_Underline


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
    def symbol_code_from_unicode(unicode: str) -> str | None:
        return SYMBOL_MAP_INV.get(unicode)

    @staticmethod
    def replace_html_entities(text: str, underline: CT_Underline | bool | None) -> str:
        is_underline = CT_Sym.is_underline(underline)
        if not is_underline:
            return text

        return re.sub(
            r'<|>',
            lambda m: UNDERLINE_REPL_MAP[str(m.group(0))],
            text,
        )

    @staticmethod
    def is_underline(underline: CT_Underline | bool | None) -> bool:
        if underline is None:
            return False

        if isinstance(underline, bool):
            return underline

        if not underline.val:
            return False

        return underline.val in [WD_UNDERLINE.SINGLE, WD_UNDERLINE.INHERITED]

UNDERLINE_REPL_MAP = {
    "<": "\u2264",
    ">": "\u2265",
}


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
    "F0AC": "\u2190",
    "F0AD": "\u2191",
    "F0AE": "\u2192",
    "F0AF": "\u2193",
    "F0B0": "\u00b0",
    "F0B1": "\u00b1",
    "F0B2": "\u0022",
    "F0B3": "\u2265",
    "F0B4": "\u00d7",
    "F0B5": "\u221d",
    "F0B6": "\u2202",
    "F0B7": "\u0095",
    "F0B8": "\u00f7",
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

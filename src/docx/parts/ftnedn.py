
"""Header and footer part objects."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.oxml.ftnedn import CT_Endnotes, CT_Footnotes
from docx.oxml.parser import parse_xml
from docx.parts.story import StoryPart
from docx.text.ftnedn import Endnote, Endnotes, Footnote, Footnotes

if TYPE_CHECKING:
    from docx.package import Package


class FootnotesPart(StoryPart):
    """Footnotes part."""

    @classmethod
    def new(cls, package: Package):
        """Return newly created footnotes part."""
        partname = PackURI("/word/footnotes.xml")
        content_type = CT.WML_FOOTNOTES
        element = cast(CT_Footnotes, parse_xml(cls._default_footnotes_xml()))
        return cls(partname, content_type, element, package)

    @classmethod
    def _default_footnotes_xml(cls) -> bytes:
        """Return bytes containing XML for a default footnotes part."""
        path = os.path.join(os.path.split(__file__)[0], "..", "templates", "default-footnotes.xml")
        with open(path, "rb") as f:
            xml_bytes = f.read()

        return xml_bytes

    @property
    def footnotes(self) -> Footnotes:
        """The |_Footnotes| instance containing the styles (<w:style> element proxies) for
        this styles part."""
        return Footnotes(self._element)

    def add_footnote(self, footnote: Footnote) -> None:
        self._element._insert_footnote(footnote._element)


class EndnotesPart(StoryPart):
    """Endnotes part."""

    @classmethod
    def new(cls, package: Package):
        """Return newly created endnotes part."""
        partname = PackURI("/word/endnotes.xml")
        content_type = CT.WML_ENDNOTES
        element = cast(CT_Endnotes, parse_xml(cls._default_endnotes_xml()))
        return cls(partname, content_type, element, package)

    @classmethod
    def _default_endnotes_xml(cls):
        """Return bytes containing XML for a default footnotes part."""
        path = os.path.join(os.path.split(__file__)[0], "..", "templates", "default-endnotes.xml")
        with open(path, "rb") as f:
            xml_bytes = f.read()

        return xml_bytes

    @property
    def endnotes(self):
        """The |_Styles| instance containing the styles (<w:style> element proxies) for
        this styles part."""
        return Endnotes(self.element)

    def add_endnote(self, endnote: Endnote) -> None:
        endnotes = Endnotes(self.element)
        endnotes.add_endnote(endnote)

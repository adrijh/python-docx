"""|DocumentPart| and closely related objects."""

from __future__ import annotations

from typing import IO, TYPE_CHECKING, cast

from docx.document import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.parts.comments import (
    CommentsExtendedPart,
    CommentsExtensiblePart,
    CommentsIdsPart,
    CommentsPart,
)
from docx.parts.ftnedn import EndnotesPart, FootnotesPart
from docx.parts.hdrftr import FooterPart, HeaderPart
from docx.parts.numbering import NumberingPart
from docx.parts.people import PeoplePart
from docx.parts.settings import SettingsPart
from docx.parts.story import StoryPart
from docx.parts.styles import StylesPart
from docx.shape import InlineShapes
from docx.shared import lazyproperty

if TYPE_CHECKING:
    from docx.opc.coreprops import CoreProperties
    from docx.settings import Settings
    from docx.styles.style import BaseStyle
    from docx.text.ftnedn import Endnotes, Footnotes


class DocumentPart(StoryPart):
    """Main document part of a WordprocessingML (WML) package, aka a .docx file.

    Acts as broker to other parts such as image, core properties, and style parts. It
    also acts as a convenient delegate when a mid-document object needs a service
    involving a remote ancestor. The `Parented.part` property inherited by many content
    objects provides access to this part object for that purpose.
    """

    def add_footer_part(self):
        """Return (footer_part, rId) pair for newly-created footer part."""
        footer_part = FooterPart.new(self.package)
        rId = self.relate_to(footer_part, RT.FOOTER)
        return footer_part, rId

    def add_header_part(self):
        """Return (header_part, rId) pair for newly-created header part."""
        header_part = HeaderPart.new(self.package)
        rId = self.relate_to(header_part, RT.HEADER)
        return header_part, rId

    @property
    def core_properties(self) -> CoreProperties:
        """A |CoreProperties| object providing read/write access to the core properties
        of this document."""
        return self.package.core_properties

    @property
    def document(self):
        """A |Document| object providing access to the content of this document."""
        return Document(self._element, self)

    def drop_header_part(self, rId: str) -> None:
        """Remove related header part identified by `rId`."""
        self.drop_rel(rId)

    def footer_part(self, rId: str):
        """Return |FooterPart| related by `rId`."""
        return self.related_parts[rId]

    def get_style(self, style_id: str | None, style_type: WD_STYLE_TYPE) -> BaseStyle:
        """Return the style in this document matching `style_id`.

        Returns the default style for `style_type` if `style_id` is |None| or does not
        match a defined style of `style_type`.
        """
        return self.styles.get_by_id(style_id, style_type)

    def get_style_id(self, style_or_name, style_type):
        """Return the style_id (|str|) of the style of `style_type` matching
        `style_or_name`.

        Returns |None| if the style resolves to the default style for `style_type` or if
        `style_or_name` is itself |None|. Raises if `style_or_name` is a style of the
        wrong type or names a style not present in the document.
        """
        return self.styles.get_style_id(style_or_name, style_type)

    def header_part(self, rId: str):
        """Return |HeaderPart| related by `rId`."""
        return self.related_parts[rId]

    @lazyproperty
    def inline_shapes(self):
        """The |InlineShapes| instance containing the inline shapes in the document."""
        return InlineShapes(self._element.body, self)

    @lazyproperty
    def numbering_part(self) -> NumberingPart:
        """A |NumberingPart| object providing access to the numbering definitions for
        this document.

        Creates an empty numbering part if one is not present.
        """
        try:
            return cast(NumberingPart, self.part_related_by(RT.NUMBERING))
        except KeyError:
            numbering_part = NumberingPart.new()
            self.relate_to(numbering_part, RT.NUMBERING)
            return numbering_part

    def save(self, path_or_stream: str | IO[bytes]):
        """Save this document to `path_or_stream`, which can be either a path to a
        filesystem location (a string) or a file-like object."""
        self.package.save(path_or_stream)

    @property
    def settings(self) -> Settings:
        """A |Settings| object providing access to the settings in the settings part of
        this document."""
        return self._settings_part.settings

    @property
    def styles(self):
        """A |Styles| object providing access to the styles in the styles part of this
        document."""
        return self._styles_part.styles

    @property
    def footnotes(self) -> Footnotes:
        """A |Footnotes| object providing access to the footnotes in the footnotes part of this
        document."""
        return self._footnotes_part.footnotes

    @property
    def endnotes(self) -> Endnotes:
        """A |Endnotes| object providing access to the endnotes in the endnotes part of this
        document."""
        return self._endnotes_part.endnotes

    @property
    def _settings_part(self) -> SettingsPart:
        """A |SettingsPart| object providing access to the document-level settings for
        this document.

        Creates a default settings part if one is not present.
        """
        try:
            return cast(SettingsPart, self.part_related_by(RT.SETTINGS))
        except KeyError:
            settings_part = SettingsPart.default(self.package)
            self.relate_to(settings_part, RT.SETTINGS)
            return settings_part

    @property
    def _styles_part(self) -> StylesPart:
        """Instance of |StylesPart| for this document.

        Creates an empty styles part if one is not present.
        """
        try:
            return cast(StylesPart, self.part_related_by(RT.STYLES))
        except KeyError:
            package = self.package
            assert package is not None
            styles_part = StylesPart.default(package)
            self.relate_to(styles_part, RT.STYLES)
            return styles_part

    @lazyproperty
    def _comments_part(self) -> CommentsPart:
        try:
            return cast(CommentsPart, self.part_related_by(RT.COMMENTS))
        except KeyError:
            comments_part = CommentsPart.new()
            self.relate_to(comments_part, RT.COMMENTS)
            return comments_part

    @lazyproperty
    def _comments_ids_part(self) -> CommentsIdsPart:
        try:
            return cast(CommentsIdsPart, self.part_related_by(RT.COMMENTS_IDS))
        except KeyError:
            comments_ids_part = CommentsIdsPart.new()
            self.relate_to(comments_ids_part, RT.COMMENTS_IDS)
            return comments_ids_part

    @lazyproperty
    def _comments_extended_part(self) -> CommentsExtendedPart:
        try:
            return cast(CommentsExtendedPart, self.part_related_by(RT.COMMENTS_EXTENDED))
        except KeyError:
            comments_extended_part = CommentsExtendedPart.new()
            self.relate_to(comments_extended_part, RT.COMMENTS_EXTENDED)
            return comments_extended_part

    @lazyproperty
    def _comments_extensible_part(self) -> CommentsExtensiblePart:
        try:
            return cast(CommentsExtensiblePart, self.part_related_by(RT.COMMENTS_EXTENSIBLE))
        except KeyError:
            comments_extensible_part = CommentsExtensiblePart.new()
            self.relate_to(comments_extensible_part, RT.COMMENTS_EXTENSIBLE)
            return comments_extensible_part

    @lazyproperty
    def _people_part(self) -> PeoplePart:
        try:
            return cast(PeoplePart, self.part_related_by(RT.PEOPLE))
        except KeyError:
            people_part = PeoplePart.new()
            self.relate_to(people_part, RT.PEOPLE)
            return people_part 

    @lazyproperty
    def _footnotes_part(self) -> FootnotesPart:
        try:
            part = self.part_related_by(RT.FOOTNOTES)
            assert part.package is not None
            return FootnotesPart.load(part.partname, part.content_type, part.blob, part.package)
        except KeyError:
            package = self.package
            assert package is not None
            footnotes_part = FootnotesPart.new(package)
            self.relate_to(footnotes_part, RT.FOOTNOTES)
            return footnotes_part

    @lazyproperty
    def _endnotes_part(self) -> EndnotesPart:
        try:
            part = self.part_related_by(RT.ENDNOTES)
            assert part.package is not None
            return EndnotesPart.load(part.partname, part.content_type, part.blob, part.package)
        except KeyError:
            package = self.package
            assert package is not None
            endnotes_part = EndnotesPart.new(package)
            self.relate_to(endnotes_part, RT.ENDNOTES)
            return endnotes_part

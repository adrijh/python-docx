"""|CommentsPart| and closely related objects."""

from typing import Self

from ..opc.part import XmlPart


class CommentsPart(XmlPart):
    """Proxy for the comments.xml part containing numbering definitions for a document
    or glossary."""

    @classmethod
    def new(cls) -> Self:
        """Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element."""
        raise NotImplementedError


class CommentsIdsPart(XmlPart):
    """Proxy for the comments.xml part containing numbering definitions for a document
    or glossary."""

    @classmethod
    def new(cls) -> Self:
        """Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element."""
        raise NotImplementedError


class CommentsExtendedPart(XmlPart):
    """Proxy for the comments.xml part containing numbering definitions for a document
    or glossary."""

    @classmethod
    def new(cls) -> Self:
        """Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element."""
        raise NotImplementedError


class CommentsExtensiblePart(XmlPart):
    """Proxy for the comments.xml part containing numbering definitions for a document
    or glossary."""

    @classmethod
    def new(cls) -> Self:
        """Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element."""
        raise NotImplementedError

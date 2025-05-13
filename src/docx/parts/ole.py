"""The proxy class for an OLE part, and related objects."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING, Self

from docx.opc.constants import CONTENT_TYPE
from docx.opc.part import Part

if TYPE_CHECKING:
    from docx.opc.package import OpcPackage
    from docx.opc.packuri import PackURI


class OlePart(Part):
    """An OLE part.

    Corresponds to the target part of a relationship with type RELATIONSHIP_TYPE.OLE.
    """

    def __init__(
        self, partname: PackURI, content_type: str, blob: bytes):
        super(OlePart, self).__init__(partname, content_type, blob)

    @classmethod
    def from_object(cls, ole_object: bytes, partname: PackURI) -> Self:
        """Return an |OlePart| instance newly created from `."""
        return cls(partname, CONTENT_TYPE.OFC_OLE_OBJECT, ole_object)

    @classmethod
    def load(cls, partname: PackURI, content_type: str, blob: bytes, package: OpcPackage):
        """Called by ``docx.opc.package.PartFactory`` to load an ole part from a
        package being opened by ``Document(...)`` call."""
        return cls(partname, content_type, blob)

    @property
    def sha1(self):
        """SHA1 hash digest of the blob of this ole part."""
        return hashlib.sha1(self.blob).hexdigest()

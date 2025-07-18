"""Provides objects that can characterize image streams.

That characterization is as to content type and size, as a required step in including
them in a document.
"""

from docx.image.bmp import Bmp
from docx.image.emf import Emf
from docx.image.gif import Gif
from docx.image.jpeg import Exif, Jfif, RawJpeg
from docx.image.png import Png
from docx.image.svg import Svg
from docx.image.tiff import Tiff
from docx.image.webp import Webp
from docx.image.wmf import PlaceableWmf

SIGNATURES = (
    # class, offset, signature_bytes
    (Png, 0, b"\x89PNG\x0D\x0A\x1A\x0A"),
    (Jfif, 6, b"JFIF"),
    (Exif, 6, b"Exif"),
    (RawJpeg, 0, b"\xff\xd8"), # Jpeg without App headers
    (Gif, 0, b"GIF87a"),
    (Gif, 0, b"GIF89a"),
    (Tiff, 0, b"MM\x00*"),  # big-endian (Motorola) TIFF
    (Tiff, 0, b"II*\x00"),  # little-endian (Intel) TIFF
    (Bmp, 0, b"BM"),
    (Emf, 40, b"\x20EMF"),
    (Svg, 0, b"<svg"),
    (PlaceableWmf, 0, b"\xd7\xcd\xc6\x9a"),
    (Webp, 0, b"RIFF"),
)

SIGNATURE_READ_BYTES = max([
    len(signature_bytes) + offset
    for _, offset, signature_bytes in SIGNATURES
])

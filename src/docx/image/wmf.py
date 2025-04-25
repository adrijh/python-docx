from struct import unpack
from typing import IO

from .constants import MIME_TYPE
from .image import BaseImageHeader


class PlaceableWmf(BaseImageHeader):
    HEADER_BYTES = 16

    @property
    def content_type(self):
        return MIME_TYPE.WMF

    @property
    def default_ext(self) -> str:
        return "wmf"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        stream.seek(0)
        header = stream.read(cls.HEADER_BYTES)
        _, _, left, top, right, bottom, inch = unpack('<I H H H H H H', header)

        width_units = right - left
        height_units = bottom - top

        horizontal_dpi = vertical_dpi = inch
        width_px = width_units
        height_px = height_units

        return cls(int(width_px), int(height_px), int(horizontal_dpi), int(vertical_dpi))

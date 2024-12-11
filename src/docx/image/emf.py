from struct import unpack
from typing import IO

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Emf(BaseImageHeader):
    HEADER_BYTES = 88
    BOUNDS_POS = (8, 24)
    DEVICE_PX_POS = (72, 80)
    DEVICE_MM_POS = (80, 88)
    MM_PER_INCH = 25.4
    INCLUSIVE_PER_MM = 100

    @property
    def content_type(self):
        return MIME_TYPE.EMF

    @property
    def default_ext(self) -> str:
        return "emf"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        stream.seek(0)
        header = stream.read(cls.HEADER_BYTES)

        dv_width_px, dv_height_px = unpack('<ii', header[cls.DEVICE_PX_POS[0]:cls.DEVICE_PX_POS[1]])
        dv_width_mm, dv_height_mm = unpack('<ii', header[cls.DEVICE_MM_POS[0]:cls.DEVICE_MM_POS[1]])

        horz_dpi = dv_width_px * cls.MM_PER_INCH / dv_width_mm
        vert_dpi = dv_height_px * cls.MM_PER_INCH / dv_height_mm

        left, top, right, bottom = unpack('<iiii', header[cls.BOUNDS_POS[0]:cls.BOUNDS_POS[1]])
        logical_width = right - left
        logical_height = bottom - top

        width_px = logical_width * horz_dpi / cls.INCLUSIVE_PER_MM
        height_px = logical_height * vert_dpi / cls.INCLUSIVE_PER_MM
        return cls(int(width_px), int(height_px), int(horz_dpi), int(vert_dpi))

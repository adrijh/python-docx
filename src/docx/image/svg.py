from typing import IO, Tuple

from lxml import etree

from docx.exceptions import PythonDocxError
from docx.shared import Cm, Inches, Length, Pt

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Svg(BaseImageHeader):
    DEFAULT_DPI = 96

    @property
    def content_type(self):
        return MIME_TYPE.SVG

    @property
    def default_ext(self) -> str:
        return "svg"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        stream.seek(0)
        root = etree.parse(stream).getroot()

        try:
            width = Svg._parse_size(root.attrib["width"])
            height = Svg._parse_size(root.attrib["height"])
        except Exception as e:
            raise PythonDocxError(f"Could not parse SVG file: {e}")

        return cls(width, height, cls.DEFAULT_DPI, cls.DEFAULT_DPI)

    @staticmethod
    def _parse_size(size_descriptor: str) -> Length:
        if size_descriptor.isdigit():
            return Length(int(size_descriptor))

        units_val, units_type = Svg._parse_string_descriptor(size_descriptor)
        units_cls = {
            "px": Length,
            "cm": Cm,
            "in": Inches,
            "pt": Pt,
        }.get(units_type, Length)

        return units_cls(units_val)

    @staticmethod
    def _parse_string_descriptor(size_descriptor: str) -> Tuple[int, str]:
        units_val = int("".join(filter(str.isdigit, size_descriptor)))
        units_type = "".join(filter(str.isalpha, size_descriptor))
        return units_val, units_type

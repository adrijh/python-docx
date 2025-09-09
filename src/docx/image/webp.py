from struct import unpack
from typing import IO

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Webp(BaseImageHeader):
    HEADER_BYTES = 50
    DEFAULT_DPI = 96
    
    @property
    def content_type(self):
        return MIME_TYPE.WEBP
    
    @property
    def default_ext(self) -> str:
        return "webp"
    
    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        stream.seek(0)
        header = stream.read(cls.HEADER_BYTES)
        
        if header[:4] != b'RIFF':
            raise ValueError("Invalid WebP file: missing RIFF header")
        
        if header[8:12] != b'WEBP':
            raise ValueError("Invalid WebP file: missing WEBP signature")
        
        chunk_type = header[12:16]
        
        if chunk_type == b'VP8 ':
            width_px, height_px = cls._parse_vp8(header)
        elif chunk_type == b'VP8L':
            width_px, height_px = cls._parse_vp8l(header)
        elif chunk_type == b'VP8X':
            width_px, height_px = cls._parse_vp8x(header)
        else:
            raise ValueError(f"Unsupported WebP chunk type: {str(chunk_type)}")
        
        horz_dpi = cls.DEFAULT_DPI
        vert_dpi = cls.DEFAULT_DPI
        
        return cls(int(width_px), int(height_px), int(horz_dpi), int(vert_dpi))
    
    @classmethod
    def _parse_vp8(cls, header: bytes) -> tuple[int, int]:
        """Parse VP8 (lossy) format"""
        if len(header) < 30:
            raise ValueError("Header too short for VP8 format")
        
        frame_tag = unpack('<I', header[20:23] + b'\x00')[0] & 0xFFFFFF
        if frame_tag & 1:
            raise ValueError("VP8 frame is not a key frame")
        
        if len(header) >= 30:
            data = unpack('<HH', header[26:30])
            width_px = data[0] & 0x3FFF
            height_px = data[1] & 0x3FFF
        else:
            raise ValueError("VP8 header too short to read dimensions")
        
        return width_px, height_px
    
    @classmethod
    def _parse_vp8l(cls, header: bytes) -> tuple[int, int]:
        """Parse VP8L (lossless) format"""

        if len(header) < 25:
            raise ValueError("Header too short for VP8L format")
        
        if header[20] != 0x2F:
            raise ValueError("Invalid VP8L signature")
        
        dimension_data = unpack('<I', header[21:25])[0]
        
        width_px = (dimension_data & 0x3FFF) + 1
        height_px = ((dimension_data >> 14) & 0x3FFF) + 1
        
        return width_px, height_px
    
    @classmethod
    def _parse_vp8x(cls, header: bytes) -> tuple[int, int]:
        """Parse VP8X (extended) format"""

        if len(header) < 30:
            raise ValueError("Header too short for VP8X format")
        
        width_data = header[24:27] + b'\x00'
        height_data = header[27:30] + b'\x00'
        
        width_px = unpack('<I', width_data)[0] + 1
        height_px = unpack('<I', height_data)[0] + 1
        
        return width_px, height_px

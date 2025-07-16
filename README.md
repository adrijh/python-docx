# python-docx

*python-docx* is a Python library for reading, creating, and updating Microsoft Word 2007+ (.docx) files.

## Fork
This fork differs from the main repository in that it includes:
- Add sdt element
- Image support: Emf, Svg, WMF, raw Jpeg, Webp
- Symbol to utf8 unicode when retrieving text from par or run
- Add basic fldSimple element support

## Installation

```
pip install python-docx
```

## Example

```python
>>> from docx import Document

>>> document = Document()
>>> document.add_paragraph("It was a dark and stormy night.")
<docx.text.paragraph.Paragraph object at 0x10f19e760>
>>> document.save("dark-and-stormy.docx")

>>> document = Document("dark-and-stormy.docx")
>>> document.paragraphs[0].text
'It was a dark and stormy night.'
```

More information is available in the [python-docx documentation](https://python-docx.readthedocs.org/en/latest/)

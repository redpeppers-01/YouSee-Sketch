# PDF to PNG Conversion Tool

This tool converts PDF files to high-quality PNG images using PyMuPDF (fitz). It's designed to process multi-page PDFs and save each page as a separate PNG file with configurable resolution.

## Features

- Convert PDF files to PNG images
- Support for multi-page PDFs
- Configurable DPI settings
- Automatic output directory creation
- Error handling and reporting

## Requirements

- Python 3.x
- PyMuPDF (fitz)

## Installation

```bash
pip install PyMuPDF
```

## Usage

### Basic Usage

Place your PDF file in the `static/pdfs` directory and run:

```bash
python pdfpng.py
```

### Function Parameters

```python
pdf_to_png(pdf_path, output_folder, dpi=300)
```

- `pdf_path`: Path to the input PDF file
- `output_folder`: Directory where PNG files will be saved
- `dpi`: Resolution for output images (default: 300)

### Output

- Creates numbered PNG files (page_1.png, page_2.png, etc.)
- Files are saved in the specified output folder
- Returns a list of paths to created files

## Directory Structure

```
convert/
├── pdfpng.py           # Main conversion script
├── output_images/      # Default output directory
│   └── page_*.png      # Generated PNG files
└── README.md           # This documentation
```

## Example

```python
# Convert a specific PDF file
pdf_path = "" #edit this path!!!!
output_folder = "output_images"
output_files = pdf_to_png(pdf_path, output_folder, dpi=300)
```

## Error Handling

The script includes error handling for common issues:
- Missing input files
- Invalid PDF files
- Permission errors
- Output directory creation failures

## Notes

- Higher DPI values result in larger file sizes but better quality
- Default 300 DPI is suitable for most use cases
- Memory usage increases with page size and DPI

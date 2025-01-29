# Test Image Generator

A simple Python script to generate test images for the UC-Sketch coloring book application.

## Description

This script creates a basic black and white outline drawing suitable for coloring. The generated image includes:
- A house with a triangular roof
- A front door
- Two windows
- A sun with radiating rays

## Requirements

- Python 3.6+
- Pillow (PIL) library

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script from the project root directory:
```bash
python static/create/generate_test_image.py
```

The script will generate a PNG file at:
```
static/images/test-page.png
```

## Output

- Image dimensions: 800x600 pixels
- Format: PNG
- Colors: Black outlines on white background
- File location: ../images/test-page.png

## Notes

- The script automatically creates directories if they don't exist
- Previous versions of the test image will be overwritten
- The generated image uses anti-aliasing for smooth lines

## Contributing

To add new test patterns:
1. Modify the draw commands in generate_test_image.py
2. Use the PIL.ImageDraw methods for shapes
3. Keep outlines black (#000000) and fills white (#FFFFFF)
4. Maintain the 800x600 canvas size

import fitz  # PyMuPDF
import os

def pdf_to_png(pdf_path, output_folder, dpi=300):
    """
    Convert a PDF file to PNG images.

    Parameters:
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Folder to save the output PNG images.
        dpi (int): Resolution for the output images. Default is 300.

    Returns:
        List of paths to the created PNG files.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    output_files = []

    # Iterate through each page
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        # Define the transformation matrix for DPI
        zoom = dpi / 72  # Default resolution is 72 DPI
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # Create the output file name
        output_file = os.path.join(output_folder, f"page_{page_number + 1}.png")
        pix.save(output_file)
        output_files.append(output_file)

    pdf_document.close()
    return output_files

if __name__ == "__main__":
    # Input PDF file
    pdf_path = "coloringbook.pdf"  # Replace with your PDF file path

    # Output folder for PNG files
    output_folder = "output_images"

    # Convert PDF to PNG
    try:
        output_files = pdf_to_png(pdf_path, output_folder)
        print("Conversion successful! Files saved at:")
        for file in output_files:
            print(file)
    except Exception as e:
        print(f"An error occurred: {e}")


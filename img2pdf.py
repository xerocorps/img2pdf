import os
import shutil
import argparse
from PIL import Image
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas

def convert_images_to_pdf(input_dir, output_pdf, width, height):
    # Create a temporary directory to store cropped images
    temp_dir = "temp_images"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    try:
        # Get list of image files in the input directory and sort them numerically
        image_files = sorted([f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))], key=lambda x: int(os.path.splitext(x)[0]))

        if not image_files:
            print("No image files found in the directory.")
            return

        # Crop and save each image to the temporary directory
        for image_file in image_files:
            image_path = os.path.join(input_dir, image_file)
            try:
                # Open the image file
                img = Image.open(image_path)
                # Crop the right portion of the image
                right_portion = img.crop((img.width - width, 0, img.width, height))
                # Save the cropped image to the temporary directory
                output_path = os.path.join(temp_dir, image_file)
                right_portion.save(output_path)
                print(f"Cropped {image_file}.")
            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")

        # Create a new PDF file with the specified dimensions
        c = canvas.Canvas(output_pdf, pagesize=(width, height))

        # Add each cropped image to the PDF in sequential order
        for cropped_image_file in image_files:
            cropped_image_path = os.path.join(temp_dir, cropped_image_file)
            c.drawImage(cropped_image_path, 0, 0, width, height)
            c.showPage()
            print(f"Added {cropped_image_file} to PDF.")

        # Save the PDF file
        c.save()
        print(f"PDF file saved as {output_pdf}")
    finally:
        # Remove the temporary directory
        shutil.rmtree(temp_dir)

def main():
    parser = argparse.ArgumentParser(description="Convert images in a directory to a PDF file.")
    parser.add_argument("input_dir", help="Path to the input directory containing images.")
    parser.add_argument("output_pdf", help="Path to the output PDF file.")
    parser.add_argument("--width", type=int, default=934, help="Width of the PDF pages.")
    parser.add_argument("--height", type=int, default=608, help="Height of the PDF pages.")
    args = parser.parse_args()

    convert_images_to_pdf(args.input_dir, args.output_pdf, args.width, args.height)

if __name__ == "__main__":
    main()

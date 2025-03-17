from PIL import Image
import sys

def flip_image_horizontally(input_path, output_path=None):
    """
    Flip an image horizontally and save the result.
    
    Args:
        input_path (str): Path to the input image
        output_path (str, optional): Path where the flipped image will be saved.
            If not provided, will add '_flipped' to the original filename.
    """
    try:
        # Open the image
        image = Image.open(input_path)
        
        # Flip the image horizontally
        flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        
        # Create output filename if not provided
        if output_path is None:
            # Split the input path into name and extension
            name, ext = input_path.rsplit('.', 1)
            output_path = f"{name}_flipped.{ext}"
        
        # Save the flipped image
        flipped_image.save(output_path)
        print(f"Image successfully flipped and saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if command line arguments are provided
    if len(sys.argv) == 1:
        print("Usage: python flip_image.py input_image.jpg [output_image.jpg]")
    elif len(sys.argv) == 2:
        flip_image_horizontally(sys.argv[1])
    else:
        flip_image_horizontally(sys.argv[1], sys.argv[2])
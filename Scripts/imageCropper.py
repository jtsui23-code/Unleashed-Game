import os
from PIL import Image

def ReSizeImages(inputDir, outputDir, targetSize=(16, 16)):
    """
    Resize all images in a directory to a target size and save them to an output directory.
    
    Args:
        inputDir (str): Path to directory containing the original images
        outputDir (str): Path to directory where resized images will be saved
        targetSize (tuple): Desired width and height in pixels, defaults to (16, 16)
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
    # Supported image formats
    validFormats = ['.png', '.jpg', '.jpeg', '.bmp']
    
    # Track progress
    processed = 0
    errors = 0
    
    # Process each file in the input directory
    for filename in os.listdir(inputDir):
        # Check if file is an image
        if any(filename.lower().endswith(fmt) for fmt in validFormats):
            inputPath = os.path.join(inputDir, filename)
            outputPath = os.path.join(outputDir, filename)
            
            try:
                # Open and resize the image
                with Image.open(inputPath) as img:
                    # Use LANCZOS resampling for better quality
                    resizedImg = img.resize(targetSize, Image.Resampling.LANCZOS)
                    
                    # Preserve original image mode and transparency
                    resizedImg = resizedImg.convert(img.mode)
                    
                    # Save the resized image
                    resizedImg.save(outputPath, quality=95, optimize=True)
                
                processed += 1
                print(f"Resized: {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                errors += 1
    
    return processed, errors

if __name__ == "__main__":
    # Input and output directories
    inputDirectory = ""  
    outputDirectory = ""  
    print("Starting image resizing...")
    processed, errors = ReSizeImages(inputDirectory, outputDirectory)
    print(f"\nCompleted! Processed {processed} images with {errors} errors.")
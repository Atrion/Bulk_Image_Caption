from PIL import Image, ImageDraw, ImageFont
import os

def add_text_below_image(image_path, text, output_path):
    # Open the image
    img = Image.open(image_path)
    
    # Define dimensions
    width, height = img.size
    font_size = 20  # Set font size to 20
    font_path = "DejaVuSans-Bold.ttf"  # Update this to your TrueType font path
    font = ImageFont.truetype(font_path, font_size)
    
    # Check if the image is animated
    if getattr(img, "is_animated", False):
        # Process each frame
        frames = []
        for frame in range(img.n_frames):
            img.seek(frame)
            frame_img = img.copy()
            frame_img = add_text_to_frame(frame_img, text, font, width, height)
            frames.append(frame_img)
        
        # Save the frames as an animated GIF
        frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0)
    else:
        # Handle static images
        new_img = Image.new('RGB', (width, height + 50), 'white')
        new_img.paste(img, (0, 0))
        new_img = add_text_to_frame(new_img, text, font, width, height)
        new_img.save(output_path, format='PNG')

def add_text_to_frame(image, text, font, width, height):
    """Add text to a single frame."""
    draw = ImageDraw.Draw(image)
    max_text_width = width - 20
    wrapped_text = wrap_text(text, font, max_text_width)
    
    text_height = sum(draw.textsize(line, font=font)[1] for line in wrapped_text) + 10 * len(wrapped_text)
    new_height = height + text_height + 30
    
    new_img = Image.new('RGB', (width, new_height), 'white')
    new_img.paste(image, (0, 0))
    
    draw = ImageDraw.Draw(new_img)
    y_text = height + 10
    for line in wrapped_text:
        text_width, _ = draw.textsize(line, font=font)
        text_x = (width - text_width) / 2
        draw.text((text_x, y_text), line, fill='black', font=font)
        y_text += draw.textsize(line, font=font)[1] + 10
    
    return new_img

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.getsize(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

def batch_process_images(image_folder, text_file, output_folder):
    # Read text file
    with open(text_file, 'r') as f:
        texts = f.readlines()
    
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each image
    for i, text in enumerate(texts):
        text = text.strip()  # Remove any leading/trailing whitespace
        image_number = str(i + 1).zfill(3)  # Create image number as '001', '002', etc.
        image_files = [f"{image_folder}/{image_number}.{ext}" for ext in ['jpg', 'jpeg', 'png', 'gif']]
        
        for image_file in image_files:
            if os.path.isfile(image_file):
                output_file = f"{output_folder}/{image_number}_edited.gif" if image_file.lower().endswith('.gif') else f"{output_folder}/{image_number}_edited.png"
                add_text_below_image(image_file, text, output_file)
                break  # Stop after processing the first found image
        else:
            print(f"Image {image_number} not found in the folder.")

# Example usage
batch_process_images('input_images', 'imagetext.txt', 'output_images')

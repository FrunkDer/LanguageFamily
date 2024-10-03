import os
from PIL import Image

def collect_images(root_dir):
    image_files = []
    # Traverse the directory structure
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == 'graph.png' or file == 'graphcompleteeuclidean.png':
                image_files.append(os.path.join(subdir, file))
                print(f"Added graph from {subdir}")
    # Sort images by timestamp
    image_files.sort(key=lambda x: os.path.basename(os.path.dirname(x)))
    return image_files

def create_gif(image_files, output_path, duration=1000, size=(1024, 1024)):
    images = []
    for image_file in image_files:
        img = Image.open(image_file).convert('RGB')
        img_resized = img.resize(size, Image.LANCZOS)  # Use LANCZOS for better quality
        images.append(img_resized)
    # Save as GIF
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)

# Define the root directory and output path
root_dir = r'C:\Users\jinfa\OneDrive\Desktop\UDHR AI\Updates'
output_path = r'C:\Users\jinfa\OneDrive\Desktop\UDHR AI\progress.gif'

# Collect images and create GIF
image_files = collect_images(root_dir)
create_gif(image_files, output_path, duration=1000, size=(1024, 1024))

print(f"GIF created at {output_path}")

# augmentation.py
from PIL import Image, ImageEnhance, ImageOps

def augment_image(
    image_path: str,
    output_path: str,
    rotation: int = 0,
    scale: float = 1.0,
    flip_horizontal: bool = False,
    flip_vertical: bool = False,
    brightness: float = 1.0,
    contrast: float = 1.0,
    saturation: float = 1.0,
    grayscale: bool = False
):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            if flip_horizontal:
                img = ImageOps.mirror(img)
            if flip_vertical:
                img = ImageOps.flip(img)
            if scale != 1.0:
                new_size = (int(img.width * scale), int(img.height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            if rotation != 0:
                img = img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation)
            if grayscale:
                img = ImageOps.grayscale(img).convert("RGBA")
            final_img = img.convert("RGB")
            final_img.save(output_path)
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

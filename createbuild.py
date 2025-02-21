import sys
from PIL import Image, ImageDraw, ImageFont
import os

def load_image(path, size=None):
    """Load an image and resize if size is provided."""
    img = Image.open(path).convert("RGBA")
    if size:
        img = resize_with_aspect_ratio(img, size)  # Use custom resize function
    return img

def resize_with_aspect_ratio(img, target_size):
    """Resize an image while preserving its aspect ratio."""
    original_width, original_height = img.size
    target_width, target_height = target_size

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Resize based on the target dimensions
    if target_width / target_height > aspect_ratio:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
    else:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)

    # Resize the image
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a new image with the target size and paste the resized image in the center
    new_img = Image.new("RGBA", target_size, (0, 0, 0, 0))
    new_img.paste(img, ((target_width - new_width) // 2, (target_height - new_height) // 2))

    return new_img

def create_build_image(perks, item, addons, offering, build_name, assets_path):
    # Load background
    background_path = os.path.join(assets_path, "background2.png")
    background = load_image(background_path)

    # Print the size of the background image
    print(f"Background image size: {background.size}")  # Width x Height

    # Image sizes
    perk_size = (240, 273)  # Adjusted to match source image resolution
    item_size = (204, 204)
    addon_size = (168, 168)
    offering_size = (203, 232)

    # Load perks background image
    perks_background_path = os.path.join(assets_path, "perksbackground.png")
    perks_background = load_image(perks_background_path, perk_size)  # Resize to match perk size

    draw = ImageDraw.Draw(background)

    # Font for labels
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"  # Arial Bold font on Windows
    font = ImageFont.truetype(font_path, 45)
    title_font = ImageFont.truetype(font_path, 102)  # Larger font for the build name

    # Add Build Name
    title_x, title_y = 49, 25
    draw.text((title_x, title_y), build_name.upper(), font=title_font, fill="white")

    # Add Perks Background
    draw.text((49, 171), "PERKS", font=ImageFont.truetype(font_path, 50), fill="white")
    perk_start_x = 120
    perk_y = 230  # Adjusted to make space for the build name
    spacing_between_perks = 241  # Increased spacing between perks
    for i, perk in enumerate(perks):
        # Paste perks background under each perk
        background.paste(perks_background, (perk_start_x + i * (perk_size[0] + spacing_between_perks), perk_y), perks_background)

    # Add Perks
    for i, perk in enumerate(perks):
        perk_img = load_image(os.path.join(assets_path, f"{perk}.png"), perk_size)
        perk_x = perk_start_x + i * (perk_size[0] + spacing_between_perks)
        background.paste(perk_img, (perk_x, perk_y), perk_img)

        # Calculate the width of the text
        text_width = draw.textlength(perk, font=font)

        # Center the text horizontally
        text_x = perk_x + (perk_size[0] - text_width) // 2
        text_y = perk_y + perk_size[1] + 11  # Position text below the perk

        # Draw the centered text
        draw.text((text_x, text_y), perk, font=font, fill="white")

    # Add Item
    item_img = load_image(os.path.join(assets_path, f"{item}.png"), item_size)
    draw.text((280, 792), "+", font=title_font, fill="white")
    item_x, item_y = 49, 738  # Adjusted to make space for the build name
    background.paste(item_img, (item_x, item_y), item_img)
    #draw.text((item_x, item_y + item_size[1] + 5), item, font=font, fill="white")
    draw.text((49, 659), "ITEM", font=font, fill="white")
    draw.text((360, 659), "ADD-ONS", font=ImageFont.truetype(font_path, 50), fill="white")

    # Add Add-ons
    for i, addon in enumerate(addons):
        addon_img = load_image(os.path.join(assets_path, f"{addon}.png"), addon_size)
        background.paste(addon_img, (item_x + (i + 2) * (addon_size[0] + 10), item_y + (item_size[1] - addon_size[1]) // 2), addon_img)

    # Add Offering
    offering_img = load_image(os.path.join(assets_path, f"{offering}.png"), offering_size)
    offering_x, offering_y = 817, 724  # Adjusted to make space for the build name
    background.paste(offering_img, (offering_x, offering_y), offering_img)
    #draw.text((offering_x, offering_y + offering_size[1] + 5), offering, font=font, fill="white")
    draw.text((817, 659), "OFFERING", font=ImageFont.truetype(font_path, 50), fill="white")

    

    # Save Output
    output_path = f"{build_name}.png"  # Use build_name as the output file name
    background.save(output_path, dpi=(900,900))
    print(f"Build image saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 10:
        print("Usage: python build_creator.py <perk1> <perk2> <perk3> <perk4> <item> <addon1> <addon2> <offering> <build_name>")
        sys.exit(1)

    perks = sys.argv[1:5]
    item = sys.argv[5]
    addons = sys.argv[6:8]
    offering = sys.argv[8]
    build_name = sys.argv[9]

    # Paths
    assets_path = "perks"

    create_build_image(perks, item, addons, offering, build_name, assets_path)
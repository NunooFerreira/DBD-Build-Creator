import sys
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk  # For modern themes
import difflib  # For finding closest matches


def get_assets_path():
    """Get the path to the assets folder, whether running as a script or as a bundled exe."""
    if hasattr(sys, '_MEIPASS'):
        # Running as a bundled exe
        return os.path.join(sys._MEIPASS, "perks")
    else:
        # Running as a script
        return "perks"

# Use this function to get the path to the perks folder
assets_path = get_assets_path()


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

class BuildCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Build Creator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Apply a modern theme
        self.style = ttk.Style(self.root)
        self.style.theme_use("equilux")  # You can try other themes like "arc", "plastik", etc.

        # Variables
        self.perks = [tk.StringVar() for _ in range(4)]
        self.item = tk.StringVar()
        self.addons = [tk.StringVar() for _ in range(2)]
        self.offering = tk.StringVar()
        self.build_name = tk.StringVar()

        # Layout
        self.create_widgets()

    def create_widgets(self):
        # Frame for the form
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(form_frame, text="Build Creator", font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Perks
        for i in range(4):
            ttk.Label(form_frame, text=f"Perk {i+1}:").grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            ttk.Entry(form_frame, textvariable=self.perks[i], width=30).grid(row=i+1, column=1, padx=10, pady=5)

        # Item
        ttk.Label(form_frame, text="Item:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.item, width=30).grid(row=5, column=1, padx=10, pady=5)

        # Add-ons
        for i in range(2):
            ttk.Label(form_frame, text=f"Add-on {i+1}:").grid(row=6+i, column=0, padx=10, pady=5, sticky="w")
            ttk.Entry(form_frame, textvariable=self.addons[i], width=30).grid(row=6+i, column=1, padx=10, pady=5)

        # Offering
        ttk.Label(form_frame, text="Offering:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.offering, width=30).grid(row=8, column=1, padx=10, pady=5)

        # Build Name
        ttk.Label(form_frame, text="Build Name:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.build_name, width=30).grid(row=9, column=1, padx=10, pady=5)

        # Create Button
        create_button = ttk.Button(form_frame, text="Create Build", command=self.create_build, style="Accent.TButton")
        create_button.grid(row=10, column=0, columnspan=2, pady=20)

        # Configure styles for a modern look
        self.style.configure("Accent.TButton", font=("Helvetica", 12), padding=10)

    def get_valid_perks(self):
        """Get a list of valid perk names from the assets directory."""
        valid_perks = []
        for filename in os.listdir(assets_path):
            if filename.endswith(".png"):
                perk_name = os.path.splitext(filename)[0]
                valid_perks.append(perk_name)
        return valid_perks

    def correct_typo(self, input_name, valid_names):
        """Correct a typo by finding the closest match from the list of valid names."""
        matches = difflib.get_close_matches(input_name, valid_names, n=1, cutoff=0.6)
        return matches[0] if matches else input_name

    def create_build(self):
        perks = [perk.get() for perk in self.perks]
        item = self.item.get()
        addons = [addon.get() for addon in self.addons]
        offering = self.offering.get()
        build_name = self.build_name.get()

        # Validate inputs
        if not all(perks) or not item or not all(addons) or not offering or not build_name:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Get valid perk names
        valid_perks = self.get_valid_perks()

        # Correct typos in perks
        corrected_perks = [self.correct_typo(perk, valid_perks) for perk in perks]

        # Correct typos in item, addons, and offering
        corrected_item = self.correct_typo(item, valid_perks)
        corrected_addons = [self.correct_typo(addon, valid_perks) for addon in addons]
        corrected_offering = self.correct_typo(offering, valid_perks)

        # Create the build image with corrected names
        create_build_image(corrected_perks, corrected_item, corrected_addons, corrected_offering, build_name, assets_path)
        messagebox.showinfo("Success", f"Build image saved as {build_name}.png")

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")  # Use a modern theme
    app = BuildCreatorApp(root)
    root.mainloop()
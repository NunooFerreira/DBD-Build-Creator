# Dead by Daylight Build Creator Program

## Overview
This program allows users to create custom build images for **Dead by Daylight** using pre-scraped images of perks, add-ons, items, and offerings. It includes two ways to generate builds:

1. **Console-based script** (`createbuild.py`) for generating builds via command-line.
2. **GUI-based script** (`withui.py`) using a user-friendly interface.

The images used by this program were obtained by running a separate scraping process (`scrape.py`) to collect the necessary assets.

---

## Features
- **Image Generation:** Combine selected perks, items, add-ons, and offerings into a cohesive build image.
- **Command-line Tool:** Create builds directly from the terminal.
- **Graphical Interface:** Use an intuitive GUI for easier build creation.
- **Typo Correction:** The GUI auto-corrects minor typos in input names.
- **Flexible Input:** Both the console and GUI versions can handle minor misspellings of perks, add-ons, items, and offerings, automatically adjusting them to the closest matching names.

---

## Setup

### Prerequisites
Ensure you have the following Python packages installed:

```bash
pip install pillow selenium beautifulsoup4 requests ttkthemes
```

You also need a **Chrome WebDriver** for Selenium if you plan to use the scraper. Download it from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and add it to your system's PATH.

### Folder Structure
```
build-creator/
│
├── perks/               # Folder where images are saved
│   └── *.png
│
├── createbuild.py       # Console script
├── scrape.py            # Image scraper (used to gather images)
├── withui.py            # GUI script
└── README.md            # Program documentation
```

---

## Usage

### 1. Scrape Images (Optional)
If you need to download images of perks, items, add-ons, and offerings, run the scraper:

```bash
python scrape.py
```

Images will be saved in the `perks/` folder.

*Note: The scraper only downloads images and does not interact with the build creation process.*

### 2. Console-Based Build Creation
Use `createbuild.py` to create a build via command-line:

```bash
python createbuild.py <perk1> <perk2> <perk3> <perk4> <item> <addon1> <addon2> <offering> <build_name>
```

#### Example:
```bash
python createbuild.py "SprintBurst" "IronWill" "DeadHard" "BorrowedTime" "MedKit" "Bandages" "GauzeRoll" "SacrificialCake" "SurvivorBuild1"
```

The resulting build image will be saved as `SurvivorBuild1.png`.

*Note: You can mistype perks, add-ons, items, or offerings, and the program will automatically adjust them to the closest matching names.*

### 3. GUI-Based Build Creation
Launch the graphical interface:

```bash
python withui.py
```

- Enter the names of the perks, item, add-ons, offering, and build name.
- Click **Create Build** to generate and save the image.

The GUI will auto-correct minor typos and display success/error messages.

*Note: The GUI also handles typos in perks, add-ons, items, and offerings, correcting them to the closest match.*

---

## Known Issues
- **Web Scraping:** The scraper relies on page structure and may break if the source website changes.
- **Image Matching:** Typos might not always be corrected accurately in the GUI.
- **Fonts:** The program uses `arialbd.ttf` from Windows fonts. On other OS, you may need to adjust the font path.

---

## Future Improvements
- Add support for scraping killer perks and images.
- Implement drag-and-drop functionality in the GUI.
- Enhance typo correction using advanced algorithms.
- Cross-platform font support.

---

## License
This program is open-source and available under the [MIT License](LICENSE).

---

## Acknowledgments
- Inspired by **Dead by Daylight** community.
- Images sourced from [gigglingcorpse.com](https://gigglingcorpse.com/).

Happy build crafting!


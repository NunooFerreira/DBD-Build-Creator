import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# URL of the page to scrape
url = "https://gigglingcorpse.com/dev/deadbydaylight/#query=;survivor=1;killer=0;type=perks"

# Folder to save the images
save_folder = "perks"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Initialize Selenium WebDriver (use the correct driver for your browser)
driver = webdriver.Chrome()  # Or use another browser driver
driver.get(url)

# Wait for the page to load completely (adjust the sleep time if needed)
time.sleep(10)

# Locate the element with class="page-inner"
page_inner = driver.find_element(By.CLASS_NAME, "page-inner")

# Get the inner HTML of the element
page_inner_html = page_inner.get_attribute("innerHTML")

# Close the Selenium WebDriver
driver.quit()

# Parse the inner HTML using BeautifulSoup
soup = BeautifulSoup(page_inner_html, 'html.parser')

# Find all image tags with the perks
perk_images = soup.find_all('img', src=True)

# Base URL for the images
base_url = "https://gigglingcorpse.com/dev/deadbydaylight/"

# Download each image
for img in perk_images:
    img_url = img['src']
    if "images/" in img_url:  # Ensure it's a perk image
        full_img_url = base_url + img_url
        img_name = os.path.basename(img_url)
        img_path = os.path.join(save_folder, img_name)

        # Download the image
        img_data = requests.get(full_img_url).content
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Downloaded: {img_name}")

print("All images downloaded successfully!")
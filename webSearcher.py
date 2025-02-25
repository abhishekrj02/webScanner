from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re

def reverse_image_search(image_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)

    try:
        driver.get("https://lens.google.com/")

        # Wait for the upload button
        upload_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        upload_button.send_keys(image_path)  # Upload the image

        # Wait for results
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href]"))
        )

        # Navigate to "Exact match" tab
        try:
            exact_match_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Exact match')]"))
            )
            exact_match_tab.click()
        except Exception:
            print(f"Exact match tab not found for {image_path}")
            driver.quit()
            return []

        # Wait for "Exact match" results to load
        time.sleep(5)  # Adjust if needed
        video_links = []

        # Extract video links from "Exact match"
        all_links = [a.get_attribute('href') for a in driver.find_elements(By.XPATH, "//a[@href]")]
        video_platforms = ["youtube.com/watch", "youtube.com/shorts", "instagram.com", "facebook.com", "twitter.com", "x.com"]
        video_links = [link for link in all_links if any(platform in link for platform in video_platforms)]

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        video_links = []

    driver.quit()
    return video_links

def filter_social_links(links):
    """Filters valid Instagram (Reels, Posts) and YouTube (Shorts, Videos) links, removing unnecessary parameters."""
    valid_links = set()  # Use a set to remove duplicates
    
    for link in links:
        # Clean URL by removing query parameters
        clean_link = re.sub(r"\?.*", "", link)
        
        # Check for Instagram Reels or Posts
        if "instagram.com" in clean_link and ("/reel/" in clean_link or "/p/" in clean_link):
            valid_links.add(clean_link)
        
        # Check for YouTube Shorts or Videos
        if "youtube.com" in clean_link or "youtu.be" in clean_link:
            if "/shorts/" in clean_link or "/watch" in clean_link or "youtu.be/" in clean_link:
                valid_links.add(clean_link)

    return list(valid_links)

# Process all extracted frames
frames_folder = r"F:\copyrightDetection\extracted_frames"
all_valid_links = set()



for frame in os.listdir(frames_folder):
    frame_path = os.path.join(frames_folder, frame)
    links = reverse_image_search(frame_path)
    all_valid_links.update(links)

# Print potential matches
print("Potential Video Matches:")
for link in sorted(all_valid_links):
    print(link)

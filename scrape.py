# Requires: pip install playwright beautifulsoup4 requests pillow
# And run once: python -m playwright install

# Title | Genre | Players | Time | Desc | Complexity | Rating | Image

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import requests
from PIL import Image
from io import BytesIO
import os

os.makedirs("images", exist_ok=True)

def fetch_game_info(url, img_index=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")  
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    data = {}

    title_tag = soup.select_one("span[itemprop='name']")
    data["title"] = title_tag.get_text(strip=True) if title_tag else None

    genre = soup.select("span.rank-title.ng-binding")
    data["genre"] = genre[1].get_text(strip=True) if len(genre) > 1 else None

    data["players"] = None
    p_tag = soup.select_one("p.gameplay-item-primary.mb-0")
    if p_tag:
        text = p_tag.get_text(" ", strip=True)  
        numbers = re.findall(r"\d+", text)     
        if len(numbers) == 2:
            data["players"] = f"{numbers[0]} - {numbers[1]}"
        elif len(numbers) == 1:
            data["players"] = numbers[0]

    data["play_time"] = None
    time_li = None
    for li in soup.select("li.gameplay-item"):
        sec_div = li.select_one("div.gameplay-item-secondary")
        if sec_div and "Playing Time" in sec_div.get_text(strip=True):
            time_li = li
            break
    if time_li:
        p_tag = time_li.select_one("p.gameplay-item-primary.mb-0")
        if p_tag:
            text = p_tag.get_text(" ", strip=True)  
            numbers = re.findall(r"\d+", text) 
            if len(numbers) == 2:
                data["play_time"] = f"{numbers[0]} - {numbers[1]} Min"
            elif len(numbers) == 1:
                data["play_time"] = f"{numbers[0]} Min"

    desc = soup.select_one("span[itemprop='description']")
    data["desc"] = desc.get_text(strip=True) if desc else None
    
    weight_tag = soup.select_one("span.ng-binding[class*='gameplay-weight']")
    data["weight"] = weight_tag.get_text(strip=True) if weight_tag else None

    rating_tag = soup.select_one("span[itemprop='ratingValue']")  
    data["average_rating"] = rating_tag.get_text(strip=True) if rating_tag else None

    data["image_file"] = None
    if img_index is not None:
        img_tag = soup.select_one("img[itemprop='image']")
        if img_tag:
            img_url = img_tag.get("src")
            if img_url:
                try:
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        img_filename = f"images/{img_index}.png"
                        img.save(img_filename, format="PNG")
                        data["image_file"] = img_filename
                except Exception as e:
                    print("Failed to download image:", e)

    print(f"✅ {data['title']}")
    return data

input_file = "input.txt"
output_file = "output.txt"

with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
    img_counter = 0
    for line in f_in:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  
        url = line
        info = fetch_game_info(url, img_index=img_counter)
        img_counter += 1

        formatted = (
            f"{info.get('title', '')} | "
            f"{info.get('genre', '')} | "
            f"{info.get('players', '')} Players | "
            f"{info.get('play_time', '')} | "
            f"\"{info.get('desc', '')}\" | "
            f"weight: {info.get('weight', '')} | "
            f"Rating: {info.get('average_rating', '')}"
        )

        f_out.write(formatted + "\n")

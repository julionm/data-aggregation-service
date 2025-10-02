# ! THIS WAS DONE BY CHATGPT :(
import csv
import uuid
import random
from datetime import datetime, timedelta

# Hollow Knight characters
characters = [
    "The Knight", "Hornet", "The Hollow Knight", "Zote", "Grimm", "Quirrel", 
    "Cloth", "Bretta", "Tiso", "Sly", "Elderbug", "Lurien", "Monomon", 
    "Herrah", "Myla", "The Radiance", "Nosk", "Hive Knight", "Dung Defender", "Menderbug"
]

# Generate 50 fictional ads
ads = []
for num in range(50):
    id = num + 1
    character = random.choice(characters)
    description_templates = [
        f"Cuddle up with a super soft {character} plushie from Farloom!",
        f"Bring {character} home with our limited edition Farloom plushies!",
        f"Perfect gift: a {character} plush from Farloom's Hollow Knight collection!",
        f"Soft, squishy, and full of charm – meet our {character} plushie!",
        f"Only at Farloom: premium Hollow Knight plushies like {character}!",
        f"Every {character} fan needs this adorable plush from Farloom!",
        f"Now available – {character} plushies by Farloom, crafted with love!",
        f"Farloom’s {character} plush is a must-have for any Hollow Knight fan!",
        f"Bring the world of Hollow Knight to life with our {character} plushie!",
        f"Farloom plushies: where {character} becomes your cuddly companion!"
    ]
    ad_description = random.choice(description_templates)[:250]
    created_at = datetime.now() - timedelta(days=random.randint(0, 365)) # change this to spit a timestamp other than a date
    ads.append([id, ad_description, created_at.strftime("%Y-%m-%d %H:%M:%S"), character])

# Write to CSV
csv_filename = "farloom_ads.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "ad_description", "created_at", "character_advertised"])
    writer.writerows(ads)

print(f"CSV file '{csv_filename}' created successfully.")

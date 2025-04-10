import os
import csv
import re
import markdown
import random
from datetime import datetime, timedelta
from pathlib import Path
import yaml
from openai import OpenAI
import textwrap

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Set the folder with markdown files
MARKDOWN_FOLDER = "./_posts"
OUTPUT_CSV = "converted_blogposts.csv"

# Set static values (you can customize)
COLLECTION_ID = "662a1b809adeb156702a5d75"
LOCALE_ID = "662a1b8028d7e78401160d02"
ITEM_ID = "PLACEHOLDER_ITEM_ID"

def generate_short_description(title, content, max_length=150):
    """Generate a short description using OpenAI's API"""
    if not OPENAI_API_KEY:
        return ""

    try:
        prompt = f"""
        Generate a concise and engaging summary of the following blog post in about 2-3 sentences.
        The summary should highlight the main points and be less than 150 characters if possible.
        It should be suitable for use in a blog post's metadata. It shouldn't contain hashtags or links.

        Title: {title}
        Content: {textwrap.shorten(content, width=1000, placeholder="...")}
        """

        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a skilled blog editor who writes concise, engaging summaries."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7)

        description = response.choices[0].message.content.strip()

        return description
    except Exception as e:
        print(f"Error generating description: {e}")
        return ""

def parse_markdown_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split front matter
    front_matter_match = re.match(r"---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not front_matter_match:
        raise ValueError(f"Front matter not found in {filepath}")

    front_matter = yaml.safe_load(front_matter_match.group(1))
    body_md = front_matter_match.group(2)

    body_html = markdown.markdown(body_md)

    return front_matter, body_md, body_html

def generate_csv_row(filepath, front_matter, body_md, html_content):
    filename = Path(filepath).stem

    # Fix the date parsing - extract complete date from filename
    # Instead of splitting at first hyphen, extract the full YYYY-MM-DD part
    match = re.match(r'(\d{4}-\d{2}-\d{2})-(.*)', filename)
    if match:
        date_str = match.group(1)
        slug = match.group(2)
    else:
        # Fallback if pattern doesn't match
        date_parts = filename.split('-', 3)[:3]  # Get first 3 parts
        date_str = '-'.join(date_parts)
        slug = '-'.join(filename.split('-')[3:])

    post_date = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = post_date.strftime("%a %b %d %Y 00:00:00 GMT+0000 (Coordinated Universal Time)")

    # Create timestamps with small random hour variations based on the post date
    created_date = post_date.replace(hour=random.randint(8, 11), minute=random.randint(0, 59))
    updated_date = post_date.replace(hour=random.randint(12, 15), minute=random.randint(0, 59))
    published_date = post_date.replace(hour=random.randint(16, 18), minute=random.randint(0, 59))

    created_str = created_date.strftime("%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)")
    updated_str = updated_date.strftime("%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)")
    published_str = published_date.strftime("%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)")

    # Generate short description
    title = front_matter.get("title", "")
    short_description = generate_short_description(title, body_md)

    return [
        title,                          # Name
        slug,                           # Slug
        COLLECTION_ID,                  # Collection ID
        LOCALE_ID,                      # Locale ID
        ITEM_ID,                        # Item ID (placeholder)
        created_str,                    # Created On - aligned with post date
        updated_str,                    # Updated On - aligned with post date
        published_str,                  # Published On - aligned with post date
        f"https://blog.magicblock.gg/{front_matter.get('image')}",  # Cover - changed domain
        short_description,              # Short Description generated by ChatGPT
        formatted_date,                 # Date
        html_content,                   # Main Content (HTML)
        "true",                         # Main Post
        "false",                        # Home Post
        "false"                         # Top Post
    ]

def convert_all_markdown_to_csv():
    files = [f for f in os.listdir(MARKDOWN_FOLDER) if f.endswith(".md")]
    rows = []

    for file in files:
        path = os.path.join(MARKDOWN_FOLDER, file)
        try:
            front_matter, body_md, html_content = parse_markdown_file(path)
            row = generate_csv_row(path, front_matter, body_md, html_content)
            rows.append(row)
        except Exception as e:
            print(f"Error processing {file}: {e}")

    headers = [
        "Name", "Slug", "Collection ID", "Locale ID", "Item ID", "Created On",
        "Updated On", "Published On", "Cover", "Short Description", "Date",
        "Main Content", "Main Post", "Home Post", "Top Post"
    ]

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Conversion completed. CSV saved to: {OUTPUT_CSV}")

if __name__ == "__main__":
    convert_all_markdown_to_csv()

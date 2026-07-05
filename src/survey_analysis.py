"""
EV Charging Survey Analysis - Chart Generation

Generates individual PNG charts for each survey question.
Cross-platform compatible (Windows, macOS, Linux).

@author: Meer Shali
@year: 2026
"""

from pathlib import Path
import re
import textwrap
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from . import utils

# ─── Configuration ─────────────────────────────────────────────────────────

OUTPUT_DIR = utils.get_figures_dir() / "survey_charts"
DATA_FILE = utils.get_data_dir() / "raw" / "EV_Charging_Survey_2026_Final_165_Results.csv"

IMAGE_WIDTH = 1400
IMAGE_HEIGHT = 805
MARGIN = 0

CARD_BACKGROUND = utils.CARD_BACKGROUND
TITLE_COLOR = utils.TITLE_COLOR
TEXT_COLOR = utils.TEXT_COLOR
PERCENT_COLOR = utils.PERCENT_COLOR

# ─── Functions ─────────────────────────────────────────────────────────────

def load_questions_from_csv(csv_path):
    """
    Load survey questions and responses from CSV.
    
    Expected columns:
    - Column 1: Question text
    - Column 4: Response option
    - Column 6: Percentage value
    """
    df = pd.read_csv(csv_path, dtype=str)
    
    questions = []
    current = None
    previous_title = None
    
    for idx, row in df.iterrows():
        question_raw = str(row.iloc[0]) if len(row) > 0 else ""
        option_raw = str(row.iloc[3]) if len(row) > 3 else ""
        percentage_raw = str(row.iloc[5]) if len(row) > 5 else "0"
        
        question = utils.remove_question_number(utils.english_only(question_raw))
        option = utils.english_only(option_raw)
        percentage = utils.parse_percentage(percentage_raw)
        
        # Start new question
        if re.match(r"^Q\d+\.", question_raw):
            if question != previous_title:
                current = {"title": question, "options": []}
                questions.append(current)
                previous_title = question
        
        # Add option to current question
        if current and option and not re.match(r"^(Total|Gesamt)", option, re.IGNORECASE):
            current["options"].append({
                "label": option,
                "percentage": percentage,
            })
    
    return questions

def draw_question_card(draw, question, box, palette):
    """
    Draw a single survey question chart.
    
    Layout: Bar chart on left, legend with percentages on right.
    """
    left, top, right, bottom = box
    card_width = right - left
    card_height = bottom - top
    
    draw.rectangle(box, fill=CARD_BACKGROUND)
    
    # Title
    inner_left = left + 30
    inner_right = right - 30
    title_top = top + 10
    
    title_font = utils.get_system_font(64, bold=True)
    option_font = utils.get_system_font(50, bold=False)
    percent_font = utils.get_system_font(50, bold=True)
    
    title_lines = textwrap.wrap(question["title"], width=39)[:2]
    title_text = "\n".join(title_lines)
    draw.multiline_text(
        (inner_left, title_top),
        title_text,
        font=title_font,
        fill=TITLE_COLOR,
        spacing=6,
    )
    
    options = question["options"]
    if not options:
        return
    
    # Calculate content area
    title_box = draw.multiline_textbbox(
        (inner_left, title_top),
        title_text,
        font=title_font,
        spacing=12,
    )
    content_top = title_box[3] + 2
    content_bottom = bottom - 45
    content_height = content_bottom - content_top
    
    chart_left = inner_left
    chart_right = left + int(card_width * 0.40)
    legend_left = left + int(card_width * 0.41)
    legend_right = inner_right
    
    # Chart calculations
    max_value = max((item["percentage"] for item in options), default=1.0)
    max_value = max(max_value, 1.0)
    
    number_of_bars = len(options)
    bar_gap = 14
    available_chart_width = chart_right - chart_left
    bar_width = max(22, min(72, (available_chart_width - bar_gap * (number_of_bars - 1)) // number_of_bars))
    
    total_bars_width = bar_width * number_of_bars + bar_gap * (number_of_bars - 1)
    bars_start = chart_left + max(0, (available_chart_width - total_bars_width) // 2)
    
    baseline = content_bottom
    maximum_bar_height = content_height
    
    # Draw bars
    for index, item in enumerate(options):
        color = palette[index % len(palette)]
        value = item["percentage"]
        
        x1 = bars_start + index * (bar_width + bar_gap)
        x2 = x1 + bar_width
        bar_height = max(4, int(maximum_bar_height * value / max_value))
        y1 = baseline - bar_height
        
        draw.rounded_rectangle((x1, y1, x2, baseline), radius=7, fill=color)
    
    # Draw legend
    legend_gap = min(86, max(60, content_height // max(number_of_bars, 1)))
    legend_total_height = legend_gap * number_of_bars
    legend_y = content_top + max(0, (content_height - legend_total_height) // 2)
    
    for index, item in enumerate(options):
        color = palette[index % len(palette)]
        row_y = legend_y + index * legend_gap
        
        draw.rounded_rectangle(
            (legend_left, row_y + 8, legend_left + 34, row_y + 42),
            radius=5,
            fill=color,
        )
        
        label = utils.shorten(item["label"], 22)
        label_x = legend_left + 46
        draw.text(
            (label_x, row_y),
            label,
            font=option_font,
            fill=TEXT_COLOR,
        )
        
        percentage_text = f'{item["percentage"]:.1%}'
        percentage_box = draw.textbbox((0, 0), percentage_text, font=percent_font)
        percentage_width = percentage_box[2] - percentage_box[0]
        label_box = draw.textbbox((0, 0), label, font=option_font)
        label_width = label_box[2] - label_box[0]
        percentage_x = min(label_x + label_width + 18, legend_right - percentage_width)
        
        draw.text(
            (percentage_x, row_y),
            percentage_text,
            font=percent_font,
            fill=PERCENT_COLOR,
        )

def create_images(questions):
    """
    Generate PNG image for each survey question.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    for index, question in enumerate(questions, start=1):
        image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), PAGE_BACKGROUND="#FFFFFF")
        draw = ImageDraw.Draw(image)
        palette = utils.PALETTES[(index - 1) % len(utils.PALETTES)]
        
        draw_question_card(
            draw,
            question,
            (MARGIN, MARGIN, IMAGE_WIDTH - MARGIN, IMAGE_HEIGHT - MARGIN),
            palette,
        )
        
        output_file = OUTPUT_DIR / f"Q{index:02d}_Chart.png"
        image.save(output_file, "PNG", dpi=(300, 300))
        print(f"✓ Created: {output_file}")

if __name__ == "__main__":
    print("📊 Loading survey data...")
    questions = load_questions_from_csv(DATA_FILE)
    print(f"✓ Found {len(questions)} questions")
    print("📈 Generating charts...")
    create_images(questions)
    print(f"✅ All charts saved to {OUTPUT_DIR}")

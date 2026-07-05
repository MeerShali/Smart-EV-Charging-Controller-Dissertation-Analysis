"""
Utility functions for chart generation and data processing.

Shared utilities for color palettes, font handling, and text processing.
"""

from pathlib import Path
import re
from PIL import ImageFont

# ─── Color Definitions ──────────────────────────────────────────────────────

# Survey Chart Colors
TITLE_COLOR = "#11213A"
TEXT_COLOR = "#40516B"
PERCENT_COLOR = "#082B65"
CARD_BACKGROUND = "#FFFFFF"

# Energy Analysis Colors
BLUE = "#4CA9D8"
ORANGE = "#E8963A"
BACKGROUND = "#FFFFFF"

# Color Palettes for Survey Questions
PALETTES = [
    ["#D97706", "#F59E0B", "#FBBF24", "#FCD34D", "#FDE68A", "#FEF3C7"],
    ["#2457A6", "#3478C9", "#5B9BE1", "#8DBCEB", "#BDD8F3", "#DCEAF8"],
    ["#168AA3", "#24A4BC", "#4BB9CA", "#7CCDD8", "#B1E1E7", "#D9F0F3"],
    ["#198754", "#2FA866", "#68BE7C", "#9AD4A7", "#C8E7CF", "#E4F3E8"],
    ["#7C3AED", "#8B5CF6", "#A78BFA", "#C4B5FD", "#DDD6FE", "#EDE9FE"],
    ["#C2415A", "#D45A70", "#E47C8E", "#EFA8B3", "#F6CDD3", "#FBE7EA"],
]

# ─── Font Handling ──────────────────────────────────────────────────────────

def get_system_font(size=40, bold=False):
    """
    Get system font with fallback to default.
    Cross-platform compatible.
    """
    font_candidates = [
        r"C:\Windows\Fonts\segoeui.ttf" if not bold else r"C:\Windows\Fonts\segoeuib.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" if not bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    
    for font_path in font_candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except (FileNotFoundError, OSError):
            continue
    
    return ImageFont.load_default()

# ─── Text Processing ───────────────────────────────────────────────────────

def parse_percentage(value):
    """
    Convert various percentage formats to float [0, 1].
    Handles: None, int, float, strings like "45.5%" or "45,5%"
    """
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value) if value <= 1 else float(value) / 100
    
    text = str(value).strip().replace(",", ".").replace("%", "")
    try:
        return float(text) / 100
    except ValueError:
        return 0.0

def english_only(text):
    """
    Extract English text from bilingual labels (English / German format).
    """
    text = str(text).strip()
    if " / " in text:
        text = text.split(" / ", 1)[0].strip()
    return text

def remove_question_number(text):
    """
    Remove question numbering (e.g., "Q1. " or "Q12. ") from text.
    """
    return re.sub(r"^Q\d+\.\s*", "", str(text)).strip()

def shorten(text, width=32):
    """
    Shorten text to specified width with ellipsis if needed.
    """
    text = str(text).strip()
    return text if len(text) <= width else text[:width - 3].rstrip() + "..."

# ─── Path Utilities ────────────────────────────────────────────────────────

def get_project_root():
    """Get the root directory of the project."""
    return Path(__file__).parent.parent

def get_data_dir():
    """Get the data directory path."""
    return get_project_root() / "data"

def get_figures_dir():
    """Get the figures directory path."""
    return get_project_root() / "figures"

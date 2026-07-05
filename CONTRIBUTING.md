# Reproduction Guide & Contribution Instructions

## Quick Setup (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/MeerShali/Smart-EV-Charging-Controller-Dissertation-Analysis.git
cd Smart-EV-Charging-Controller-Dissertation-Analysis
```

### 2. Install Git LFS
```bash
# macOS
brew install git-lfs

# Linux
sudo apt-get install git-lfs

# Windows: Download from https://git-lfs.github.com/

git lfs install
```

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Generate All Figures
```bash
python -m src.energy_price_analysis
python -m src.survey_analysis
python -m src.make_4_chart_pages
```

✅ All figures now in `figures/` directory!

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'openpyxl'"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Fonts not found (Linux/Mac)
Edit `src/utils.py` line 25-35 to use system fonts:
```python
font_candidates = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/Arial.ttf",
]
```

---

## Customization

### Change Colors
Edit `src/utils.py` PALETTES:
```python
PALETTES = [
    ["#YOUR_COLOR_1", "#YOUR_COLOR_2", ...],
]
```

### Adjust Output Size
Edit `src/survey_analysis.py`:
```python
IMAGE_WIDTH = 1400   # Change to desired width
IMAGE_HEIGHT = 805   # Change to desired height
```

---

## Project Structure

```
data/
├── raw/                          # Survey data
│   └── EV_Charging_Survey_2026_Final_165_Results.csv
└── energy_prices/                # Energy price data
    ├── GUI_ENERGY_PRICES_2025.csv
    └── GUI_ENERGY_PRICES_2026.csv

src/
├── __init__.py
├── utils.py                      # Shared utilities
├── survey_analysis.py            # Generate Q01-Q25 charts
├── energy_price_analysis.py      # Generate energy visualizations
└── make_4_chart_pages.py         # Generate 4-page summary

figures/
├── survey_charts/                # Q01_Chart.png - Q25_Chart.png
├── energy_analysis/              # combined_2025, 2026, comparison
└── Survey_Charts_Page_*.png      # 4-page layout (optional)
```

---

## Data Format

### Survey CSV
Columns: Question | Option | Count | Percentage
- 165 responses
- 25 questions
- Bilingual (English/German)

### Energy Prices CSV
Columns: MTU | Day-ahead Price [EUR/kWh]
- 15-minute intervals
- Germany-Luxembourg zone (DE-LU)
- Public historical data

---

## Questions?

📧 Contact: Meer Shali  
🔗 GitHub: [@MeerShali](https://github.com/MeerShali)


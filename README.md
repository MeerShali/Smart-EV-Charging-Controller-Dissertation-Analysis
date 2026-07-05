# Smart Residential Energy Management System with Dynamic Tariff Optimization and Smart EV Charging Control
## A Case Study of Nuremberg

**Author**: Meer Shali  
**Institution**: BSBI  
**Year**: 2026  
**Status**: Master's Dissertation Analysis

---

## 📊 Project Overview

This repository contains reproducible Python analysis and data visualization for a master's dissertation on smart residential energy management with dynamic EV charging optimization in Nuremberg, Germany.

### Key Research Areas

1. **EV Charging Survey Analysis**
   - 165 survey responses across 25 questions
   - Bilingual (English/German) survey data
   - Consumer attitudes toward smart charging and tariff optimization

2. **Energy Price Analytics**
   - Germany-Luxembourg day-ahead electricity prices (2025–2026)
   - Time series analysis, hourly profiles, monthly distributions
   - 2025 vs 2026 comparative analysis
   - 15-minute resolution price data

### Outputs

- **25 survey charts** (Q01–Q25) with colored option breakdowns
- **3 energy analysis figures** showing price trends and patterns
- **4-page survey summary** with all questions organized

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (with Git LFS for large files)

### Installation

```bash
# Clone the repository
git clone https://github.com/MeerShali/Smart-EV-Charging-Controller-Dissertation-Analysis.git
cd Smart-EV-Charging-Controller-Dissertation-Analysis

# Install Git LFS
git lfs install

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### Generate All Figures

```bash
python src/energy_price_analysis.py
python src/survey_analysis.py
python src/make_4_chart_pages.py
```

---

## 📁 Repository Structure

```
data/
├── raw/
│   └── EV_Charging_Survey_2026_Final_165_Results.csv
├── energy_prices/
│   ├── GUI_ENERGY_PRICES_202412312300-202512312300.csv
│   └── GUI_ENERGY_PRICES_202512312300-202612312300.csv

src/
├── survey_analysis.py
├── energy_price_analysis.py
├── make_4_chart_pages.py
└── utils.py

figures/
├── survey_charts/
├── energy_analysis/
```

---

## 📄 License

MIT License - See LICENSE file

**Contact**: Meer Shali | BSBI | 2026

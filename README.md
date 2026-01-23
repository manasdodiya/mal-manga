## Overview

This project scrapes the top 250 manga and manhwa entries from MyAnimeList, extracting detailed information including metadata and statistics. The scraped data is saved as CSV files in an uncleaned format, ready for data cleaning and analysis.

## Project Structure

```
mal-manga/
├── src/
│   ├── manga.py          # Manga scraping script
│   └── manhwa.py         # Manhwa scraping script
├── data/
│   ├── manga_scraped.csv # Scraped manga data (uncleaned)
│   └── manhwa_scraped.csv # Scraped manhwa data (uncleaned)
├── notebook/
│   ├── manga.ipynb       # Data cleaning notebook for manga
│   └── manhwa.ipynb      # Data cleaning notebook for manhwa
├── pyproject.toml        # Project dependencies
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd mal-manga
```

```bash
uv venv
source .venv/bin/activate
uv sync
```
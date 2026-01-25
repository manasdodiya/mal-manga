## Overview

This project collects all manga entries from MyAnimeList, extracting detailed metadata and statistics for each title. The data is first scraped and saved as raw CSV files, and then cleaned for further analysis.

## Project Structure

```
mal-manga/
├── data/
│   └── manga_scraped.csv
├── .gitignore
├── main.ipynb
├── main.py
├── pyproject.toml
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
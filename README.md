## Overview

This dataset contains comprehensive metadata and statistics for over 81,000 manga entries scraped from [MyAnimeList](https://myanimelist.net/), one of the largest anime and manga community databases. The dataset provides detailed information about manga titles, including ratings, popularity metrics, genres, themes, demographics, authors, and publication details.

## Dataset Information

- **Format**: CSV (Comma-Separated Values)
- **File Size**: 20 MB
- **Total Entries**: ~81,000 manga titles
- **Last Updated**: January 2026

## Column Descriptions

### Basic Information

| Column | Type | Description |
|--------|------|-------------|
| `manga_name` | string | Primary title of the manga |
| `manga_synonym` | string | Alternative titles or synonyms (comma-separated) |
| `manga_japanese` | string | Original Japanese title |
| `manga_english` | string | Official English title |
| `manga_type` | string | Publication format (Manga, Manhwa, Manhua, Light Novel, Novel, One-shot, Doujinshi) |

### Publication Details

| Column | Type | Description |
|--------|------|-------------|
| `manga_volume` | float | Total number of volumes published (empty if ongoing) |
| `manga_chapters` | float | Total number of chapters (empty if ongoing) |
| `manga_status` | string | Publication status (Publishing, Finished, On Hiatus) |
| `manga_serialization` | string | Magazine or platform where the manga is/was serialized |
| `manga_published_from` | date | Start date of publication (YYYY-MM-DD format) |
| `manga_published_to` | date | End date of publication (empty if ongoing) |

### Metrics & Rankings

| Column | Type | Description |
|--------|------|-------------|
| `manga_ranked` | float | Overall rank on MyAnimeList based on rating |
| `manga_popularity` | integer | Popularity rank based on number of members |
| `manga_members` | integer | Number of users who added this manga to their list |
| `manga_favorites` | integer | Number of users who marked this as favorite |
| `manga_rating` | float | Average rating score (scale: 0-10) |
| `manga_rating_by_user` | float | Total number of users who rated this manga |

### Content Classification

#### Genres (up to 9 genres per entry)
- `manga_genre_1` through `manga_genre_9`: Primary story genres
- Common genres include: Action, Adventure, Romance, Comedy, Drama, Fantasy, Horror, Mystery, Psychological, Sci-Fi, Slice of Life, Sports, Supernatural, Suspense, Award Winning, Ecchi, Girls Love, Boys Love, Hentai, Gourmet

#### Themes (up to 6 themes per entry)
- `manga_theme_1` through `manga_theme_6`: Specific thematic elements
- Common themes include: Historical, School, Military, Psychological, Isekai, Reincarnation, Time Travel, Vampire, Gore, Music, Combat Sports, Team Sports, Adult Cast, Childcare, Delinquents, Gag Humor, Iyashikei, Love Polygon, Magical Sex Shift, Mahou Shoujo, Mecha, Medical, Mythology, Organized Crime, Performing Arts, Pets, Reverse Harem, Romantic Subtext, Samurai, Strategy Game, Super Power, Survival, Urban Fantasy, Video Game, Visual Arts, Workplace, Anthropomorphic, CGDCT, Crossdressing, Detective, Educational, Harem, High Stakes Game, Idols (Female), Idols (Male), Martial Arts, Memoir, Otaku Culture, Parody, Racing, Showbiz, Space

#### Demographics (up to 2 demographics per entry)
- `manga_demographic_1` and `manga_demographic_2`: Target audience
- Values: Shounen (young male), Shoujo (young female), Seinen (adult male), Josei (adult female)

### Creator Information

| Column | Type | Description |
|--------|------|-------------|
| `manga_author_story` | string | Author/Writer of the story |
| `manga_author_art` | string | Artist/Illustrator (may be same as story author) |

## Data Characteristics

### Missing Values
- Ongoing manga will have empty values for `manga_volume`, `manga_chapters`, and `manga_published_to`
- Not all manga have English titles, synonyms, or serialization information
- Genre, theme, and demographic columns may be empty if not applicable
- Some entries may have incomplete author information

### Data Types
- Dates are in ISO format (YYYY-MM-DD)
- Numerical ratings use decimal precision
- Empty cells represent missing or not applicable data

## Data Quality Notes

- The dataset includes manga from various sources (Japanese manga, Korean manhwa, Chinese manhua, light novels)
- Ratings are community-driven and subject to selection bias
- Some entries may have incomplete metadata, especially older titles
- Genre and theme assignments follow MyAnimeList's taxonomy

## Contact

For questions, issues, or suggestions regarding this dataset, please open an issue on the repository.

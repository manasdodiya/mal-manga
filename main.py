import httpx
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import time

# completed: 60000 | next: 65000, 70000
START, STOP, STEP = 60000, 65000, 50
HEADERS, TIMEOUT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, 40
URL, FILEPATH = 'https://myanimelist.net/topmanga.php', Path('./data/manga_raw.csv')
SCRAPING_ERROR = []
CSV_HEADER = [
    'manga_name',
    'manga_synonym',
    'manga_japanese',
    'manga_english',
    'manga_type',
    'manga_volume',
    'manga_chapters',
    'manga_status',
    'manga_published',
    'manga_genre',
    'manga_theme',
    'manga_demographic',
    'manga_serialization',
    'manga_author',
    'manga_score',
    'manga_ranked',
    'manga_popularity',
    'manga_members',
    'manga_favorites',
]
MANGA_DETAILS = {
    'Synonyms': 'manga_synonym',
    'Japanese': 'manga_japanese',
    'English': 'manga_english',
    'Type': 'manga_type',
    'Volumes': 'manga_volume',
    'Chapters': 'manga_chapters',
    'Status': 'manga_status',
    'Published': 'manga_published',
    'Genre': 'manga_genre',
    'Genres': 'manga_genre',
    'Theme': 'manga_theme',
    'Themes': 'manga_theme',
    'Demographic': 'manga_demographic',
    'Demographics': 'manga_demographic',
    'Serialization': 'manga_serialization',
    'Authors': 'manga_author',
    'Score': 'manga_score',
    'Ranked': 'manga_ranked',
    'Popularity': 'manga_popularity',
    'Members': 'manga_members',
    'Favorites': 'manga_favorites',
}


def fetch_page(url, client):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.get(url, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except httpx.HTTPError as e:
            if attempt < max_retries - 1:
                if attempt == 0:
                    print()
                print(f'error fetching {url}, retrying... ({attempt + 1}/{max_retries})')
                time.sleep(10)
            else:
                print(f'error fetching {url} after {max_retries} attempts: {e}')
                SCRAPING_ERROR.append(url)
                return None


def scrape_manga(manga_soup, manga_name=None):
    scraped_row = {k: '' for k in CSV_HEADER}

    if manga_name:
        scraped_row['manga_name'] = manga_name
    else:
        name_tag = manga_soup.find('span', {'itemprop': 'name'})
        if name_tag:
            scraped_row['manga_name'] = next(name_tag.children, '')

    manga_details = manga_soup.select('div.leftside div.spaceit_pad')

    for detail in manga_details:
        info = detail.get_text(strip=True)

        if ':' not in info:
            continue

        key, value = info.split(':', 1)
        key_ = MANGA_DETAILS.get(key)
        if key_:
            scraped_row[key_] = value

    return scraped_row


def scrape_page(page_url, page_num, client):
    scraped_data = []
    page_soup = fetch_page(page_url, client)
    if not page_soup:
        return scraped_data

    print(f'\n\nscraping page {page_num}')
    print('=' * 100)

    manga_list = page_soup.select('tr h3.manga_h3 a')

    for manga in manga_list:
        manga_name = manga.get_text(strip=True)
        manga_url = manga['href']

        manga_soup = fetch_page(manga_url, client)
        if not manga_soup:
            print(f'skipped {manga_name}')
            continue

        print(f'scraping {manga_name}')

        scraped_row = scrape_manga(manga_soup, manga_name)
        scraped_data.append(scraped_row)

    return scraped_data


def insert_data(filepath, mode, data):
    with open(filepath, mode, newline='', encoding='utf-8') as manga_raw:
        csv_writer = csv.DictWriter(manga_raw, CSV_HEADER)
        if mode == 'w':
            csv_writer.writeheader()
        csv_writer.writerows(data)
        print('=' * 100)
        print(f'{len(data)} rows added to {filepath}')


def scrape_error():
    print('\nscraping errors...')
    time.sleep(10)

    errors_to_retry = SCRAPING_ERROR.copy()
    SCRAPING_ERROR.clear()

    with httpx.Client() as client:
        page_num = 0
        for error in errors_to_retry:
            if error.count('limit') == 1:
                page_num += 1
                scraped_page = scrape_page(error, page_num, client)
                insert_data(FILEPATH, 'a', scraped_page)
            else:
                manga_soup = fetch_page(error, client)
                if not manga_soup:
                    print(f'skipped {error}')
                    continue

                print(f'\nscraping {error}')

                scraped_row = scrape_manga(manga_soup)
                insert_data(FILEPATH, 'a', [scraped_row])


def main():
    with httpx.Client() as client:
        page_num = 0

        for limit in range(START, STOP, STEP):
            page_num += 1

            if limit == 0:
                scraped_page = scrape_page(URL, page_num, client)
                insert_data(FILEPATH, 'w', scraped_page)
            else:
                page_url = f'{URL}?limit={limit}'

                if page_num % 6 == 0:
                    print()
                    print('=' * 22)
                    print('waiting... rate limit')
                    print('=' * 22, end='')
                    time.sleep(30)

                time.sleep(10)
                scraped_page = scrape_page(page_url, page_num, client)
                insert_data(FILEPATH, 'a', scraped_page)


if __name__ == '__main__':
    FILEPATH.parent.mkdir(parents=True, exist_ok=True)

    main()

    while SCRAPING_ERROR:
        scrape_error()

    print('\nscraping completed...')

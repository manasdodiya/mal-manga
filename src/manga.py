import httpx
from bs4 import BeautifulSoup
import csv
import time


def scrape_page(page_url):
    page_response = httpx.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    print(f'\n\nScraping: {page_url}')
    print('=' * 100)
    manga_list = page_soup.select('tr h3.manga_h3 a')
    scrapped_data = []

    for manga in manga_list:
        scrapped_row = {}
        manga_name = manga.get_text(strip=True)
        scrapped_row.update({'manga_name': manga_name})
        manga_url = manga['href']

        manga_response = httpx.get(manga_url)
        manga_soup = BeautifulSoup(manga_response.content, 'lxml')
        print(f'Scrapping: {manga_name}')
        manga_details = manga_soup.select('div.leftside div.spaceit_pad')

        for details in manga_details:
            detail = details.get_text(strip=True)

            data = detail.split(':', 1)
            match data[0]:
                case 'Synonyms':
                    scrapped_row.update({'manga_synonym': data[1]})
                case 'Japanese':
                    scrapped_row.update({'manga_japanese': data[1]})
                case 'English':
                    scrapped_row.update({'manga_english': data[1]})
                case 'Type':
                    scrapped_row.update({'manga_type': data[1]})
                case 'Volumes':
                    scrapped_row.update({'manga_volume': data[1]})
                case 'Chapters':
                    scrapped_row.update({'manga_chapters': data[1]})
                case 'Status':
                    scrapped_row.update({'manga_status': data[1]})
                case 'Published':
                    scrapped_row.update({'manga_published': data[1]})
                case 'Genre' | 'Genres':
                    scrapped_row.update({'manga_genre': data[1]})
                case 'Theme' | 'Themes':
                    scrapped_row.update({'manga_theme': data[1]})
                case 'Demographic' | 'Demographics':
                    scrapped_row.update({'manga_demographic': data[1]})
                case 'Serialization':
                    scrapped_row.update({'manga_serialization': data[1]})
                case 'Authors':
                    scrapped_row.update({'manga_author': data[1]})
                case 'Score':
                    scrapped_row.update({'manga_score': data[1]})
                case 'Ranked':
                    scrapped_row.update({'manga_ranked': data[1]})
                case 'Popularity':
                    scrapped_row.update({'manga_popularity': data[1]})
                case 'Members':
                    scrapped_row.update({'manga_members': data[1]})
                case 'Favorites':
                    scrapped_row.update({'manga_favorites': data[1]})

        scrapped_data.append(scrapped_row)

    return scrapped_data


if __name__ == '__main__':
    page_url = 'https://myanimelist.net/topmanga.php'
    filepath = './data/manga_scraped_.csv'
    csv_header = [
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

    page_scraped = scrape_page(page_url)
    with open(filepath, 'w') as manga_scraped:
        csv_writer = csv.DictWriter(manga_scraped, csv_header)
        csv_writer.writeheader()
        csv_writer.writerows(page_scraped)
        print(f'{len(page_scraped)} rows added to {filepath}')

    for limit in range(50, 300, 50):
        time.sleep(2)
        page_url_ = f'{page_url}?limit={limit}'
        page_scraped_ = scrape_page(page_url_)
        with open(filepath, 'a') as manga_scraped:
            csv_writer = csv.DictWriter(manga_scraped, csv_header)
            csv_writer.writeheader()
            csv_writer.writerows(page_scraped_)
            print(f'{len(page_scraped_)} rows added to {filepath}')

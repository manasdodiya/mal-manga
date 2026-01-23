import httpx
from bs4 import BeautifulSoup
import csv
import time


def scrape_page(page_url):
    page_response = httpx.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    print(f'\n\nScraping: {page_url}')
    print('=' * 100)
    manhwa_list = page_soup.select('tr h3.manga_h3 a')
    scrapped_data = []

    for manhwa in manhwa_list:
        scrapped_row = {}
        manhwa_name = manhwa.get_text(strip=True)
        scrapped_row.update({'manhwa_name': manhwa_name})
        manhwa_url = manhwa['href']

        manhwa_response = httpx.get(manhwa_url)
        manhwa_soup = BeautifulSoup(manhwa_response.content, 'lxml')
        print(f'Scrapping: {manhwa_name}')
        manhwa_details = manhwa_soup.select('div.leftside div.spaceit_pad')

        for details in manhwa_details:
            detail = details.get_text(strip=True)

            data = detail.split(':', 1)
            match data[0]:
                case 'Synonyms':
                    scrapped_row.update({'manhwa_synonym': data[1]})
                case 'Japanese':
                    scrapped_row.update({'manhwa_japanese': data[1]})
                case 'English':
                    scrapped_row.update({'manhwa_english': data[1]})
                case 'Type':
                    scrapped_row.update({'manhwa_type': data[1]})
                case 'Volumes':
                    scrapped_row.update({'manhwa_volume': data[1]})
                case 'Chapters':
                    scrapped_row.update({'manhwa_chapters': data[1]})
                case 'Status':
                    scrapped_row.update({'manhwa_status': data[1]})
                case 'Published':
                    scrapped_row.update({'manhwa_published': data[1]})
                case 'Genre' | 'Genres':
                    scrapped_row.update({'manhwa_genre': data[1]})
                case 'Theme' | 'Themes':
                    scrapped_row.update({'manhwa_theme': data[1]})
                case 'Demographic' | 'Demographics':
                    scrapped_row.update({'manhwa_demographic': data[1]})
                case 'Serialization':
                    scrapped_row.update({'manhwa_serialization': data[1]})
                case 'Authors':
                    scrapped_row.update({'manhwa_author': data[1]})
                case 'Score':
                    scrapped_row.update({'manhwa_score': data[1]})
                case 'Ranked':
                    scrapped_row.update({'manhwa_ranked': data[1]})
                case 'Popularity':
                    scrapped_row.update({'manhwa_popularity': data[1]})
                case 'Members':
                    scrapped_row.update({'manhwa_members': data[1]})
                case 'Favorites':
                    scrapped_row.update({'manhwa_favorites': data[1]})

        scrapped_data.append(scrapped_row)

    return scrapped_data


if __name__ == '__main__':
    page_url = 'https://myanimelist.net/topmanga.php?type=manhwa'
    filepath = './data/manhwa_scraped.csv'
    csv_header = [
        'manhwa_name',
        'manhwa_synonym',
        'manhwa_japanese',
        'manhwa_english',
        'manhwa_type',
        'manhwa_volume',
        'manhwa_chapters',
        'manhwa_status',
        'manhwa_published',
        'manhwa_genre',
        'manhwa_theme',
        'manhwa_demographic',
        'manhwa_serialization',
        'manhwa_author',
        'manhwa_score',
        'manhwa_ranked',
        'manhwa_popularity',
        'manhwa_members',
        'manhwa_favorites',
    ]

    page_scraped = scrape_page(page_url)
    with open(filepath, 'w') as manhwa_scraped:
        csv_writer = csv.DictWriter(manhwa_scraped, csv_header)
        csv_writer.writeheader()
        csv_writer.writerows(page_scraped)
        print(f'{len(page_scraped)} rows added to {filepath}')

    for limit in range(50, 300, 50):
        time.sleep(2)
        page_url_ = f'{page_url}&limit={limit}'
        page_scraped_ = scrape_page(page_url_)
        with open(filepath, 'a') as manhwa_scraped:
            csv_writer = csv.DictWriter(manhwa_scraped, csv_header)
            csv_writer.writerows(page_scraped_)
            print(f'{len(page_scraped_)} rows added to {filepath}')

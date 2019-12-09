# Getting the pages
import requests
# Finding the desired informations
from bs4 import BeautifulSoup as BS
# Listing already downloaded
import os
import json
# Progress bar
from clint.textui import progress

ILLEGAL_FILENAME_CHAR = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

def replace_char(original_str, list_of_char, replacement=''):
    for char in list_of_char:
        original_str = original_str.replace(char, replacement)
    return original_str

def get_all_links(soup):
    links = soup.find_all('a')

    no_href = []
    episodes = []

    print(f'Finding link to episodes...', end=' ')
    for link in links:
        try:
            if 'saison' in link['href'] and 'episode' in link['href']:
                episodes.append(link['href'])
        except KeyError:
            no_href.append(link)

    print(f'Total number of link retrieved: {len(episodes)}.')
    print(f'Total number of link without video: {len(no_href)}.')

    return episodes

def get_videos():
    url = 'https://www.south-park-tv.biz/'
    print(f'Querying url {url}...', end=' ')
    page = requests.get(url)
    print(f'Page was returned.')
    soup = BS(page.content, 'html.parser')

    episodes = get_all_links(soup)

    print(f'Downloading episodes...')
    download_count = 0

    already_downloaded = {}

    try:
        with open('already_downloaded.json', 'r') as dl_file:
            already_downloaded = json.load(dl_file)
            print(f'Found a list of already downloaded episodes ({len(already_downloaded.keys())}).')
    except FileNotFoundError:
        print('No list of already downloaded episodes found.')

    downloading = False

    try:
        for episode_page in episodes:
            if episode_page in already_downloaded.keys():
                continue

            print(f'Querying page {episode_page}...', end=' ')
            page = requests.get(episode_page)
            print(f'Page was returned.')

            soup = BS(page.content, 'html.parser')
            video_div = soup.find('div', {'data-item': True})

            if not video_div:
                print('No video in this page.')
                continue

            video_url = video_div['data-item'].split('"')
            video_url = next((s for s in video_url if 'mp4' in s), None)
            video_url = video_url.replace('\\', '')

            try:
                name = soup.find('div', class_='entry-content').find('h2').text
            except AttributeError:
                name = soup.find('div', class_='entry-content').find('h3').text

            name = replace_char(name, ILLEGAL_FILENAME_CHAR, '')

            print(f'Downloading {name}...')
            stream = requests.get(video_url, stream=True)
            total_length = int(stream.headers.get('content-length'))
            with open(name + '.mp4', 'wb') as output_file:
                downloading = True
                for chunk in progress.bar(stream.iter_content(chunk_size=1024), expected_size=(1 + total_length / 1024)):
                    if chunk:
                        output_file.write(chunk)
                        output_file.flush()

            stream.close()
            downloading = False
            download_count += 1
            already_downloaded[episode_page] = name

    except KeyboardInterrupt:
        if stream:
            stream.close()

        if output_file:
            output_file.close()

        if downloading and os.path.exists(name + '.mp4'):
            os.remove(name + '.mp4')
            print(f"Removed {name + '.mp4'} (interrupted download).")

    with open('already_downloaded.json', 'w') as dl_file:
        json.dump(already_downloaded, dl_file)

    print(f'Number of episode fully downloaded: {download_count}.')

if __name__ == '__main__':
    get_videos()

# Getting the pages
import requests
# Finding the desired informations
from bs4 import BeautifulSoup as BS
# Download
import urllib.request
# Progress bar
from clint.textui import progress

url = 'https://www.south-park-tv.biz/'
print(f'Querying url {url}...', end=' ')
page = requests.get(url)
print(f'Page was returned.')
soup = BS(page.content, 'html.parser')

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

print(f'Downloading episodes...')
download_count = 0
for episode_page in episodes:
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

    name = soup.find('div', class_='entry-content').find('h2').text

    print(f'Downloading {name}...')
    stream = requests.get(video_url, stream=True)
    total_length = int(stream.headers.get('content-length'))
    with open(name + '.mp4', 'wb') as output_file:
        for chunk in progress.bar(stream.iter_content(chunk_size=1024), expected_size=(1 + total_length / 1024)):
            if chunk:
                output_file.write(chunk)
                output_file.flush()

    stream.close()

    download_count += 1

print(f'All episode downloaded (final number : {download_count}).')

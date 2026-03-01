import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

SITES = [
    {
        'name': 'HitMotop',
        'search_base_url': 'https://rus.hitmotop.com/search?q={}',
        'download_selector': '.song-link > a[href]'
    },
    {
        'name': 'Zvukofon',
        'search_base_url': 'https://muz.zvukofon.com/music/{}',
        'download_selector': '.topcharts__item-info-btn_download'
    }
]

def find_and_download_song(title, artist):
    """Функция ищет песню на заданных сайтах и скачивает её."""
    print(f"Пытаемся скачать: {title} ({artist})")

    search_query = f"{artist}+{title}"
    
    for site in SITES:
        print(f"\nПроверяем сайт: {site['name']}")
        

        full_url = site['search_base_url'].format(search_query)
        print(f"URL для поиска: {full_url}")
        
        try:
            response = requests.get(full_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            download_links = soup.select(site['download_selector'])
            
            if download_links:
                link = download_links[0].get('href')
                
           
                if not link.startswith('http'):
                    link = 'https://muz.zvukofon.com/' + link
                    
           
                print(f"Нажата кнопка скачивания: {link}")
                music_response = requests.get(link)
                
                if music_response.status_code == 200:
                    filename = f"{artist}-{title}.mp3"
                    filepath = os.path.join(output_folder, filename)
                    
                    with open(filepath, 'wb') as file:
                        file.write(music_response.content)
                        
                    print(f"Трек успешно сохранён: {filepath}")
                    return True
                else:
                    print("Ошибка при скачивании.")
            else:
                print("Композиция не найдена на данном сайте.")
        except Exception as e:
            print(f"Ошибка при обработке страницы: {e}")
    
    print("\nКомпозицию не удалось найти ни на одном сайте.")
    return False
def main():
    global output_folder
    df = pd.read_csv(r'C:\Users\Admin\Desktop\muzik.txt', sep='\t', header=None, names=['Название', 'Исполнитель', 'Длительность'])
    df.fillna('', inplace=True)
    
    output_folder = r'D:'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    success_count = 0
    total_songs = len(df)
    
    for index, row in df.iterrows():
        title = row['Название'].strip()
        artist = row['Исполнитель'].strip()
        
        if find_and_download_song(title, artist):
            success_count += 1
    
    print(f'\n\nВсего обработано композиций: {total_songs}')
    print(f'Успешно скачаны: {success_count}')
    print(f'Не найдены: {total_songs - success_count}')

if __name__ == "__main__":
    main()

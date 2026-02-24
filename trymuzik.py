import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def download_music(file_path):
    df = pd.read_csv(file_path, sep='\t', header=None, names=["Название", "Исполнитель", "Длительность"])

    df.fillna('', inplace=True)

    output_folder = r"F:\Audio"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_url = "https://rus.hitmotop.com/search?q="

    for _, row in df.iterrows():
        title = row["Название"].strip()
        artist = row["Исполнитель"].strip()
        print(f"Обрабатываю: {title}, {artist}")

        search_query = f"{artist} {title}".replace(" ", "+")
        full_url = base_url + search_query

        print(f"Ищем '{title}' от {artist}: {full_url}")

        try:
            response = requests.get(full_url)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            download_links = soup.select('.song-link > a[href]')

            if download_links:
                first_link = download_links[0]['href']

                music_response = requests.get(first_link)
                if music_response.status_code == 200:
                    filename = f"{artist}-{title}.mp3"
                    filepath = os.path.join(output_folder, filename)

                    with open(filepath, 'wb') as file:
                        file.write(music_response.content)

                    print(f"Скачано: {filename}")
                else:
                    print("Ошибка при скачивании.")
            else:
                print("Ссылка на музыкальный файл не найдена.")
        except requests.RequestException as err:
            print(f"Ошибка HTTP: {err}")

download_music(r'C:\Users\User\Desktop\muzik.txt')
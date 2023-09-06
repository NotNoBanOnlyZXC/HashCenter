import os
import requests
import time
import sys

from packaging import version

def clear():
    os.system('cls')

print(' > Подготовка...')
time.sleep(.7)
try:
    clear()
    os.mkdir('./bin/')
    print(' > Подготовка...')
except: pass
try:
    clear()
    os.mkdir('./bin/releases/')
    print(' > Подготовка...')
except: pass
try:
    clear()
    os.mkdir('./bin/center/')
    print(' > Подготовка...')
except: pass
try:
    clear()
    os.mkdir('./bin/center/telehash/')
    print(' > Подготовка...')
except: pass
try:
    clear()
    os.mkdir('./bin/center/telehash/temp/')
    print(' > Подготовка...')
except: pass
clear()

def check_version():
    print(' > Проверяем наличие обновлений...')
    local_version = get_local_version()
    latest_version = get_latest_version()

    if version.Version(local_version) < version.Version(latest_version):
        print(f' > Найдено обновление ({local_version} -> {latest_version})')
        download_latest_release()
        update_local_version(latest_version)

    run_program()

def get_local_version():
    version_file = './bin/center/telehash/version.txt'

    if not os.path.exists(version_file):
        return '0.0.0'  # Версия по умолчанию, если файл не существует

    with open(version_file, 'r') as file:
        local_version = file.read().strip()

    return local_version

def get_latest_version():
    releases_url = 'https://github.com/NoBanOnlyZXC/Telehash/releases/latest'
    response = requests.get(releases_url)
    latest_version = response.url.split('/')[-1]  # Получаем номер последнего релиза из URL (например, v1.0.0)

    return latest_version

def download_latest_release():
    latest_release_url = 'https://github.com/NoBanOnlyZXC/Telehash/releases/latest/download/Telehash.exe'
    releases_folder = './bin/releases/'

    response = requests.get(latest_release_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))  # Получаем общий размер файла
    downloaded_size = 0
    clear()
    print(f' > Обновляем Telehash до версии {get_latest_version()}...')
    temp_file = './bin/center/telehash/temp/Telehash_new.exe'
    with open(temp_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
                progress = int(downloaded_size / total_size * 100)
                progress_bar = "█" * (progress // 2) + " " + str(progress) + "%" + " " + " " * (47 - progress // 2)
                print(f" [{progress_bar}] | {downloaded_size / (1024 * 1024):.2f} MB / {total_size / (1024 * 1024):.2f} MB ", end="\r")

    print("Успешно обновлено")

    os.replace(temp_file, os.path.join(releases_folder, 'Telehash.exe'))

def update_local_version(version):
    version_file = './bin/center/telehash/version.txt'

    with open(version_file, 'w') as file:
        file.write(version)

def run_program():
    clear()
    print(' > Запускаем Telehash...')
    program_path = '.\\bin\\releases\\Telehash.exe'

    os.system(program_path)  # Запускаем программу

if get_local_version() == '0.0.0':
    choice = input(f'''-= HashCenter v1.0 =-
Вы собираетесь установить Telehash.
> Software card
╔ Telehash
║ {get_latest_version()}
╚ Beta edition''')
    if choice == '1':
        check_version()
    else:
        sys.exit()
else:
    check_version()
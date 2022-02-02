import requests
from bs4 import BeautifulSoup

def get_menu():
    url = 'https://socle.ru/mainmenu'
    r = requests.get(url=url)

    soup = BeautifulSoup(r.text, 'lxml')
    main_menu = soup.find_all('div', class_='t397__tab t397__tab_active t397__width_20') + soup.find_all('div', class_='t397__tab t397__width_20')

    for main in main_menu:
        menu = main.find('div', class_='t397__title t-name t-name_xs').text.strip()
        print(menu)
get_menu()


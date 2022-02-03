#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

def main():
    token='your token'
    bot = telebot.TeleBot(token)

    def get_menu():
        url = 'https://socle.ru/mainmenu'
        r = requests.get(url=url)

        soup = BeautifulSoup(r.text, 'lxml')
        main_menu = soup.find_all('div', class_='t397__tab t397__tab_active t397__width_20') + soup.find_all('div',
                                                                                                             class_='t397__tab t397__width_20')
        menu_up = []
        for main in main_menu:
            menu = main.find('div', class_='t397__title t-name t-name_xs').text.strip()
            menu_up.append(menu)
        return menu_up

    def get_down_menu(call):
        url = 'https://socle.ru/mainmenu'
        r = requests.get(url=url)

        soup = BeautifulSoup(r.text, 'lxml')
        main_menu = soup.find_all('div', class_='t-container t-align_center')

        menu_down = []
        for main in main_menu:
            menu = main.find('div', class_='t030__title t-title t-title_xxs').text.strip()
            menu_down.append(menu)

        zavt_and_sand = menu_down[:2]
        napitki = menu_down[4:10]
        osnovnoe = menu_down[10:]

        if call.data == 'Завтраки и сэндвичи':
            # Динамическое создание клавиатуры
            buttons = []
            markup = types.InlineKeyboardMarkup(row_width=2)
            for i in range(len(zavt_and_sand)):
                buttons.append(types.InlineKeyboardButton(text=zavt_and_sand[i],
                                                          callback_data=zavt_and_sand[i]))
            markup.add(*buttons)

            bot.send_message(call.message.chat.id, 'Выберите подпункт меню',
                             reply_markup=markup)

        elif call.data == 'Напитки':
            # Динамическое создание клавиатуры
            buttons = []
            markup = types.InlineKeyboardMarkup(row_width=3)
            for i in range(len(napitki)):
                buttons.append(types.InlineKeyboardButton(text=napitki[i],
                                                          callback_data=napitki[i]))
            markup.add(*buttons)

            bot.send_message(call.message.chat.id, 'Выберите подпункт меню',
                             reply_markup=markup)
        elif call.data == 'Основное меню':
            # Динамическое создание клавиатуры
            buttons = []
            markup = types.InlineKeyboardMarkup(row_width=3)
            for i in range(len(osnovnoe)):
                buttons.append(types.InlineKeyboardButton(text=osnovnoe[i],
                                                          callback_data=osnovnoe[i]))
            markup.add(*buttons)

            bot.send_message(call.message.chat.id, 'Выберите подпункт меню',
                             reply_markup=markup)
        elif call.data == 'Veggie меню':
            get_bluda(call)
        elif call.data == 'Десерты':
            get_bluda(call)

    def get_bluda(call):
        url = 'https://socle.ru/mainmenu'
        r = requests.get(url=url)

        soup = BeautifulSoup(r.text, 'lxml')
        main_menu = soup.find_all('div', class_='t681__title t-heading t-heading_sm')
        #print(main_menu)

        name = []
        for main in main_menu:
            menu = main.text.strip()
            name.append(menu)
        print(name)

        soup = BeautifulSoup(r.text, 'lxml')
        main_menu = soup.find_all('div', class_='t681__textwrapper')
        #print(main_menu)

        description = []
        for main in main_menu:
            menu = main.text.strip()
            description.append(menu)
        print(description)

        soup = BeautifulSoup(r.text, 'lxml')
        main_menu = soup.find_all('div', class_='t681__pricewrapper')
        #print(main_menu)

        price = []
        weight = []
        for main in main_menu:
            if main.find('div', class_='t681__price t-heading t-heading_sm') != None:
                pr = main.find('div', class_='t681__price t-heading t-heading_sm').text.strip()
                price.append(pr)
            if main.find('div', class_='t681__price t-descr t-descr_xxs') != None:
                we = main.find('div', class_='t681__price t-descr t-descr_xxs').text.strip()
                weight.append(we)
            else:
                weight.append('20г')
        print(len(price))
        print(len(weight))

        if call.data == 'Завтраки':
            out = 'Завтраки: \n\n'
            for i in range(len(name)):
                out += name[i] + ' - ' + price[i] + '\n' + description[i] + '  (' + weight[i] + ')\n'
                out += '\n'
                if name[i] == 'Панкейки из цукини с чесночным соусом':
                    break
            print(out)

        if call.data == 'Сэндвичи':
            out = 'Сэндвичи: \n\n'
            for i in range(8, 13):
                out += name[i] + ' - ' + price[i] + '\n' + description[i] + '  (' + weight[i] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Veggie меню':
            out = 'Veggie меню: \n\n'
            for i in range(13, 16):
                out += name[i] + ' - ' + price[i] + '\n' + description[i] + '  (' + weight[i] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Десерты':
            out = 'Десерты: \n\n'
            for i in range(16, 23):
                if name[i] == 'Мороженое':
                    out += name[i] + ' - ' + price[i] + '\n' + '  (' + weight[i] + ')\n'
                    out += '\n'
                    break
                out += name[i] + ' - ' + price[i] + '\n' + description[i] + '  (' + weight[i] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Напитки на основе ЭСПРЕССО':
            out = 'Напитки на основе ЭСПРЕССО: \n\n'
            for i in range(23, 33):
                if name[i] == 'Раф':
                    out += name[i] + ' - ' + price[i] + '\n' + description[i-6] + '  (' + weight[i] + ')\n'
                    out += '\n'
                else:
                    out += name[i] + ' - ' + price[i] + '\n' + '  (' + weight[i] + ')\n'
                    out += '\n'
            print(out)

        if call.data == 'ЧАЙ':
            out = 'Чай: \n\n'
            for i in range(33, 38):
                if name[i] == 'Черный чай':
                    out += name[i] + ' - ' + price[i] + '\n' + description[i-10] + '  (' + weight[i] + ')\n'
                    out += '\n'
                elif name[i] == 'Зеленый чай':
                    out += name[i] + ' - ' + price[i] + '\n' + description[i-10] + '  (' + weight[i] + ')\n'
                    out += '\n'
                else:
                    out += name[i] + ' - ' + price[i] + '\n' + '  (' + weight[i] + ')\n'
                    out += '\n'
            print(out)

        if call.data == 'Фруктовые шейки':
            out = 'Фруктовые шейки: \n\n'
            for i in range(38, 41):
                out += name[i] + ' - ' + price[i] + '\n' + '  (' + weight[i] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Милкшейки':
            out = 'Милкшейки: \n\n'
            for i in range(41, 44):
                out += name[i] + ' - ' + price[i] + '\n' + description[i-16] + '  (' + weight[i] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Горячие коктейли':
            out = 'Горячие коктейли: \n\n'
            for i in range(44, 49):
                out += name[i] + ' - ' + price[i] + '\n' + description[i-16] + '  (' + weight[i] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Разливное пиво':
            out = 'Разливное пиво: \n\n'
            for i in range(49, 53):
                if name[i] == 'Гостевое пиво из Австрии, Великобритании, Германии, России, Бельгии':
                    out += name[i] + ' - ' + price[i] + '\n' + description[i - 16] + '\n'
                else:
                    out += name[i] + ' - ' + price[i] + '\n' + description[i-16] + '  (' + weight[i] + ')\n'
                    out += '\n'
            print(out)

        if call.data == 'Салаты':
            out = 'Салаты: \n\n'
            for i in range(53, 58):
                out += name[i] + ' - ' + price[i-1] + '\n' + description[i-16] + '  (' + weight[i-1] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'СУПЫ':
            out = 'Супы: \n\n'
            for i in range(58, 63):
                out += name[i] + ' - ' + price[i-1] + '\n' + description[i-16] + '  (' + weight[i-1] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'ГРИЛЬ меню':
            out = 'Гриль меню: \n\n'
            for i in range(63, 72):
                out += name[i] + ' - ' + price[i-1] + '\n' + description[i-16] + '  (' + weight[i-1] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'ГАРНИРЫ':
            out = 'Гарниры: \n\n'
            for i in range(72, 77):
                out += name[i] + ' - ' + price[i-1] + '\n' + '  (' + weight[i-1] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Бургеры':
            out = 'Бургеры: \n\n'
            for i in range(77, 85):
                out += name[i] + ' - ' + price[i-1] + '\n' + description[i-21] + '  (' + weight[i-1] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Горячие сковородки':
            out = 'Горячие сковородки: \n\n'
            for i in range(85, 88):
                out += name[i] + ' - ' + price[i-1] + '\n' + description[i-21] + '  (' + weight[i-1] + ')\n'
                out += '\n'
            print(out)

        if call.data == 'Пасты и соусы':
            out = 'Пасты и соусы: \n\n'
            for i in range(88, 98):
                if name[i] == 'Гречневая лапша с овощами и кунжутом':
                    out += name[i] + ' - ' + price[i-1] + '\n' + description[i - 25] + '\n'
                    out += '\n'
                else:
                    out += name[i] + ' - ' + price[i-1] + '\n' + '  (' + weight[i-1] + ')\n'
                    out += '\n'
            print(out)

        if call.data == 'Закуски':
            out = 'Закуски: \n\n'
            for i in range(98, 103):
                if name[i] == 'Креветки в винном соусе' or name[i] == 'Крылья Баффало':
                    out += name[i] + ' - ' + price[i - 1] + '\n' + '  (' + weight[i - 1] + ')\n'
                    out += '\n'
                elif name[i] == 'Сырная тарелка':
                    out += name[i] + ' - ' + price[i - 1] + '\n' + description[i - 31] + '  (' + weight[i - 1] + ')\n'
                    out += '\n'
                else:
                    out += name[i] + ' - ' + price[i-1] + '\n' + description[i-32] + '  (' + weight[i-1] + ')\n'
                    out += '\n'
            print(out)

        if call.data == 'Для дружной компании':
            out = 'Для дружной компании: \n\n'
            for i in range(103, 106):
                out += name[i] + ' - ' + price[i-1] + '\n' + description[i-32] + '  (' + weight[i-1] + ')\n'
                out += '\n'
            print(out)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=out)


    @bot.message_handler(commands=['start'])
    def start_message(message):
        buttons = []
        list_menu_up = get_menu()

        # Динамическое создание клавиатуры
        markup = types.InlineKeyboardMarkup(row_width=2)
        for i in range(len(list_menu_up)):
            buttons.append(types.InlineKeyboardButton(text=list_menu_up[i],
                                                      callback_data=list_menu_up[i]))
        markup.add(*buttons)

        bot.send_message(message.chat.id, 'Вас приветствует ресторан Цоколь!',
                         reply_markup=markup)

    #Обработчик
    @bot.callback_query_handler(func=lambda call:True)
    def callback(call):
        print(call.data)
        if call.message.text == 'Вас приветствует ресторан Цоколь!':
            get_down_menu(call)
        elif call.message.text == 'Выберите подпункт меню':
            get_bluda(call)


    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()

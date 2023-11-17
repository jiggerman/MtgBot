import gspread
from gspread import Client, Spreadsheet


url_sheet = '---'
gc: Client = gspread.service_account('./service_account.json')
sh: Spreadsheet = gc.open_by_url(url_sheet)


def create_new_client_sheet(user_name):
    """
    :param user_name: id человека из тг (используется как название)
    :return: создает новый worksheet
    """
    worksheet_list = [wh.title for wh in sh.worksheets()]
    if user_name not in worksheet_list:
        sh.add_worksheet(user_name, rows=100, cols=5)


def add_cards(user_name, cards):
    """
    :param user_name:
    :param cards: сообщение от пользователя
    :return: добавляет 1 карту в формате: ссылка колическо качесво цена
    """

    card = cards.replace('/n', ' ').split()
    len_card = len(card)

    if len_card == 3:
        if 'https://www.cardkingdom.com' in card[0] and card[1].isdigit() and card[2].upper() in ['NM', 'EX', 'VG', 'G']:
            sh.worksheet(user_name).insert_row(cards.split())
            return 1
        else:
            return 404
    elif len_card > 3:
        for i in range(0, len_card, 3):
            if 'https://www.cardkingdom.com' in card[i] and card[i + 1].isdigit() and card[i + 2].upper() in ['NM', 'EX', 'VG', 'G']:
                sh.worksheet(user_name).insert_row([card[i], card[i + 1], card[i + 2]])
            else:
                return 404
        else:
            return 1


def add_all_cards_from_file(user_name, destination):
    """
    :param user_name:
    :param file: файл полученные от человека
    :return: добавляет все карты в формате: ссылка колическо качесво цена
    """
    with open(destination, 'r') as cards:
        for card in cards:
            card = card.split()
            if 'https://www.cardkingdom.com' in card[0] and card[1].isdigit() and card[2].upper() in ['NM', 'EX', 'VG', 'G']:
                sh.worksheet(user_name).insert_row(card)
            else:
                return 404
        return 1


def print_all_cards_from_sheet(user_name):
    """
    :param user_name:
    :return: Список карт человека
    """
    return sh.worksheet(user_name).get_all_values()


def delete_card(user_name, url_card):
    """
    :param :
    :return: Удаляет карту по ссылке
    """
    if 'https://www.cardkingdom.com' not in url_card:
        return 404
    else:
        list_of_cards = sh.worksheet(user_name).get_all_values()
        for idx, card in enumerate(list_of_cards):
            if url_card == card[0]:
                sh.worksheet(user_name).delete_rows(idx + 1)  # В таблице отсчет с 1
                return 1
        else:
            return 404

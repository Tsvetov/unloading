# -*- coding: utf-8 -*-

# std
import os

import requests

__author__ = 'cpn'


class Request(object):
    """
        Класс для HTTP запросов к сервису

        пользоваться примерно так:

        >>> obj = Request('login', 'password')
        >>> file_iter = obj.get_file('2015-08-12', '2015-08-24')
        >>> print ''.join(file_iter)
    """

    def __init__(self, login, password, url="https://mtm.ipayoptions.com"):
        self.login_address = 'login.htm'
        self.transaction_address = 'transactions.htm'
        self.url_start = url
        self.username = login
        self.password = password
        self.session = self.login()

    def login(self):
        """
            Метод авторизации в сервисе
        """
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0'}
        data = {
            "username": self.username,
            "password": self.password,
            'send': "1",
            "Submit": "Login Now"
        }
        session.post(self.url_login, data=data, headers=headers)
        return session

    def get_file(self, date_start, date_finish, type_file='csv'):
        """
            Получаем файл

            @date_start: дата начала периода
            @type: str

            @date_finish: дата окончания периода
            @type: str

            @type_file: тип файла,
            @default: 'csv'
            @type: str

            @return: возвращаем итератор по файлу
        """
        obj = self.__post_request(date_start, date_finish, type_file)
        return obj.iter_content(1024)

    def __post_request(self, date_start, date_finish, type_file):
        """
            Делаем POST-запрос на файл

            @date_start: дата начала периода
            @type: str

            @date_finish: дата окончания периода
            @type: str

            @return: возвращаем объект запроса
        """
        url = self.url_transactions
        step = 'export' if type_file == 'csv' else 'list'
        data = {
            'datefrom': date_start,
            'dateto': date_finish,
            'step': step,

            # TODO: непонятные данные в форме, нужно их проверять
            'accountid': '0',
            'methid': 'All',
            'next':	'0',
            'perpage': '25',
            'previous': '0',
            'search': '',
            'txstatus': '-1'
        }
        return self.session.post(url, data)

    @property
    def url_login(self):
        """
            Свойство - полный url адрес до страницы логина

            @return: полный url
            @rtype: str
        """
        return os.path.join(self.url_start, self.login_address)

    @property
    def url_transactions(self):
        """
            Свойство - полный url адрес до страницы транзакций

            @return: полный url
            @rtype: str
        """
        return os.path.join(self.url_start, self.transaction_address)

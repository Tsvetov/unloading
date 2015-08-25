# -*- coding: utf-8 -*-

# std
import os
import itertools

from requests_ipayoptions import Request

__author__ = 'cpn'


class Unloading(object):
    """
        Класс для выгрузки файла и по желанию загрузки его в фс

        пользоваться примерно так:

        >>> obj = Unloading('login', 'password')
        >>> file_iter = obj.create_unloading('2015-08-12', '2015-08-24')
        >>> print ''.join(file_iter)
        >>> obj.save_file()
    """
    def __init__(self, login, password, path_to='/tmp'):
        self.login = login
        self.password = password
        self.path_to = path_to
        self.file_iter = None
        self.date_start = None
        self.date_finish = None
        self.__file_iter = None

    def create_unloading(self, date_start, date_finish=None):
        """
        Создание выгрузки
        @param date_start: дата начала, в формате '2015-08-12'
        @type: str

        @param date_finish: дата окончания. В формате '2015-08-12'
        @type: str

        @return: итератор по файлу.
        @rtype: generator
        """
        obj = Request(self.login, self.password)
        self.file_iter, self.__file_iter = itertools.tee(
            obj.get_file(date_start, date_finish), 2
        )

        # если date_finish не определена, делаем ее == date_start
        self.date_finish = date_finish if date_finish else date_start
        self.date_start = date_start

        return self.file_iter

    def save_file(self):
        if self.__file_iter:
            full_name = os.path.join(
                self.path_to, self.generate_name_new_file()
            )
            with open(full_name, 'wb') as f:
                for it in self.__file_iter:
                    f.write(it)
            return full_name

    def generate_name_new_file(self):
        if self.date_finish == self.date_finish:
            return 'ipayoptions-{}.csv'.format(self.date_start)

        return 'ipayoptions-{}_{}.csv'.format(
            self.date_start, self.date_finish
        )
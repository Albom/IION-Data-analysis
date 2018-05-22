# Copyright © 2018 Stanislav Hnatiuk.  All rights reserved.

#!/usr/bin/env python3

import struct
import datetime
from abc import ABCMeta
from abc import abstractmethod


class BasicOperations(metaclass=ABCMeta):
    '''Базовый абстрактный класс с базовыми операциями.'''
    @abstractmethod
    def __init__(self):
        self._data = []

    def __repr__(self):
        return ', '.join(map(str, self._data))

    def __str__(self):
        return str(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __len__(self):
        return len(self._data) 


class BaseFile(BasicOperations):
    '''Базовый класс файла.'''
    def __init__(self, file_name):
        self.path = ''
        self.file_name = file_name
        try:
            self.date = datetime.datetime.strptime(self.file_name, '%d%m%y.%H%M')
        except ValueError:
            self.date = 'unknown'

    def write(self):
        '''Записать файл.'''
        with open('{}{}'.format(self.path, self.file_name), 'wt') as file:
            for item in self._data:
                file.write(item.__repr__())
                file.write('\n')

    def print(self):
        '''Вывести данные в консоль.'''
        for i in range(680):
            print(i + 1, end='\t')
            print(self._data[i])


class SFile(BaseFile):
    '''Класс для работы с S-файлами (исходные данные).'''
    class SAkf(BasicOperations):
        '''Класс для хранения значений АКФ (19 точек).'''
        def __init__(self):
            self._data = [0 for x in range(19)]

    def __init__(self, file_name):
        self._data = [SFile.SAkf() for _ in range(680)]
        super().__init__(file_name)
        self.path = 'data/'

    def encode(self):
        '''Закодировать данные. Возвращает обьект bytes.'''
        temp = bytearray([0 for x in range(12920)])
        for i, item in enumerate(self._data[0]):
            struct.pack_into('>i', temp, i * 4, item[0])
        return bytes(temp)

    @staticmethod
    def decode(arr):
        '''Раскодировать данные. Возвращает список значений.'''
        temp = [0 for _  in range(0, len(arr), 4)]
        for i in range(len(temp)):
            temp[i] = struct.unpack_from('<i', arr, i * 4)[0]
        return temp

    def read(self):
        '''Считать файл.'''
        with open('{}{}'.format(self.path, self.file_name), 'rb') as file:
            arr = self.decode(file.read())
            for i in range(680):
                for j in range(19):
                    self._data[i][j] = arr[i * 19 + j]


class FFile(BaseFile):
    '''Класс для работы с F-файлами (данные фильтрации).'''
    def __init__(self, file_name):
        self._data = [0 for _ in range(680)]
        super().__init__(file_name)
        self.path = 'filter/'

    def read(self):
        '''Считать данные.'''
        with open('{}{}'.format(self.path, self.file_name), 'rb') as file:
            arr = file.read().split()
            for i in range(680):
                self._data[i] = int(arr[i])

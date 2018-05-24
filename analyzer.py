# Copyright © 2018 Stanislav Hnatiuk.  All rights reserved.

#!/usr/bin/env python3

import os
from files import SFile
from files import FFile
from files import AFile


class Analyzer:
    '''Главный класс для работы с данными.'''
    def __init__(self):
        self.data_path = 'data/'
        self.filter_path = 'filter/'
        self.analysis_path = 'analysis/'
        self._data = []
        self._filter = []
        self._analysis = []

    def _read_data(self):
        '''Считать данные из директории по умолчанию.'''
        count_files = len(os.listdir(self.data_path))
        for file_name in os.listdir(self.data_path):
            try:
                sfile = SFile(file_name=file_name)
                sfile.read()
                self._data.append(sfile)
                print('{} read.'.format(file_name))
            except IOError:
                print('{} do not read!'.format(file_name))
        print('{} files readed.'.format(len(self._data)))
        
        error_files = count_files - len(self._data)
        if error_files:
            print('Warning: {} files do not read!'.format(error_files))
        print()

    def read_filtering(self):
        '''Считать данные фильтрации из директории по умолчанию.'''
        count_files = len(os.listdir(self.filter_path))
        for file_name in os.listdir(self.filter_path):
            try:
                ffile = FFile(file_name)
                ffile.read()
                self._filter.append(ffile)
                print('{} read.'.format(file_name))
            except IOError:
                print('{} do not read!'.format(file_name))
        print('{} files readed.'.format(len(self._filter)))
        
        error_files = count_files - len(self._filter)
        if error_files:
            print('Warning: {} files do not read!'.format(error_files))
        print()

    def _write_filtering(self):
        '''Записать данные фильтрации в дирректорию по умолчанию.'''
        for one_filter in self._filter:
            try:
                one_filter.write()
                print('{} save.'.format(one_filter.file_name))
            except IOError:
                print('{} do not save!'.format(one_filter.file_name))
        print('{} files save.'.format(len(self._filter)))
        
        error_files = len(os.listdir(self.filter_path)) - len(self._filter)
        if error_files:
            print('Warning: {} files do not save!'.format(error_files))
        print()

    def filtering(self):
        '''Фильтровать данные.'''
        self._read_data()
        self._filter = [FFile(one_data.file_name) for one_data in self._data]
        print('The first stage of filtration')
        self._make_filtering(reverse=False)
        print('The second stage of filtration')
        self._make_filtering(reverse=True)
        print('The third stage of filtration')
        self._find_coherent()

        self._write_filtering()
        self._data.clear()

    def _make_filtering(self, reverse=False):
        '''Процесс фильтрации данных с направлением.'''
        if reverse:
            direction = -1
        else:
            direction = 1
        w = 15
        lev = 4.5
        nmin = 10
        for h in range(680):
            print('\r{}%'.format(int((h + 1) * 0.147059)), end='')
            for t in range(0 if direction > 0 else len(self._filter) - 1, 
                           len(self._filter) - w - 1 if direction > 0 else w, 
                           1 if direction > 0 else -1):
                num = 0
                mean = 0.0
                for offset in range(w):
                    if self._filter[t + offset * direction][h] == 0:
                        mean += self._data[t + offset * direction][h][0]
                        num += 1
                if num >= nmin:
                    mean /= num
                    dev = 0.0
                    for offset in range(w):
                        if self._filter[t + offset * direction][h] == 0:
                            dev += (self._data[t + offset * direction][h][0] - mean) ** 2
                    dev = (dev / (num - 1)) ** 0.5
                    if abs(self._data[t + w * direction][h][0] - mean) > (lev * dev):
                        self._filter[t + w * direction][h] = self._data[t + w * direction][h][0]
        print(' completed.')

    def _find_coherent(self, wmin=21, wmax=24):
        '''Поиск когерентных отражений.'''
        def clear(num, t, h):
            '''Очистка помех не попадающих в диапазон wmin-wmax по высоте.'''
            if wmin > num or num > wmax:
                while num >= 0:
                    self._filter[t][h - num] = 0
                    num -= 1
            return 0

        num = 0
        for t in range(len(self._filter)):
            print('\r{}%'.format(int((t + 1) * (100 / len(self._filter)))), end='')
            for h in range(len(self._filter[t])):
                if self._filter[t][h] > 0:
                        num += 1
                else:
                    num = clear(num, t, h)
            else:
                num = clear(num, t, h)
                        
    def analyze(self):
        '''Анализировать данные.'''
        # За все года, по всем кварталам.
        # За квартал по всем годам.
        # self._analysis = {'0.{}'.format(n): AFile('0.{}'.format(n)) for n in range(5)}
        self._analysis = [AFile('0.{}'.format(n)) for n in range(5)]
        for i in self._analysis:
            i.write()
        # За год, по всем кварталам.
        # self._analysis['2017.0'] = AFile('2017.0')
        # # За год, за квартал
        # self._analysis.append(AFile('2017.1'))
        # self._analysis.append(AFile('2017.2'))
        # self._analysis.append(AFile('2017.3'))
        # self._analysis.append(AFile('2017.4'))
        self._make_analyze()
        self._analysis.clear()
    
    def _make_analyze(self):
        '''Процесс анализа данных.'''
        pass

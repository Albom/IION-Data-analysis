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
        self._make_filtering()
        self._write_filtering()
        self._data.clear()

    def _make_filtering(self):
        '''Процесс фильтрации данных.'''
        pass

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

import unittest
from unittest import TestCase
import random
from analyzer import Analyzer
from files import BasicOperations


class TestAnalyzer(TestCase):
    def setUp(self):
        print()
        print(self.shortDescription())
        self.an = Analyzer()

    def test_make_filtering(self):
        '''Тест фильтрации выбросов.'''
        arr = [[[random.randint(90, 110)] for _ in range(680)] for _ in range(100)]
        # Отражения попадающие под оба этапа фильтрации.
        reflection = [random.randint(15, 84) for _ in range(3)]
        # Отражение на границе, не попадающее под прямую фильтрацию.
        reflection.append(0)
        # Отражение на границе, не попадающее под обратную фильтрацию.
        reflection.append(99)
        print(reflection)
        for i in reflection:
            arr[i][200][0] = 150
        zero_arr = [[0 for _ in range(680)] for _ in range(100)]
        self.an._data = arr
        self.an._filter = zero_arr
        self.an._make_filtering(reverse=False)

        self.an._make_filtering(reverse=True)
        for i in reflection:
            self.assertTrue(self.an._filter[i][200], f'Do not filtering in {i}.')

    def test_find_coherent(self):
        '''Тест поиска когерентных отражений.'''
        # Диапазон размера отражения.
        wmin, wmax = 4, 5   
        # Строки с наличием отражения.
        rows = [1, 2, 5, 6]

        arr = []
        arr.append([1, 1, 1, 1, 1, 1, 0, 1, 0, 0])  # 6..
        arr.append([1, 1, 1, 1, 1, 0, 0, 1, 0, 0])  # 5..
        arr.append([1, 1, 1, 1, 0, 0, 0, 1, 0, 1])  # 4..
        arr.append([1, 1, 1, 0, 0, 0, 0, 1, 0, 1])  # 3..
        arr.append([0, 0, 1, 0, 1, 1, 1, 1, 1, 1])  # ..6
        arr.append([0, 0, 1, 0, 0, 1, 1, 1, 1, 1])  # ..5
        arr.append([1, 0, 0, 1, 0, 0, 1, 1, 1, 1])  # ..4
        arr.append([1, 0, 0, 1, 0, 0, 0, 1, 1, 1])  # ..3

        self.an._filter = arr
        self.an._find_coherent(wmin, wmax)
        
        for i, item in enumerate(self.an._filter):
            num = 0
            for h in item:
                if h > 0:
                    num += 1
            if num:
                self.assertTrue(wmin <= num <= wmax, f'In {i} row, finded {num}:\n{item}')
                self.assertIn(i, rows, f'Finded {num}:\n{item}')


if __name__ == '__main__':
    unittest.main()
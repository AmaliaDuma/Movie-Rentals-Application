import unittest
from newd.filtr import my_filter
from newd.data import MyData
from newd.sort import shellSort


class TestMyData(unittest.TestCase):
    def test_all(self):
        anotherl = [5, 10]
        tlist = MyData()
        self.assertEqual(len(tlist), 0)
        tlist.append(5)
        tlist.append(10)
        self.assertEqual(len(tlist), 2)
        for i in range(0, len(tlist)):
            self.assertEqual(tlist[i], anotherl[i])
        i = 0
        for nr in tlist:
            self.assertEqual(nr, anotherl[i])
            i += 1
        tlist[0] = 6
        self.assertEqual(tlist[0], 6)
        tlist.pop(1)
        self.assertEqual(len(tlist), 1)
        ttlist = tlist.get_all()
        self.assertEqual(len(ttlist), 1)


class TestFilter(unittest.TestCase):
    def test_filtr(self):
        a = [2, 4, 5, 6, 7]
        after_fil = [5, 7]
        b = my_filter(lambda x: x % 2 != 0, a)
        for i in range(0, len(b)):
            self.assertEqual(b[i], after_fil[i])

    @staticmethod
    def fun(variable):
        letters = ['a', 'e', 'i', 'o', 'u']
        if variable in letters:
            return True
        else:
            return False

    def test_filtr2(self):
        sequence = ['g', 'e', 'a', 'j', 'k', 's', 'p', 'r']
        after_fil = ['e', 'a']
        filtered = my_filter(self.fun, sequence)
        for i in range(0, len(filtered)):
            self.assertEqual(filtered[i], after_fil[i])


class TestSort(unittest.TestCase):
    def test_sort(self):
        arr = [[12, 2], [55, 9], [32, 5]]
        arr_s = [[55, 9],[32, 5], [12, 2]]
        new_arr = shellSort(arr, lambda x, y: x[1] < y[1])
        for i in range(0, len(new_arr)):
            self.assertEqual(new_arr[i], arr_s[i])

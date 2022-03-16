import unittest
from datetime import date, timedelta

from domain.entity import Movie, Mexceptions, Client, CException, Rental, RException, RDays
from repo.rep import MovieR, ClientR, RentalR
from services.sv import Movies, Clients, Rentals
from services.undo_sv import UndoService, FunctionCall, Operation


class MoviesTest(unittest.TestCase):
    def setUp(self):
        self.a = MovieR()
        self.ur = UndoService()
        self._movies = Movies(self.a, self.ur)
        m1 = Movie(15, 'M1', 'D1', 'comedy')
        self._movies.add(m1)
        b = self._movies.get_list()

    def test_add(self):
        self.assertEqual(len(self._movies), 1)
        m2 = Movie(16, 'M1', 'D2', 'comedy')
        self._movies.add(m2, 1)
        self.assertEqual(len(self._movies), 2)
        m1 = Movie(15, 'M1', 'D1', 'comedy')
        self.assertRaises(Mexceptions, self._movies.add, m1)
        self.ur.undo()
        self.assertEqual(len(self._movies), 1)
        self.assertEqual(self.ur.undo(), False)
        self.ur.redo()
        self.assertEqual(len(self._movies), 2)
        self.assertEqual(self.ur.redo(), False)
        m4 = Movie(18, 'M3', 'D4', 'horror')
        self._movies.add(m4, 1)
        self.ur.undo()
        m3 = Movie(18, 'M7', 'D2', 'comedy')
        self._movies.add(m3, 1)
        self.assertEqual(len(self._movies), 3)
        self.ur.undo()
        self.ur.undo()
        self.ur.undo()
        self.assertEqual(self.ur.undo(), False)


    def test_check(self):
        self.assertEqual(self._movies.check_exists_id(15), 1)
        self.assertEqual(self._movies.check_exists_id(16), 0)

    def test_generate(self):
        self._movies.generate()
        self.assertEqual(len(self._movies), 11)

    def test_remove(self):
        self._movies.remove(15, 1)
        self.assertEqual(len(self._movies), 0)

    def test_update(self):
        self._movies.update(15, 'title', 'M11', 1)
        self.assertEqual(self.a[0].title, 'M11')
        self._movies.update(15, 'description', 'D2', 1)
        self.assertEqual(self.a[0].desc, 'D2')
        self._movies.update(15, 'genre', 'G2', 1)
        self.assertEqual(self.a[0].gen, 'G2')
        self.assertRaises(Mexceptions, self._movies.update, 11, 'title', 'T1')

    def test_search(self):
        l_ret = self._movies.search('id', '15')
        self.assertEqual(len(l_ret), 1)
        l_ret = self._movies.search('title', 'm')
        self.assertEqual(len(l_ret), 1)
        l_ret = self._movies.search('description', 'D')
        self.assertEqual(len(l_ret), 1)
        l_ret = self._movies.search('genre', 'comed')
        self.assertEqual(len(l_ret), 1)


class ClientsTest(unittest.TestCase):
    def setUp(self):
        self.a = ClientR()
        self.ur = UndoService()
        self._clients = Clients(self.a, self.ur)
        c1 = Client(111, 'Andrei')
        self._clients.add(c1)
        b = self._clients.get_list()

    def test_add(self):
        c1 = Client(111, 'Andrei')
        self.assertEqual(len(self._clients), 1)
        c2 = Client(121, 'Ana')
        self._clients.add(c2,1)
        self.assertEqual(len(self._clients), 2)
        self.assertRaises(CException, self._clients.add, c1)

    def test_generate(self):
        self._clients.generate()
        self.assertEqual(len(self._clients), 11)

    def test_check(self):
        c1 = Client(111, 'Andrei')
        self.assertEqual(self._clients.check_exists_id(111), 1)
        self.assertEqual(self._clients.check_exists_id(112), 0)
        self.assertEqual(self._clients.check_exists(c1), 1)

    def test_remove(self):
        self._clients.remove(111, 1)
        self.assertEqual(len(self._clients), 0)

    def test_update(self):
        self._clients.update(111, 'Ana', 1)
        self.assertEqual(self.a[0].name, 'Ana')
        self.assertRaises(CException, self._clients.update, 112, 'a')

    def test_search(self):
        l_ret = self._clients.search('id', '111')
        self.assertEqual(len(l_ret), 1)
        l_ret = self._clients.search('name', 'Andrei')
        self.assertEqual(len(l_ret), 1)


class RentalTest(unittest.TestCase):
    def setUp(self):
        self.c = ClientR()
        self.ur = UndoService()
        self._clients = Clients(self.c, self.ur)
        c1 = Client(111, 'Andrei')
        c2 = Client(112, 'Ana')
        c3 = Client(110, 'Ion')
        c4 = Client(113, 'Dana')
        self._clients.add(c1)
        self._clients.add(c2)
        self._clients.add(c3)
        self._clients.add(c4)
        self.m = MovieR()
        self._movies = Movies(self.m, self.ur)
        m1 = Movie(15, 'M1', 'D1', 'comedy')
        m2 = Movie(16, 'M2', 'D2', 'comedy')
        m3 = Movie(17, 'M3', 'D3', 'comedy')
        m4 = Movie(18, 'M4', 'D4', 'comedy')
        self._movies.add(m1)
        self._movies.add(m2)
        self._movies.add(m3)
        self._movies.add(m4)
        self.a = RentalR()
        self._rentals = Rentals(self.a, self._movies, self._clients, self.ur)
        self.assertEqual(len(self._rentals), 0)

    def test_generate(self):
        self._rentals.generate()
        listr = self._rentals.get_rentals()
        self.assertEqual(len(listr), 10)

    def test_search(self):
        self._rentals.generate()
        check = self._rentals.search_available(15)
        self.assertEqual(check, 1)
        check = self._rentals.search_client_rmovie(113)
        self.assertEqual(check, 1)

    def test_rent(self):
        date1 = date(2020, 5, 12)
        self.assertRaises(RException, self._rentals.rent_movie, 303, 12, 111, date1)
        self.assertRaises(RException, self._rentals.rent_movie, 303, 15, 107, date1)
        self._rentals.rent_movie(303, 15, 112, date1, 1)
        self.assertRaises(RException, self._rentals.rent_movie, 303, 15, 112, date1)
        self.assertRaises(RException, self._rentals.rent_movie, 303, 18, 110, date1)
        check = self._rentals.search_available(15)
        self.assertEqual(check, 0)
        check = self._rentals.check_exist_id(303)
        self.assertEqual(check, 1)
        check = self._rentals.check_exist_id(302)
        self.assertEqual(check, 0)
        self.assertRaises(RException, self._rentals.rent_movie, 305, 15, 107, date1)
        self.assertRaises(RException, self._rentals.rent_movie, 303, 15, 107, date1)
        self._rentals.delete_r(303)
        self.assertEqual(len(self._rentals), 0)

    def test_retur(self):
        date1 = date(2020, 5, 12)
        self._rentals.rent_movie(303, 15, 112, date1)
        self.assertRaises(RException, self._rentals.retur_movie, 455, date1)
        date2 = date(2020, 7, 2)
        self._rentals.retur_movie(303, date2, 1)
        self.assertRaises(RException, self._rentals.rent_movie, 317, 17, 112, date1)
        check = self._rentals.search_client_rmovie(112)
        self.assertEqual(check, 0)
        r1 = Rental(303, 15, 112, date1, date1, '')
        check = self._rentals.check_exist(r1)
        self.assertEqual(check, 1)
        self.assertRaises(RException, self._rentals.retur_movie, 303, date2)

    def test_st2(self):
        self._rentals.generate()
        list_sort = self._rentals.rent_c_days()
        for obj in list_sort:
            self.assertIsInstance(obj, RDays)
        final_l = self._rentals.get_statistic2()
        count = 0
        for obj in final_l:
            client = obj[0]
            self.assertIsInstance(client[0], Client)
            if count == 0:
                maxim = obj[1]
                count += 1
            else:
                self.assertGreaterEqual(maxim, obj[1])

    def test_st1(self):
        self._rentals.generate()
        list_sort = self._rentals.rent_days()
        for obj in list_sort:
            self.assertIsInstance(obj, RDays)
        final_l = self._rentals.get_statistic1()
        count = 0
        for obj in final_l:
            movie = obj[0]
            self.assertIsInstance(movie[0], Movie)
            if count == 0:
                maxim = obj[1]
                count += 1
            else:
                self.assertGreaterEqual(maxim, obj[1])

    def test_st3(self):
        d_today = date.today()
        date1 = date(2020, 8, 12)
        self._rentals.rent_movie(303, 15, 112, date1)
        date2 = date1 + timedelta(days=30)
        list_sort = self._rentals.late_r()
        self.assertEqual(len(list_sort), 1)
        date3 = d_today - date2
        for obj in list_sort:
            self.assertEqual(obj.mid, 15)
            self.assertEqual(obj.days, date3.days)
        final_l = self._rentals.get_statistic3()
        for obj in final_l:
            movie = obj[0]
            self.assertIsInstance(movie[0], Movie)
            self.assertEqual(movie[0].mid, 15)
            self.assertEqual(obj[1], date3.days)

class Function_Call_Test(unittest.TestCase):

    def add(self, a, b):
        return a+b

    def sub(self, a, b):
        return a-b

    def test_add_sub(self):
        f1 = FunctionCall(self.add, 2, 3)
        result = f1()
        self.assertEqual(result, 5)
        f2 = FunctionCall(self.sub, 3, 2)
        result = f2()
        self.assertEqual(result, 1)
        op = Operation(f1, f2)




import unittest
from datetime import date

from domain.entity import Movie, Mexceptions, Client, CException, Rental, RException
from repo.rep import MovieR, ClientR, RentalR


class MovieRTest(unittest.TestCase):
    def setUp(self):
        self._repom = MovieR()
        m1 = Movie(15, 'M1', 'D1', 'comedy')
        self._repom.add_movie(m1)

    def test_add(self):
        self.assertEqual(len(self._repom), 1)
        m2 = Movie(17, 'M2', 'D2', 'comedy')
        self._repom.add_movie(m2)
        self.assertEqual(len(self._repom), 2)
        self.assertRaises(Mexceptions, self._repom.add_movie, 5)

    def test_remove_id(self):
        self._repom.remove_movie_id(15)
        self.assertEqual(len(self._repom), 0)
        self.assertRaises(Mexceptions, self._repom.remove_movie_id, 15)


class ClientRTest(unittest.TestCase):
    def setUp(self):
        self._repoc = ClientR()
        c1 = Client(111, 'Andrei')
        self._repoc.add_client(c1)

    def test_add(self):
        self.assertEqual(len(self._repoc), 1)
        c2 = Client(151, 'Ana')
        self._repoc.add_client(c2)
        self.assertEqual(len(self._repoc), 2)
        self.assertRaises(CException, self._repoc.add_client, 5)

    def test_remove_id(self):
        self._repoc.remove_client_id(111)
        self.assertEqual(len(self._repoc), 0)
        self.assertRaises(CException, self._repoc.remove_client_id, 111)


class RentalRTest(unittest.TestCase):

    def setUp(self):
        self._repor = RentalR()
        r1 = Rental(455, 51, 105, date(2020, 5, 10), date(2020, 5, 12), date(2020, 6, 12))
        self._repor.add_rental(r1)

    def test_add(self):
        self.assertEqual(len(self._repor), 1)
        r2 = Rental(356, 57, 105, date(2020, 5, 10), date(2020, 5, 12), date(2020, 6, 12))
        self._repor.add_rental(r2)
        self.assertEqual(len(self._repor), 2)
        self.assertRaises(RException, self._repor.add_rental, 4)

    def test_remove(self):
        r1 = Rental(455, 51, 105, date(2020, 5, 10), date(2020, 5, 12), date(2020, 6, 12))
        self.assertRaises(RException, self._repor.remove_rental, r1)

        self.assertEqual(len(self._repor), 1)
        self.assertRaises(RException, self._repor.remove_rental, r1)
        self.assertRaises(RException, self._repor.remove_rental, 4)

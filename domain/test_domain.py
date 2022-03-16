import unittest
from datetime import date
from domain.entity import Movie, Client, Rental, Mexceptions, CException, RException, RDays


class MovieTest(unittest.TestCase):
    def test_movie(self):
        m1 = Movie(15, 'M1', 'D1', 'comedy')
        self.assertEqual(m1.title, 'M1')
        self.assertEqual(m1.mid, 15)
        self.assertEqual(m1.desc, 'D1')
        self.assertEqual(m1.gen, 'comedy')
        string = str(m1)
        self.assertEqual(string, 'ID: 15 title: M1 description: D1 genre: comedy')
        m1.title = 'M2'
        self.assertEqual(m1.title, 'M2')
        m1.mid = 12
        m1.desc = 'D3'
        m1.gen = 'G1'
        self.assertEqual(m1.mid, 12)
        self.assertEqual(m1.desc, 'D3')
        self.assertEqual(m1.gen, 'G1')
        self.assertRaises(Mexceptions, Movie, 5, 'M1', 'D1', 'comedy')


class ClientTest(unittest.TestCase):
    def test_client(self):
        c1 = Client(111, 'Andrei')
        self.assertEqual(c1.clid, 111)
        self.assertEqual(c1.name, 'Andrei')
        string = str(c1)
        self.assertEqual(string, 'ID: 111 name: Andrei')
        c1.clid = 112
        c1.name = 'Ana'
        self.assertEqual(c1.clid, 112)
        self.assertEqual(c1.name, 'Ana')
        self.assertRaises(CException, Client, 85, 'Ana')


class RentalTest(unittest.TestCase):
    def test_rental(self):
        r1 = Rental(455, 51, 105, date(2020, 5, 10), date(2020, 5, 12), date(2020, 6, 12))
        self.assertEqual(r1.rid, 455)
        self.assertEqual(r1.movieid, 51)
        self.assertEqual(r1.clientid, 105)
        self.assertEqual(r1.rentdate, date(2020, 5, 10))
        self.assertEqual(r1.duedate, date(2020, 5, 12))
        self.assertEqual(r1.retdate, date(2020, 6, 12))
        string = str(r1)
        self.assertEqual(string, 'ID: 455 movie ID: 51 client ID: 105' +
                         '\n'
                         + 'rent date: 2020-05-10 due date: 2020-05-12 returned date: 2020-06-12')
        self.assertRaises(RException, Rental, 200, 111, 12, date(2020, 5, 10), date(2020, 5, 12), date(2020, 6, 12))
        self.assertRaises(RException, Rental, 355, 11, 12, date(2020, 5, 10), date(2020, 5, 12), date(2020, 6, 12))
        self.assertRaises(RException, Rental, 355, 111, 155, date(2020, 5, 10), date(2020, 5, 12), date(2020, 6, 12))
        self.assertRaises(RException, Rental, 355, 11, 121, 5, 10, date(2020, 6, 12))
        self.assertRaises(RException, Rental, 355, 11, 151, date(2020, 5, 10), date(2020, 5, 12), 5)
        r2 = Rental(455, 51, 105, date(2020, 5, 10), date(2020, 5, 12), '')
        r2.retdate = date(2020, 5, 6)

class RDaysTest(unittest.TestCase):
    def test_r(self):
        r1 = RDays(55, 15)
        self.assertEqual(r1.mid, 55)
        self.assertEqual(r1.days, 15)
        r1.days = 12
        self.assertEqual(r1.days, 12)


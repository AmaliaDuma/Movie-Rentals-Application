from datetime import date

from domain.entity import Mexceptions, Movie, CException, Client, RException, Rental
from repo.rep import MovieR, ClientR, RentalR
import pickle


class MovieRB(MovieR):
    def __init__(self, file_name):
        MovieR.__init__(self)
        self._file_name = file_name
        try:
            self._load_file()
        except:
            self._ini_file()
            self._load_file()

    def _load_file(self):
        try:
            f = open(self._file_name, 'rb')
        except IOError:
            raise Mexceptions('Input file not found')
        movies = pickle.load(f)
        for movie in movies:
            MovieR.add_movie(self, movie)
        f.close()

    def _ini_file(self):
        movies = [Movie(12, 'T1', 'D1', 'G1'), Movie(15, 'T2', 'D2', 'G2'), Movie(22, 'T3', 'D3', 'G3'),
                  Movie(67, 'T4', 'D4', 'G4'), Movie(34, 'T2', 'D5', 'G5'), Movie(47, 'T5', 'D6', 'G6')]
        f = open(self._file_name, 'wb')
        pickle.dump(movies, f)
        f.close()

    def save_file(self):
        f = open(self._file_name, 'wb')
        m_list = MovieR.get_all(self)
        pickle.dump(m_list, f)
        f.close()

    def add_movie(self, movie):
        MovieR.add_movie(self, movie)
        self.save_file()

    def remove_movie_id(self, movieid):
        MovieR.remove_movie_id(self, movieid)
        self.save_file()


class ClientRB(ClientR):
    def __init__(self, file_name):
        ClientR.__init__(self)
        self._file_name = file_name
        try:
            self._load_file()
        except:
            self._ini_file()
            self._load_file()

    def _load_file(self):
        try:
            f = open(self._file_name, 'rb')
        except IOError:
            raise CException('Input file not found')
        clients = pickle.load(f)
        for client in clients:
            ClientR.add_client(self, client)
        f.close()

    def _ini_file(self):
        clients = [Client(152, 'N1'), Client(199, 'N2'), Client(251, 'N7'), Client(102, 'N4'),
                   Client(221, 'N3'), Client(127, 'N5')]
        f = open(self._file_name, 'wb')
        pickle.dump(clients, f)
        f.close()

    def save_file(self):
        f = open(self._file_name, 'wb')
        c_list = ClientR.get_all(self)
        pickle.dump(c_list, f)
        f.close()

    def add_client(self, client):
        ClientR.add_client(self, client)
        self.save_file()

    def remove_client_id(self, clientid):
        ClientR.remove_client_id(self, clientid)
        self.save_file()


class RentalRB(RentalR):
    def __init__(self, file_name):
        RentalR.__init__(self)
        self._file_name = file_name
        try:
            self._load_file()
        except:
            self._ini_file()
            self._load_file()

    def _load_file(self):
        try:
            f = open(self._file_name, 'rb')
        except IOError:
            raise RException('Input file not found')
        rentals = pickle.load(f)
        for rental in rentals:
            RentalR.add_rental(self, rental)
        f.close()

    def _ini_file(self):
        rentals = [Rental(341, 67, 152, date(2020, 1, 6), date(2020, 2, 5), date(2020, 1, 11)),
                   Rental(301, 15, 127, date(2020, 8, 6), date(2020, 9, 5), date(2020, 8, 13)),
                   Rental(444, 12, 199, date(2020, 5, 3), date(2020, 6, 2), date(2020, 5, 6)),
                   Rental(317, 22, 251, date(2020, 9, 10), date(2020, 10, 10), date(2020, 9, 16))]
        f = open(self._file_name, 'wb')
        pickle.dump(rentals, f)
        f.close()

    def save_file(self):
        f = open(self._file_name, 'wb')
        r_list = RentalR.get_all(self)
        pickle.dump(r_list, f)
        f.close()

    def add_rental(self, rental):
        RentalR.add_rental(self, rental)
        self.save_file()

    def remove_rental(self, rid):
        RentalR.remove_rental(self, rid)
        self.save_file()
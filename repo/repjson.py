import json
from datetime import date
from domain.entity import Mexceptions, Movie, CException, Client, Rental
from repo.rep import MovieR, ClientR, RentalR


class MovieRJ(MovieR):
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
        with open(self._file_name, 'r') as handle:
            movies = [json.loads(line) for line in handle]
        for i in range(0, len(movies)):
            mv = Movie(movies[i]['_mid'], movies[i]['_title'], movies[i]['_desc'], movies[i]['_gen'])
            MovieR.add_movie(self, mv)

    def _ini_file(self):
        movies = [Movie(12, 'T1', 'D1', 'G1'), Movie(15, 'T2', 'D2', 'G2'), Movie(22, 'T3', 'D3', 'G3'),
                  Movie(67, 'T4', 'D4', 'G4'), Movie(34, 'T2', 'D5', 'G5'), Movie(47, 'T5', 'D6', 'G6')]
        f = open(self._file_name, 'w')
        for movie in movies:
            json.dump(vars(movie), f)
            f.write('\n')
        f.close()

    def save_file(self):
        f = open(self._file_name, 'w')
        m_list = MovieR.get_all(self)
        for movie in m_list:
            json.dump(vars(movie), f)
            f.write('\n')
        f.close()

    def add_movie(self, movie):
        MovieR.add_movie(self, movie)
        self.save_file()

    def remove_movie_id(self, movieid):
        MovieR.remove_movie_id(self, movieid)
        self.save_file()


class ClientRJ(ClientR):
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
        with open(self._file_name, 'r') as handle:
            clients = [json.loads(line) for line in handle]
        for i in range(0, len(clients)):
            cl = Client(clients[i]['_clid'], clients[i]['_name'])
            ClientR.add_client(self, cl)
        f.close()

    def _ini_file(self):
        clients = [Client(152, 'N1'), Client(199, 'N2'), Client(251, 'N7'), Client(102, 'N4'),
                   Client(221, 'N3'), Client(127, 'N5')]
        f = open(self._file_name, 'w')
        for client in clients:
            json.dump(vars(client), f)
            f.write('\n')
        f.close()

    def save_file(self):
        f = open(self._file_name, 'w')
        c_list = ClientR.get_all(self)
        for client in c_list:
            json.dump(vars(client), f)
            f.write('\n')
        f.close()

    def add_client(self, client):
        ClientR.add_client(self, client)
        self.save_file()

    def remove_client_id(self, clientid):
        ClientR.remove_client_id(self, clientid)
        self.save_file()


class RentalRJ(RentalR):
    def __init__(self, file_name):
        RentalR.__init__(self)
        self._file_name = file_name
        self._load_file()

    def encode(self, rental):
        if rental.retdate == '':
            mydict = {
                '_rid': rental.rid,
                '_movieid': rental.movieid,
                '_clientid': rental.clientid,
                '_y1': rental.rentdate.year,
                '_m1': rental.rentdate.month,
                '_d1': rental.rentdate.day,
                '_y2': rental.duedate.year,
                '_m2': rental.duedate.month,
                '_d2': rental.duedate.day,
                '_y3': '',
                '_retdate': ''
            }
        else:
            mydict = {
                '_rid': rental.rid,
                '_movieid': rental.movieid,
                '_clientid':  rental.clientid,
                '_y1': rental.rentdate.year,
                '_m1': rental.rentdate.month,
                '_d1': rental.rentdate.day,
                '_y2': rental.duedate.year,
                '_m2': rental.duedate.month,
                '_d2': rental.duedate.day,
                '_y3': rental.retdate.year,
                '_m3': rental.retdate.month,
                '_d3': rental.retdate.day,
            }
        return mydict

    def _load_file(self):
        try:
            f = open(self._file_name, 'rb')
        except IOError:
            raise CException('Input file not found')
        with open(self._file_name, 'r') as handle:
            rentals = [json.loads(line) for line in handle]
        for i in range(0, len(rentals)):
            date1 = date(rentals[i]['_y1'], rentals[i]['_m1'], rentals[i]['_d1'])
            date2 = date(rentals[i]['_y2'], rentals[i]['_m2'], rentals[i]['_d2'])
            if rentals[i]['_y3'] == '':
                date3 = ''
            else:
                date3 = date(rentals[i]['_y3'], rentals[i]['_m3'], rentals[i]['_d3'])
            rr = Rental(rentals[i]['_rid'], rentals[i]['_movieid'], rentals[i]['_clientid'], date1, date2, date3)
            RentalR.add_rental(self, rr)
        f.close()

    def _ini_file(self):
        rentals = [Rental(341, 67, 152, date(2020, 1, 6), date(2020, 2, 5), date(2020, 1, 11)),
                   Rental(301, 15, 127, date(2020, 8, 6), date(2020, 9, 5), date(2020, 8, 13)),
                   Rental(444, 12, 199, date(2020, 5, 3), date(2020, 6, 2), date(2020, 5, 6)),
                   Rental(317, 22, 251, date(2020, 9, 10), date(2020, 10, 10), date(2020, 9, 16))]
        f = open(self._file_name, 'w')
        for rental in rentals:
            json.dump(self.encode(rental), f)
            f.write('\n')
        f.close()

    def save_file(self):
        f = open(self._file_name, 'w')
        r_list = RentalR.get_all(self)
        for rental in r_list:
            json.dump(self.encode(rental), f)
            f.write('\n')
        f.close()

    def add_rental(self, rental):
        RentalR.add_rental(self, rental)
        self.save_file()

    def remove_rental(self, rid):
        RentalR.remove_rental(self, rid)
        self.save_file()

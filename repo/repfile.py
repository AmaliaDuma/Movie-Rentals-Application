from datetime import date

from domain.entity import Mexceptions, Movie, CException, Client, RException, Rental
from repo.rep import MovieR, ClientR, RentalR


class MovieRF(MovieR):
    def __init__(self, file_name):
        MovieR.__init__(self)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        try:
            f = open(self._file_name, 'r')
        except IOError:
            raise Mexceptions('Input file not found')

        line = f.readline().strip()
        while line != "":
            attrs = line.split(";")
            movie = Movie(int(attrs[0]), attrs[1], attrs[2], attrs[3])
            MovieR.add_movie(self, movie)
            line = f.readline().strip()
        f.close()

    def save_file(self):
        f = open(self._file_name, 'w')
        m_list = MovieR.get_all(self)
        for movie in m_list:
            string = str(movie.mid) + ';' + movie.title + ';' + movie.desc + ';' + movie.gen + '\n'
            f.write(string)
        f.close()

    def add_movie(self, movie):
        MovieR.add_movie(self, movie)
        self.save_file()

    def remove_movie_id(self, movieid):
        MovieR.remove_movie_id(self, movieid)
        self.save_file()


class ClientRF(ClientR):
    def __init__(self, file_name):
        ClientR.__init__(self)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        try:
            f = open(self._file_name, 'r')
        except IOError:
            raise CException('Input file not found')

        line = f.readline().strip()
        while line != "":
            attrs = line.split(";")
            client = Client(int(attrs[0]), attrs[1])
            ClientR.add_client(self, client)
            line = f.readline().strip()
        f.close()

    def save_file(self):
        f = open(self._file_name, 'w')
        c_list = ClientR.get_all(self)
        for client in c_list:
            string = str(client.clid) + ';' + client.name + '\n'
            f.write(string)
        f.close()

    def add_client(self, client):
        ClientR.add_client(self, client)
        self.save_file()

    def remove_client_id(self, clientid):
        ClientR.remove_client_id(self, clientid)
        self.save_file()


class RentalRF(RentalR):
    def __init__(self, file_name):
        RentalR.__init__(self)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        try:
            f = open(self._file_name, 'r')
        except IOError:
            raise RException('Input file not found')

        line = f.readline().strip()
        while line != "":
            attrs = line.split(";")
            date_a = attrs[3].split('-')
            date1 = date(int(date_a[0]), int(date_a[1]), int(date_a[2]))
            date_a = attrs[4].split('-')
            date2 = date(int(date_a[0]), int(date_a[1]), int(date_a[2]))
            if attrs[5] != '':
                date_a = attrs[5].split('-')
                date3 = date(int(date_a[0]), int(date_a[1]), int(date_a[2]))
            else:
                date3 = ''
            rental = Rental(int(attrs[0]), int(attrs[1]), int(attrs[2]), date1, date2, date3)
            RentalR.add_rental(self, rental)
            line = f.readline().strip()
        f.close()

    def save_file(self):
        f = open(self._file_name, 'w')
        r_list = RentalR.get_all(self)
        for rental in r_list:
            if rental.retdate == '':
                string = str(rental.rid) + ';' + str(rental.movieid) +\
                     ';' + str(rental.clientid) + ';' + str(rental.rentdate) + \
                     ';' + str(rental.duedate) + '' + '\n'
            else:
                string = str(rental.rid) + ';' + str(rental.movieid) +\
                     ';' + str(rental.clientid) + ';' + str(rental.rentdate) + \
                     ';' + str(rental.duedate) + ';' + str(rental.retdate) + '\n'
            f.write(string)
        f.close()

    def add_rental(self, rental):
        RentalR.add_rental(self, rental)
        self.save_file()

    def remove_rental(self, rid):
        RentalR.remove_rental(self, rid)
        self.save_file()
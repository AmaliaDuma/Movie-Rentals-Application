import sqlite3
from datetime import datetime

from domain.entity import Movie, Client, Rental
from repo.rep import MovieR, ClientR, RentalR


class MovieRDB(MovieR):
    def __init__(self, file_name):
        MovieR.__init__(self)
        self._file_name = file_name
        self._load()

    def _load(self):
        con = sqlite3.connect(self._file_name)
        cursor = con.cursor()
        for item in cursor.execute('SELECT * FROM movies'):
            MovieR.add_movie(self, Movie(*item))
        con.close()

    def add_movie(self, movie):
        MovieR.add_movie(self, movie)
        con = sqlite3.connect(self._file_name)
        cursor = con.cursor()
        entities = (movie.mid, movie.title, movie.desc, movie.gen)
        cursor.execute('INSERT INTO movies(id, title, description, genre) VALUES(?, ?, ?, ?)', entities)
        con.commit()
        con.close()

    def remove_movie_id(self, movieid):
        MovieR.remove_movie_id(self, movieid)
        con = sqlite3.connect(self._file_name)
        cursor = con.cursor()
        cursor.execute('DELETE FROM movies WHERE id=?', (movieid,))
        con.commit()
        con.close()


class ClientRDB(ClientR):
    def __init__(self, file_name):
        ClientR.__init__(self)
        self._file_name = file_name
        self._load()

    def _load(self):
        con = sqlite3.connect(self._file_name)
        cursor = con.cursor()
        for item in cursor.execute('SELECT * FROM clients'):
            ClientR.add_client(self, Client(*item))
        con.close()

    def add_client(self, client):
        ClientR.add_client(self, client)
        con = sqlite3.connect(self._file_name)
        cursor = con.cursor()
        entities = (client.clid, client.name)
        cursor.execute('INSERT INTO clients(id, name) VALUES(?, ?)', entities)
        con.commit()
        con.close()

    def remove_client_id(self, clientid):
        ClientR.remove_client_id(self, clientid)
        con = sqlite3.connect(self._file_name)
        cursor = con.cursor()
        cursor.execute('DELETE FROM clients WHERE id=?', (clientid,))
        con.commit()
        con.close()

class RentalRDB(RentalR):
    def __init__(self, file_name):
        RentalR.__init__(self)
        self._file_name = file_name
        self._load()

    def _load(self):
        con = sqlite3.connect(self._file_name)
        cursor = con.cursor()
        for item in cursor.execute('SELECT * FROM rentals'):
            rent_date = datetime.strptime(item[3], '%Y-%m-%d').date()
            due_date = datetime.strptime(item[4], '%Y-%m-%d').date()
            if item[5] == 'None':
                ret_date = ''
            else:
                ret_date = datetime.strptime(item[5], '%Y-%m-%d').date()
            RentalR.add_rental(self, Rental(item[0], item[1], item[2], rent_date, due_date, ret_date))
        con.close()

    def add_rental(self, rental):
        RentalR.add_rental(self, rental)
        con = sqlite3.connect(self._file_name)
        cursor = con.cursor()
        entities = (rental.rid, rental.movieid, rental.clientid, str(rental.rentdate), str(rental.duedate), str(rental.retdate))
        cursor.execute('INSERT INTO rentals(id, movie_id, client_id, rent_date, due_date, return_date) VALUES(?, ?, ?, ?, ?, ?)', entities)
        con.commit()
        con.close()
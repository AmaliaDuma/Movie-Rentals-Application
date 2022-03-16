import sqlite3

from domain.entity import Movie, Mexceptions, Client, CException, Rental, RException, RDays
from random import randint, choice
from datetime import date, timedelta
from newd.sort import shellSort
from services.undo_sv import FunctionCall, Operation


class Rentals:

    def __init__(self, rental, movies, clients, undo_sv):
        self._rentals = rental
        self._movies = movies
        self._clients = clients
        self._undo_sv = undo_sv

    def __len__(self):
        return len(self._rentals)

    @staticmethod
    def check_exist_mdays(value, listr):
        for i in range(0, len(listr)):
            if listr[i].mid == value.mid:
                return 0
        return 1

    @staticmethod
    def update_days(value, listr):
        for i in range(0, len(listr)):
            if listr[i].mid == value.mid:
                listr[i].days = listr[i].days + value.days
                break

    def get_statistic1(self):
        final = []
        list_r = self.rent_days()
        for i in range(0, len(list_r)):
            elem = self._movies.search('id', str(list_r[i].mid))
            if len(elem) != 0:
                final.append([elem, list_r[i].days])
        return final

    def get_statistic2(self):
        final = []
        list_r = self.rent_c_days()
        for i in range(0, len(list_r)):
            elem = self._clients.search('id', str(list_r[i].mid))
            if len(elem) != 0:
                final.append([elem, list_r[i].days])
        return final

    def get_statistic3(self):
        final = []
        list_r = self.late_r()
        for i in range(0, len(list_r)):
            elem = self._movies.search('id', str(list_r[i].mid))
            if len(elem) != 0:
                final.append([elem, list_r[i].days])
        return final

    def late_r(self):
        list_rent_days = []
        d_today = date.today()
        for i in range(0, len(self._rentals)):
            if d_today > self._rentals[i].duedate and self._rentals[i].retdate == '':
                delta = d_today - self._rentals[i].duedate
                mdays = RDays(self._rentals[i].movieid, delta.days)
                if self.check_exist_mdays(mdays, list_rent_days) == 1:
                    list_rent_days.append(mdays)
        list_rent_sort = shellSort(list_rent_days, lambda x, y: x.days > y.days)
        return list_rent_sort

    def rent_days(self):
        list_rent_days = []
        for i in range(0, len(self._rentals)):
            if self._rentals[i].retdate != '':
                delta = self._rentals[i].retdate - self._rentals[i].rentdate
                mdays = RDays(self._rentals[i].movieid, delta.days)
                if self.check_exist_mdays(mdays, list_rent_days) == 1:
                    list_rent_days.append(mdays)
                else:
                    self.update_days(mdays, list_rent_days)
        list_rent_sort = shellSort(list_rent_days, key=lambda x, y: x.days > y.days)
        return list_rent_sort

    def rent_c_days(self):
        list_rent_days = []
        for i in range(0, len(self._rentals)):
            if self._rentals[i].retdate != '':
                delta = self._rentals[i].retdate - self._rentals[i].rentdate
                mdays = RDays(self._rentals[i].clientid, delta.days)
                if self.check_exist_mdays(mdays, list_rent_days) == 1:
                    list_rent_days.append(mdays)
                else:
                    self.update_days(mdays, list_rent_days)
        list_rent_sort = shellSort(list_rent_days, lambda x, y: x.days > y.days)
        return list_rent_sort

    def retur_movie(self, rentid, dater, check=None, sql=None):
        if self.check_exist_id(rentid) == 0:
            raise RException('Rental not found!')
        if check == 1:
            undo = FunctionCall(self.set_return_date, rentid, '', 1)
            redo = FunctionCall(self.retur_movie, rentid, dater)
            op = Operation(undo, redo)
            self._undo_sv.record(op)
        if sql == 1:
            self.set_return_date(rentid, dater, 0, 1)
        else:
            self.set_return_date(rentid, dater)
        try:
            self._rentals.save_file()
        except:
            pass

    def delete_r(self, rentid):
        self._rentals.remove_rental(rentid)

    def rent_movie(self, rentid, movieid, clientid, dater, check=None):
        if self._movies.check_exists_id(movieid) == 0:
            raise RException('Movie not found!')
        if self._clients.check_exists_id(clientid) == 0:
            raise RException('Client not found!')
        if self.search_available(movieid) == 0:
            raise RException('Movie not available!')
        if self.search_client_rmovie(clientid) == 0:
            raise RException('This client can not rent movies!')
        if check == 1:
            undo = FunctionCall(self.delete_r, rentid)
            redo = FunctionCall(self.rent_movie, rentid, movieid, clientid, dater)
            op = Operation(undo, redo)
        date2 = timedelta(days=30)
        new_rental = Rental(rentid, movieid, clientid, dater, dater+date2, '')
        if self.check_exist(new_rental) == 1:
            raise RException('Rental already exists!')
        self._rentals.add_rental(new_rental)
        if check == 1:
            self._undo_sv.record(op)

    def search_client_rmovie(self, cid):
        for i in range(0, len(self._rentals)):
            if self._rentals[i].clientid == cid:
                if self._rentals[i].duedate < self._rentals[i].retdate:
                    return 0
        return 1

    def search_available(self, mvid):
        for i in range(0, len(self._rentals)):
            if self._rentals[i].movieid == mvid:
                if self._rentals[i].retdate == '':
                    return 0
        return 1

    def check_exist(self, rental):
        for i in range(0, len(self._rentals)):
            if self._rentals[i].rid == rental.rid:
                return 1
        return 0

    def check_exist_id(self, rentalid):
        for i in range(0, len(self._rentals)):
            if self._rentals[i].rid == rentalid:
                return 1
        return 0

    def set_return_date(self, rentalid, dater, check=None, sq=None):
        for i in range(0, len(self._rentals)):
            if self._rentals[i].rid == rentalid:
                if check == 1:
                    self._rentals[i].retdate = dater
                else:
                    if self._rentals[i].retdate != '':
                        raise RException('This movie is already returned!')
                    self._rentals[i].retdate = dater
                    if sq == 1:
                        con = sqlite3.connect(r'D:\fp folders\a10-913-Amalia-Duma\ui\mydata.db')
                        cursor = con.cursor()
                        cursor.execute('UPDATE rentals SET return_date = ? where id = ?', (str(dater), rentalid))
                        con.commit()
                        con.close()
                    break

    def generate(self):
        clientids = []
        listc = self._clients.get_list()
        for client in listc:
            clientids.append(client.clid)
        movieids = []
        listc = self._movies.get_list()
        for movie in listc:
            movieids.append(movie.mid)
        i = 1
        while i <= 10:
            rid = randint(300, 499)
            clientid = choice(clientids)
            movieid = choice(movieids)
            month = randint(1, 12)
            day = randint(1, 10)
            day2 = randint(1, 10) + day
            date1 = date(2020, month, day)
            date2 = timedelta(days=30)
            date3 = date(2020, month, day2)
            r1 = Rental(rid, movieid, clientid, date1, date1+date2, date3)
            if self.check_exist(r1) == 0:
                self._rentals.add_rental(r1)
                i += 1

    def get_rentals(self):
        return self._rentals


class Movies:

    """
    Convention - all movies id must be between 10 - 99
    """

    def __init__(self, movies, undo_sv):
        self._mlist = movies
        self._undo_sv = undo_sv

    def __len__(self):
        return len(self._mlist)

    def add(self, movie, check=None):
        """
        Ads a movie to our list
        :param movie: the movie object
        :return: -
        """
        try:
            if check == 1:
                undo = FunctionCall(self.remove, movie.mid)
                redo = FunctionCall(self.add, movie)
                op = Operation(undo, redo)
        except:
            pass
        if self.check_exists(movie) == 0:
            self._mlist.add_movie(movie)
            if check == 1:
                self._undo_sv.record(op)
        else:
            raise Mexceptions('Movie already exists')

    def check_exists_id(self, movieid):
        """
        Check by id if the movie exists in our list
        :param movieid: the id of the movie object
        :return: 1 if it exists or 0 otherwise
        """
        for i in range(0, len(self._mlist)):
            if self._mlist[i].mid == movieid:
                return 1
        return 0

    def check_exists(self, movie):
        """
        Checks if a movie exists in our list
        :param movie: the movie object
        :return: 1 if it exists or 0 otherwise
        """
        for i in range(0, len(self._mlist)):
            if self._mlist[i].mid == movie.mid or self._mlist[i].title == movie.title and \
                    self._mlist[i].desc == movie.desc and self._mlist[i].gen == movie.gen:
                return 1
        return 0

    def generate(self):
        """
        Generates 10 entries in our list
        :return: -
        """
        title_l = ['T1', 'T2', 'T3', 'T4', 'T5']
        desc_l = ['D1', 'D2', 'D3', 'D4', 'D5']
        gen_l = ['G1', 'G2', 'G3', 'G4', 'G5']
        i = 1
        while i <= 10:
            m_id = randint(10, 90)
            title = choice(title_l)
            desc = choice(desc_l)
            gen = choice(gen_l)
            try:
                self.add(Movie(m_id, title, desc, gen))
                i += 1
            except:
                continue

    def remove(self, mid, check=None):
        """
        Removes a movie from our list by the ID
        :param mid: the movie object ID
        :return: -
        """
        try:
            if check == 1:
                movie = self.search('id', str(mid))
                undo = FunctionCall(self.add, movie[0])
                redo = FunctionCall(self.remove, mid)
                op = Operation(undo, redo)
        except:
            pass
        self._mlist.remove_movie_id(mid)
        if check == 1:
            self._undo_sv.record(op)

    def update(self, mid, option, value, check=None, sql=None):
        """
        Updates a value of a movie object from our list
        :param mid: movie id
        :param option: the option to be updated
        :param value:  the new value
        :return: -
        """
        try:
            if check == 1:
                movie = self.search('id', str(mid))
                if option == 'title':
                    undo = FunctionCall(self.update, mid, option, movie[0].title)
                elif option == 'description':
                    undo = FunctionCall(self.update, mid, option, movie[0].desc)
                else:
                    undo = FunctionCall(self.update, mid, option, movie[0].gen)
                redo = FunctionCall(self.update, mid, option, value)
                op = Operation(undo, redo)
        except:
            pass
        ok = 0
        for i in range(0, len(self._mlist)):
            if self._mlist[i].mid == mid:
                ok = 1
                if option == 'title':
                    self._mlist[i].title = value
                    if sql == 1:
                        con = sqlite3.connect(r'D:\fp folders\a10-913-Amalia-Duma\ui\mydata.db')
                        cursor = con.cursor()
                        cursor.execute('UPDATE movies SET title = ? where id = ?', (value, mid))
                        con.commit()
                        con.close()
                    break
                elif option == 'description':
                    self._mlist[i].desc = value
                    if sql == 1:
                        con = sqlite3.connect(r'D:\fp folders\a10-913-Amalia-Duma\ui\mydata.db')
                        cursor = con.cursor()
                        cursor.execute('UPDATE movies SET description = ? where id = ?', (value, mid))
                        con.commit()
                        con.close()
                    break
                elif option == 'genre':
                    self._mlist[i].gen = value
                    if sql == 1:
                        con = sqlite3.connect(r'D:\fp folders\a10-913-Amalia-Duma\ui\mydata.db')
                        cursor = con.cursor()
                        cursor.execute('UPDATE movies SET genre = ? where id = ?', (value, mid))
                        con.commit()
                        con.close()
                    break
        try:
            self._mlist.save_file()
        except:
            pass
        if ok == 0:
            raise Mexceptions('Movie not found!')
        if check == 1:
            self._undo_sv.record(op)

    def search(self, field, value):
        list_returned = []
        if field == 'id':
            for i in range(0, len(self._mlist)):
                if value in str(self._mlist[i].mid):
                    list_returned.append(self._mlist[i])
            return list_returned
        elif field == 'title':
            for i in range(0, len(self._mlist)):
                if value.lower() in self._mlist[i].title.lower():
                    list_returned.append(self._mlist[i])
            return list_returned
        elif field == 'description':
            for i in range(0, len(self._mlist)):
                if value.lower() in self._mlist[i].desc.lower():
                    list_returned.append(self._mlist[i])
            return list_returned
        else:
            for i in range(0, len(self._mlist)):
                if value.lower() in self._mlist[i].gen.lower():
                    list_returned.append(self._mlist[i])
            return list_returned

    def get_list(self):
        """
        :return: the list
        """
        return self._mlist


class Clients:

    """
    Convention - all clients id must be between 100-299
    """

    def __init__(self, clients, undo_sv):
        self._clist = clients
        self._undo_sv = undo_sv

    def __len__(self):
        return len(self._clist)

    def generate(self):
        """
        Generates 10 entries for our list
        :return:
        """
        i = 1
        name_l = ['N1', 'N2', 'N3', 'N4', 'N5']
        while i <= 10:
            cid = randint(100, 299)
            name = choice(name_l)
            if self.check_exists(Client(cid, name)) == 0:
                self._clist.add_client(Client(cid, name))
                i += 1

    def add(self, client, check=None):
        """
        Ads a new client to our list
        :param client: the client object
        :return: -
        """
        try:
            if check == 1:
                undo = FunctionCall(self.remove, client.clid)
                redo = FunctionCall(self.add, client)
                op = Operation(undo, redo)
        except:
            pass
        if self.check_exists(client) == 1:
            raise CException('Client already exists!')
        else:
            self._clist.add_client(client)
            if check == 1:
                self._undo_sv.record(op)


    def check_exists_id(self, clientid):
        """
        Check by id if the client exists in our list
        :param clientid: client id
        :return: 1 if it exists or 0 otherwise
        """
        for i in range(0, len(self._clist)):
            if self._clist[i].clid == clientid:
                return 1
        return 0

    def check_exists(self, client):
        """
        Check if the client exists in our list
        :param client: the client object
        :return: 1 if it exists or 0 otherwise
        """
        for i in range(0, len(self._clist)):
            if self._clist[i].clid == client.clid:
                return 1
        return 0

    def remove(self, cid, check=None):
        """
        Removes a client from our list
        :param cid: the client id
        :return: -
        """
        try:
            if check == 1:
                client = self.search('id', str(cid))
                undo = FunctionCall(self.add, client[0])
                redo = FunctionCall(self.remove, cid)
                op = Operation(undo, redo)
        except:
            pass
        self._clist.remove_client_id(cid)
        if check == 1:
            self._undo_sv.record(op)

    def update(self, cid, value, check=None, sql=None):
        """
        Updates the name for a client
        :param cid: client id
        :param value: new name
        :return: -
        """
        try:
            if check == 1:
                client = self.search('id', str(cid))
                undo = FunctionCall(self.update, cid, client[0].name)
                redo = FunctionCall(self.update, cid, value)
                op = Operation(undo, redo)
        except:
            pass
        ok = 0
        for i in range(0, len(self._clist)):
            if self._clist[i].clid == cid:
                self._clist[i].name = value
                if sql == 1:
                    con = sqlite3.connect(r'D:\fp folders\a10-913-Amalia-Duma\ui\mydata.db')
                    cursor = con.cursor()
                    cursor.execute('UPDATE clients SET name = ? where id = ?', (value, cid))
                    con.commit()
                    con.close()
                ok = 1
                break
        try:
            self._clist.save_file()
        except:
            pass
        if ok == 0:
            raise CException('Client not found!')
        if check == 1:
            self._undo_sv.record(op)

    def search(self, field, value):
        list_returned = []
        if field == 'id':
            for i in range(0, len(self._clist)):
                if value in str(self._clist[i].clid):
                    list_returned.append(self._clist[i])
            return list_returned
        else:
            for i in range(0, len(self._clist)):
                if value.lower() in self._clist[i].name.lower():
                    list_returned.append(self._clist[i])
            return list_returned

    def get_list(self):
        return self._clist

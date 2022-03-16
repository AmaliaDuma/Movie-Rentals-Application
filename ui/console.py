from datetime import date
from domain.entity import Movie, Mexceptions, Client, CException, RException



class Ui:
    def __init__(self, list1, list2, list3, undo_sv, check=None, sql=None):
        self._undo_sv = undo_sv
        self._moviesl = list1
        self._clientsl = list2
        self._rentalsl = list3
        if check == 1:
            self._moviesl.generate()
            self._clientsl.generate()
            self._rentalsl.generate()
        self.sql = sql

    def undo_op(self):
        return self._undo_sv.undo()

    def redo_op(self):
        return self._undo_sv.redo()

    def st1(self):
        list_ret = self._rentalsl.get_statistic1()
        return list_ret

    def st2(self):
        list_ret = self._rentalsl.get_statistic2()
        return list_ret

    def st3(self):
        list_ret = self._rentalsl.get_statistic3()
        if len(list_ret) == 0:
            raise RException('List empty!')
        return list_ret

    def add_m_ui(self, mid, title, desc, gen):
        m1 = Movie(mid, title, desc, gen)
        self._moviesl.add(m1, 1)

    def add_c_ui(self, clid, name):
        c1 = Client(clid, name)
        self._clientsl.add(c1, 1)

    def show_m_ui(self):
        mylist = self._moviesl.get_list()
        return mylist

    def show_c_ui(self):
        mylist = self._clientsl.get_list()
        return mylist

    def show_r_ui(self):
        mylist = self._rentalsl.get_rentals()
        return mylist

    def remove_m_ui(self, mid):
        self._moviesl.remove(mid, 1)

    def remove_c_ui(self, clid):
        self._clientsl.remove(clid, 1)

    def update_ui(self, mid, option, value):
        l = ['title', 'description', 'genre']
        if option not in l:
            raise Mexceptions('Invalid category!')
        if self.sql == 1:
            self._moviesl.update(mid, option, value, 1, 1)
        else:
            self._moviesl.update(mid, option, value, 1)

    def update_c_ui(self, cid, value):
        if self.sql == 1:
            self._clientsl.update(cid, value, 1, 1)
        else:
            self._clientsl.update(cid, value, 1)

    def search_m_ui(self, field, value):
        fields = ['id', 'title', 'description', 'genre']
        if field not in fields:
            raise Mexceptions('Invalid field!')
        list_m_returned = self._moviesl.search(field, value)
        if len(list_m_returned) == 0:
            raise Mexceptions('Movie not found!')
        return list_m_returned

    def search_c_ui(self, field, value):
        fields = ['id', 'name']
        if field not in fields:
            raise CException('Invalid field!')
        list_c_returned = self._clientsl.search(field, value)
        if len(list_c_returned) == 0:
            raise CException('Client not found!')
        return list_c_returned

    def rent_m_ui(self, rentid, movieid, clid, month, day):
        dater = date(2020, month, day)
        self._rentalsl.rent_movie(rentid, movieid, clid, dater, 1)

    def retur_m_ui(self, rid, month, day):
        dater = date(2020, month, day)
        if self.sql == 1:
            self._rentalsl.retur_movie(rid, dater, 1, 1)
        else:
            self._rentalsl.retur_movie(rid, dater, 1)



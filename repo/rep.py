from domain.entity import Rental, RException, Movie, Mexceptions, Client, CException
from newd.data import MyData


class MovieR:

    def __init__(self):
        self._mlist = MyData()

    def __len__(self):
        return len(self._mlist)

    def __getitem__(self, item):
        return self._mlist[item]

    def add_movie(self, movie):
        """
        Ads a movie to our list
        :param movie: a movie object
        :return: -
        """
        if not isinstance(movie, Movie):
            raise Mexceptions('The object is not a Movie.')
        self._mlist.append(movie)

    def remove_movie_id(self, movieid):
        """
        Removes a movie from our list by the ID
        :param movieid: the id of the movie object
        :return: -
        """
        ok = 0
        for i in range(0, len(self._mlist)):
            if self._mlist[i].mid == movieid:
                self._mlist.pop(i)
                ok = 1
                break
        if ok == 0:
            raise Mexceptions('Movie not found!')

    def get_all(self):
        return self._mlist.get_all()


class ClientR:

    def __init__(self):
        self._clist = MyData()

    def __len__(self):
        return len(self._clist)

    def __getitem__(self, item):
        return self._clist[item]

    def add_client(self, client):
        """
        Ads a client to our list
        :param client: a client object
        :return: -
        """
        if not isinstance(client, Client):
            raise CException('The object is not a Client.')
        self._clist.append(client)

    def remove_client_id(self, clientid):
        """
        Removes a client from our list by the ID
        :param clientid: the client object id
        :return: -
        """
        ok = 0
        for i in range(0, len(self._clist)):
            if self._clist[i].clid == clientid:
                self._clist.pop(i)
                ok = 1
                break
        if ok == 0:
            raise CException('Client not found!')

    def get_all(self):
        return self._clist.get_all()


class RentalR:

    def __init__(self):
        self._rlist = MyData()

    def __len__(self):
        return len(self._rlist)

    def __getitem__(self, item):
        return self._rlist[item]

    def add_rental(self, rental):
        """
        Ads a new rental to our list
        :param rental: the rental object
        :return: -
        """
        if not isinstance(rental, Rental):
            raise RException('The object is not a Rental.')
        self._rlist.append(rental)

    def remove_rental(self, rid):
        """
        Removes a rental from our list
        :param rid: the rental object id
        :return: -
        """
        ok = 0
        for i in range(0, len(self._rlist)):
            if self._rlist[i].rid == rid:
                self._rlist.pop(i)
                ok = 1
                break
        if ok == 0:
            raise RException('Rental not found!')

    def get_all(self):
        return self._rlist.get_all()

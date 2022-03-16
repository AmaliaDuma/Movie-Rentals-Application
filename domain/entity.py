from datetime import date


class Mexceptions(Exception):
    def __init__(self, msg):
        self._msg = msg


class Movie:
    """
    Creates a movie object
    """
    def __init__(self, mid, title, desc, gen):
        if mid < 10 or mid > 99:
            raise Mexceptions('Invalid movie id input!')
        self._mid = mid
        self._title = title
        self._desc = desc
        self._gen = gen

    # getters
    @property
    def mid(self):
        return self._mid

    @property
    def title(self):
        return self._title

    @property
    def desc(self):
        return self._desc

    @property
    def gen(self):
        return self._gen

    # setters
    @mid.setter
    def mid(self, value):
        self._mid = value

    @title.setter
    def title(self, value):
        self._title = value

    @desc.setter
    def desc(self, value):
        self._desc = value

    @gen.setter
    def gen(self, value):
        self._gen = value

    def __str__(self):
        return 'ID: ' + str(self._mid) + ' title: ' + self._title + \
               ' description: ' + self._desc + ' genre: ' + self._gen


class CException(Exception):
    def __init__(self, msg):
        self._msg = msg


class Client:
    """
    Creates a Client object
    """
    def __init__(self, clid, name):
        if clid < 100 or clid > 300:
            raise CException('Invalid client id input')
        self._clid = clid
        self._name = name

    # getters
    @property
    def clid(self):
        return self._clid

    @property
    def name(self):
        return self._name

    # setters
    @clid.setter
    def clid(self, value):
        self._clid = value

    @name.setter
    def name(self, value):
        self._name = value

    def __str__(self):
        return 'ID: ' + str(self._clid) + ' name: ' + self._name


class RException(Exception):
    def __init__(self, msg):
        self._msg = msg


class Rental:
    """
    Creates a Rental object
    """

    def __init__(self, rid, movieid, clientid, rentdate, duedate, retdate):
        if rid < 300 or rid > 500:
            raise RException('Invalid rental ID!')
        self._rid = rid
        if movieid < 10 or movieid > 99:
            raise RException('Invalid movie ID!')
        self._movieid = movieid
        if clientid < 100 or clientid > 300:
            raise RException('Invalid client ID!')
        self._clientid = clientid
        if not isinstance(rentdate, date) or not isinstance(duedate, date):
            raise RException('Invalid dates input!')
        self._rentdate = rentdate
        self._duedate = duedate
        if retdate == '':
            self._retdate = retdate
        else:
            if not isinstance(retdate, date):
                raise RException('Invalid dates input!')
            self._retdate = retdate

    def __str__(self):
        return 'ID: ' + str(self._rid) + ' movie ID: ' + str(self._movieid) +\
               ' client ID: ' + str(self._clientid) + '\n' + \
               'rent date: ' + str(self._rentdate) + ' due date: ' + str(self._duedate) +\
               ' returned date: ' + str(self._retdate)

    # getters
    @property
    def rid(self):
        return self._rid

    @property
    def movieid(self):
        return self._movieid

    @property
    def clientid(self):
        return self._clientid

    @property
    def rentdate(self):
        return self._rentdate

    @property
    def duedate(self):
        return self._duedate

    @property
    def retdate(self):
        return self._retdate

    @retdate.setter
    def retdate(self, value):
        self._retdate = value


class RDays:

    def __init__(self, mid, days):
        self._mid = mid
        self._days = days

    @property
    def mid(self):
        return self._mid

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, value):
        self._days = value

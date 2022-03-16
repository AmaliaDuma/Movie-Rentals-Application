import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QInputDialog, QGroupBox, QTextBrowser, QTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from domain.entity import RException
from repo.rep import RentalR, ClientR, MovieR
from repo.repbinary import MovieRB, ClientRB, RentalRB
from repo.repfile import MovieRF, ClientRF, RentalRF
from repo.repjson import MovieRJ, ClientRJ, RentalRJ
from repo.reposql import MovieRDB, ClientRDB, RentalRDB
from services.sv import Movies, Clients, Rentals
from services.undo_sv import UndoService
from ui.console import Ui
from settings.settings import Settings


class StatisticsWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Most rented movies.')
        b2 = QPushButton('Most active clients.')
        b3 = QPushButton('Late rentals.')
        self.box = QGroupBox('Output')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2, b3)
        b1.clicked.connect(self.most_r_movies)
        b2.clicked.connect(self.most_a_clients)
        b3.clicked.connect(self.late_rentals)

    def create_layout(self, b1, b2, b3):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def most_r_movies(self):
        mylist = self.ui.st1()
        for stc in mylist:
            movie = stc[0]
            string = str(movie[0]) + ' days: ' + str(stc[1])
            self.output.append(string)
        self.output.append('\n')

    def most_a_clients(self):
        mylist = self.ui.st2()
        for stc in mylist:
            client = stc[0]
            string = str(client[0]) + ' days: ' + str(stc[1])
            self.output.append(string)
        self.output.append('\n')

    def late_rentals(self):
        try:
            mylist = self.ui.st3()
            for stc in mylist:
                movie = stc[0]
                string = str(movie[0]) + ' days: ' + str(stc[1])
                self.output.append(string)
            self.output.append('\n')
        except RException as exc:
            self.output.append(str(exc))
            self.output.append('\n')


class RentalsWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Rent a movie.')
        b2 = QPushButton('Return a movie.')
        b3 = QPushButton('List rentals.')
        self.box = QGroupBox('Output')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2, b3)
        b1.clicked.connect(self.rent_m)
        b2.clicked.connect(self.retur_m)
        b3.clicked.connect(self.list_r)

    def create_layout(self, b1, b2, b3):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def rent_m(self):
        try:
            rentid, result = QInputDialog.getInt(self, 'Input Dialog', 'Enter the rental id: ')
            if result:
                movieid, result1 = QInputDialog.getInt(self, 'Input Dialog', 'Enter the movie id: ')
                if result1:
                    clid, result2 = QInputDialog.getInt(self, 'Input Dialog', 'Enter the client id: ')
                    if result2:
                        string_f = 'Now please enter the rent date.' + '\n' + 'Enter the month: '
                        month, result3 = QInputDialog.getInt(self, 'Input Dialog', string_f)
                        if result3:
                            day, result4 = QInputDialog.getInt(self, 'Input Dialog', 'Enter the day: ')
                            if result4:
                                self.ui.rent_m_ui(rentid, movieid, clid, month, day)
        except Exception as exc:
            self.output.append(str(exc))

    def retur_m(self):
        try:
            rid, result = QInputDialog.getInt(self, 'Input Dialog', 'Enter the rental id: ')
            if result:
                string_f = 'Now please enter the return date.' + '\n' + 'Enter the month: '
                month, result1 = QInputDialog.getInt(self, 'Input Dialog', string_f)
                if result1:
                    day, result2 = QInputDialog.getInt(self, 'Input Dialog', 'Enter the day: ')
                    if result2:
                        self.ui.retur_m_ui(rid, month, day)
        except Exception as exc:
            self.output.append(str(exc))

    def list_r(self):
        mylist = self.ui.show_r_ui()
        for rental in mylist:
            self.output.append(str(rental))
        self.output.append('\n')


class MoviesWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Add a movie.')
        b2 = QPushButton('Remove a movie.')
        b3 = QPushButton('List movies.')
        b4 = QPushButton('Update a movie.')
        b5 = QPushButton('Search a movie.')
        self.box = QGroupBox('Output')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2, b3, b4, b5)
        b1.clicked.connect(self.add_m)
        b2.clicked.connect(self.remove_m)
        b3.clicked.connect(self.list_m)
        b4.clicked.connect(self.update_m)
        b5.clicked.connect(self.search_m)

    def create_layout(self, b1, b2, b3, b4, b5):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(b4)
        layout.addWidget(b5)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def add_m(self):
        try:
            mid, result = QInputDialog.getInt(self, 'Input Dialog', 'Enter the movie id: ')
            if result:
                title, result1 = QInputDialog.getText(self, 'Input Dialog', 'Enter the title: ')
                if result1:
                    desc, result2 = QInputDialog.getText(self, 'Input Dialog', 'Enter the description: ')
                    if result2:
                        gen, result3 = QInputDialog.getText(self, 'Input Dialog', 'Enter the genre: ')
                        if result3:
                            self.ui.add_m_ui(mid, title, desc, gen)
        except Exception as exc:
            self.output.append(str(exc))

    def remove_m(self):
        try:
            mid, result = QInputDialog.getInt(self, 'Input Dialog', 'Enter the movie id: ')
            if result:
                self.ui.remove_m_ui(mid)
        except Exception as exc:
            self.output.append(str(exc))

    def update_m(self):
        try:
            mid, result = QInputDialog.getInt(self, 'Input Dialog', 'Enter the movie id: ')
            if result:
                string_f = 'Choose one of the following: "title", "description", "genre" : '
                option, result1 = QInputDialog.getText(self, 'Input Dialog', string_f)
                if result1:
                    value, result2 = QInputDialog.getText(self, 'Input Dialog', 'Enter the new value: ')
                    if result2:
                        self.ui.update_ui(mid, option, value)
        except Exception as exc:
            self.output.append(str(exc))

    def list_m(self):
        mylist = self.ui.show_m_ui()
        for mov in mylist:
            self.output.append(str(mov))
        self.output.append('\n')

    def search_m(self):
        try:
            string_f = 'You can search by "id", "title", "description" or "genre".' + '\n' + 'Choose one: '
            field, result = QInputDialog.getText(self, 'Input Dialog', string_f)
            if result:
                value, result1 = QInputDialog.getText(self, 'Input Dialog', 'Enter the value: ')
                if result1:
                    mylist = self.ui.search_m_ui(field, value)
                    for movie in mylist:
                        self.output.append(str(movie))
                    self.output.append('\n')
        except Exception as exc:
            self.output.append(str(exc))


class ClientsWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Add a client.')
        b2 = QPushButton('Remove a client.')
        b3 = QPushButton('List clients.')
        b4 = QPushButton('Update a client.')
        b5 = QPushButton('Search a client.')
        self.box = QGroupBox('Output')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2, b3, b4, b5)
        b1.clicked.connect(self.add_c)
        b2.clicked.connect(self.remove_c)
        b3.clicked.connect(self.list_c)
        b4.clicked.connect(self.update_c)
        b5.clicked.connect(self.search_c)

    def create_layout(self, b1, b2, b3, b4, b5):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(b4)
        layout.addWidget(b5)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def add_c(self):
        try:
            clid, result = QInputDialog.getInt(self, 'Input Dialog', 'Enter the client id: ')
            if result:
                name, result1 = QInputDialog.getText(self, 'Input Dialog', 'Enter the name: ')
                if result1:
                    self.ui.add_c_ui(clid, name)
        except Exception as exc:
            self.output.append(str(exc))

    def remove_c(self):
        try:
            clid, result = QInputDialog.getInt(self, 'Input Dialog', 'Enter the client id: ')
            if result:
                self.ui.remove_c_ui(clid)
        except Exception as exc:
            self.output.append(str(exc))

    def list_c(self):
        mylist = self.ui.show_c_ui()
        for client in mylist:
            self.output.append(str(client))
        self.output.append('\n')

    def update_c(self):
        try:
            clid, result = QInputDialog.getInt(self, 'Input Dialog', 'Enter the client id: ')
            if result:
                string_f = 'You can only modify the name' + '\n' + 'Enter the name: '
                name, result1 = QInputDialog.getText(self, 'Input Dialog', string_f)
                if result1:
                    self.ui.update_c_ui(clid, name)
        except Exception as exc:
            self.output.append(str(exc))

    def search_c(self):
        try:
            string_f = 'You can search by "id" or "name".' + '\n' + 'Choose one: '
            field, result = QInputDialog.getText(self, 'Input Dialog', string_f)
            if result:
                value, result1 = QInputDialog.getText(self, 'Input Dialog', 'Enter the value: ')
                if result1:
                    mylist = self.ui.search_c_ui(field, value)
                    for client in mylist:
                        self.output.append(str(client))
                    self.output.append('\n')
        except Exception as exc:
            self.output.append(str(exc))


class MVui(QMainWindow):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.setWindowTitle('Movie rental')
        self.setFixedSize(500, 250)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        b1 = QPushButton('Movies.')
        b2 = QPushButton('Clients.')
        b3 = QPushButton('Rentals.')
        b4 = QPushButton('Statistics.')
        b5 = QPushButton('Undo.')
        b6 = QPushButton('Redo.')
        self.box = QTextEdit('Output', self._centralWidget)
        self.box.hide()
        self.create_layout(b1, b2, b3, b4, b5, b6)
        b1.clicked.connect(self.movies)
        b2.clicked.connect(self.clients)
        b3.clicked.connect(self.rentals)
        b4.clicked.connect(self.statistics)
        b5.clicked.connect(self.undo)
        b6.clicked.connect(self.redo)

    def create_layout(self, b1, b2, b3, b4, b5, b6):
        generalL = QHBoxLayout()
        generalL.addWidget(b1)
        generalL.addWidget(b2)
        generalL.addWidget(b3)
        generalL.addWidget(b4)
        generalL.addWidget(b5)
        generalL.addWidget(b6)
        generalL.addWidget(self.box)
        self._centralWidget.setLayout(generalL)

    def undo(self):
        self.box.hide()
        a = self.ui.undo_op()
        if not a:
            self.box.setText('No more undos')
            self.box.show()

    def redo(self):
        self.box.hide()
        a = self.ui.redo_op()
        if not a:
            self.box.setText('No more redos')
            self.box.show()

    def movies(self):
        self.box.hide()
        self.w = MoviesWindow(self.ui)
        self.w.show()

    def clients(self):
        self.box.hide()
        self.w = ClientsWindow(self.ui)
        self.w.show()

    def rentals(self):
        self.box.hide()
        self.w = RentalsWindow(self.ui)
        self.w.show()

    def statistics(self):
        self.box.hide()
        self.w = StatisticsWindow(self.ui)
        self.w.show()


def main():
    s = Settings()
    undo_sv = UndoService()
    if s.repo == 'file':
        m_repo = MovieRF(s.movies)
        c_repo = ClientRF(s.clients)
        r_repo = RentalRF(s.rentals)
        ok = 0
        sq = 0
    elif s.repo == 'binary':
        m_repo = MovieRB(s.movies)
        c_repo = ClientRB(s.clients)
        r_repo = RentalRB(s.rentals)
        ok = 0
        sq = 0
    elif s.repo == 'json':
        m_repo = MovieRJ(s.movies)
        c_repo = ClientRJ(s.clients)
        r_repo = RentalRJ(s.rentals)
        ok = 0
        sq = 0
    elif s.repo == 'data':
        m_repo = MovieRDB(s.movies)
        c_repo = ClientRDB(s.clients)
        r_repo = RentalRDB(s.rentals)
        ok = 0
        sq = 1
    else:
        m_repo = MovieR()
        c_repo = ClientR()
        r_repo = RentalR()
        ok = 1
        sq = 0
    m_ser = Movies(m_repo, undo_sv)
    c_ser = Clients(c_repo, undo_sv)
    r_ser = Rentals(r_repo, m_ser, c_ser, undo_sv)
    a = Ui(m_ser, c_ser, r_ser, undo_sv, ok, sq)
    mv = QApplication(sys.argv)
    view = MVui(a)
    view.show()
    sys.exit(mv.exec_())


if __name__ == '__main__':
    main()

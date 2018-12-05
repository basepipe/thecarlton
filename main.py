import sys
import datetime
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGridLayout, QDockWidget, QMainWindow,\
    QTableWidget, QFormLayout, QCalendarWidget, QDialog, QSpinBox, QListWidget, QListWidgetItem, QLineEdit, QComboBox


def date_iterator(start_date, end_date):
    for date in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(days=date)


def style(widget):
    widget.setStyleSheet("QMainWindow { background-color: rgb(197, 183, 183) }"
                         "QListWidget { background-color: rgb(201, 214, 223) }"
                         "QTableWidget { background-color: rgb(201, 214, 223) }"
                         "QDialog { background-color: rgb(201, 214, 223) }"
                         "QToolBar { background-color: lightgrey }")


class Show:
    def __init__(self, name, prod_days, start_date):
        self.name = name
        self.prod_days = prod_days
        self.start_date = start_date
        print("Show created! Name:", self.name, "Start date:", self.start_date, "Days of Production:", self.prod_days)


class CrewPanel(QDockWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Crew Members")
        self.setWidget(QWidget())
        crew_dock_widget_layout = QFormLayout()
        self.widget().setLayout(crew_dock_widget_layout)
        new_crew_button = QPushButton("New Crew Member")
        crew_dock_widget_layout.addRow(new_crew_button)
        self.crew_list_widget = QListWidget()
        crew_dock_widget_layout.addRow(self.crew_list_widget)

        new_crew_button.pressed.connect(self.add_crew_member)

    def add_crew_member(self):
        w = QDialog()
        w.setWindowTitle("Add New Crew Member")
        w.setLayout(QFormLayout())
        crew_name = QLineEdit("New Crew Member")
        w.layout().addRow(QLabel("Crew Member Name:"), crew_name)
        specialization = QComboBox()
        specialization.addItems(
            ["Directing", "Cinematography", "Producing", "Production Design", "Editing", "Visual Effects"])
        w.layout().addRow(QLabel("Specialization:"), specialization)
        accept = QPushButton("Create")
        accept.clicked.connect(w.accept)
        reject = QPushButton("Cancel")
        reject.clicked.connect(w.reject)
        w.layout().addRow(accept, reject)
        if w.exec_() == QDialog.Accepted:
            new_crew_item = QListWidgetItem(crew_name.text())
            new_crew_item.setFlags(new_crew_item.flags() | Qt.ItemIsEditable)
            self.crew_list_widget.addItem(new_crew_item)


class PositionPanel(QDockWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Crew Positions")
        self.setWidget(QWidget())
        pos_dock_widget_layout = QFormLayout()
        self.widget().setLayout(pos_dock_widget_layout)
        new_pos_button = QPushButton("New Crew Position")
        pos_dock_widget_layout.addRow(new_pos_button)
        self.pos_list_widget = QListWidget()
        pos_dock_widget_layout.addRow(self.pos_list_widget)

        new_pos_button.pressed.connect(self.add_position)

    def add_position(self):
        w = QDialog()
        w.setWindowTitle("Create New Position")
        w.setLayout(QFormLayout())
        pos_name = QLineEdit("New Position")
        w.layout().addRow(QLabel("Position Name:"), pos_name)
        pre_pro_days = QSpinBox()
        post_pro_days = QSpinBox()
        w.layout().addRow(QLabel("Days of pre-production:"), pre_pro_days)
        w.layout().addRow(QLabel("Days of immediate post-production:"), post_pro_days)
        accept = QPushButton("Create")
        accept.clicked.connect(w.accept)
        reject = QPushButton("Cancel")
        reject.clicked.connect(w.reject)
        w.layout().addRow(accept, reject)
        if w.exec_() == QDialog.Accepted:
            print("Days of pre-production", pre_pro_days.value(), "Days of post-productions", post_pro_days.value())
            new_pos_item = QListWidgetItem(pos_name.text())
            new_pos_item.setFlags(new_pos_item.flags() | Qt.ItemIsEditable)
            self.pos_list_widget.addItem(new_pos_item)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Carlton 2.0")
        self.setCentralWidget(QWidget())
        grid = QGridLayout()
        self.centralWidget().setLayout(grid)
        self.start_date = None
        self.end_date = None

        grid.addWidget(QLabel("Calendar"), 0, 0)
        self.calendar_view = QTableWidget()
        grid.addWidget(self.calendar_view, 1, 0, 1, 4)
        self.start_button = QPushButton("Start Date")
        self.start_button.clicked.connect(lambda: self.get_date(True))
        self.end_button = QPushButton("End Date")
        self.end_button.clicked.connect(lambda: self.get_date(False))
        grid.addWidget(self.start_button, 0, 2)
        grid.addWidget(self.end_button, 0, 3)

        self.create_panels()
        toolbar = self.addToolBar("Toolbar")
        toolbar.addAction("New Show", self.create_new_show)

        self.shows = []

    def create_panels(self):
        crew_dock = CrewPanel()
        self.addDockWidget(Qt.RightDockWidgetArea, crew_dock)

        pos_dock = PositionPanel()
        self.addDockWidget(Qt.RightDockWidgetArea, pos_dock)

    def create_new_show(self):
        w = QDialog()
        w.setWindowTitle("Create New Show")
        w.setLayout(QFormLayout())
        show_name = QLineEdit("New Show")
        w.layout().addRow(QLabel("New Show Title:"), show_name)
        prod_days = QSpinBox()
        w.layout().addRow(QLabel("Days of production:"), prod_days)
        calendar_input = QCalendarWidget()
        w.layout().addRow(QLabel("Start date:"))
        w.layout().addRow(calendar_input)
        if self.shows:  # If a show has already been created.
            previous_show = self.shows[-1]
            prod_days.setValue(previous_show.prod_days)
        accept = QPushButton("Create")
        accept.clicked.connect(w.accept)
        reject = QPushButton("Cancel")
        reject.clicked.connect(w.reject)
        w.layout().addRow(accept, reject)
        if w.exec_() == QDialog.Accepted:
            print("New show name:", show_name.text(), "Days of pre-production", prod_days.value())
            selected_date = calendar_input.selectedDate()
            start_date = datetime.date(selected_date.year(), selected_date.month(), selected_date.day())
            self.shows.append(Show(show_name.text(), prod_days.value(), start_date))

    def get_date(self, is_start):
        w = QDialog()
        w.setLayout(QFormLayout())
        calendar_input = QCalendarWidget()
        w.layout().addRow(calendar_input)
        accept_button = QPushButton("Accept")
        accept_button.clicked.connect(w.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(w.reject)
        w.layout().addRow(accept_button, cancel_button)
        if w.exec() == QDialog.Accepted:
            selected_date = calendar_input.selectedDate()
            new_date = datetime.date(selected_date.year(), selected_date.month(), selected_date.day())
            print("New date is", new_date)
            if is_start:
                self.start_date = new_date
                self.start_button.setText(str(new_date))
                if self.end_date:
                    print("Number of days is", self.end_date - self.start_date)
                    self.calendar_view.setColumnCount((self.end_date - self.start_date).days)
                    date_labels = [str(date) for date in date_iterator(self.start_date, self.end_date)]
                    self.calendar_view.setHorizontalHeaderLabels(date_labels)
            else:
                self.end_date = new_date
                self.end_button.setText(str(new_date))
                if self.start_date:
                    print("Number of days is", (self.end_date - self.start_date).days)
                    self.calendar_view.setColumnCount((self.end_date - self.start_date).days)
                    date_labels = [str(date) for date in date_iterator(self.start_date, self.end_date)]
                    self.calendar_view.setHorizontalHeaderLabels(date_labels)


if __name__ == "__main__":
    app = QApplication([])
    style(app)

    main = MainWindow()
    main.resize(800, 600)
    main.show()

    sys.exit(app.exec_())
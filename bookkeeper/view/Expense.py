from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton

from bookkeeper.view.TableModel import TableModel

class ExpenseWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = None

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel('Расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.bottom_controls = QGridLayout()
        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)
        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 2, 1)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)
        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def set_expense_table(self, datas):
        if datas:
            self.model = TableModel(datas)
            self.expenses_grid.setModel(self.model)

    def set_category_dropdown(self, datas):
        for data in datas:
            self.category_dropdown.addItem(data[1], data[0])

    def on_expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)

    def get_amount(self) -> float:
        try:
            number = float(self.amount_line_edit.text())
        except Exception:
            QtGui.QMessageBox.about(self, 'Error','Input can only be a number')
        return number

    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())
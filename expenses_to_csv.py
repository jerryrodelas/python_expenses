import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QAction, QHeaderView, QLineEdit, QLabel,
                             QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QPainter, QStandardItemModel, QIcon , QPixmap
from PyQt5.Qt import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries


class DataEntryForm(QWidget):
    def __init__(self):
        super().__init__()
        self.items = 0

        self._data = {"Phone bill": 50.5, "Gas": 30.0, "Rent": 1850.0,
                      "Car Payment": 420.0, "Comcast": 105.0,
                      "Public transportation": 60.0, "Coffee": 90.5}

        # Right side
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('Description', 'Price'))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.layoutRight = QVBoxLayout()
        # chart widget

        self.chartView = QChartView()
        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.lineEditDescription = QLineEdit()
        self.lineEditPrice = QLineEdit()
        self.Total_Expenses = QLabel()
        #sets up the text widgets


        self.buttonAdd = QPushButton('Add')
        self.buttonClear = QPushButton('Clear')
        self.buttonQuit = QPushButton('Quit')
        self.buttonPlot = QPushButton('Plot')
        self.buttonAddTotal = QPushButton('Add Total') #write code for this
        self.buttonAdd.setEnabled(False)

        self.layoutRight.setSpacing(15)
        self.layoutRight.addWidget(QLabel('Description'))
        self.layoutRight.addWidget(self.lineEditDescription)
        self.layoutRight.addWidget(QLabel('Price'))
        self.layoutRight.addWidget(self.lineEditPrice)
        self.layoutRight.addWidget(self.Total_Expenses)


        self.layoutRight.addWidget(self.buttonAdd)
        self.layoutRight.addWidget(self.buttonPlot)
        self.layoutRight.addWidget(self.chartView)
        self.layoutRight.addWidget(self.buttonClear)
        self.layoutRight.addWidget(self.buttonAddTotal) # write code for this
        self.layoutRight.addWidget(self.buttonQuit)


        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table, 70)
        self.layout.addLayout(self.layoutRight, 50)
        self.setLayout(self.layout)



        self.buttonQuit.clicked.connect(lambda:app.quit())
        self.buttonClear.clicked.connect(self.reset_table)
        self.buttonPlot.clicked.connect(self.graph_chart)
        self.buttonAdd.clicked.connect(self.add_entry)
        self.buttonAddTotal.clicked.connect(self.add_total)
        self.lineEditDescription.textChanged[str].connect(self.check_disable)
        self.lineEditPrice.textChanged[str].connect(self.check_disable)


        self.fill_table()

    def fill_table(self, data=None):
        data = self._data if not data else data

        for desc, price in data.items():
            descItem = QTableWidgetItem(desc)
            priceItem = QTableWidgetItem('${0:.2f}'.format(price))
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, descItem)
            self.table.setItem(self.items, 1, priceItem)
            self.items += 1

    def add_entry(self):
        desc = self.lineEditDescription.text()
        price = self.lineEditPrice.text()

        try:
            descItem = QTableWidgetItem(desc)
            priceItem = QTableWidgetItem('${0:.2f}'.format(float(price)))
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, descItem)
            self.table.setItem(self.items, 1, priceItem)
            self.items += 1

            self.lineEditDescription.setText('')
            self.lineEditPrice.setText('')
        except ValueError:
            pass

    def add_total(self):

        # allRows = self.table.rowCount() #gets the number of rows
        # print ('the total number of row =',allRows)
        index=(self.table.selectionModel().currentIndex())
        # value=index.sibling(index.row(),index.column()).data() # will return cell data
        msg2 =  'Click on the table to get total expenses.'
        msg3 = 'If there are no values, then enter expenses on the table.'
        if index.row() <= 0 or index.column() <= 0:
            self.Total_Expenses.setText('You havent selected the values on the table!\n'+msg2+msg3)
        # else:
        #     print('this is row number =',index.row()) # gives current selected row
        #     print('this is column number =',index.column()) # gives current selected column.
        #     print(float(value[1:8]))

        try:
            total = 0
            for i in range(self.table.rowCount()):
                # text = self.table.item(i, 0).text()
                val = float(self.table.item(i, 1).text().replace('$', ''))
                # print(val)
                #     print ('${0:.2f}'.format(val))
                total += val
                # print('$',total)
                self.Total_Expenses.setText('Total Expenses =  AU$ '+ str(total))
        except ValueError:
            pass
        return

    def check_disable(self):
        if self.lineEditDescription.text() and self.lineEditPrice.text():
            self.buttonAdd.setEnabled(True)
        else:
            self.buttonAdd.setEnabled(False)

    def reset_table(self):
        self.table.setRowCount(0)
        self.items = 0
        self.Total_Expenses.setText('Fill up the tables to calculate expenses')
        chart = QChart()
        self.chartView.setChart(chart)


    def graph_chart(self):

        series = QPieSeries()

        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            val = float(self.table.item(i, 1).text().replace('$', ''))
            series.append(text, val)


        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignTop)

        self.chartView.setChart(chart)

class MainWindow(QMainWindow):
    def __init__(self, w):
        super().__init__()
        self.setWindowTitle('Expense Data Entry Form')
        self.setWindowIcon(QIcon(r"expenses.jpg"))
        self.resize(1200, 600)

        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('File')

        # export to csv file action
        exportAction = QAction('Export to CSV', self)
        exportAction.setShortcut('Ctrl+E')
        exportAction.triggered.connect(self.export_to_csv)



        # exit action
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(lambda: app.quit())

        self.fileMenu.addAction(exportAction)
        self.fileMenu.addAction(exitAction)

        self.setCentralWidget(w)



    def export_to_csv(self):
        try:
            with open('Expense Report.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow((w.table.horizontalHeaderItem(0).text(), w.table.horizontalHeaderItem(1).text()))
                for rowNumber in range(w.table.rowCount()):
                    writer.writerow([w.table.item(rowNumber, 0).text(), w.table.item(rowNumber, 1).text()])
            file.close()
            self.statusBar().showMessage('CSV file has been exported to this directory!') # information shows on the bottom of form.
        except Exception as e:
            print(e)
if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = DataEntryForm()

    tab_gui = MainWindow(w)
    tab_gui.show()

    sys.exit(app.exec_())
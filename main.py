import sys
from os import getcwd

#DB logic
import json
import TableModels
import db_handler

#gui
from customDialogs import addRowDialog, editRowDialog

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class TableWidget(QtWidgets.QWidget):
    def __init__(self, t_model):
        super().__init__()
        self.model_name = t_model.name
        self.name = t_model.displayName

        layout = QtWidgets.QHBoxLayout()

        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(t_model)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tableView.setFont(font)

        header = self.tableView.horizontalHeader()  
        for i in range(t_model.columnCount((0,0))):     
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView.setSortingEnabled(True)

        layout.addWidget(self.tableView)
        self.setLayout(layout)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Knihi")
        self.setObjectName("MainWindow")

        self.centralWidget = QtWidgets.QWidget(self)

        self.tablesWidgets = []
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)

        self.addRowButton = QtWidgets.QPushButton(self.centralWidget)
        self.addRowButton.clicked.connect(self.__addRowDialogInit)
        self.loadDBButton = QtWidgets.QPushButton(self.centralWidget)
        self.loadDBButton.clicked.connect(self.__loadDB)

        self.__contextMenuEnabled = False
        self.__setupUI()

    def __setupUI(self):
        MW_Layout = QtWidgets.QGridLayout()

        #Main Window
        self.resize(1500, 1000)
        # self.setStyleSheet("background-color: rgb(164, 211, 53);")

        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(MW_Layout)

        #tabWidget
        MW_Layout.addWidget(self.tabWidget, 0, 0, 4, 4)
        self.tabWidget.currentChanged.connect(self.__updateTable)

        MW_Layout.addWidget(self.addRowButton, 5, 2)
        self.addRowButton.setText('Add new row')
        self.addRowButton.hide()
        MW_Layout.addWidget(self.loadDBButton, 5, 3)
        self.loadDBButton.setText('Load DB')

        # пра мяне :)
        label = QtWidgets.QLabel(self.centralWidget)
        label.setText("Ангеліна Пашкавец, 4к, 4гр, 2023")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
        MW_Layout.addWidget(label, 5, 0)

    def contextMenuEvent(self, event):
        if self.__contextMenuEnabled == False:
            return
        menu = QtWidgets.QMenu(self.centralWidget)

        acAdd_row = QtWidgets.QAction("Add row", self)
        acEdit_row = QtWidgets.QAction("Edit row", self)
        acDel_row = QtWidgets.QAction("Delete Row", self)

        acAdd_row.triggered.connect(self.__addRowDialogInit)
        acEdit_row.triggered.connect(self.__editRowDialogInit)
        acDel_row.triggered.connect(self.__deleteRow)

        menu.addActions([acAdd_row, acEdit_row, acDel_row])
        menu.exec(event.globalPos())

    def __showErrorDialog(self, mes):
        msb = QtWidgets.QMessageBox(self)
        msb.setWindowTitle("ERROR")
        msb.setText(mes)
        msb.setIcon(QtWidgets.QMessageBox.Critical)
        msb.exec()

    def __loadDB(self):
        self.tabWidget.clear()
        self.tablesWidgets.clear()
        self.addRowButton.hide()

        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', f'{getcwd()}\\',"JSON files (*.json)")
        if fname[0] == '':
            return
        try:
            with open(fname[0]) as f:
                dbDescJSON = json.load(f)
        except:
            self.__showErrorDialog("Can't load description.json")
            return

        path_list = fname[0].split('/')[:-1]
        path = '/'
        path = path.join(path_list)
        try:
            self.TML = TableModels.TableModelsList(dbDescJSON["tables"])
        except:
            self.__showErrorDialog("Incorrect JSON file")
            return
        
        try:
            self.db = db_handler.dataBase(path + '/' + dbDescJSON["path"])
        except:
            self.__showErrorDialog("Incorrect DB file")
            return

        for t_model in self.TML:
            self.db.fillModel(t_model)
            self.tablesWidgets.append(TableWidget(t_model))
            
        for t_widget in self.tablesWidgets:
            self.tabWidget.addTab(t_widget, t_widget.name)
        self.addRowButton.show()
        self.__contextMenuEnabled = True

    def __updateTable(self):
        t_name = self.tabWidget.currentWidget().model_name
        self.db.fillModel(self.TML[t_name])

    def __addRowDialogInit(self):
        t_name = self.tabWidget.currentWidget().model_name

        dlg = addRowDialog(self.TML, t_name, parent=self)
        if dlg.exec():
            inp_data = dlg.getData(self.TML)
            success, data = self.db.addDataToDB(self.TML[t_name], inp_data)
            if success:
                self.TML[t_name].addNewRow(data)
            else:
                msb = QtWidgets.QMessageBox(self)
                msb.setWindowTitle("Warning")
                msb.setText("Incorrect input values!\nPlease, read tables description")
                msb.setIcon(QtWidgets.QMessageBox.Warning)
                msb.exec()

    def __getSelectedRow(self):
        t_name = self.tabWidget.currentWidget().model_name
        rows = set(index.row() for index in self.tabWidget.currentWidget().tableView.selectedIndexes())
        if len(rows) != 1:
            msb = QtWidgets.QMessageBox(self)
            msb.setWindowTitle("Warning")
            msb.setText("Please, select exacly one row")
            msb.setIcon(QtWidgets.QMessageBox.Warning)
            msb.exec()
            return None, None
        
        return t_name, list(rows)[0]

    def __editRowDialogInit(self):
        t_name, row_ind = self.__getSelectedRow()
        if t_name is None:
            return
        dlg = editRowDialog(self.TML, t_name, row_ind, parent=self)
        if dlg.exec():
            inp_data = dlg.getData(self.TML)
            success, data = self.db.updateDB(self.TML[t_name], self.TML[t_name].data[row_ind][0], inp_data)
            if success:
                self.TML[t_name].updateRow(data, row_ind)
            else:
                msb = QtWidgets.QMessageBox(self)
                msb.setWindowTitle("Warning")
                msb.setText("Incorrect input values!\nPlease, read tables description")
                msb.setIcon(QtWidgets.QMessageBox.Warning)
                msb.exec()

    def __deleteRow(self):
        t_name, row_ind = self.__getSelectedRow()
        if t_name is None:
            return
        success = self.db.softDeleteFromDB(self.TML[t_name], self.TML[t_name].data[row_ind][0])
        if success:
            self.TML[t_name].deleteRow(row_ind)
        else:
            msb = QtWidgets.QMessageBox(self)
            msb.setWindowTitle("Warning")
            msb.setText("Something went wrong...")
            msb.setIcon(QtWidgets.QMessageBox.Warning)
            msb.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
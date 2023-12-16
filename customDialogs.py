import datetime
from PyQt5 import QtGui, QtWidgets, QtCore


class mainDialog(QtWidgets.QDialog):
    def __init__(self, TML, t_model_name, parent=None):
        super().__init__(parent)
        self.t_model_name = t_model_name
        t_model = TML[t_model_name]

        QBtn = QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok 
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.inputFields = {}

        for f_col_name, f_col_set in t_model.foreignColumns.items():
            ref_table = TML[f_col_set['table_ref']]
            r_col_name = f_col_set['col_ref']
            d_col_name = f_col_set['col_display']

            inp1 = QtWidgets.QComboBox(self)
            values = ref_table.getColumnValues(d_col_name)

            inp1.addItems(values)
            inp1.setObjectName(f'{f_col_name}')
            self.inputFields[f'{f_col_set['dname']} (foreign)']  = inp1


        for col_name, col_set in t_model.columns.items():
            if str.lower(col_set['dtype']) == 'date':
                inp1 = QtWidgets.QCalendarWidget()
            elif str.lower(col_set['dtype']) == 'text':
                inp1 = QtWidgets.QTextEdit()
            else:
                inp1 = QtWidgets.QLineEdit()
                if str.lower(col_set['dtype']) == 'integer':
                    inp1.setValidator(QtGui.QIntValidator(bottom = 0))
                elif str.lower(col_set['dtype']) == 'real':
                    inp1.setValidator(QtGui.QDoubleValidator(bottom = 0, decimals = 2))
            inp1.setObjectName(f'{col_name}')
            self.inputFields[col_set['dname']]  = inp1

    def setupUI(self):
        self.resize(800, 500)
        self.layout = QtWidgets.QVBoxLayout()
        
        for dname, QtInp in self.inputFields.items():
            self.layout.addWidget(QtWidgets.QLabel(f'Input "{dname}":'))
            self.layout.addWidget(QtInp)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


    def getData(self, TML):
        t_model = TML[self.t_model_name]
        res = []
        for i, inp_widget in enumerate(self.inputFields.values()):
            col_name = inp_widget.objectName()
            
            if col_name in t_model.foreignColumns.keys():
                presented_ind = inp_widget.currentIndex()

                f_col_set = t_model.foreignColumns[col_name]
                ref_table = TML[f_col_set['table_ref']]
                r_col_name = f_col_set['col_ref']

                res += [ref_table.getColumnValues(r_col_name)[presented_ind]]
            
            if col_name in t_model.columns.keys():
                dtype = t_model.columns[col_name]['dtype']
                if str.lower(dtype) == 'date':
                    year, month, day = inp_widget.selectedDate().getDate()
                    res += [datetime.date(year, month, day).strftime('%Y-%m-%d')]
                elif str.lower(dtype) == 'text':
                    res += [inp_widget.toPlainText()]
                elif str.lower(dtype) == 'real':
                    res += [inp_widget.text().replace(',', '.')]
                else:
                    res += [inp_widget.text()]
        return res

class addRowDialog(mainDialog):
    def __init__(self, TML, t_model_name, parent=None):
        super().__init__(TML, t_model_name, parent)
        t_model = TML[t_model_name]
        self.setWindowTitle(f'Add new row to {t_model.displayName}')
        super().setupUI()

class editRowDialog(mainDialog):
    def __init__(self, TML, t_model_name, ind, parent=None):
        super().__init__(TML, t_model_name, parent)
        t_model = TML[t_model_name]
        self.setWindowTitle(f'Edit row in {t_model.displayName}')

        before_vals = t_model.getRowValues(ind)[2 + len(t_model.foreignColumns):]

        for i, (_, col_set) in enumerate(t_model.columns.items()):
            if str.lower(col_set['dtype']) == 'date':
                self.inputFields[col_set['dname']].setSelectedDate(QtCore.QDate.fromString(before_vals[i], 'yyyy-MM-dd'))
            elif str.lower(col_set['dtype']) == 'text':
                self.inputFields[col_set['dname']].setText(before_vals[i])
            else:
                self.inputFields[col_set['dname']].setText(str(before_vals[i]))
        self.setupUI()
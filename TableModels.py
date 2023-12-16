# with open('.\\db\\description.json') as f:
#     tablesJSON = json.load(f)
from PyQt5.QtCore import Qt, QAbstractTableModel
from datetime import datetime

class TableModelsList:
    def __init__(self, tablesJSON) -> None:
        self.list = []

        for tname in list(tablesJSON.keys()):
            table = TableModel(tname)

            colFromJSON = tablesJSON[table.name]["columns"]

            table.displayName = tablesJSON[table.name]["display_name"]
            
            for cname, settings in colFromJSON.items():
                if "foreign-key" in settings:
                    table.addForeignColumn(cname, settings["foreign-key"]["table"], settings["foreign-key"]["column"], settings["foreign-key"]["display_column"])
                else:
                    if not table.addColumn(cname, settings["display_name"], settings["type"]):
                        raise Exception(f'WRONG TYPE! Table {table.name}, column {cname}')
            self.__addTable(table)

        self.__connectForeign()

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return self.list[arg]
        if isinstance(arg, str):
            for table in self.list:
                if table.name == arg:
                    return table
    
    def __connectForeign(self):
        for table in self.list:
            if len(table.foreignColumns):
                act_names = list(table.foreignColumns.keys())
                for name in act_names:
                    set = table.foreignColumns[name]

                    look_table = set['table_ref']
                    look_column_ref = set['col_ref']
                    look_column_d = set['col_display']

                    present = False
                    for t in self.list:
                        if (look_table == t.name) and (look_column_d in t.columns):
                            table.foreignColumns[name]['dname'] = t.columns[look_column_d]['dname']
                            table.foreignColumns[name]['dtype'] = t.columns[look_column_d]['dtype']
                            present = True

                    if not present:
                        del table.foreignColumns[name]

    def __addTable(self, table):
        self.list.append(table)


class TableModel(QAbstractTableModel):
    def __init__(self, tname):
        super().__init__()

        self.name = tname #name of ACTUAL column in db
        self.displayName = tname
        self.columns = {}
        self.data = []
        self.foreignColumns = {}

    def __getitem__(self, arg):
        act_names = list(self.foreignColumns.keys()) + list(self.columns.keys())
        if arg < len(self.foreignColumns):
            return self.foreignColumns[act_names[arg]]
        else:
            return self.columns[act_names[arg]]

    def addColumn(self, name, dname, dtype):
        if dtype not in ['integer', 'real', 'date', 'text']:
            return False
        self.columns[name] = {"dname": dname, "dtype": dtype} #name -- actual, display name -- відавочна
        return True

    def addForeignColumn(self, name, table_ref, col_ref, col_display):
        self.foreignColumns[name] = {"table_ref": table_ref,"col_ref": col_ref, "col_display": col_display, "dname": None, "dtype": None}

    def getColumnValues(self, c_name):
        fc_flag = False
        if c_name in self.columns.keys():
            columns = self.columns
        elif c_name in self.foreignColumns.keys():
            fc_flag = True
            columns = self.foreignColumns
        else: #ask for ID
            return [d[0] for d in self.data]

        i = 0
        for i, key in enumerate(columns.keys()):
            if c_name == key:
                break

        if fc_flag:
            return [d[i+2] for d in self.data]
        else:
            return [d[i+2+len(self.foreignColumns)] for d in self.data]
        
    def getRowValues(self, ind):
        return self.data[ind]
        
    def loadData(self, rawAnswer):
        self.data = []

        for row in rawAnswer:
            if row[1] is None: #not deleted
                self.data += [row]

    def addNewRow(self, rawRow):
        self.layoutAboutToBeChanged.emit()
        if rawRow[1] is None: #not deleted
                self.data += [rawRow]
        self.layoutChanged.emit()

    def deleteRow(self, ind):
        self.layoutAboutToBeChanged.emit()
        del self.data[ind]
        self.layoutChanged.emit()

    def updateRow(self, data, ind):
        self.deleteRow(ind)
        self.addNewRow(data)

    def data(self, index, role):
        col_in_raw = index.column() + 2
        if role == Qt.DisplayRole:
            if self[index.column()]["dtype"] == 'date':
                return '.'.join( reversed(self.data[index.row()][col_in_raw].split('-')) )
            return self.data[index.row()][col_in_raw]

    def rowCount(self, index):
        return len(self.data)

    def columnCount(self, index):
        return len(self.columns) + len(self.foreignColumns)

    def sort(self, Ncol, order):
        self.layoutAboutToBeChanged.emit()
        col_type = self[Ncol]['dtype']
        if str.lower(col_type) == 'date':
            date_format = '%Y-%m-%d'
            sort_key = lambda x: datetime.strptime(x[Ncol+2], date_format)
        elif str.lower(col_type) == 'integer' or str.lower(col_type) == 'real':
            sort_key = lambda x: float(x[Ncol+2])
        else:
            sort_key = lambda x: x[Ncol+2]
        self.data.sort(key=sort_key, reverse = (order == Qt.DescendingOrder))
        self.layoutChanged.emit()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self[section]['dname']
                    
        
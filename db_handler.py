import sqlite3

class dataBase:
    def __init__(self, path):
        self.db = sqlite3.connect(path) 
        self.cur = self.db.cursor()
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
        
    def fillModel(self, t_model):
        data = []
        fc_data = []
        
        if len(t_model.foreignColumns):
            for fc_name, fc_settings in t_model.foreignColumns.items():
                ref_table = fc_settings['table_ref']
                ref_col = fc_settings['col_ref']
                d_col = fc_settings['col_display']
                self.cur.execute(f'SELECT fc.{d_col} FROM {t_model.name} a JOIN {ref_table} fc ON fc.{ref_col} = a.{fc_name}')
                fc_data += [self.cur.fetchall()]
        

        self.cur.execute(f'SELECT * FROM {t_model.name}')
        raw_data = self.cur.fetchall()

        for i, row in enumerate(raw_data):
            d = [row[0], row[1]] #id and deleted
            for fc in fc_data:
                d += fc[i]
            for it in row[2+len(t_model.foreignColumns):]:
                d += [it]
            data += [d]

        t_model.loadData(data)

    def __checkRow(self, t_model, id):
        self.cur.execute(f'SELECT * FROM {t_model.name} WHERE id={id}')
        raw_data = list(self.cur.fetchone())

        fc_data = []
        if len(t_model.foreignColumns):
            for fc_name, fc_settings in t_model.foreignColumns.items():
                ref_table = fc_settings['table_ref']
                ref_col = fc_settings['col_ref']
                d_col = fc_settings['col_display']
                self.cur.execute(f'SELECT fc.{d_col} FROM {t_model.name} a JOIN {ref_table} fc ON fc.{ref_col} = a.{fc_name} WHERE a.id={id}')
                fc_data += list(self.cur.fetchone())
        return raw_data[0:2] + fc_data + raw_data[2+len(t_model.foreignColumns):]
    

    def addDataToDB(self, t_model, data):
        inputed_data = []
        try:
            with self.db:
                columns = ','
                columns = columns.join(list(t_model.foreignColumns.keys()) + list(t_model.columns.keys()))
                quest = ','
                quest = quest.join(['?' for _ in range(t_model.columnCount((0,0)))])

                self.cur.execute(f'INSERT INTO {t_model.name} ({columns}) VALUES ({quest})', data)

                id = self.cur.lastrowid
                inputed_data = self.__checkRow(t_model, id)

        except Exception as ex:
            print(f'Exception while addin into DB: {ex}')
            return False, None
        
        return True, inputed_data
    
    def updateDB(self, t_model, ind, data):
        updated_data = []
        try:
            with self.db:
                columns = ' = ?, '
                columns = columns.join(list(t_model.foreignColumns.keys()) + list(t_model.columns.keys())) + '= ?'

                self.cur.execute(f'UPDATE {t_model.name} SET {columns} WHERE id = {ind}', data)

                updated_data = self.__checkRow(t_model, ind)

        except Exception as ex:
            print(f'Exception while updating DB: {ex}')
            return False, None
        
        return True, updated_data
    

    def softDeleteFromDB(self, t_model, ind):
        try:
            with self.db:
                self.cur.execute(f'UPDATE {t_model.name} SET deleted="1" WHERE id = {ind}')
                self.__checkRow(t_model, ind)
        except Exception as ex:
            print(f'Exception while soft deleting from DB: {ex}')
            return False
        return True
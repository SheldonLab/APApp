import multiprocessing
from databaseWrapper import DatabaseWrapper
from datetime import datetime, tzinfo
from pytz import timezone

class DatabaseUpload(multiprocessing.Process, DatabaseWrapper):

    def __init__(self, database, data):
        multiprocessing.Process.__init__(self)
        DatabaseWrapper.__init__(self, database)
        self.database_name = "AP_APP"
        self.table_name = "AP_Physics"
        self.data = data

    def upload_item(self, data):
        column_names = []
        column_values = []
        for i in data:
            column_names.append(i)
            column_values.append(data[i])
            if i == "initials" and len(data[i]) > 4:
                return
        column_names.append("date")

        eastern = timezone('US/Eastern')
        current_est_time = datetime.now(tz=eastern)
        fmt = '%Y-%m-%d'
        current_est_time = current_est_time.strftime(fmt)

        column_values.append(current_est_time)

        if self.table_exists(self.database_name, self.table_name):
            self.insert_into_database(database_name = self.database_name,
                                      table_name    = self.table_name,
                                      column_names  = column_names,
                                      values        = column_values)
        else:
            self.create_table(database_name = self.database_name,
                              table_name    = self.table_name,
                              column_names  = column_names,
                              column_types  = ["VARCHAR(100)", "VARCHAR(100)","INT", "VARCHAR(100)", "VARCHAR(100)"])
            self.insert_into_database(database_name = self.database_name,
                                      table_name    = self.table_name,
                                      column_names  = column_names,
                                      values        = column_values)

        return True
    
    def run(self):
        self.upload_item(self.data)
        return True

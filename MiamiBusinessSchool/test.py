import dbconnection

connection = dbconnection.DBConnection()
storer = connection.storer

storer.store_test()

connection.disconnect()
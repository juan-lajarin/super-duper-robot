import csv
from cxo import Oracle as oracle
from datetime import date, timedelta
import json

Oracle = oracle()
yesterday = date.today() - timedelta(days=1)
formatted_date = yesterday.strftime('%Y%m%d')
connections = {}

class db_connection: 
    def __init__(self,data):
        self.username = data["username"]
        self.password = data["password"]
        self.hostname = data["hostname"]
        self.port = data["port"]
        self.servicename = data["servicename"]
        self.query = data["query"]

def queryToCSV(query,csv_path):
	csv_file = open(csv_path, "w")
	writer = csv.writer(csv_file, delimiter=';', lineterminator="\n", quoting=csv.QUOTE_NONE)
	try:	
    # No commit as you don-t need to commit DDL.
		Oracle.execute(query)
		for row in Oracle.cursor:
			writer.writerow(row)
	finally:
		csv_file.close()


if __name__== "__main__":
		
	with open('data.txt') as json_file:
		data = json.load(json_file)
		
	for p in data["connection"]:
		
		db = db_connection(data["connection"][p])
		connections.update( {db.username : db} )
		print(db.username+'   ---> ' + str(connections[db.username]))
	
		Oracle.connect(db.username, 
			db.password, 
			db.hostname,
			db.port,
			db.servicename)
		try:
			for i in db.query:
				queryToCSV(i["sql"],i["name"]+formatted_date+".csv")
		# Ensure that we always disconnect from the database to avoid
		# ORA-00018: Maximum number of sessions exceeded. 
		finally:
			Oracle.disconnect()
		
import sqlite3
import random, string
from collections import OrderedDict

db_name = "debts.db"

dbconn = sqlite3.connect(db_name)
cur = dbconn.cursor()

def insert_debt():
	name = raw_input("Name: ")
	amount =  raw_input ("Amount (pesos): ")
	date = raw_input("Date: ")
	date_paid = raw_input("Date paid (blank for not paid): ")
	paid = raw_input("Paid? (Leave blank for not paid): ")

	amount = int(amount)
	if paid:
		paid = 1
	else:
		paid = 0

	cur.execute("INSERT INTO Debts VALUES(?, ?, ?, ?, ?)", (name, date, amount, paid, date_paid))
	dbconn.commit()

def get_debts():
	column = ''
	orderby = ''
	n = ''
	where = raw_input("Enter search query (in field = value form): ")
	if ('all' in where):
		if ',' in where:
			n = where.split(", ")[1]
			for i in ["Name", "Date", "Amount", "Paid", "DatePaid"]:
				if (n == i):
					orderby = n
					break
			if column:
				cur.execute("SELECT * FROM Debts ORDER BY %s ASC" % orderby)
			else:
				print "No such column."
				return
		else:
			cur.execute("SELECT * FROM Debts")
	else:
		where = where.split(' ')
		x = 0
		final = 0
		for i in where:
			if (',' in i):
				n = where[x + 1]
				where[x] = i.rstrip(",")
				final = x
				break
			x += 1
			
		for i in ["Name", "Date", "Amount", "Paid", "DatePaid"]:
			if (where[0] == i):
				column = where[0]
				break
				
		for i in ["Name", "Date", "Amount", "Paid", "DatePaid"]:
			if (n == i):
				orderby = n
				break
				
		for i in ["=", ">", "<", "<>", ">=", "<="]:
			if (i == where[1]):
				op = where[1]
				break
				
		if column and op:
			if orderby:
				cur.execute("SELECT * FROM Debts WHERE %s %s ? ORDER BY %s ASC" % (column, op, orderby), (' '.join(where[2:(final + 1)]),))
			else:
				print ' '.join(where[2:])
				cur.execute("SELECT * FROM Debts WHERE %s %s ?" % (column, op), (' '.join(where[2:]),))
		else:
			print "No such column."
			return
	return cur.fetchall()


def print_results(lines):
	if not lines:
		return
	for result in lines:
		print "Name:", result[0]
		print "Date:", result[1]
		print "Amount (pesos):", result[2]
		print "Paid?:",
		if result[3]:
			print "Yes"
		else:
			print "No"
		print "Date paid (if any): ", result[4]
		print "\n"

def search_debts():
	print_results(get_debts())

def change_record():
	result_list = get_debts()
	print_results(result_list)
	num = raw_input("Which record to change? (number): ")
	to_change = result_list[int(num) - 1]
	print to_change

	print "Leave a line blank to leave it unchanged."
	name = raw_input("Name: ")
	amount =  raw_input ("Amount (pesos): ")
	date = raw_input("Date: ")
	date_paid = raw_input("Date paid: ")
	paid = raw_input("Paid?: ")

	dict = OrderedDict([("Name", name), ("Date", date), ("Amount", amount), ("Paid", paid), ("DatePaid", date_paid)])
	x = 0
	for i in dict:
		if not dict[i]:
			dict[i] = to_change[x]
		x += 1

	dict['Amount'] = int(dict['Amount'])
	for i in ['Name', 'Date', 'DatePaid']:
		dict[i] = "'" + dict[i] + "'"

	set = ""
	for i in dict:
		set += (i + "=" + str(dict[i]) + ",")
	set = set.rstrip(',')
	cur.execute("UPDATE Debts SET %s WHERE Name = ? AND Date = ? AND Amount = ?" % (set), (to_change[0], to_change[1], to_change[2]))
	print "Record changed."
	dbconn.commit()

def remove_record():
	result_list = get_debts()
	if not result_list:
		print "No matches found."
		return
	print_results(result_list)
	num = raw_input("Which record to change? (number): ")
	to_delete = result_list[int(num) - 1]
	print to_delete
	
	question = raw_input("Are you sure you want to delete this record (leave blank to cancel)? ")
	if question:
		cur.execute("DELETE FROM Debts WHERE Name = ? AND Date = ? AND Amount = ?", (to_delete[0], to_delete[1], to_delete[2]))
		dbconn.commit()

def input_loop():
	while True:
		try:
			cmd = raw_input("What to do? ")
			if ('insert' in cmd.lower()):
				insert_debt()
			elif ('search' in cmd.lower()):
				search_debts()
			elif ('change' in cmd.lower()):
				change_record()
			elif('exit' in cmd.lower()):
				exit(0)
			elif ('delete' in cmd.lower()):
				remove_record()
			elif('help' in cmd.lower()):
				print "Available commands: insert, search, change"
		except KeyboardInterrupt:
			exit(0)

if __name__ == '__main__':
	input_loop()

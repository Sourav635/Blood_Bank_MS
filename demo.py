import sqlite3
import Blood_Bank_Sys

file = sqlite3.connect("mydb.db")
cur = file.cursor()


# # 						-->CREATE TABLE FOR DONOR DATA

cur.execute("""CREATE TABLE IF NOT EXISTS Donor_DB(
				DonorID integer PRIMARY KEY AUTOINCREMENT,
				FirstName varchar(255) NOT NULL,
				LastName varchar(255) NOT NULL,
				Gender varchar(10) NOT NULL,
				BloodGRP varchar(10) NOT NULL,
				City varchar(255) NOT NULL,
				Day date);""")


# # 									--> DROP TABLE

# q = """
# 	DROP TABLE Donor_DB
# 	"""
# cur.execute(q)


# # 									--> SELECT QUERY

def showDD(var):
    q = """
		SELECT {} FROM Donor_DB
		""".format(var)
    res = cur.execute(q)
    for x in res.fetchall():
        print(x)


# # 									--> SELECT QUERY

def showRD(var):
    q = """
		SELECT {} FROM Request_DB
		""".format(var)
    res = cur.execute(q)
    for x in res.fetchall():
        print(x)

# # 									--> INSERT DATA


def insertdata(fname, lname, gender, bg, mob, city, date):

    q = """
		INSERT INTO Donor_DB(FirstName,LastName,Gender,BloodGRP,Mobile,City,Day)
		VALUES(?,?,?,?,?,?,?);
	"""

    if gender == 1:
        gender = "Male"
    elif gender == 2:
        gender = "Female"

    cur.execute(q, (fname, lname, gender, bg, mob, city, date))

    file.commit()

# # 										--> Bank Data

def bank_data():

    q = """
		SELECT BloodGRP,COUNT(BloodGRP)
		FROM Donor_DB
		GROUP BY BloodGRP;
		"""
    res = cur.execute(q)
    return res.fetchall()


# #									 ---> CREATE TABLE FOR REQUEST FORM


cur.execute("""CREATE TABLE IF NOT EXISTS Request_DB(
				RecieverID integer PRIMARY KEY AUTOINCREMENT,
				Name varchar(255) NOT NULL,
				Age integer NOT NULL,
				Disease varchar(255),
				Mobile integer NOT NULL
				);""")


# # 						---> INSERT DATA IN REQUEST FORM

def store_data_reqform(name, bg, age, disease, mob):

    q = """
		INSERT INTO Request_DB(Name,BloodGRP,Age,Disease,Mobile)
		VALUES(?,?,?,?,?);
		"""
    res = cur.execute(q, (name, bg, age, disease, mob))
    file.commit()


# # 									--> ADD NEW COLUMN


# q = """
# 	ALTER TABLE Request_DB
# 	ALTER COLUMN LL=
# 	"""
# res = cur.execute(q)


if __name__ == "__main__":

    showDD("*")

    # showRD("*")

    # store_data_reqform()

    # Print Column Names
    cursor = file.execute('select * from Request_DB')
    names = list(map(lambda x: x[0], cursor.description))
    print(names)

    # print(cur.execute("SELECT name FROM sqlite_master where type='table'").fetchall())

    # print(bank_data())

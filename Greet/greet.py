import uuid
import MySQLdb
import _mysql

def greet():
    name = get_name()
    greeting ='"Hello '
    greeting += name
    greeting += '."'
    print greeting

#gets MAC address to identify user
def get_mac():
    return str(uuid.getnode())

#attempts to get the user's name from the acquaintances table
def get_name():
    mac = get_mac()
	#password censored for security reasons
    db = MySQLdb.connect("localhost","root","*****","elric_db")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT firstName, lastName FROM acquaintances WHERE id = '%s';" % mac
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            name = row["firstName"]
        if not rows:
            name = new_acquaintence(mac, db, cursor)
    except _mysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

    return name

#If the MAC address is not in the MySQL table, ELRIC must learn who the user is
def new_acquaintence(mac, db, cursor):
    firstName = raw_input("I don't think I know you. What is your first name?\n")
    lastName = raw_input("Thank you. Now what is your last name?\n")
    name = firstName + " " + lastName
    insertsql = "INSERT INTO acquaintances(id, firstName, lastName) VALUES ('%s', '%s', '%s');" % (mac, firstName, lastName)
    try:
        cursor.execute(insertsql)
        db.commit()
    except _mysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    return name

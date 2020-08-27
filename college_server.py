import mysql.connector as mysql

db = mysql.connect(host="localhost",user="root",password="",database="college")

command_handler = db.cursor(buffered=True)

def auth_admin():
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin":
        if password == "admin":
                admin_accs()
        else:
            print("Wrong password")
    else:
        print("Wrong cradentials")

def admin_accs():
    while 1 :
        print("Admin Menu")
        print("1. New Student Entry")
        print("2. New teacher Entry")
        print("3. Delete Exesting Student")
        print("4. Delete Existing Teacher")
        print("5. Logout")
        user_option = input(str("Option : "))
        if user_option == "1":
            stu_un = input(str("Student Username:"))
            stu_pw = input(str("Student Password:"))
            quary_valu = (stu_un,stu_pw)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s,'student')",quary_valu)
            db.commit()
            print("Registred Successfully")
        elif user_option == "2":
            stu_un = input(str("Teacher Username:"))
            stu_pw = input(str("Teacher Password:"))
            quary_valu = (stu_un,stu_pw)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s,'teacher')",quary_valu)
            db.commit()
            print("Registred Successfully")
        elif user_option == "3":
            stu_un = input(str("Student Username:"))
            quary_valu = (stu_un,'student')
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s ",quary_valu)
            db.commit()
            if command_handler.rowcount < 1 :
                print("User not found")
            else:
                print("Deleted Successfully")
        elif user_option == "4":
            stu_un = input(str("teacher Username:"))
            quary_valu = (stu_un,'teacher')
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s ",quary_valu)
            db.commit()
            if command_handler.rowcount < 1 :
                print("User not found")
            else:
                print("Deleted Successfully")
        elif user_option == "5":
            break
        else:
            print("Option not correct")
        
def auth_student():
    username = input(str("Username : "))
    password = input(str("Password : "))
    quary_valu = (username,password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'student'",quary_valu)
    if command_handler.rowcount <=0 :
        print("Login Failed")
    else:
        print("Welcome ",username)
        stu_accs(username)

def stu_accs(uname):
    while 1:
        print("1. View Register")
        print("2. Downloade register")
        print("3. Logout")
        user_option = input(str("Option :"))
        if user_option == "1":
            print("Your Attadence")
            username = (str(uname),)
            command_handler.execute("SELECT username, date, status FROM attendance WHERE username = %s ",username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == "2":
            print("Downloading the Register record")
            username = (str(uname),)
            command_handler.execute("SELECT username, date, status FROM attendance WHERE username = %s ",username)
            records = command_handler.fetchall()
            for record in records:
                file = open("/home/prem/pythonProjects/register.txt","w")
                file.write(str(records)+"\n")
                file.close()
            print("Downloade Completed")
            
        elif user_option == "3":
            break

def auth_teacher():
    username = input(str("Username : "))
    password = input(str("Password : "))
    quary_valu = (username,password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'teacher'",quary_valu)
    if command_handler.rowcount <=0 :
        print("Login Failed")
    else:
        print("Welcome ",username)
        tch_accs()

def tch_accs():
    while 1:
        print("1. Mark Register")
        print("2. View Register")
        print("3. Logout")
        user_option = input(str("Option :"))
        if user_option == "1":
            print("Mark Student Attadence")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input(str("Date: DD/MM/YYYY :"))
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                # Present | Absent | Late
                status = input(str("Status for "+ str(record) + " P/A/L:"))
                quary_vals = (str(record),date,status)
                command_handler.execute("INSERT INTO attendance (username,date,status) VALUES (%s,%s,%s)",quary_vals)
                db.commit()
                
        elif user_option == "2":
            print("Student Register")
            command_handler.execute("SELECT * FROM attendance ")
            records = command_handler.fetchall()
            for record in records :
                print(record)
                
        elif user_option == "3":
            break
        else:
            print("Invalid options")
    

def main():
    while 1:
        print("Welcome to the college system")
        print("1. Login as Admin")
        print("2. Login as Student")
        print("3. Login as teacher")
        print("4. Exit")

        user_option = input(str("Option :"))
        if user_option == "1":
            print("Admin Login")
            auth_admin()
        elif user_option == "2":
            print("Student Login")
            auth_student()
        elif user_option == "3":
            print("Teacher Login")
            auth_teacher()
        elif user_option == "4":
            break
        else:
            print("Wrong input")


main()

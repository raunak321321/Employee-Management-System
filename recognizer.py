import cv2
import numpy as np
# Employee Management System Using Python
from os import system
import re
# importing mysql connector
import mysql.connector as mysql_db


# making Connection
# con = mysql_db.connect(host="localhost",user="root", password="")
con = mysql_db.connect(host="localhost",user="root", password="",database="employee")

# print(con)

mycursor = con.cursor()

# mycursor.execute("create database employee")

# mycursor.execute("Create table empdata (ID BIGINT primary key,name varChar(1000),emailID text(1000), phoneNO BIGINT,address text(1000),post text(1000),salary BIGINT)")

# make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
# for validating an Phone Number
Pattern = re.compile("(0|91)?[7-9][0-9]{9}")

def attendance(isComing):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('model/trained_model2.yml')
    cascadePath = "haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    cam = cv2.VideoCapture(0)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        
        taken = False
        for(x,y,w,h) in faces:
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
            cv2.putText(im, str(Id), (x,y-40),font, 2, (255,255,255), 3)
            # print(Id)
            # string =
            sql = ''
            c = con.cursor()
            if(isComing):
                sql = 'insert into goingIn(empID) values(' + str(Id) + ')'
                cv2.imshow('im',im)
            else:
                sql = 'insert into goingOut(empID) values(' + str(Id) + ')'
                cv2.imshow('im',im)

            # Executing the sql Query
            # data = str(Id)
            c.execute(sql)

            # Commit() method to make changes in the table
            con.commit()
            taken = True
            break
            
            
        if(taken):
            print("Successfully Attendace taken")
            break    
            
        

        if cv2.waitKey(10) & 0xFF==ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    press = input("Press Any Key To Continue..")
    menu()

# Function to Add_Employ
def Add_Employ():
    print("{:>60}".format("-->>Add Employee Record<<--"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if (check_employee(Id) == True):
        print("Employee ID Already Exists\nTry Again..")
        press = input("Press Any Key To Continue..")
        Add_Employ()
    Name = input("Enter Employee Name: ")
    # checking If Employee Name is Exit Or Not
    if (check_employee_name(Name) == True):
        print("Employee Name Already Exists\nTry Again..")
        press = input("Press Any Key To Continue..")
        Add_Employ
    Email_Id = input("Enter Employee Email ID: ")
    if(re.fullmatch(regex, Email_Id)):
        print("Valid Email")
    else:
        print("Invalid Email")
        press = input("Press Any Key To Continue..")
        Add_Employ()
    Phone_no = input("Enter Employee Phone No.: ")
    if(Pattern.match(Phone_no)):
        print("Valid Phone Number")
    else:
        print("Invalid Phone Number")
        press = input("Press Any Key To Continue..")
        Add_Employ()
    gender = input("Enter Employee gender: ")
    age = input("Enter Employee age: ")
    Salary = input("Enter Employee Salary: ")
    Bonus = input("Enter Employee Bonus: ")
    jobID = input("Enter Employee job id: ")
    data = (Id, Name, gender,age,Phone_no,Email_Id, Salary,Bonus,jobID)
    # Instering Employee Details in
    # the Employee (empdata) Table
    sql = 'insert into Employee values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    c = con.cursor()

    # Executing the sql Query
    c.execute(sql, data)

    # Commit() method to make changes in the table
    con.commit()
    print("Successfully Added Employee Record")
    press = input("Press Any Key To Continue..")
    menu()

# Function To Check if Employee With
# given Name Exist or not
def check_employee_name(employee_name):
    # query to select all Rows from
    # employee(empdata) table
    sql = 'select * from Employee where name=%s'

    # making cursor buffered to make
    # rowcount method work properly
    c = con.cursor(buffered=True)
    data = (employee_name,)

    # Execute the sql query
    c.execute(sql, data)

    # rowcount method to find number
    # of rowa with given values
    r = c.rowcount
    if r == 1:
        return True
    else:
        return False


# Function To Check if Employee With
# given Id Exist or not
def check_employee(employee_id):
    # query to select all Rows from
    # employee(empdata) table
    sql = 'select * from Employee where empId=%s'

    # making cursor buffered to make
    # rowcount method work properly
    c = con.cursor(buffered=True)
    data = (employee_id,)

    # Execute the sql query
    c.execute(sql, data)

    # rowcount method to find number
    # of rowa with given values
    r = c.rowcount
    if r == 1:
        return True
    else:
        return False

# Function to Display_Employ
def Display_Employ():
    print("{:>60}".format("-->> Display Employee Record <<--"))
    # query to select all rows from Employee (empdata) Table
    sql = 'select * from Employee'
    c = con.cursor()

    # Executing the sql query
    c.execute(sql)

    # Fetching all details of all the Employees
    r = c.fetchall()
    for i in r:
        print("Employee Id: ", i[0])
        print("Employee Name: ", i[1])
        print("Employee Gender: ", i[2])
        print("Employee Age.: ", i[3])
        print("Employee Phone Number: ", i[4])
        print("Employee Employee Email: ", i[5])
        print("Employee Salary: ", i[6])
        print("Employee Bonus: ", i[7])
        print("Employee jobID: ", i[8])
        print("\n")
    press = input("Press Any key To Continue..")
    menu()

# Function to Update_Employ
def Update_Employ():
    print("{:>60}".format("-->> Update Employee Record <<--\n"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee(Id) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        Email_Id = input("Enter Employee Email ID: ")
        if(re.fullmatch(regex, Email_Id)):
            print("Valid Email")
        else:
            print("Invalid Email")
            press = input("Press Any Key To Continue..")
            Update_Employ()
        Phone_no = input("Enter Employee Phone No.: ")
        if(Pattern.match(Phone_no)):
            print("Valid Phone Number")
        else:
            print("Invalid Phone Number")
            press = input("Press Any Key To Continue..")
            Update_Employ()
        # Updating Employee details in empdata Table
        sql = 'UPDATE Employee set empEmail = %s, contactNumber = %s where empId = %s'
        data = (Email_Id, Phone_no, Id)
        c = con.cursor()

        # Executing the sql query
        c.execute(sql, data)

        # commit() method to make changes in the table
        con.commit()
        print("Updated Employee Record")
        press = input("Press Any Key To Continue..")
        menu()

# Function to Promote_Employ
def Promote_Employ():
    print("{:>60}".format("-->> Promote Employee Record <<--\n"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee(Id) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        Amount  = int(input("Enter Increase Salary: "))
        #query to fetch salary of Employee with given data
        sql = 'select salary from Employee where empId=%s'
        data = (Id,)
        c = con.cursor()
        
        #executing the sql query
        c.execute(sql, data)
        
        #fetching salary of Employee with given Id
        r = c.fetchone()
        t = r[0]+Amount
        
        #query to update salary of Employee with given id
        sql = 'update Employee set salary = %s where empId = %s'
        d = (t, Id)

        #executing the sql query
        c.execute(sql, d)

        #commit() method to make changes in the table 
        con.commit()
        print("Employee Promoted")
        press = input("Press Any key To Continue..")
        menu()

# Function to Remove_Employ
def Remove_Employ():
    print("{:>60}".format("-->> Remove Employee Record <<--\n"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee(Id) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        #query to delete Employee from empdata table
        sql = 'delete from Employee where empId = %s'
        data = (Id,)
        c = con.cursor()

        #executing the sql query
        c.execute(sql, data)

        #commit() method to make changes in the empdata table
        con.commit()
        print("Employee Removed")
        press = input("Press Any key To Continue..")
        menu()
        
# Function to Search_Employ
def Search_Employ():
    print("{:>60}".format("-->> Search Employee Record <<--\n"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee(Id) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        #query to search Employee from empdata table
        sql = 'select * from Employee where empId = %s'
        data = (Id,)
        c = con.cursor()
        
        #executing the sql query
        c.execute(sql, data)

        #fetching all details of all the employee
        r = c.fetchall()
        for i in r:
            print("Employee Id: ", i[0])
            print("Employee Name: ", i[1])
            print("Employee Gender: ", i[2])
            print("Employee Age.: ", i[3])
            print("Employee Phone Number: ", i[4])
            print("Employee Employee Email: ", i[5])
            print("Employee Salary: ", i[6])
            print("Employee Bonus: ", i[7])
            print("Employee jobID: ", i[8])
            print("\n")
        press = input("Press Any key To Continue..")
        menu()

# Menu function to display menu
def menu():
    system("cls") # what this function does check
    print("{:>60}".format("************************************"))
    print("{:>60}".format("-->> Employee Management System <<--"))
    print("{:>60}".format("************************************"))
    print("1. Add Employee")
    print("2. Display Employee Record")
    print("3. Update Employee Record")
    print("4. Promote Employee Record")
    print("5. Remove Employee Record")
    print("6. Search Employee Record")
    print("7. Take Attendance")
    print("8. Going Outside?")
    print("9. Exit\n")
    print("{:>60}".format("-->> Choice Options: [1/2/3/4/5/6/7] <<--"))

    ch = int(input("Enter your Choice: "))
    if ch == 1:
        system("cls")
        Add_Employ()
    elif ch == 2:
        system("cls")
        Display_Employ()
    elif ch == 3:
        system("cls")
        Update_Employ()
    elif ch == 4:
        system("cls")
        Promote_Employ()
    elif ch == 5:
        system("cls")
        Remove_Employ()
    elif ch == 6:
        system("cls")
        Search_Employ()
    elif ch == 7:
        system("cls")
        attendance(True)
    elif ch == 8:
        system("cls")
        attendance(False)
    elif ch == 9:
        system("cls")
        print("{:>60}".format("Have A NIce Day :)"))
        exit(0)
    else:
        print("Invalid Choice!")
        press = input("Press Any key To Continue..")
        menu()


# Calling menu function
menu()


#pip install opencv-contrib-python
def attendance():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('model/trained_model2.yml')
    cascadePath = "haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    cam = cv2.VideoCapture(0)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        
        for(x,y,w,h) in faces:
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
            cv2.putText(im, str(Id), (x,y-40),font, 2, (255,255,255), 3)
            
        cv2.imshow('im',im)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    

import tkinter
from tkinter import ttk
from PIL import ImageTk
import sqlite3

def enter_data():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    title = title_combobox.get()
    age = age_spinbox.get()
    nationality = nationality_combobox.get()
    registration_status = reg_status_var.get()
    numcourses = numcourses_spinbox.get()
    numsemesters = numsemesters_spinbox.get()

    #Create table
    conn = sqlite3.connect('players.db') 
    table_create_query = '''CREATE TABLE IF NOT EXISTS Student_Data
                            (firstname TEXT, lastname TEXT, title TEXT, age INT, nationality TEXT, 
                            registration_status TEXT, num_courses INT, num_semesters INT)
    '''
    conn.execute(table_create_query)
    #Insert data
    data_insert_query = '''INSERT INTO Student_Data (firstname, lastname, title,
                            age, nationality, registration_status, num_courses, num_semesters) VALUES
                            (?,?,?,?,?,?,?,?)
                            '''
    data_insert_tuple = (first_name, last_name, title, age, nationality, registration_status, numcourses, numsemesters)
    cursor = conn.cursor()
    cursor.execute(data_insert_query, data_insert_tuple)
    conn.commit() 
    conn.close()

    print("First name:", first_name, "Last Name:", last_name, "Title: ", title, "Age:", age, "Nationality", nationality,"Reg. status", registration_status, 'num_course', numcourses, 'numsems', numsemesters)

window = tkinter.Tk()
window.title('Data Entry Form')

frame = tkinter.Frame(window)
frame.pack()
user_info_frame = tkinter.LabelFrame(frame, text="User information")
user_info_frame.grid(row=0, column=0)

first_name_label = tkinter.Label(user_info_frame, text='First Name')
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text='Last Name')
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

title_label = tkinter.Label(user_info_frame, text='Title')
title_combobox = ttk.Combobox(user_info_frame, values=["", "Mr.", "Ms.", "Dr."])
title_label.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)

age_label = tkinter.Label(user_info_frame, text='Age')
age_spinbox = ttk.Spinbox(user_info_frame, from_=18, to=110)
age_label.grid(row=2, column=0)
age_spinbox.grid(row=3, column=0)

nationality_label = tkinter.Label(user_info_frame, text='Nationality')
nationality_combobox = ttk.Combobox(user_info_frame, values=["Africa", "Antarctica", "Asia", "Europe"])
nationality_label.grid(row=2, column=1)
nationality_combobox.grid(row=3, column=1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)


# Saving info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=20)
registered_label = tkinter.Label(courses_frame, text="Registration Status")
reg_status_var = tkinter.StringVar(value="Not registered")
registered_check = tkinter.Checkbutton(courses_frame, text="Currently registered",
                                         variable=reg_status_var, onvalue="Registered", offvalue="Not registered")
logo_img = ImageTk.PhotoImage(file='assets\ceo.jpg')
registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)

numcourses_label = tkinter.Label(courses_frame, text="# completed courses")
numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
numcourses_label.grid(row=0, column=1)
numcourses_spinbox.grid(row=1, column=1)

numsemesters_label = tkinter.Label(courses_frame, text="# completed semesters")
numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox.grid(row=1, column=2)

terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=20)
terms_check = tkinter.Checkbutton(terms_frame, text="I accept terms")
terms_check.grid(row=0, column=0)

button = tkinter.Button(frame, text="Enter Data", command=enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=20)

window.mainloop()
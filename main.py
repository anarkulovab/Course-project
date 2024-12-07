import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

class Users:
    def __init__(self, user_id, login, password, role):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.role = role

class Authorization:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход в систему")
        self.root.config(bg = "lightblue")
        self.conn = sqlite3.connect('language_course.db')
        self.cursor = self.conn.cursor()
        self.create_widgets()

    #Создание окна авторизации
    def create_widgets(self):
        self.root.geometry("300x200")
        self.login_label = ttk.Label(self.root, text="Логин:")
        self.login_label.pack()
        self.login_label.configure(font="helvetica 10", background="lightblue")
        self.login_entry = ttk.Entry(self.root)
        self.login_entry.pack()

        self.password_label = ttk.Label(self.root, text="Пароль:")
        self.password_label.pack()
        self.password_label.configure(font="helvetica 10", background="lightblue")
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack()
        style = ttk.Style()
        style.configure("TButton", background="whitesmoke")
        self.login_button = ttk.Button(self.root, text="Войти", style = "TButton", command=self.login)
        self.login_button.pack()
        self.current_window = None

    #Вход пользователя в систему, вводит логин и пароль
    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        self.cursor.execute("SELECT * FROM Users WHERE login=? AND password=?", (login, password))
        user = self.cursor.fetchone()
        if user:
            user_id, login, password, role = user
            if role == 'student':
                messagebox.showinfo("Успешно", "Авторизация прошла успешно")
                self.student_interface(user_id)
            elif role == 'teacher':
                messagebox.showinfo("Успешно", "Авторизация прошла успешно")
                self.teacher_interface(user_id)
            elif role == 'admin':
                messagebox.showinfo("Успешно", "Авторизация прошла успешно")
                self.admin_interface(user_id)
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")

    # создание экземпляра класса StudentApp
    def student_interface(self, user_id):
        self.root.destroy()
        student_root = tk.Tk()
        student_root.config(bg="lavender")
        student_app = StudentApp(student_root, user_id)
        student_root.mainloop()

    # создание экземпляра класса TeacherApp
    def teacher_interface(self, user_id):
        self.root.destroy()
        teacher_root = tk.Tk()
        teacher_root.config(bg="lavender")
        teacher_app = TeacherApp(teacher_root, user_id)
        teacher_root.mainloop()

    # создание экземпляра класса AdminApp
    def admin_interface(self, user_id):
        self.root.destroy()
        admin_root = tk.Tk()
        admin_root.config(bg = "lavender")
        admin_app = AdminApp(admin_root, user_id)
        admin_root.mainloop()

class StudentApp:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Личный кабинет студента")
        self.root.geometry("400x100")
        self.user_id = user_id
        self.conn = sqlite3.connect('language_course.db')
        self.cursor = self.conn.cursor()
        self.create_widgets()

    def exit_to_auth(self):
        self.root.destroy()
        root = tk.Tk()
        app = Authorization(root)
        root.mainloop()

    def return_to_main(self, window):
        window.destroy()
        self.root.deiconify()

    #Создание окна с кнопками - интерфейс для студента
    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", background="lightblue", width=30, height=2 )
        self.view_schedule_button = ttk.Button(self.root, text="Посмотреть расписание", command=self.view_schedule)
        self.view_schedule_button.pack()
        self.exit_bt = ttk.Button(self.root, text="Выход", command=self.exit_to_auth)
        self.exit_bt.pack()

    #Просмотр расписания
    def view_schedule(self):
        query = """SELECT s.day_of_week, s.start_time, c.name, t.surname, t.name, t.last_name
                   FROM Schedule s
                   INNER JOIN Teachers t ON s.teacher_id = t.teacher_id
                   INNER JOIN Groups g ON s.group_id = g.group_id
                   INNER JOIN Course c ON c.course_id = g.course_id
                   INNER JOIN Students st ON g.group_id = st.group_id
                   WHERE st.user_id = ?"""
        values = (self.user_id,)
        self.root.withdraw()
        self.cursor.execute(query, values)
        schedule = self.cursor.fetchall()

        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Расписание")

        columns = ("day", "time", "course", "teacher", "group")
        table = ttk.Treeview(schedule_window, columns=columns, show='headings')
        table.heading("day", text="День недели")
        table.heading("time", text="Время")
        table.heading("course", text="Курс")
        table.heading("teacher", text="Преподаватель")

        st = ttk.Style()
        st.configure("Treeview", rowheight=25)
        #вывод расписания в виде таблицы
        for col in columns:
            table.column(col, anchor='center')

        for day, time, course, teacher_surname, teacher_name, teacher_last_name in schedule:
            teacher_full = f"{teacher_surname} {teacher_name} {teacher_last_name}"
            table.insert("", "end", values=(day, time, course, teacher_full))
        table.pack(expand=True, fill='both')

        ttk.Button(schedule_window, text="Назад", command=lambda: self.return_to_main(schedule_window)).pack()

class TeacherApp:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Личный кабинет преподавателя")
        self.root.geometry("400x100")
        self.user_id = user_id

        self.conn = sqlite3.connect('language_course.db')
        self.cursor = self.conn.cursor()
        self.create_widgets()
        style = ttk.Style()
        style.configure("TButton", background="lightblue", width=30, height=2)

    def exit_to_auth(self):
        self.root.destroy()
        root = tk.Tk()
        app = Authorization(root)
        root.mainloop()

    def return_to_main(self, window):
        window.destroy()
        self.root.deiconify()

    #Создание окна с кнопками (интерфейс для преподавателя)
    def create_widgets(self):
        self.view_schedule_button = ttk.Button(self.root, text="Посмотреть расписание", command=self.view_schedule)
        self.view_schedule_button.pack()

        self.exit_bt = ttk.Button(self.root, text="Выход", command=self.exit_to_auth)
        self.exit_bt.pack()

    #Просмотр расписания
    def view_schedule(self):
        self.root.withdraw()
        query = """SELECT s.day_of_week, s.start_time, c.name, g.group_id
                   FROM Schedule s
                   INNER JOIN Groups g ON s.group_id = g.group_id
                   INNER JOIN Course c ON c.course_id = g.course_id
                   WHERE s.teacher_id = (SELECT teacher_id FROM Teachers WHERE user_id = ?)
                   ORDER BY g.group_id ASC"""
        values = (self.user_id,)
        self.cursor.execute(query, values)
        schedule = self.cursor.fetchall()

        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Расписание")
        #вывод расписания в виде таблицы
        columns = ("day", "time", "course", "group")
        table = ttk.Treeview(schedule_window, columns=columns, show='headings')
        table.heading("day", text="День недели")
        table.heading("time", text="Время")
        table.heading("course", text="Курс")
        table.heading("group", text="Группа")

        st = ttk.Style()
        st.configure("Treeview", rowheight=25)

        for col in columns:
            table.column(col, anchor='center')
        for day, time, course, group in schedule:
            table.insert("", "end", values=(day, time, course, group))
        table.pack(expand=True, fill='both')
        ttk.Button(schedule_window, text="Назад", command=lambda: self.return_to_main(schedule_window)).pack()

class AdminApp:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Личный кабинет администратора")
        self.root.geometry("400x200")
        self.user_id = user_id
        self.conn = sqlite3.connect('language_course.db')
        self.cursor = self.conn.cursor()
        self.create_widgets()
        style = ttk.Style()
        style.configure("TButton", background="lightblue", width=30, height=2)

    #Создание окна с кнопками (интерфейс администратора)
    def create_widgets(self):
        self.add_student_button = ttk.Button(self.root, text="Добавить нового студента",style = "TButton", command=self.add_student)
        self.add_student_button.pack()

        self.add_teacher_button = ttk.Button(self.root, text="Добавить нового преподавателя", command=self.add_teacher)
        self.add_teacher_button.pack()

        self.add_course_button = ttk.Button(self.root, text="Добавить курс", command=self.add_course)
        self.add_course_button.pack()

        self.edit_schedule_button = ttk.Button(self.root, text="Редактировать расписание", command=self.edit_schedule)
        self.edit_schedule_button.pack()

        self.view_schedule_button = ttk.Button(self.root, text="Отслеживание расписания", command=self.view_schedule)
        self.view_schedule_button.pack()

        self.view_personal_data_button = ttk.Button(self.root, text="Личные данные", command=self.view_personal_data)
        self.view_personal_data_button.pack()

        self.print_form_button = ttk.Button(self.root, text = "Распечатать анкету",  command = self.print_form)
        self.print_form_button.pack()

        self.exit_bt = ttk.Button(self.root, text = "Выход", command = self.exit_to_auth)
        self.exit_bt.pack()

    #Добавление нового студента
    def add_student(self):
        self.root.withdraw()
        add_student_window = tk.Toplevel(self.root)
        add_student_window.geometry("400x500")
        add_student_window.config(bg="lightblue")
        add_student_window.title("Добавить студента")

        ttk.Label(add_student_window, text="ID студента:", background = "lightblue").pack()
        student_id_entry = ttk.Entry(add_student_window)
        student_id_entry.pack()

        ttk.Label(add_student_window, text="ID группы:", background = "lightblue").pack()
        group_id_entry = ttk.Entry(add_student_window)
        group_id_entry.pack()

        ttk.Label(add_student_window, text="Фамилия:", background = "lightblue").pack()
        surname_entry = ttk.Entry(add_student_window)
        surname_entry.pack()

        ttk.Label(add_student_window, text="Имя:", background = "lightblue").pack()
        name_entry = ttk.Entry(add_student_window)
        name_entry.pack()

        ttk.Label(add_student_window, text="Отчество:", background = "lightblue").pack()
        last_name_entry = ttk.Entry(add_student_window)
        last_name_entry.pack()

        ttk.Label(add_student_window, text="E-mail:", background = "lightblue").pack()
        e_mail_entry = ttk.Entry(add_student_window)
        e_mail_entry.pack()

        ttk.Label(add_student_window, text="Телефон:", background = "lightblue").pack()
        phone_entry = ttk.Entry(add_student_window)
        phone_entry.pack()

        ttk.Label(add_student_window, text="Дата рождения:", background = "lightblue").pack()
        birth_date_entry = ttk.Entry(add_student_window)
        birth_date_entry.pack()

        ttk.Label(add_student_window, text="Логин:", background = "lightblue").pack()
        login_entry = ttk.Entry(add_student_window)
        login_entry.pack()

        ttk.Label(add_student_window, text="Пароль:", background = "lightblue").pack()
        password_entry = ttk.Entry(add_student_window, show="*")
        password_entry.pack()


        def save_student():
            student_id = student_id_entry.get()
            group_id = group_id_entry.get()
            surname = surname_entry.get()
            name = name_entry.get()
            last_name = last_name_entry.get()
            e_mail = e_mail_entry.get()
            phone = phone_entry.get()
            birth_date = birth_date_entry.get()
            login = login_entry.get()
            password = password_entry.get()

            # Добавляем пользователя в таблицу Users
            user_query = """INSERT INTO Users (login, password, role)
                            VALUES (?, ?, 'student')"""
            user_values = (login, password)
            self.cursor.execute(user_query, user_values)
            self.conn.commit()

            # Получаем ID добавленного пользователя
            self.cursor.execute("SELECT last_insert_rowid()")
            user_id = self.cursor.fetchone()[0]

            # Добавляем студента в таблицу Students
            student_query = """INSERT INTO Students (student_id, group_id, surname, name, last_name, e_mail, phone, birth_date, user_id)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            student_values = (student_id, group_id, surname, name, last_name, e_mail, phone, birth_date, user_id)
            self.cursor.execute(student_query, student_values)
            self.conn.commit()

            messagebox.showinfo("Успех", "Студент добавлен!")

        ttk.Button(add_student_window, text = "Назад", command = lambda: self.return_to_main(add_student_window)).pack()
        ttk.Button(add_student_window, text="Сохранить", command = save_student).pack()

    #Добавление нового преподавателя
    def add_teacher(self):
        self.root.withdraw()
        add_teacher_window = tk.Toplevel(self.root)
        add_teacher_window.title("Добавить преподавателя")
        add_teacher_window.geometry("400x400")
        add_teacher_window.config(bg="lightblue")

        ttk.Label(add_teacher_window, text="ID преподавателя:", background = "lightblue").pack()
        teacher_id_entry = ttk.Entry(add_teacher_window)
        teacher_id_entry.pack()

        ttk.Label(add_teacher_window, text="Фамилия:", background = "lightblue").pack()
        surname_entry = ttk.Entry(add_teacher_window)
        surname_entry.pack()

        ttk.Label(add_teacher_window, text="Имя:", background = "lightblue").pack()
        name_entry = ttk.Entry(add_teacher_window)
        name_entry.pack()

        ttk.Label(add_teacher_window, text="Отчество:", background = "lightblue").pack()
        last_name_entry = ttk.Entry(add_teacher_window)
        last_name_entry.pack()

        ttk.Label(add_teacher_window, text="E-mail:", background = "lightblue").pack()
        e_mail_entry = ttk.Entry(add_teacher_window)
        e_mail_entry.pack()

        ttk.Label(add_teacher_window, text="Телефон:", background = "lightblue").pack()
        phone_entry = ttk.Entry(add_teacher_window)
        phone_entry.pack()

        ttk.Label(add_teacher_window, text="Логин:", background = "lightblue").pack()
        login_entry = ttk.Entry(add_teacher_window)
        login_entry.pack()

        ttk.Label(add_teacher_window, text="Пароль:", background = "lightblue").pack()
        password_entry = ttk.Entry(add_teacher_window, show="*")
        password_entry.pack()

        def save_teacher():
            teacher_id = teacher_id_entry.get()
            surname = surname_entry.get()
            name = name_entry.get()
            last_name = last_name_entry.get()
            e_mail = e_mail_entry.get()
            phone = phone_entry.get()
            login = login_entry.get()
            password = password_entry.get()

            # Добавляем пользователя в таблицу Users
            user_query = """INSERT INTO Users (login, password, role)
                            VALUES (?, ?, 'teacher')"""
            user_values = (login, password)
            self.cursor.execute(user_query, user_values)
            self.conn.commit()

            # Получаем ID добавленного пользователя
            self.cursor.execute("SELECT last_insert_rowid()")
            user_id = self.cursor.fetchone()[0]

            # Добавляем преподавателя в таблицу Teachers
            teacher_query = """INSERT INTO Teachers (teacher_id, surname, name, last_name, e_mail, phone, user_id)
                               VALUES (?, ?, ?, ?, ?, ?, ?)"""
            teacher_values = (teacher_id, surname, name, last_name, e_mail, phone, user_id)
            self.cursor.execute(teacher_query, teacher_values)
            self.conn.commit()

            messagebox.showinfo("Успех", "Преподаватель добавлен!")

        ttk.Button(add_teacher_window, text="Назад", command=lambda: self.return_to_main(add_teacher_window)).pack()
        ttk.Button(add_teacher_window, text="Сохранить", command=save_teacher).pack()

    #Добавление нового курса
    def add_course(self):
        self.root.withdraw()
        add_course_window = tk.Toplevel(self.root)
        add_course_window.title("Добавить курс")
        add_course_window.geometry("400x200")
        add_course_window.config(bg="lightblue")

        ttk.Label(add_course_window, text="ID курса:", background = "lightblue").pack()
        course_id_entry = ttk.Entry(add_course_window)
        course_id_entry.pack()

        ttk.Label(add_course_window, text="Название курса:", background = "lightblue").pack()
        name_entry = ttk.Entry(add_course_window)
        name_entry.pack()

        ttk.Label(add_course_window, text="Язык:", background = "lightblue").pack()
        language_entry = ttk.Entry(add_course_window)
        language_entry.pack()

        def save_course():
            course_id = course_id_entry.get()
            name = name_entry.get()
            language = language_entry.get()

            query = """INSERT INTO Course (course_id, name, language)
                       VALUES (?, ?, ?)"""
            values = (course_id, name, language)

            self.cursor.execute(query, values)
            self.conn.commit()

            messagebox.showinfo("Успех", "Курс добавлен!")

        ttk.Button(add_course_window, text="Назад", command=lambda: self.return_to_main(add_course_window)).pack()
        ttk.Button(add_course_window, text="Сохранить", command=save_course).pack()
    #Внесение изменений в расписание
    def edit_schedule(self):
        self.root.withdraw()
        edit_schedule_window = tk.Toplevel(self.root)
        edit_schedule_window.title("Редактировать расписание")
        edit_schedule_window.geometry("400x350")
        edit_schedule_window.config(bg="lightblue")

        ttk.Label(edit_schedule_window, text="ID расписания:", background = "lightblue").pack()
        schedule_id_entry = ttk.Entry(edit_schedule_window)
        schedule_id_entry.pack()

        ttk.Label(edit_schedule_window, text="Группа:", background = "lightblue").pack()
        group_id_entry = ttk.Entry(edit_schedule_window)
        group_id_entry.pack()

        ttk.Label(edit_schedule_window, text="День недели:", background = "lightblue").pack()
        day_of_week_entry = ttk.Entry(edit_schedule_window)
        day_of_week_entry.pack()

        ttk.Label(edit_schedule_window, text="Начало:", background = "lightblue").pack()
        start_time_entry = ttk.Entry(edit_schedule_window)
        start_time_entry.pack()

        ttk.Label(edit_schedule_window, text="Конец:", background = "lightblue").pack()
        end_time_entry = ttk.Entry(edit_schedule_window)
        end_time_entry.pack()

        ttk.Label(edit_schedule_window, text="ID преподавателя:", background = "lightblue").pack()
        teacher_id_entry = ttk.Entry(edit_schedule_window)
        teacher_id_entry.pack()

        def save_schedule():
            schedule_id = schedule_id_entry.get()
            group_id = group_id_entry.get()
            day_of_week = day_of_week_entry.get()
            start_time = start_time_entry.get()
            end_time = end_time_entry.get()
            teacher_id = teacher_id_entry.get()

            query = """UPDATE Schedule
                       SET group_id = ?, day_of_week = ?, start_time = ?, end_time = ?, teacher_id = ?
                       WHERE schedule_id = ?"""
            values = (group_id, day_of_week, start_time, end_time, teacher_id, schedule_id)

            self.cursor.execute(query, values)
            self.conn.commit()

            messagebox.showinfo("Успешно", "Расписание обновлено!")

        ttk.Button(edit_schedule_window, text="Назад", command=lambda: self.return_to_main(edit_schedule_window)).pack()
        ttk.Button(edit_schedule_window, text="Сохранить", command=save_schedule).pack()
    #Просмотр расписания
    def view_schedule(self):
        self.root.withdraw()
        view_schedule_window = tk.Toplevel(self.root)
        view_schedule_window.title("Просмотр расписания")
        view_schedule_window.geometry("1000x400")
        view_schedule_window.config(bg="lightblue")

        query = """SELECT s.day_of_week, s.start_time, c.name, t.surname, t.name, t.last_name, g.group_id
                   FROM Schedule s
                   INNER JOIN Teachers t ON s.teacher_id = t.teacher_id
                   INNER JOIN Groups g ON s.group_id = g.group_id
                   INNER JOIN Course c ON c.course_id = g.course_id"""

        self.cursor.execute(query)
        schedule = self.cursor.fetchall()

        columns = ("day", "time", "course", "teacher", "group")
        table = ttk.Treeview(view_schedule_window, columns = columns, show = 'headings')
        table.heading("day", text = "День недели")
        table.heading("time", text = "Время")
        table.heading("course", text = "Курс")
        table.heading("teacher", text = "Преподаватель")
        table.heading("group", text = "Группа")

        for col in columns:
            table.column(col, anchor='center')

        for day, time, course, teacher_surname, teacher_name, teacher_last_name, group in schedule:
            teacher_full = f"{teacher_surname} {teacher_name} {teacher_last_name}"
            table.insert("", "end", values=(day, time, course, teacher_full, group))

        table.pack(expand=True, fill='both')
        ttk.Button(view_schedule_window, text="Назад", command=lambda: self.return_to_main(view_schedule_window)).pack()
    #Метод для вывода личных данных пользователя
    def view_personal_data(self):
        self.root.withdraw()
        view_personal_data_window = tk.Toplevel(self.root)
        view_personal_data_window.title("Личные данные")
        view_personal_data_window.geometry("300x200")
        view_personal_data_window.config(bg="lightblue")

        ttk.Label(view_personal_data_window, text="ID пользователя:", background = "lightblue").pack()
        user_id_entry = ttk.Entry(view_personal_data_window)
        user_id_entry.pack()

        def show_personal_data():
            user_id = user_id_entry.get()

            query = """SELECT * FROM Students WHERE user_id = ?"""
            values = (user_id,)

            self.cursor.execute(query, values)
            student = self.cursor.fetchone()

            if student:
                student_id, group_id, surname, name, last_name, e_mail, phone, birth_date, user_id = student
                ttk.Label(view_personal_data_window, text=f"Студент: {surname} {name} {last_name}\nГруппа: {group_id}\nE-mail: {e_mail}\nТелефон: {phone}\nДата рождения: {birth_date}", background = "gainsboro").pack(pady = 10)

            else:
                query = """SELECT * FROM Teachers WHERE user_id = ?"""
                values = (user_id,)

                self.cursor.execute(query, values)
                teacher = self.cursor.fetchone()

                if teacher:
                    teacher_id, surname, name, last_name, e_mail, phone, user_id = teacher
                    ttk.Label(view_personal_data_window, text=f"Преподаватель: {surname} {name} {last_name}\nE-mail: {e_mail}\nТелефон: {phone} ", background = "lavender").pack(pady = 10)

                else:
                    messagebox.showerror("Ошибка", "Пользователь не найден")
        ttk.Button(view_personal_data_window, text ="Назад", command = lambda: self.return_to_main(view_personal_data_window)).pack()
        ttk.Button(view_personal_data_window, text="Показать", command=show_personal_data).pack()
    #Метод для открытия документа - анкеты в Word
    def print_form(self):
        self.root.withdraw()
        print_form_window = tk.Toplevel(self.root)
        print_form_window.title("Печать анкеты")
        print_form_window.geometry("300x150")
        print_form_window.config(bg="lightblue")

        def open_student_form():
            os.startfile('Анкета для новых студентов.docx')

        def open_teacher_form():
            os.startfile('Анкета для новых преподавателей.docx')

        def open_parent_form():
            os.startfile('Анкета для родителей.docx')

        ttk.Button(print_form_window, text = "Для студента", command = open_student_form).pack()
        ttk.Button(print_form_window, text = "Для преподавателя", command = open_teacher_form).pack()
        ttk.Button(print_form_window, text = "Для законного представителя", command = open_parent_form).pack()
        ttk.Button(print_form_window, text="Назад", command=lambda: self.return_to_main(print_form_window)).pack()

    def return_to_main(self, window):
        window.destroy()
        self.root.deiconify()

    def exit_to_auth(self):
        self.root.destroy()
        root = tk.Tk()
        app = Authorization(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Authorization(root)
    root.mainloop()
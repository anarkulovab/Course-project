from managers import manager_interface
from students import Students
from teachers import Teachers

def sign_up():
    """Функция для регистрации. Пользователь вводит логин. Происходит чтение данных из файла users.
    Для каждой строки в файле проверяется соответствие логина на нулевой элемент строки, при истинности
    далее проверяется наличие логина в файле("_" - означает отсутствие пароля) При наличии выводится ошибка, что пользователь уже зарегистрирован.
    В ином случае пользователю дается возможность придумать пароль, который сохранятся в файле users (нижнее подчеркивание заменяется на пароль"""
    login = input("Введите логин: ")
    found = False
    with open ('users.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        st = lines[i].strip().split(',')
        if st[0] == login:
            found = True
            if st[1] == '_':
                password = input("Придумайте пароль: ")
                st[1] = password
                print("Вы успешно зарегистрировались")
                lines[i] = ','.join(st) + '\n'
            else:
                print("Ошибка. Вы уже зарегистрированы")
                break
    if not found:
        print("Пользователь не найден в системе")

    with open('users.txt', 'w', encoding='utf-8') as file:
        file.writelines(lines)

def log_in(login, password):
    """Функция для авторизации в систему. Происходит чтение файла users, вводится логин и пароль, затем в зависимости от роли
    пользователя (2 элемент строки) открывается соответсвующий интерфейс. При авторизации как преподаватель, создается экземпляр класса Teachers
    значение логина передается методу класса get_teacher_surname. При авторизации как студент также создается экземпляр класса Students
    Значение логина передается методу student_interface. При авторизации как менеджер, вызывается функция из модуля Managers"""
    with open ('users.txt', 'r', encoding='utf-8') as file:
        for line in file:
            st = line.strip().split(',')
            if st[0] == login and st[1] == password:
                if st[2] == 'менеджер':
                    manager_interface()
                elif st[2] == 'преподаватель':
                    teacher = Teachers(login, None, None, None, None, None,None)
                    surname = teacher.get_teacher_surname(login)
                    if surname:
                        teacher.teacher_interface(login, surname)
                elif st[2] == 'студент':
                    student = Students(login, None, None, None, None, None, None, None)
                    student.student_interface(login)
            else:
                print("Неправильный логин или пароль")
                break

def main():
    """Точка входа в программу, реализует основной цикл взаимодействия с пользователем"""
    while True:
        f = input("Выберите действие:\n 1 - Войти\n 2 - Зарегистрироваться\n 3 - Выход: \n")
        if f == '1':
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            log_in(login, password)
        elif f == '2':
            sign_up()
        elif f == '3':
            break
        else:
            print("Ошибка. Введите соответствующее действие")

if __name__ == "__main__":
    main()
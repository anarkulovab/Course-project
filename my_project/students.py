from schedule import Schedule
from user import User
class Students(User):
    """Класс для представления студентов, наследуется от класса User
    Атрибуты (не считая тех, которые наследуются): group - номер группы студента
    используется функция super для доступа к атрибутам и методам родительского класса"""
    def __init__(self, user_id, group, surname, name, last_name, e_mail, phone, birth_date):
        super().__init__(user_id, surname, name, last_name, e_mail, phone, birth_date)
        self.group = group
        self.get_student_group()

    def __str__(self):
        """Возвращает строковое представление данных о студенте"""
        return f"""Личные данные студента: {super().__str__()}
                Группа: {self.group}
                Дата рождения: {self.birth_date}"""

    def get_student_group(self, login):
        """Функция для получения группы студента по его логину из файла students"""
        try:
            with open('students.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    st = line.strip().split(',')
                    if st[0] == login:
                        return st[1]
        except Exception as e:
            print(f"Error {e}")

    def get_schedule_for_student(self, login):
        """Функция для вывода расписания для студента.
        Функции передается логин, вызывается предыдущая функция. Полученные данные записываются в переменную group
        Затем происходит чтение данных из файла schedule, где нулевой элемент каждой строки проверяется на равенство со значением
        group. Создается экземпляр класса и выводится с помощью метода класса"""
        try:
            group = self.get_student_group(login)
            found = False
            with open('schedule.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    st = line.strip().split(',')
                    if group == st[0]:
                        schedule = Schedule(st[0], st[1], st[2], st[3], st[4])
                        print(schedule.without_group())
                        found = True

                if not found:
                    print("Расписание не найдено")

        except Exception as e:
            print(f"Error {e}")

    def student_interface(self, login):
        """Функция для взаимодействия со студентом"""
        while True:
            action = input("Выберите соответствующее действие\n 1. Посмотреть расписание\n 2. Выйти из аккаунта\n")
            if action == '1':
                self.get_schedule_for_student(login)
            elif action == '2':
                print("Выход из аккаунта")
                break
            else:
                print("Ошибка. Введите соответствующий номер действия.")
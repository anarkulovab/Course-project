from schedule import Schedule
from user import User
class Teachers(User):
    """Класс для представления преподавателей, наследуется от класса User.
       Используется функция super для доступа к атрибутам и методам родительского класса"""
    def __init__(self,user_id, surname, name, last_name, e_mail, phone, birth_date):
        super().__init__(user_id, surname, name, last_name, e_mail, phone, birth_date)

    def __str__(self):
        """Возвращает строковое представление данных о преподавателе"""
        return f"Личные данные преподавателя: \n {super().__str__()}"

    def get_teacher_surname(self, login):
        """Функция для получения фамилии преподавателя из файла teachers по логину.
        Происходит чтение файла teachers, где нулевой элемент каждой строки сверяется с логином и возвращает первый элемент - фамилию"""
        try:
            with open('teachers.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    st = line.strip().split(',')
                    if st[0] == login:
                        return st[1]
        except Exception as e:
            print(f"Error {e}")

    def get_schedule_for_teacher(self, surname):
        """Функция для вывода расписания для преподавателя. В функцию передается значение surname, далее
        при чтении файла с расписанием каждый четвертый элемент сравнивается с surname. Если такая строка существует,
        создается экземпляр класса Schedule и выводится расписание с помощью метода класса"""
        found = False
        with open('schedule.txt', 'r', encoding='utf-8') as file:
            for line in file:
                st = line.strip().split(',')
                if surname == st[4]:
                    schedule = Schedule(st[0], st[1], st[2], st[3], st[4])
                    print(schedule.without_teacher())
                    found = True

            if not found:
                print("Расписание не найдено")

    def teacher_interface(self, login, surname):
        """Функция для взаимодействия с преподавателем"""
        while True:
            action = input("Выберите соответствующее действие\n 1. Посмотреть расписание\n 2. Выйти из аккаунта\n")
            if action == '1':
                self.get_schedule_for_teacher(surname)
            elif action == '2':
                print("Выход из аккаунта")
                break
            else:
                print("Ошибка. Введите соответствующий номер действия.")





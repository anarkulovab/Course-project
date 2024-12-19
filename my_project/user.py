class User:
    """Базовый родительский класс для представления пользователей
    Атрибуты класса:
    user_id - логин пользователя
    surname - фамилия
    last_name - имя
    e_mail - электронная почта
    phone - телефон
    birth_date - дата рождения """
    def __init__(self, user_id, surname, name, last_name, e_mail, phone, birth_date):
        self.user_id = user_id
        self.surname = surname
        self.name = name
        self.last_name = last_name
        self.e_mail = e_mail
        self.phone = phone
        self.birth_date = birth_date

    def __str__(self):
        """
        Возвращает строковое представление данных с использованием f-строк
        """
        return f"""Логин: {self.user_id}
                ФИО: {self.surname} {self.name} {self.last_name}
                E-mail: {self.e_mail}
                Телефон: {self.phone}
                День рождения: {self.birth_date}"""
class Schedule:
    """Класс для представления информации о расписании
    Атрибуты:
        group - номер группы
        day_of_week - день недели проведения занятия
        start_time - время начала занятия
        course - название курса
        teacher - фамилия преподавателя, ведущего занятие"""
    def __init__(self, group, day_of_week, start_time, course, teacher):
        self.group = group
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.course = course
        self.teacher = teacher

    def __str__(self):
        """Возвращает строковое представление расписания для группы (для менеджеров). Используется в модуле managers"""
        return f"""Расписание для группы: {self.group}
           День недели: {self.day_of_week}
           Начало: {self.start_time}
           Курс: {self.course}
           Преподаватель: {self.teacher}"""

    def without_group(self):
        """Возвращает строковое представление расписания без номера группы (для студентов).
        Используется в модуле students"""
        return f"""Расписание на день недели: {self.day_of_week}
        Начало: {self.start_time}
        Курс: {self.course}
        Преподаватель: {self.teacher}"""

    def without_teacher(self):
        """Возвращает строковое представление расписания без фамилии преподавателя (для преподавателей.
        Используется в модуле teachers"""
        return f"""Расписание:
           Группа: {self.group}
           День недели: {self.day_of_week}
           Начало: {self.start_time}
           Курс: {self.course}"""


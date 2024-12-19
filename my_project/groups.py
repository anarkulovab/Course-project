class Groups:
    """Класс, представляющий собой информацию о группах
    Атрибуты:
        group_id - номер группы
        teacher - преподаватель
        level - уровень языка
        course название курса """
    def __init__(self, group_id, teacher, level, course):
        self.group_id = group_id
        self.teacher = teacher
        self.level = level
        self.course = course

    def __str__(self):
        """Возвращает строковое представление информации о группе."""
        return f"""Данные о группе: 
            ID: {self.group_id}
            Преподаватель: {self.teacher}
            Уровень языка: {self.level}
            Курс: {self.course}"""
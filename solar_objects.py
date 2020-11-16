# coding: utf-8
# license: GPLv3


class Star:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    type = "star"
    """Признак объекта звезды"""

    m = 0
    """Масса звезды"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус звезды"""

    color = "red"
    """Цвет звезды"""

    image = None
    """Изображение звезды"""

    def color_reassigner(self):
        if self.color == 'red':
            self.color = (255, 0, 0)
        elif self.color == 'orange':
            self.color = (255, 128, 0)
        elif self.color == 'green':
            self.color = (0, 255, 0)
        elif self.color == 'blue':
            self.color = (255, 0, 0)
        elif self.color == 'yellow':
            self.color = (255, 255, 0)
        elif self.color == 'white':
            self.color = (255, 255, 255)
        elif self.color == 'gray':
            self.color = (128, 128, 128)
        elif self.color == 'cyan':
            self.color = (0, 255, 255)


class Planet:
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """

    type = "planet"
    """Признак объекта планеты"""

    m = 0
    """Масса планеты"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус планеты"""

    color = "green"
    """Цвет планеты"""

    image = None
    """Изображение планеты"""

    def color_reassigner(self):
        if self.color == 'red':
            self.color = (255, 0, 0)
        elif self.color == 'orange':
            self.color = (255, 128, 0)
        elif self.color == 'green':
            self.color = (0, 255, 0)
        elif self.color == 'blue':
            self.color = (255, 0, 0)
        elif self.color == 'yellow':
            self.color = (255, 255, 0)
        elif self.color == 'white':
            self.color = (255, 255, 255)
        elif self.color == 'gray':
            self.color = (128, 128, 128)
        elif self.color == 'cyan':
            self.color = (0, 255, 255)
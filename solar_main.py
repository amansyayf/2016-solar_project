# coding: utf-8
# license: GPLv3
# Сяйфетдинов, Хомяков, Серебряков

import tkinter
from tkinter.filedialog import *
from typing import Tuple, Callable
from pygame.font import SysFont, get_default_font
import pygame
import pygame.draw
import solar_vis as sv
import solar_model as sm
import solar_input as si

black = (0, 0, 0)

start_button_exists = False

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


def _round_rect(surface, rect, color, radius=None):
    trans = (255, 255, 1)
    if not radius:
        pygame.draw.rect(surface, color, rect)
        return

    radius = min(radius, rect.width / 2, rect.height / 2)

    r = rect.inflate(-radius * 2, -radius * 2)
    for corn in (r.topleft, r.topright, r.bottomleft, r.bottomright):
        pygame.draw.circle(surface, color, corn, radius)
    pygame.draw.rect(surface, color, r.inflate(radius * 2, 0))
    pygame.draw.rect(surface, color, r.inflate(0, radius * 2))


class Button:
    """
    Button class
    Contructor params:
    surface: surface to display button
    x, y: top-left coordinates
    click_handler: function that is called when the button is clicked,
        default is lambda, doing nothing
    text: text to display on button
    width, height: button size. If not provided, calculated by size of text
    color: button color, default is (224, 224, 224)
    hover_color: button color when hovered, if None (default), no effect
    clicked_color: button color when clicked, if None (default), no effect
    border_color, border_width, border_radius - border params
    font: text font, pygame.font.Font instance, default is Courier New 20
    font_color: default is black
    Methods defined:
    draw(): draws the button on given surface
    handle_event(event): handles mouse events (hover and click). Must be called in
        main loop.
    handle_events(event_list): handles all events in event_list
    To check if given point is inside the button, use 'in' operator:
        if (120, 50) in button: ...
    """

    def __init__(
            self,
            surface: pygame.surface.Surface,
            x: int,
            y: int,
            click_handler: Callable = lambda: None,
            text="",
            width=0,
            height=0,
            color: Tuple[int] = None,
            border_width=0,
            hover_color=None,
            clicked_color=None,
            border_radius=0,
            border_color=None,
            font: pygame.font.Font = None,
            font_color=None
    ):

        self.surface = surface
        self.x = x
        self.y = y
        self.click_handler = click_handler
        self.color = color or (224, 224, 224)
        self.border_width = border_width
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        self.border_radius = border_radius
        self.text = text

        if font is None:
            self.font = SysFont('couriernew', 20)

        text_size = self.font.size(text)
        self.width = width or text_size[0] + self.border_width + 2
        self.height = height or text_size[1] + self.border_width + 2
        self.font_color = font_color or (0, 0, 0)

        self.hovered = False
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def __repr__(self):
        return f'<Button "{self.text}" at ({self.x}, {self.y})>'

    def __contains__(self, point: Tuple[int]):
        return self.rect.collidepoint(point)

    def draw(self):
        color = self.color
        if self.clicked and self.clicked_color:
            color = self.clicked_color
        elif self.hovered and self.hover_color:
            color = self.hover_color

        if not self.border_width:
            _round_rect(self.surface, self.rect, color, self.border_radius)
        else:
            _round_rect(self.surface, self.rect, (0, 0, 0), self.border_radius)
            _round_rect(
                self.surface,
                self.rect.inflate(-self.border_width, -self.border_width),
                color,
                self.border_radius
            )
        text = self.font.render(self.text, 1, self.font_color)
        place = text.get_rect(center=self.rect.center)
        self.surface.blit(text, place)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = event.pos in self
        elif event.type == pygame.MOUSEBUTTONDOWN and event.pos in self:
            self.clicked = True
            self.click_handler()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

    def handle_events(self, event_list):
        for event in event_list:
            self.handle_event(event)


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    global displayed_time
    sm.recalculate_space_objects_positions(space_objects, time_step)
    for body in space_objects:
        sv.update_object_position(space, body)
    physical_time += time_step
    # displayed_time.set("%.1f" % physical_time + " seconds gone")
    # Остатки ткинтера

    if perform_execution:
        # space.after(101 - int(time_speed.get()), execution)
        pygame.display.update()


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    if start_button_exists:
        start_button.text = 'Pause'
        start_button.click_handler = stop_execution()
    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button.text = 'Start'
    start_button.click_handler = start_execution()
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global perform_execution
    perform_execution = False
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = si.read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    sv.calculate_scale_factor(max_distance)

    for obj in space_objects:
        if obj.type == 'star':
            sv.create_star_image(space, obj)
        elif obj.type == 'planet':
            sv.create_planet_image(space, obj)
        else:
            raise AssertionError()


#    sv.update_system_name(filename)


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    si.write_space_objects_data_to_file(out_filename, space_objects)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки pygame: окно, холст, фрейм с кнопками, кнопки.
    """
    global start_button_exists
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    time_step = 1000
    time_speed = 100  # связать в dt

    pygame.init()
    pygame.font.init()

    print('Modelling started!')
    physical_time = 0

    # space - экран
    space = pygame.display.set_mode((sv.window_width, sv.window_height))  # каждый пробег перекрашивать в черный
    clock = pygame.time.Clock()
    finished = False
    FPS = 30
    myfont = pygame.font.SysFont('arial', 28)
    start_button = Button(space, sv.window_width - 50, sv.window_height - 20, start_execution(), 'Start', 50, 20)
    start_button_exists = True
    load_file_button = Button(space, 0, sv.window_height - 20, open_file_dialog(), 'Open file...', 50, 20)
    save_file_button = Button(space, 50, sv.window_height - 20, save_file_dialog(), 'Save file...', 50, 20)

    c = 0
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            start_button.handle_event(event)
            load_file_button.handle_event(event)
            save_file_button.handle_event(event)
            if event.type == pygame.QUIT:
                finished = True
            elif perform_execution:
                execution()
        c += 1
        time_total = c * time_step
        space.fill(black)
        text_surface = myfont.render(('Time in model = ', time_total), False, (0, 0, 0))
        space.blit(text_surface, (sv.window_width - 50, 0))
        start_button.draw()
        load_file_button.draw()
        save_file_button.draw()
        pygame.display.update()
    pygame.quit()
    print('Modelling finished!')


if __name__ == "__main__":
    main()

from tkinter import filedialog as fd 
import tkinter
import pygame

from player import Player
player = None

class Button():
    def __init__(self, x:int, y:int, usual_skin_list:list, hold_skin_list:list, press_skin_list:list, on_click):
        """Класс кнопки

        Args:
            x (int): координата x левого верхнего угла кнопки
            y (int): координата y левого верхнего угла кнопки кнопки
            usual_skin_list (list): Список обычных скинов
            hold_skin_list (list): Список скинов используемых при наведении
            press_skin_list (list): Список скинов используемых при нажатии
            on_click (_type_): функция, которая вызывается при нажатии
        """
        self.x = x
        self.y = y

        self.usual_skin_list = usual_skin_list
        self.hold_skin_list = hold_skin_list
        self.press_skin_list = press_skin_list

        self.usual_skin = pygame.image.load(usual_skin_list[0])
        self.hold_skin = pygame.image.load(hold_skin_list[0]) 
        self.press_skin = pygame.image.load(press_skin_list[0])
        self.image_rect = self.usual_skin.get_rect(topleft=(x, y))
        
        self.x_max = self.image_rect.right
        self.y_max = self.image_rect.bottom

        self.clicked = False
        self.is_on = False

        self.cnt_clicks = 0
        self.on_click = on_click
    
    def is_in(self, coords:tuple)->bool:
        """ Проверяет, внутри ли кнопки координаты.

        Args:
            coords (tuple): координаты для проверки

        Returns:
            bool: True, если внутри.
        """
        x, y = coords
        return self.x <= x and x <= self.x_max and self.y <= y and y <= self.y_max

    def change_skin(self)->None:
        """
        Смена скина кнопки
        """

        self.usual_skin = pygame.image.load(self.usual_skin_list[self.cnt_clicks % len(self.usual_skin_list)])
        self.hold_skin = pygame.image.load(self.hold_skin_list[self.cnt_clicks % len(self.hold_skin_list)]) 
        self.press_skin = pygame.image.load(self.press_skin_list[self.cnt_clicks % len(self.press_skin_list)])
        self.image_rect = self.usual_skin.get_rect(topleft=(self.x, self.y))
        
        self.x_max = self.image_rect.right
        self.y_max = self.image_rect.bottom
    

    def update_event(self, event)->bool:
        """Принимает event.
        Обрабатывает event, если ивент - клик, то проверяет внутри ли он кнопки

        Args:
            event (event): event pygame
        Возвращает True если кнопка нажата.
        """

        if event.type == pygame.MOUSEMOTION:
            if self.is_in(event.pos):
                self.is_on = True
            else:
                self.is_on = False
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_in(event.pos):
            self.clicked = True
            self.cnt_clicks += self.on_click(self.cnt_clicks)
            self.change_skin()
            return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
        return False
    
    def draw(self, screen, update:bool=False):
        """Нарисовать кнопку на экране

        Args:
            screen (screen): Экран, на котором рисовать кнопку 
            update (bool): Если да - делает следующий скин
        """

        if update:
            self.cnt_clicks += 1
            self.change_skin()
        if self.clicked:
            screen.blit(self.press_skin, self.image_rect)
        elif self.is_on:
            screen.blit(self.hold_skin, self.image_rect)
        else:
            screen.blit(self.usual_skin, self.image_rect)


class Text_Field():
    def __init__(self, x:int, y:int, max_y:int, texts:list)->None:
        """Текстовое поле

        Args:
            x (int): x левого верхнего угла
            y (int): y левого верхнего угла
            max_y (int): высота поля
            texts (list): изначальные тексты
        """
        self.x = x
        self.y = y
        self.max_y = max_y
        self.texts = texts
        self.text_selected = None
        self.now_y = 0

        self.font = pygame.font.SysFont(None, 20)

        self.ys = [0]

        y_ = 0
        for i in range(len(texts)):
            txt = self.font.render(texts[i], True, (0, 0, 0))
            y_ += txt.get_size()[1] + 3
            self.ys.append(y_)
        

    def add_text(self, text:str)->None:
        """Добавить текст к text-fieldу

        Args:
            text (str): строка для добавления. обязательно .mp3 на конце.
        """
        if len(text) > 4 and text[-4:] == '.mp3':
            self.texts.append(text)

            txt = self.font.render(text, True, (0, 0, 0))
            self.ys.append(self.ys[-1] + txt.get_size()[1] + 3)
    
    def next_text(self):
        """выбрать следующий текст в списке
        """

        self.text_selected = (self.text_selected + 1) % len(self.texts)
        player.change_song(self.texts[self.text_selected])

    def previous_text(self):
        """выбрать предыдущий текст в списке
        """
        self.text_selected = (self.text_selected - 1 + len(self.texts)) % len(self.texts)
        player.change_song(self.texts[self.text_selected])

    def update_event(self, event)->bool:
        """выбрать текст в списке по клику, либо прокрутить список вверх/вниз
           
            возвращает True, если новый текст выбран
        """
        if self.ys[-1] > self.max_y - self.y:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # вверх
                    self.now_y -= 10
                    self.now_y = max(self.now_y, 0)
                elif event.button == 5:  # вниз
                    self.now_y += 10
                    self.now_y = min(self.now_y, self.ys[-1] - self.max_y + self.y + 10)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.ys[0] <= event.pos[1] + self.now_y - self.y and self.ys[-1] >= event.pos[1] + self.now_y - self.y:
                for i in range(len(self.ys) - 1):
                    if self.ys[i] < event.pos[1] + self.now_y - self.y and self.ys[i + 1] >= event.pos[1] + self.now_y - self.y:
                        self.text_selected = i
                        player.change_song(self.texts[self.text_selected])
                        return True
        return False
                        


    def draw(self, screen)->None:
        """Отрисовка окна

        Args:
            screen (screen): экран для отрисовки
        """
        
        y_now = self.y

        for i in range(len(self.texts)):
            txt = self.font.render(self.texts[i], True, (0, 0, 0))
            size = txt.get_size()

            if y_now + size[1] - self.now_y > self.max_y:
                break

            if y_now >= self.now_y + self.y:
                if i == self.text_selected:
                    pygame.draw.rect(screen, (130, 130, 130), 
                                     pygame.Rect(0, y_now - self.now_y, 854, size[1]))
                screen.blit(txt, (25, y_now - self.now_y))

            y_now += size[1] + 3

songs = None

def init_songs()->None:
    """Определяет переменные songs и player
    """
    global songs, player
    player = Player()
    songs = Text_Field(25, 50, 400, [])
    
    

def on_click_pause_play(cnt_clicks:int)->int:
    """пауза/плей

    Args:
        cnt_clicks (int): количество кликов уже нажатых на button

    Returns:
        int: прошел ли клик(1 если да), 0 иначе
    """
    if songs.text_selected is None:
        return 0
    if cnt_clicks % 2 == 0:
        player.play()
    else:
        player.pause()
    return 1

def on_click_stop(cnt_clicks:int)->int:
    '''
    стоп при нажатии на стоп
    '''
    player.stop()
    return 1

def on_click_next_b(cnt_clicks:int)->int:
    '''
    следующая песня при нажатии на следующую песню
    '''
    songs.next_text()
    return 1

def on_click_past_b(cnt_clicks:int)->int:
    '''
    предыдущая песня при нажатии на предыдущую песню
    '''
    songs.previous_text()
    return 1

def on_click_add_b(cnt_clicks:int)->int:
    '''
    создание окна диалога, вызывается при нажатии на Add Song кнопку
    '''
    top = tkinter.Tk()
    top.withdraw()
    songs.add_text(fd.askopenfilename())
    top.destroy()
    return 1

class UI():
    def __init__(self, screen):
        """Класс для удобства взаимодействия с пользователем

        Args:
            screen (screen): окно на котором все отображается 
        """
        self.screen = screen

        self.play_pause_b = Button(50, 430, ['keys/Play1.png', 'keys/Pause1.png'],
                             ['keys/Play2.png', 'keys/Pause2.png'], ['keys/Play3.png', 'keys/Pause3.png'], on_click_pause_play)
        self.stop_b = Button(75, 430, ['keys/Stop1.png'], ['keys/Stop2.png'], ['keys/Stop3.png'], on_click_stop)
        self.next_b = Button(100, 430, ['keys/Next1.png'], ['keys/Next2.png'], ['keys/Next3.png'], on_click_next_b)
        self.past_b = Button(25, 430, ['keys/Past1.png'], ['keys/Past2.png'], ['keys/Past3.png'], on_click_past_b)

        self.add_b = Button(25, 10, ['keys/add_song1.png'],
                            ['keys/add_song2.png'], ['keys/add_song3.png'], on_click_add_b)

        self.pause_upd = False


    def draw(self):
        '''
        Функция для отрисовки
        '''
        pygame.draw.rect(self.screen, (130, 130, 130), pygame.Rect(0, 0, 854, 40))
        self.play_pause_b.draw(self.screen, update=self.pause_upd)
        self.pause_upd = False
        self.stop_b.draw(self.screen)
        self.next_b.draw(self.screen)
        self.past_b.draw(self.screen)
        self.add_b.draw(self.screen)
        global songs
        songs.draw(self.screen)


    def next_event(self, event):
        '''
        Функция обработки event pygame
        '''
        self.play_pause_b.update_event(event)
        self.pause_upd = self.stop_b.update_event(event) and self.play_pause_b.cnt_clicks % 2 == 1
        self.next_b.update_event(event)
        self.past_b.update_event(event)
        self.add_b.update_event(event)
        global songs
        self.pause_upd = self.pause_upd or songs.update_event(event) and self.play_pause_b.cnt_clicks % 2 == 0
    
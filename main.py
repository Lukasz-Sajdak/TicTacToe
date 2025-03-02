#Autorzy: Arkadiusz Kowalczyk, Krystian Bajerski, Łukasz Sajdak
#Temat: kółko i krzyżyk
#Python 3.9

# Importujremy potrzebne biblioteki
from backend import *
import time

#klasa odpowiadająca za wszystkie przyciski
class Button():
    #konstruktor przypisujący odpowiednie wartości przyciskom
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.cliced = False
        self.font_path = 'ARCADECLASSIC.TTF'
        self.font = pygame.font.Font(self.font_path, 40)

    #metoda sprawdzająca czy kursor znajduje sie ponad przyciskiem
    def is_over(self, pos):
        #warunki sprawdzające czy kursor znajduje sie nad polem przycisku
        if pos[0] > self.x and pos[0] < self.x + self.width: #w poziomie
            if pos[1] > self.y and pos[1] < self.y + self.height: #w pionie
                return True
            return False

    #metoda która wyświetla przycisk na ekranie
    def draw(self, win):
        #warunek sprawdzający czy przycisk został poprawnie stworzony
        if self.text != '':
            text = self.font.render(self.text, 1, (255, 255, 255))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2),
                      self.y + (self.height / 2 - text.get_height() / 2)))

        #warunek sprawdzający czy przycisk został naciśnięty
        if (self.is_over(pygame.mouse.get_pos())):
            if (pygame.mouse.get_pressed()[0] == 1 and self.cliced == False): #naciśnięty
                self.cliced = True
                return True
            if (pygame.mouse.get_pressed()[0] == 0): #nie naciśnięty
                self.cliced = False
                return False

#klasa odpowiadająca za przebieg gry
class Play(object):
    #konstruktor który tworzy okno gry
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((330, 330))
        pygame.display.set_icon(pygame.image.load('Tic-tac-toe.png'))
        pygame.display.set_caption('Kółko i krzyżyk')

    #metoda odpowiadająca za wszystkie akcje związane z klawiszami na klawiaturze oraz zamykaniem okna przez "X"
    @staticmethod
    def events():
        for event in pygame.event.get():
            if event.type == QUIT: #kiedy naciśnieto X - okno sie zamyka
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE: #kiedy nacisnięto esc - okno sie zamyka
                sys.exit()
            if event.type == KEYDOWN and event.key == K_q: #kiedy naciśnieto Q - powrót do menu
                play.main_menu()

    #metoda odpowiadająca za menu główne
    def main_menu(self):
        #tworzenei przycisków
        button_start = Button((0, 0, 0), 64, 64, 192, 32, 'START')
        button_instruction = Button((0, 0, 0), 64, 128, 192, 64, 'INSTRUCTION')
        button_quit = Button((0, 0, 0), 64, 192, 192, 64, 'QUIT')
        pygame.mouse.set_cursor(pygame.cursors.arrow) #zmiana kursora
        #nieskończona pętla odpowiadająca za klikanie
        while True:
            self.screen.fill((0, 0, 0))
            self.events()
            if button_start.draw(self.screen): #wciśniecie przycisku start
                time.sleep(0.1)
                game = Game(self)
                game.run()
            if button_instruction.draw(self.screen): #wciśniecie przycisku instruction
                self.instruction()
            if button_quit.draw(self.screen): #wciśniecie przycisku quit
                sys.exit()
            pygame.display.flip()

    #metoda odpowiadająca za strone instrukcji
    def instruction(self):
        #ustawienie czcionki
        self.font_path = 'ARCADECLASSIC.TTF'
        self.font = pygame.font.Font(self.font_path, 18)
        # zaczytanie tekstu instrukcji z pliku
        f = open("instruction.txt", "r")
        tab = []
        #pętla odpowiadająca za przypisanie konkretnych linijek do tablicy
        for line in f:
            line = line[:len(line)-1]
            tab.append(self.font.render(line, True, (255, 255, 255), (0, 0, 0)))
        #pętla wyświetlająca instrukcje
        while True:
            self.screen.fill((0, 0, 0))
            height=10
            for value in tab:
                self.screen.blit(value, (10,height))
                height += 18
            self.events()
            pygame.display.flip()

#warunek odpowiadający za poprawne uruchomienie
if __name__ == "__main__":
    play = Play()
    play.main_menu()

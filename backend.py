import pygame, sys
from random import randint
from pygame.locals import *

WIN_SIZE = 330 #zmienna zamierająca rozmiar okna

vec2 = pygame.math.Vector2 # Tworzony jest wektor 2-wymiarowy

#klasa odpowiadająca za mechanike gry
class Tic_Tac_Toe:
  #konstruktor odpowiada za przypisanie wszystkich parametrów
  def __init__(self, game, play):
    self.play = play
    self.game = game
    self.game.screen = pygame.display.set_mode([WIN_SIZE]*2)
    self.font_path = 'ARCADECLASSIC.TTF'
    self.font = pygame.font.Font(self.font_path, 20)
    self.board_img = pygame.image.load('Tic-tac-toe.png') # plansza
    self.X_img = pygame.image.load('X.png') #Tu obrazki się łądują i są przypisywane do zmiennych
    self.O_img = pygame.image.load('O.png')
    self.game_array = [[12, 12, 12], # Tablica z grą
                       [12, 12, 12],
                       [12, 12, 12]]
    self.player = randint(0, 1) #losuje który gracz zaczyna 0 - dla O / 1 - dla X
    self.char = '' #zmiana przechowujaca znak gracza ktorego jest ruch
    self.winning_combination = [[(0, 0), (0, 1), (0, 2)], #tablica zawierająca wszystkie mozliwe kombinacje zwyciestw
                                [(1, 0), (1, 1), (1, 2)],
                                [(2, 0), (2, 1), (2, 2)],
                                [(0, 0), (1, 1), (2, 2)],
                                [(0, 2), (1, 1), (2, 0)],
                                [(0, 0), (1, 0), (2, 0)],
                                [(0, 1), (1, 1), (2, 1)],
                                [(0, 2), (1, 2), (2, 2)]]
    self.winner = None #informacja o zwyciezcy
    self.step = 0 #ilosc posuniec

  #metoda sprawdzająca zwyciezce
  def check_winner(self):
    for winning_values in self.winning_combination:
      suma = sum(self.game_array[i][j] for i, j in winning_values)
      if suma in {0, 3}:
        self.winner = 'XO'[suma == 0]

  #metoda odpowiadająca za wyswietlanie znakow
  def draw_objects(self):
    for y, row in enumerate(self.game_array):
      for x, obj in enumerate(row):
        if obj != 12:
          vecX = vec2(x, y) * 110
          self.game.screen.blit(self.X_img if obj else self.O_img, (vecX.x+15, vecX.y+15))

  #metoda odpowiadająca za wyswietlenie panelu końcowego
  def draw_winner(self):
      back_label = self.font.render("Nacisnij  R  by  zagrac  ponownie", True, (255, 255, 255), (0, 0, 0))
      #warunek sprawdzajacy czy ktos wygrał
      if self.winner:
        self.game.screen.fill((0, 0, 0))
        for event in pygame.event.get():
          if event.type == KEYDOWN and event.key == K_r:
            self.game.new_game()
          if event.type == QUIT:
            sys.exit()
          if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        winning_label = self.font.render("Wygral  gracz  "+self.char, True, (255, 255, 255), (255, 0, 0))
        self.game.screen.blit(winning_label, (95, 115))
        self.game.screen.blit(back_label, (20, 160))
      elif self.step == 9:
        self.game.screen.fill((0, 0, 0))
        for event in pygame.event.get():
          if event.type == KEYDOWN and event.key == K_r:
            self.game.new_game()
          if event.type == QUIT:
            sys.exit()
          if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        draw_label = self.font.render("Partia  zakonczyla  sie  remisem", True, (255, 255, 255), (255, 0, 0))
        self.game.screen.blit(draw_label, (20, 115))
        self.game.screen.blit(back_label, (20, 160))

  # Metoda odpowiadajaca za wyswietlanie na ekran
  def draw(self):
    self.game.screen.blit(self.board_img, (0, 0))
    self.draw_objects()
    self.draw_winner()

  # Metoda odpowiadająca za operacje zwiazane z myszka
  def run_game(self):
    current_cell = vec2(pygame.mouse.get_pos())//110
    col, row = map(int, current_cell)
    left_click = pygame.mouse.get_pressed()[0]

    #warunek sprawdzający czy nacisnieto lpm i czy mozna postawic znak
    if left_click and self.game_array[row][col] == 12 and not self.winner and self.step < 9:
      self.game_array[row][col] = self.player
      self.player = not self.player
      if self.player:
        self.char = 'O'
      else:
        self.char = 'X'
      self.step += 1
      self.check_winner()
    else:
      self.draw_winner()

  #metoda odpowiadająca za odpalenie gry
  def run(self):
    self.play.events()
    self.game.screen.fill((0, 0, 0))
    self.draw()
    self.run_game()

#klasa odpowiadająca za gre
class Game:

  #konstruktor odpowiadający za przypisanie odpowiednich wartosci
  def __init__(self, play):
    pygame.init()
    self.play = play
    self.screen = pygame.display.set_mode([WIN_SIZE]*2)
    self.clock = pygame.time.Clock()
    self.tic_tac_toe = Tic_Tac_Toe(self, play)

  #metoda odpowiadajaca za odpalenie gry
  def run(self):
    while True:
      self.tic_tac_toe.run()
      pygame.display.update()

  #metoda odpowiadająca za nową gre
  def new_game(self):
    self.screen.fill((0, 0, 0))
    self.tic_tac_toe = Tic_Tac_Toe(self, self.play)

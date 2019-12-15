from pygai.base import AbstractBoard
import pygame
from itertools import product
from copy import deepcopy

class Piece:
    def __init__(self, value=0, size=(97, 97)):
        self.value = value
        self.surface = -1
        self.rect = -1
        self.index = []
        self.position = pygame.Vector2(-1, -1)
        self.size = size

        if value > 0:
            self.color = 'white'
            self.image_postfix = "-white.png"
        else:
            self.color = 'black'
            self.image_postfix = "-black.png"
        return
    
    def set_image(self, image_path=''):
        self.surface = pygame.transform.scale(pygame.image.load(image_path), self.size)
        self.rect = self.surface.get_rect()
        return

    def set_position(self, pos):
        """
        pos::Coord2D (Column, Row) or (x, y) or (j, i)
        """

        self.index = [int(pos[1]), int(pos[0])]
        self.position = pos
        self.rect = pygame.Rect(self.position, self.size)
        return
    
    def is_clicked(self, event):
        if event.button == 1: # is left button clicked
            if self.rect.collidepoint(event.pos): # is mouse over button
                return True

    def draw(self, win):
        self.rect = pygame.Rect(self.position * 90, self.size)
        win.blit(self.surface, self.rect)

    def get_available_moves(self, board):
        return
    
class Pawn(Piece):
    def __init__(self, value=1):
        super().__init__(value)
        self.set_image("./asset/chess-pawn" + self.image_postfix)
        self.never_moved = True
        self.wscoreboard = [
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                [5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0],
                [1.0,1.0,2.0,3.0,3.0,2.0,1.0,1.0],
                [0.5,0.5,1.0,2.5,2.5,1.0,0.5,0.5],
                [0.0,0.0,0.0,2.0,2.0,0.0,0.0,0.0],
                [0.5,-0.5,-1.0,0.0,0.0,-1.0,-0.5,0.5],
                [0.5,1.0,1.0,-2.0,-2.0,1.0,1.0,0.5],
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            ]
        self.bscoreboard = [
               [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
               [0.5,1.0,1.0,-2.0,-2.0,1.0,1.0,0.5],
               [0.5,-0.5,-1.0,0.0,0.0,-1.0,-0.5,0.5],
               [0.0,0.0,0.0,2.0,2.0,0.0,0.0,0.0],
               [0.5,0.5,1.0,2.5,2.5,1.0,0.5,0.5],
               [1.0,1.0,2.0,3.0,3.0,2.0,1.0,1.0],
               [5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0],
               [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            ]
    
    def get_available_moves(self, board):
        """returns a list of available moves"""

        if self.color == 'black':
            direction = 1
        else:
            direction = -1

        available_moves = []
        
        i, j = int(self.position[1]), int(self.position[0])
        try:
            if board[i + 1 * direction][j] == 0:
                available_moves.append(pygame.Vector2(self.position[1] + 1 * direction, self.position[0]))
        except Exception as e:
            
            pass

        # takes move
        try:
            if board[i + 1 * direction][j - 1] != 0 and board[i + 1 * direction][j - 1].color != self.color:
                available_moves.append(pygame.Vector2(self.position[1] + 1 * direction, self.position[0] - 1))
            if board[i + 1 * direction][j + 1] != 0 and board[i + 1 * direction][j + 1].color != self.color:
                available_moves.append(pygame.Vector2(self.position[1] + 1 * direction, self.position[0] + 1))
        except Exception as e:
            
            pass

        if self.never_moved and board[self.index[0] + 1 * direction][self.index[1]] == 0 and board[self.index[0] + 2 * direction][self.index[1]] == 0:
            available_moves.append(pygame.Vector2(self.position[1] + 2 * direction, self.position[0]))
        
        return available_moves 

class King(Piece):
    def __init__(self, value=40):
        super().__init__(value)
        self.set_image("./asset/chess-king" + self.image_postfix)
        self.wscoreboard = [
                [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
                [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
                [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
                [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
                [-2.0,-3.0,-3.0,-4.0,-4.0,-3.0,-3.0,-2.0],
                [-1.0,-2.0,-2.0,-2.0,-2.0,-2.0,-2.0,-1.0],
                [2.0,2.0,0.0,0.0,0.0,0.0,2.0,2.0],
                [2.0,3.0,1.0,0.0,0.0,1.0,3.0,2.0]
            ]
        self.bscoreboard = [
                [2.0,3.0,1.0,0.0,0.0,1.0,3.0,2.0],
                [2.0,2.0,0.0,0.0,0.0,0.0,2.0,2.0],
                [-1.0,-2.0,-2.0,-2.0,-2.0,-2.0,-2.0,-1.0],
                [-2.0,-3.0,-3.0,-4.0,-4.0,-3.0,-3.0,-2.0],
                [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
                [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
                [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
                [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
            ]
    
    def get_available_moves(self, board):
        i, j = self.index
        available_moves = []

        # Diagonals
        if i - 1 >= 0 and i - 1 < 8 and j - 1 >= 0 and j - 1 < 8 and (board[i - 1][j - 1] == 0 or (board[i - 1][j - 1] != 0 and board[i - 1][j - 1].color != self.color)):
            available_moves.append((i - 1, j - 1))
        if i + 1 >= 0 and i + 1 < 8 and j + 1 >= 0 and j + 1 < 8 and (board[i + 1][j + 1] == 0 or (board[i + 1][j + 1] != 0 and board[i + 1][j + 1].color != self.color)):
            available_moves.append((i + 1, j + 1))
        if i - 1 >= 0 and i - 1 < 8 and j + 1 >= 0 and j + 1 < 8 and (board[i - 1][j + 1] == 0 or (board[i - 1][j + 1] != 0 and board[i - 1][j + 1].color != self.color)):
            available_moves.append((i - 1, j + 1))
        if i + 1 >= 0 and i + 1 < 8 and j - 1 >= 0 and j - 1 < 8 and (board[i + 1][j - 1] == 0 or (board[i + 1][j - 1] != 0 and board[i + 1][j - 1].color != self.color)):
            available_moves.append((i + 1, j - 1))

        # Vertical
        if i - 1 >= 0 and i - 1 < 8 and j >= 0 and j < 8 and (board[i - 1][j] == 0 or (board[i - 1][j] != 0 and board[i - 1][j].color != self.color)):
            available_moves.append((i - 1, j))
        if i + 1 >= 0 and i + 1 < 8 and j >= 0 and j < 8 and (board[i + 1][j] == 0 or (board[i + 1][j] != 0 and board[i + 1][j].color != self.color)):
            available_moves.append((i + 1, j))

        # Horizontal
        if i >= 0 and i < 8 and j + 1 >= 0 and j + 1 < 8 and (board[i][j + 1] == 0 or (board[i][j + 1] != 0 and board[i][j + 1].color != self.color)):
            available_moves.append((i, j + 1))
        if i >= 0 and i < 8 and j - 1 >= 0 and j - 1 < 8 and (board[i][j - 1] == 0 or (board[i][j - 1] != 0 and board[i][j - 1].color != self.color)):
            available_moves.append((i, j - 1))

        return available_moves

class Queen(Piece):
    def __init__(self, value=9):
        super().__init__(value)
        self.rook = Rook(value)

        self.bishop = Bishop(value)

        self.set_image("./asset/chess-queen" + self.image_postfix)
        self.wscoreboard = [
                [-2.0,-1.0,-1.0,-0.5,-0.5,-1.0,-1.0,-2.0],
                [-1.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0],
                [-1.0,0.0,0.5,0.5,0.5,0.5,0.0,-1.0],
                [-0.5,0.0,0.5,0.5,0.5,0.5,0.0,-0.5],
                [0.0,0.0,0.5,0.5,0.5,0.5,0.0,-0.5],
                [-1.0,0.5,0.5,0.5,0.5,0.5,0.0,-1.0],
                [-1.0,0.0,0.5,0.0,0.0,0.0,0.0,-1.0],
                [-2.0,-1.0,-1.0,-0.5,-0.5,-1.0,-1.0,-2.0]
            ]
        self.bscoreboard = [
                [-2.0,-1.0,-1.0,-0.5,-0.5,-1.0,-1.0,-2.0],
                [-1.0,0.0,0.5,0.0,0.0,0.0,0.0,-1.0],
                [-1.0,0.5,0.5,0.5,0.5,0.5,0.0,-1.0],
                [0.0,0.0,0.5,0.5,0.5,0.5,0.0,-0.5],
                [-0.5,0.0,0.5,0.5,0.5,0.5,0.0,-0.5],
                [-1.0,0.0,0.5,0.5,0.5,0.5,0.0,-1.0],
                [-1.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0],
                [-2.0,-1.0,-1.0,-0.5,-0.5,-1.0,-1.0,-2.0]
            ]
    
    def get_available_moves(self, board):
        available_moves = []

        self.rook.index = self.index
        moves_hv = self.rook.get_available_moves(board)

        self.bishop.index = self.index
        moves_diag = self.bishop.get_available_moves(board)

        available_moves.extend(moves_hv)
        available_moves.extend(moves_diag)
        return available_moves

class Rook(Piece):
    def __init__(self, value=5):
        super().__init__(value)
        self.set_image("./asset/chess-rook" + self.image_postfix)
        self.wscoreboard = [
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                [0.5,1.0,1.0,1.0,1.0,1.0,1.0,0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [0.0,0.0,0.0,0.5,0.5,0.0,0.0,0.0]
            ]
        self.bscoreboard = [
                [0.0,0.0,0.0,0.5,0.5,0.0,0.0,0.0],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5],
                [0.5,1.0,1.0,1.0,1.0,1.0,1.0,0.5],
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            ]
    
    def get_available_moves(self, board):
        """4 Directions Vertical & Horizontal"""

        i, j = self.index
        available_moves = []

        # Vertical 
        explore_i = i
        while explore_i >= 0 and j >= 0 and explore_i < 8 and j < 8:
            explore_i += 1
            if explore_i >= 0 and explore_i < 8:
                if board[explore_i][j] == 0:
                    available_moves.append((explore_i, j))
                    continue
                if board[explore_i][j] != 0 and board[explore_i][j].color != self.color:
                    available_moves.append((explore_i, j))
                    break
                else:
                    break

        explore_i = i
        while explore_i >= 0 and j >= 0 and explore_i < 8 and j < 8:
            explore_i -= 1
            if explore_i >= 0 and explore_i < 8:
                if board[explore_i][j] == 0:
                    available_moves.append((explore_i, j))
                    continue
                if board[explore_i][j] != 0 and board[explore_i][j].color != self.color:
                    available_moves.append((explore_i, j))
                    break
                else:
                    break

        # Horizontal
        explore_j = j
        while i >= 0 and explore_j >= 0 and i < 8 and explore_j < 8:
            explore_j += 1
            if explore_j >= 0 and explore_j < 8:
                if board[i][explore_j] == 0:
                    available_moves.append((i, explore_j))
                    continue
                if board[i][explore_j] != 0 and board[i][explore_j].color != self.color:
                    available_moves.append((i, explore_j))
                    break
                else:
                    break
        
        explore_j = j
        while i >= 0 and explore_j >= 0 and i < 8 and explore_j < 8:
            explore_j -= 1
            if explore_j >= 0 and explore_j < 8:
                if board[i][explore_j] == 0:
                    available_moves.append((i, explore_j))
                    continue
                if board[i][explore_j] != 0 and board[i][explore_j].color != self.color:
                    available_moves.append((i, explore_j))
                    break
                else:
                    break

        return available_moves

class Bishop(Piece):
    def __init__(self, value=3):
        super().__init__(value)
        self.set_image("./asset/chess-bishop" + self.image_postfix)
        self.wscoreboard = [
                [-2.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-2.0],
                [-1.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0],
                [-1.0,0.0,0.5,1.0,1.0,0.5,0.0,-1.0],
                [-1.0,0.5,0.5,1.0,1.0,0.5,0.5,-1.0],
                [-1.0,0.0,1.0,1.0,1.0,1.0,0.0,-1.0],
                [-1.0,1.0,1.0,1.0,1.0,1.0,1.0,-1.0],
                [-1.0,0.5,0.0,0.0,0.0,0.0,0.5,-1.0],
                [-2.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-2.0]
            ]
        self.bscoreboard = [
                [-2.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-2.0],
                [-1.0,0.5,0.0,0.0,0.0,0.0,0.5,-1.0],
                [-1.0,1.0,1.0,1.0,1.0,1.0,1.0,-1.0],
                [-1.0,0.0,1.0,1.0,1.0,1.0,0.0,-1.0],
                [-1.0,0.5,0.5,1.0,1.0,0.5,0.5,-1.0],
                [-1.0,0.0,0.5,1.0,1.0,0.5,0.0,-1.0],
                [-1.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0],
                [-2.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-2.0]
            ]

    def get_available_moves(self, board):
        # \   /
        #  \ / Diagonals
        available_moves = []
        i, j = self.index
        
        # diagonal \
        explore_i = i + 1
        explore_j = j + 1
        if explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
            while board[explore_i][explore_j] == 0 and explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                available_moves.append((explore_i, explore_j))
                explore_i += 1
                explore_j += 1
                if explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                    continue
                else:
                    break

        try:
            if board[explore_i][explore_j] != 0 and board[explore_i][explore_j].color != self.color and explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                available_moves.append((explore_i, explore_j))
        except:
            pass

        explore_i = i - 1
        explore_j = j - 1
        if explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
            while board[explore_i][explore_j] == 0 and explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                available_moves.append((explore_i, explore_j))
                explore_i -= 1
                explore_j -= 1
                if explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                    continue
                else:
                    break

        try:
            if board[explore_i][explore_j] != 0 and board[explore_i][explore_j].color != self.color and explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                available_moves.append((explore_i, explore_j))
        except:
            pass

        # diagonal /
        explore_i = i - 1
        explore_j = j + 1
        if explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
            
            while board[explore_i][explore_j] == 0 and explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                available_moves.append((explore_i, explore_j))
                explore_i -= 1
                explore_j += 1
                if explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                    continue
                else:
                    break
        try:
            if board[explore_i][explore_j] != 0 and board[explore_i][explore_j].color != self.color and explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                available_moves.append((explore_i, explore_j))
        except:
            pass
        
        explore_i = i + 1
        explore_j = j - 1
        if explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
            while board[explore_i][explore_j] == 0 and explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                available_moves.append((explore_i, explore_j))
                explore_i += 1
                explore_j -= 1
                if explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                    continue
                else:
                    break
        try:
            if board[explore_i][explore_j] != 0 and board[explore_i][explore_j].color != self.color and explore_i >= 0 and explore_j >= 0 and explore_i < 8 and explore_j < 8:
                available_moves.append((explore_i, explore_j))
        except:
            pass

        return available_moves

class Knight(Piece):
    def __init__(self, value=3):
        super().__init__(value)
        self.set_image("./asset/chess-knight" + self.image_postfix)
        self.wscoreboard = [
                [-5.0,-4.0,-3.0,-3.0,-3.0,-3.0,-4.0,-5.0],
                [-4.0,-2.0,0.0,0.0,0.0,0.0,-2.0,-4.0],
                [-3.0,0.0,1.0,1.5,1.5,1.0,0.0,-3.0],
                [-3.0,0.5,1.5,2.0,2.0,1.5,0.5,-3.0],
                [-3.0,0.5,1.5,2.0,2.0,1.5,0.5,-3.0],
                [-3.0,0.0,1.0,1.5,1.5,1.0,0.0,-3.0],
                [-4.0,-2.0,0.0,0.0,0.0,0.0,-2.0,-4.0],
                [-5.0,-4.0,-3.0,-3.0,-3.0,-3.0,-4.0,-5.0]
            ]
        
        self.bscoreboard = [
                [-5.0,-4.0,-3.0,-3.0,-3.0,-3.0,-4.0,-5.0],
                [-4.0,-2.0,0.0,0.0,0.0,0.0,-2.0,-4.0],
                [-3.0,0.0,1.0,1.5,1.5,1.0,0.0,-3.0],
                [-3.0,0.5,1.5,2.0,2.0,1.5,0.5,-3.0],
                [-3.0,0.5,1.5,2.0,2.0,1.5,0.5,-3.0],
                [-3.0,0.0,1.0,1.5,1.5,1.0,0.0,-3.0],
                [-4.0,-2.0,0.0,0.0,0.0,0.0,-2.0,-4.0],
                [-5.0,-4.0,-3.0,-3.0,-3.0,-3.0,-4.0,-5.0]
            ]

    def get_available_moves(self, board):
        i, j = self.index
        moves = list(product([i-1, i+1],[j-2, j+2])) + list(product([i-2,i+2],[j-1,j+1]))
        available_moves = []
        for i, j in moves:
            if i >= 0 and j >= 0 and i < 8 and j < 8:
                if board[i][j] == 0:
                    available_moves.append((i, j))
                if board[i][j] != 0 and board[i][j].color != self.color:
                    available_moves.append((i, j))
        return available_moves

class ChessBoard(AbstractBoard):
    """
    Represents ChessBoard 
    """

    def __init__(self, blank=False):

        self.turn = 0

        self.surface = -1
        self.position = [0, 0]
        self.pieces = []
        
        self.white_pieces = []
        self.black_pieces = []

        # Initialize a Blank board.
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        if not blank:
            self.board = [
                [Rook(-50), Knight(-30), Bishop(-30), Queen(-90), King(-900), Bishop(-30), Knight(-30), Rook(-50)],
                [Pawn(-10), Pawn(-10), Pawn(-10), Pawn(-10), Pawn(-10), Pawn(-10), Pawn(-10), Pawn(-10)],
                [ 0,  0,  0,  0,  0 ,  0,  0,  0],
                [ 0,  0,  0,  0,  0 ,  0,  0,  0],
                [ 0,  0,  0,  0,  0 ,  0,  0,  0],
                [ 0,  0,  0,  0,  0 ,  0,  0,  0],
                [Pawn( 10), Pawn( 10), Pawn( 10), Pawn( 10), Pawn( 10), Pawn( 10), Pawn( 10), Pawn( 10)],
                [Rook( 50), Knight( 30), Bishop( 30), Queen( 90), King( 900), Bishop( 30), Knight( 30), Rook( 50)]
            ]
        self.board_score = 0

        # Initialize piece
        self.update_pieces_list()
    
    def __str__(self):
        result = ""
        for row in self.board:
            row_result = "["
            for piece in row:
                if type(piece).__name__ == "int":
                    row_result += str(piece) + ", "
                else:
                    row_result += str(piece.value) + ", "
            result += row_result + "]\n"
        return result
    
    def set_image(self, image_path, size=(720,720)):
        """
        Set chessboard image.
        """

        self.surface = pygame.transform.scale(pygame.image.load(image_path), size)
    
    def update_pieces_list(self):
        self.pieces.clear()
        self.black_pieces.clear()
        self.white_pieces.clear()
        white_score = 0
        black_score = 0
        for index_row, row in enumerate(self.board):
            for index_column, piece in enumerate(row):
                if type(piece).__name__ != 'int':
                    if piece.color == 'black':
                        black_score += piece.value
                        self.black_pieces.append(piece)
                    else:
                        white_score += piece.value
                        self.white_pieces.append(piece)

                    piece.set_position(pygame.Vector2(index_column, index_row)) 
                    self.pieces.append(piece)
        self.board_score = white_score - black_score

    def make_move(self, origin, dest):
        """
        Make move on chessboard
        """

        # copy_board = deepcopy(self.board)

        ori0, ori1 = int(origin[0]), int(origin[1])
        dest0, dest1 = int(dest[0]), int(dest[1])
        print("make move", origin, dest)
        # i,j = i,j 
        temp_piece = self.board[ori0][ori1]

        # i,j = y,x, Converts Index to COORD
        temp_piece.position = pygame.Vector2(dest1, dest0)
        temp_piece.index = (dest0, dest1)

        # i,j = i,j 
        self.board[dest0][dest1] = temp_piece
        
        # i,j = i,j 
        self.board[ori0][ori1] = 0

        # Update these lines, to improve apps performance
        # copy_chessboard = ChessBoard(blank=True)
        # copy_chessboard.board = copy_board
        # copy_chessboard.update_pieces_list()
        # copy_chessboard.turn += 1
        
        self.pieces.clear()
        self.update_pieces_list()

        self.turn += 1

        # return copy_chessboard

    def calculate_board_score(self):
        """Calculate current board's score"""
        
        white_score = 0
        black_score = 0

        for piece in self.pieces:
            if piece.color == 'black':
                black_score += piece.value + 1 *piece.bscoreboard[piece.index[0]][piece.index[1]]
            else:
                white_score += piece.value + 1 *piece.wscoreboard[piece.index[0]][piece.index[1]]
            
        return abs(white_score) - abs(black_score)

    def get_possible_moves(self, color=None):
        """Returns current board possible moves."""

        if color:
            if color == 'white':
                return self.get_movements_from(self.white_pieces)
            return self.get_movements_from(self.black_pieces)

        if self.turn % 2 == 0:
            return self.get_movements_from(self.white_pieces)
        return self.get_movements_from(self.black_pieces)

    def get_movements_from(self, pieces):
        available_movements = []
        for piece in pieces:
            movement = {
                'index': piece.index,
                'available_moves': piece.get_available_moves(self.board)
            }
            if len(movement['available_moves']) > 0:
                available_movements.append(movement)
        return available_movements

    def draw(self, win):
        """
        method to draw chessboard
        """

        # draw board
        win.blit(self.surface, self.position)

        # draw pieces
        for piece in self.pieces:
            piece.draw(win)

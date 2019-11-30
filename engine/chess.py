from pygai.base import AbstractBoard
import pygame

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
            print(e)
            pass

        # takes move
        try:
            if board[i + 1 * direction][j - 1] != 0 and board[i + 1 * direction][j - 1].color != self.color:
                available_moves.append(pygame.Vector2(self.position[1] + 1 * direction, self.position[0] - 1))
            if board[i + 1 * direction][j + 1] != 0 and board[i + 1 * direction][j + 1].color != self.color:
                available_moves.append(pygame.Vector2(self.position[1] + 1 * direction, self.position[0] + 1))
        except Exception as e:
            print(e)
            pass

        if self.never_moved:
            available_moves.append(pygame.Vector2(self.position[1] + 2 * direction, self.position[0]))
        
        return available_moves 

class King(Piece):
    def __init__(self, value=40):
        super().__init__(value)
        self.set_image("./asset/chess-king" + self.image_postfix)

class Queen(Piece):
    def __init__(self, value=9):
        super().__init__(value)
        self.set_image("./asset/chess-queen" + self.image_postfix)

class Rook(Piece):
    def __init__(self, value=5):
        super().__init__(value)
        self.set_image("./asset/chess-rook" + self.image_postfix)

class Bishop(Piece):
    def __init__(self, value=3):
        super().__init__(value)
        self.set_image("./asset/chess-bishop" + self.image_postfix)

class Knight(Piece):
    def __init__(self, value=3):
        super().__init__(value)
        self.set_image("./asset/chess-knight" + self.image_postfix)

class ChessBoard(AbstractBoard):
    """
    Represents ChessBoard 
    """

    def __init__(self):
        self.surface = -1
        self.position = [0, 0]
        self.pieces = []

        # Initialize a Blank board.
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.board = [
            [Rook(-5), Knight(-3), Bishop(-3), Queen(-9), King(-40), Bishop(-3), Knight(-3), Rook(-5)],
            [Pawn(-1), Pawn(-1), Pawn(-1), Pawn(-1), Pawn(-1), Pawn(-1), Pawn(-1), Pawn(-1)],
            [ 0,  0,  0,  0,  0 ,  0,  0,  0],
            [ 0,  0,  0,  0,  0 ,  0,  0,  0],
            [ 0,  0,  0,  0,  0 ,  0,  0,  0],
            [ 0,  0,  0,  0,  0 ,  0,  0,  0],
            [Pawn( 1), Pawn( 1), Pawn( 1), Pawn( 1), Pawn( 1), Pawn( 1), Pawn( 1), Pawn( 1)],
            [Rook( 5), Knight( 3), Bishop( 3), Queen( 9), King( 40), Bishop( 3), Knight( 3), Rook( 5)]
        ]

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
        for index_row, row in enumerate(self.board):
            for index_column, piece in enumerate(row):
                if type(piece).__name__ != 'int':
                    piece.set_position(pygame.Vector2(index_column, index_row)) 
                    self.pieces.append(piece)

    def make_move(self, origin, dest):
        """
        Make move on chessboard
        """

        ori0, ori1 = int(origin[0]), int(origin[1])
        dest0, dest1 = int(dest[0]), int(dest[1])

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
        self.pieces.clear()
        self.update_pieces_list()

    def draw(self, win):
        """
        method to draw chessboard
        """

        # draw board
        win.blit(self.surface, self.position)

        # draw pieces
        for piece in self.pieces:
            piece.draw(win)
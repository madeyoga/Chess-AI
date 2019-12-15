import pygame
from engine.chess import ChessBoard
from engine.other import ShowRedTri
from engine.ai import MiniMaxDecision
import time 

board = ChessBoard()

ai = MiniMaxDecision(
    player1='white', 
    player2='black', 
    board=board,
    threshold=2
    )

# print(ai.get_decision('white'))
# exit()

board.set_image('asset/board.png')
 
win = pygame.display.set_mode((1366, 768))
pygame.display.set_caption("Visualize")

selected_piece_moves = []
selected_piece = None
showed_tri = []

turn = 0
def update_turn():
    global turn
    if turn == 0:
        turn = 1
    else:
        turn = 0

def is_valid_turn(piece_color, turn):
    if piece_color == 'white' and turn == 0:
        return True
    if piece_color == 'black' and turn == 1:
        return True
    return False

running = True
end = False
while running:
    time.sleep(1)
    pygame.time.delay(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            clicked_tri = False
            for tri in showed_tri:
                if tri.is_clicked(event):
                    clicked_tri = True

                    # perform player move
                    board.make_move(selected_piece.index, tri.move_index)
                    if selected_piece.value == 1 or selected_piece.value == -1:
                        selected_piece.never_moved = False
                    
                    # Game Logic
                    update_turn()
                    break

            if clicked_tri:
                showed_tri.clear()
                selected_piece_moves.clear()
                selected_piece = None
                break

            for piece in board.pieces:
                if piece.is_clicked(event) and is_valid_turn(piece.color, turn):
                    # indexes
                    selected_piece_moves = piece.get_available_moves(board.board)
                    selected_piece = piece
                    break
    
    # clear
    win.fill((255, 255, 255))

    # draw
    board.draw(win)

    for piece_move in selected_piece_moves:
        tri = ShowRedTri()

        if selected_piece.color == 'black':
            surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("asset/triangle.png"), (97, 97)), 180)
            tri.surface = surface
        else:
            surface = pygame.transform.scale(pygame.image.load("asset/triangle.png"), (97, 97))
            tri.surface = surface

        tri.draw(win, piece_move)
        showed_tri.append(tri)

    # update
    pygame.display.update()

    found_black_king = False
    for piece in board.black_pieces:
        if piece.value == -900:
            found_black_king = True
    
    found_white_king = False
    for piece in board.white_pieces:
        if piece.value == 900:
            found_white_king = True

    if not found_black_king or not found_white_king:
        end = True

    if not end:
        if turn % 2 == 0:
            decision = ai.get_decision('white')
        else:
            decision = ai.get_decision('black')
        board.make_move(decision[0]['index'], decision[0]['move'])
        update_turn()

pygame.quit()
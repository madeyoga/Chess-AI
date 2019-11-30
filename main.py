import pygame
from engine.chess import ChessBoard
from engine.other import ShowRedTri

board = ChessBoard()

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

running = True
while running:
    pygame.time.delay(30)

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
                    break
                    
            if clicked_tri:
                showed_tri.clear()
                selected_piece_moves.clear()
                selected_piece = None
                break

            for piece in board.pieces:
                if piece.is_clicked(event):
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

pygame.quit()
import random

class MiniMaxDecision:
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.threshold_limit = 3
    
    def get_decision(self, player):
        """Returns a decision"""

        possible_moves = self.board.get_possible_moves(player)
        random.shuffle(possible_moves)

        # Best move & score
        best_move = None
        best_score = float('inf')
        if player == self.player1:
            best_score = float('-inf')
        
        # Get Best Possible Move with Minimax
        for movement in possible_moves:
            for piece_move in movement['available_moves']:
                curr_row, curr_col = movement['index']
                dest_row, dest_col = piece_move
                dest_row, dest_col = int(dest_row), int(dest_col)

                # simulate movement
                temp = self.board.board[dest_row][dest_col]
                self.board.board[dest_row][dest_col] = self.board.board[curr_row][curr_col] # = self.board.board[dest_row][dest_col]
                self.board.board[curr_row][curr_col] = 0
                self.board.update_pieces_list()
                self.board.turn += 1

                if player == self.player1:
                    score = self.minimizer(self.board, 0)
                    if score > best_score:
                        best_score = score
                        best_move = {'index': movement['index'], 'move': piece_move}
                else:
                    score = self.maximizer(self.board, 0)
                    if score < best_score:
                        best_score = score
                        best_move = {'index': movement['index'], 'move': piece_move}

                # reset self.board
                self.board.board[curr_row][curr_col] = self.board.board[dest_row][dest_col]
                self.board.board[dest_row][dest_col] = temp
                self.board.update_pieces_list()
                self.board.turn -= 1

        return best_move, best_score
    
    def maximizer(self, board, threshold):
        """"""

        current_score = self.board.calculate_board_score()
        possible_moves = self.board.get_possible_moves()
        random.shuffle(possible_moves)
        
        if current_score != 0 or len(possible_moves) == 0 or threshold >= self.threshold_limit:
            return current_score

        highest_score = float('-inf')
        
        for movement in possible_moves:
            for piece_move in movement['available_moves']:
                curr_row, curr_col = movement['index']
                dest_row, dest_col = piece_move
                dest_row, dest_col = int(dest_row), int(dest_col)
                
                # simulate movement
                temp = self.board.board[dest_row][dest_col]
                self.board.board[dest_row][dest_col] = self.board.board[curr_row][curr_col] # = self.board.board[dest_row][dest_col]
                self.board.board[curr_row][curr_col] = 0
                self.board.update_pieces_list()
                self.board.turn += 1
                
                score = self.minimizer(self.board, threshold + 1)
                highest_score = max(highest_score, score)

                # reset board
                self.board.board[curr_row][curr_col] = self.board.board[dest_row][dest_col]
                self.board.board[dest_row][dest_col] = temp
                self.board.update_pieces_list()
                self.board.turn -= 1
                
                
        
        return highest_score

    def minimizer(self, board, threshold):
        """"""

        current_score = self.board.calculate_board_score()
        possible_moves = self.board.get_possible_moves()
        random.shuffle(possible_moves)

        if current_score != 0 or len(possible_moves) == 0 or threshold >= self.threshold_limit:
            return current_score

        lowest_score = float('inf')
        
        for movement in possible_moves:    
            for piece_move in movement['available_moves']:
                curr_row, curr_col = movement['index']
                dest_row, dest_col = piece_move
                dest_row, dest_col = int(dest_row), int(dest_col)
                
                # simulate movement
                temp = self.board.board[dest_row][dest_col]
                self.board.board[dest_row][dest_col] = self.board.board[curr_row][curr_col] # = self.board.board[dest_row][dest_col]
                self.board.board[curr_row][curr_col] = 0
                self.board.update_pieces_list()
                self.board.turn += 1

                score = self.maximizer(self.board, threshold + 1)
                lowest_score = min(lowest_score, score)

                # reset board
                self.board.board[curr_row][curr_col] = self.board.board[dest_row][dest_col]
                self.board.board[dest_row][dest_col] = temp
                self.board.update_pieces_list()
                self.board.turn -= 1
        
        return lowest_score
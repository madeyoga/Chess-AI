class MiniMaxDecision:
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.threshold_limit = 5
    
    def get_decision(self, player):
        """Returns a decision"""

        possible_moves = self.board.get_possible_moves(player)

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
                # self.board.board[curr_row][curr_col] = self.board.board[dest_row][dest_col]'
                print("init", movement['index'], piece_move)
                self.board.make_move(movement['index'], piece_move)

                if player == self.player1:
                    score = self.minimizer(0)
                    print(score, best_score)
                    if score > best_score:
                        best_score = score
                        best_move = {'index': movement['index'], 'move': piece_move}
                        print('best', best_move, best_score)
                else:
                    score = self.maximizer(0)
                    if score < best_score:
                        best_score = score
                        best_move = {'index': movement['index'], 'move': piece_move}
                        print('best', best_move, best_score)

                # reset self.board
                self.board.make_move(piece_move, movement['index'])
                self.board.turn -= 1
                # self.board.board[dest_row][dest_col] = 0

                print(score, curr_row, curr_col, piece_move)

        return best_move, best_score

    def maximizer(self, threshold):
        """"""

        current_score = self.board.calculate_board_score()
        possible_moves = self.board.get_possible_moves()

        if current_score != 0 or len(possible_moves) == 0 or threshold >= self.threshold_limit:
            return current_score

        highest_score = float('-inf')
        for movement in possible_moves:
            for piece_move in movement['available_moves']:
                curr_row, curr_col = movement['index']
                dest_row, dest_col = piece_move
                
                # simulate movement
                # board.board[curr_row][curr_col] = board.board[dest_row][dest_col]
                print("maximizer", movement['index'], piece_move)
                self.board.make_move(movement['index'], piece_move)

                score = self.minimizer(threshold + 1)
                highest_score = max(highest_score, score)

                # reset board
                # board.board[dest_row][dest_col] = 0
                self.board.make_move(piece_move, movement['index'])
                self.board.turn -= 1
        
        return highest_score

    def minimizer(self, threshold):
        """"""

        current_score = self.board.calculate_board_score()
        possible_moves = self.board.get_possible_moves()

        if current_score != 0 or len(possible_moves) == 0 or threshold >= self.threshold_limit:
            return current_score

        lowest_score = float('inf')
        print(possible_moves)

        for movement in possible_moves:    
            for piece_move in movement['available_moves']:
                curr_row, curr_col = movement['index']
                dest_row, dest_col = piece_move
                
                # simulate movement
                # board.board[curr_row][curr_col] = board.board[dest_row][dest_col]
                print("minimizer", movement['index'], piece_move)
                self.board.make_move(movement['index'], piece_move)

                score = self.maximizer(threshold + 1)
                lowest_score = min(lowest_score, score)

                # reset board
                # board.board[dest_row][dest_col] = 0
                self.board.make_move(piece_move, movement['index'])
                self.board.turn -= 2
        
        return lowest_score
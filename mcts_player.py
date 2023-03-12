import random,copy
class MyPlayer():
    '''Template Docstring for MyPlayer, look at the TODOs''' # TODO a short description of your player

    def __init__(self, my_color,opponent_color, board_size=10):
        self.name = 'username' #TODO: fill in your username
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size

    def move(self,board):
        possible_moves = self.get_all_valid_potential_moves(board,self.my_color)
        depth = 7
        rep = self.repetitions(5,possible_moves,depth)
        max_value = -1
        best_move = ()
        for move in possible_moves:
            value = 0
            if best_move == ():
                best_move = move
            if move in [(0,0),(0,self.board_size-1),(self.board_size-1,0),(self.board_size-1,self.board_size-1)]:
                best_move = move
            if move in [(1,1),(1,0),(0,1),(1,self.board_size-2),(2,self.board_size-2),(2,self.board_size-1),(self.board_size-2,0),(self.board_size-2,1),(self.board_size-1,1),
                                (self.board_size-2,self.board_size-2),(self.board_size-2,self.board_size-1),(self.board_size-1,self.board_size-2)]:    
                if not self.cornercheck(board,move):
                    continue
            for i in range(rep):
                pboard = self.play_move(move,self.opponent_color,copy.deepcopy(board))
                value += self.mcts(copy.deepcopy(pboard),self.my_color,depth)
            if value > max_value:
                best_move = move
                max_value = value
        return best_move
    
    def repetitions(self,time_limit,moves,depth):
        return int((time_limit*1000)/(depth*len(moves)))*2
    
    def mcts(self,board,color,depth):
        if depth == 0:
            return self.eval(board)
        if color == self.my_color:
            possible_moves = self.get_all_valid_potential_moves(board,self.my_color)
            if possible_moves is not None:    
                for pmove in possible_moves:
                    if pmove in [(0,0),(0,self.board_size-1),(self.board_size-1,0),(self.board_size-1,self.board_size-1)]:
                        move = pmove
                        break
                else:    
                    move = random.choice(possible_moves) 
                pboard = self.play_move(move,self.my_color,board)
                value = self.mcts(copy.deepcopy(pboard),self.opponent_color,depth-1)
            else:
                return self.eval(board)
            return value
        else:
            possible_moves = self.get_all_valid_potential_moves(board,self.opponent_color) 
            if possible_moves is not None:    
                for pmove in possible_moves:
                    if pmove in [(0,0),(0,self.board_size-1),(self.board_size-1,0),(self.board_size-1,self.board_size-1)]:
                        move = pmove
                        break
                else:    
                    move = random.choice(possible_moves)
                pboard = self.play_move(move,self.opponent_color,board)
                value = self.mcts(copy.deepcopy(pboard),self.my_color,depth-1)
            else:
                return self.eval(board)
            return value
    
    def cornercheck(self, board, move):
        if move in [(1,1),(1,0),(0,1)] and board[0][0] == self.my_color:
            return True
        elif move in [(1,self.board_size-2),(0,self.board_size-2),(1,self.board_size-1)] and board[0][self.board_size-1] == self.my_color:
            return True
        elif move in [(self.board_size-2,0),(self.board_size-2,1),(self.board_size-1,1)] and board[self.board_size-1][0] == self.my_color:
            return True
        elif move in [(self.board_size-2,self.board_size-2),(self.board_size-2,self.board_size-1),(self.board_size-1,self.board_size-2)] and board[self.board_size-1][self.board_size-1] == self.my_color:
            return True
        else:
            return False
    def eval(self,board):
            (my_score,opp_score) = (1,1)
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == self.my_color:
                        my_score +=1
                    else: 
                        opp_score += 1
            if my_score > opp_score:
                return 1
            elif my_score < opp_score:
                return 0
            else:
                return 0.5
            
    def get_all_valid_potential_moves(self, pboard, players_color):
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                temp_board = [row[:] for row in pboard]
                if self.__is_correct_potential_move([x, y], temp_board, players_color):
                    valid_moves.append( (x, y) )
        if len(valid_moves) <= 0:
            return None
        return valid_moves
    
    def __is_correct_potential_move(self, move, pboard,players_color):
        if pboard[move[0]][move[1]] == -1:
            dx = [-1, -1, -1, 0, 1, 1, 1, 0]
            dy = [-1, 0, 1, 1, 1, 0, -1, -1]
            for i in range(len(dx)):
                if self.confirm_proposed_direction(move, dx[i], dy[i],players_color, pboard):
                    return True
        return False
    
    
    
    def play_move(self,move,players_color,pboard):
        pboard[move[0]][move[1]] = players_color
        dx = [-1,-1,-1,0,1,1,1,0]
        dy = [-1,0,1,1,1,0,-1,-1]
        for i in range(len(dx)):
            if self.confirm_proposed_direction(move,dx[i],dy[i],players_color,pboard):
                pboard = self.change_stones_in_proposed_direction(move,dx[i],dy[i],players_color,pboard)
        return pboard
    
    def change_stones_in_proposed_direction(self,move,dx,dy,players_color,pboard):
        posx = move[0]+dx
        posy = move[1]+dy
        while ((pboard[posx][posy] != players_color)):
            pboard[posx][posy] = players_color
            posx += dx
            posy += dy
        return pboard

    def confirm_proposed_direction(self,move,dx,dy,players_color,pboard):
        if players_color == self.my_color:
            opponent_color = self.opponent_color
        else:
            opponent_color = self.my_color
        posx = move[0]+dx
        posy = move[1]+dy
        if (posx>=0) and (posx<self.board_size) and (posy>=0) and (posy<self.board_size):
            if pboard[posx][posy] == opponent_color:
                while (posx>=0) and (posx<self.board_size) and (posy>=0) and (posy<self.board_size):
                    posx += dx
                    posy += dy
                    if (posx>=0) and (posx<self.board_size) and (posy>=0) and (posy<self.board_size):
                        if pboard[posx][posy] == -1:
                            return False
                        if pboard[posx][posy] == players_color:
                            return True
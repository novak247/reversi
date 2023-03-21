import copy,random,math
class MyPlayer():
    '''Template Docstring for MyPlayer, look at the TODOs''' # TODO a short description of your player

    def __init__(self, my_color,opponent_color, board_size=10):
        self.name = 'essence_of_qui' #TODO: fill in your username
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        self.heuristic_board = self.get_heuristic()
        self.transposition_table = {}

    def get_heuristic(self):
        if self.board_size == 8:
            return [[100, -50, 10, 5, 5, 10, -50, 100],
                    [-50, -75, 1, 1, 1, 1, -75, -50],
                    [10, 1, 3, 2, 2, 3, 1, 10],
                    [5, 1, 2, 1, 1, 2, 1, 5],
                    [5, 1, 2, 1, 1, 2, 1, 5],
                    [10, 1, 3, 2, 2, 3, 1, 10],
                    [-50, -75, 1, 1, 1, 1, -75, -50],
                    [100, -50, 10, 5, 5, 10, -50, 100],
                    ]
        elif self.board_size == 6:
            return [[100, -50, 8, 8, -50, 100],
                    [-50, -75, 1, 1, -75, -50],
                    [8, 1, 2, 2, 1, 8],
                    [8, 1, 2, 2, 1, 8],
                    [-50, -75, 1, 1, -75, -50],
                    [100, -50, 8, 8, -50, 100]
                    ]
        else:
            return [[120, -60, 30, 15, 15, 15, 15, 30, -60, 120],
                    [-60, -90, -10, -10, -10, -10, -10, -10, -90, -60],
                    [30, -10, 15, 3, 3, 3, 3, 15, -10, 30],
                    [15, -10, 3, 3, 3, 3, 3, 3, -10, 15],
                    [15, -10, 3, 3, 3, 3, 3, 3, -10, 15],
                    [15, -10, 3, 3, 3, 3, 3, 3, -10, 15],
                    [15, -10, 3, 3, 3, 3, 3, 3, -10, 15],
                    [30, -10, 15, 3, 3, 3, 3, 15, -10, 30],
                    [-60, -90, -10, -10, -10, -10, -10, -10, -90, -60],
                    [120, -60, 30, 15, 15, 15, 15, 30, -60, 120]
                    ]
        
    def move(self,board):
        maxvalue = -math.inf
        finalmove = ()
        moves = self.get_all_valid_potential_moves(board,self.my_color) 
        depth = 5
        if moves is not None:       
            for pmove in moves:    
                if pmove in [(0,0),(0,self.board_size-1),(self.board_size-1,0),(self.board_size-1,self.board_size-1)]:
                    return pmove
                if finalmove == ():
                    finalmove = pmove
                pboard = self.play_move(pmove,self.opponent_color,copy.deepcopy(board))
                value = self.alphabeta(pboard,-math.inf,math.inf,depth,self.opponent_color)
                if pmove in [(1,1),(1,self.board_size-2),
                            (self.board_size-2,1),
                            (self.board_size-2,self.board_size-2)]:
                    continue
                
                if value > maxvalue:
                    maxvalue = value
                    finalmove = pmove
            return finalmove
        return ()
       

    def eval(self,pboard):
        my_score,opp_score = 0,0
        my_actual_score,opp_actual_score = 0,0
        for i in range(len(pboard)):
            for j in range(len(pboard[0])):
                if pboard[i][j] == self.my_color:
                    my_score += self.heuristic_board[i][j]
                    my_actual_score +=1
                elif pboard[i][j] == self.opponent_color: 
                    opp_score += self.heuristic_board[i][j]
                    opp_actual_score +=1
        return (my_score-opp_score)
    
    def alphabeta(self,board,alpha,beta,depth,color):
        board_key = hash(tuple(map(tuple,board)))
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]
        if depth == 0:
            value = self.eval(board)
            self.transposition_table[board_key] = value
            return value
        if color == self.my_color:
            value = -math.inf
            possible_moves = self.get_ordered_moves(board, self.my_color)
            if possible_moves is not None:    
                for move in possible_moves:
                    pboard = self.play_move(move,self.my_color,board)
                    value = max(value,self.alphabeta(pboard,alpha,beta,depth-1,self.opponent_color))
                    if value > beta:
                        break
                    alpha = max(alpha,value)
            return value
        else:
            value = math.inf
            possible_moves = self.get_ordered_moves(board, self.opponent_color) 
            if possible_moves is not None:    
                for move in possible_moves:
                    pboard = self.play_move(move,self.opponent_color,board)
                    value = min(value,self.alphabeta(pboard,alpha,beta,depth-1,self.my_color))
                    if value < alpha:
                        break
                    beta = min(beta,value)
            return value
    
    def get_ordered_moves(self, board, color):
        possible_moves = self.get_all_valid_potential_moves(board, color)
        ordered_moves = []
        if possible_moves is not None:    
            for move in possible_moves:
                pboard = self.play_move(move,self.my_color,copy.deepcopy(board))
                ordered_moves.append((self.eval(pboard), move))
        ordered_moves.sort(reverse=True)
        return [move for (_, move) in ordered_moves]
    
        # creating boards as states used in alphabeta 
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
        prboard = copy.deepcopy(pboard)
        prboard[move[0]][move[1]] = players_color
        dx = [-1,-1,-1,0,1,1,1,0]
        dy = [-1,0,1,1,1,0,-1,-1]
        for i in range(len(dx)):
            if self.confirm_proposed_direction(move,dx[i],dy[i],players_color,prboard):
                prboard = self.change_stones_in_proposed_direction(move,dx[i],dy[i],players_color,prboard)
        return prboard
    
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

        return False
    def __confirm_direction(self, move, dx, dy, board):
        posx = move[0]+dx
        posy = move[1]+dy
        opp_stones_inverted = 0
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if board[posx][posy] == self.opponent_color:
                opp_stones_inverted += 1
                while (posx >= 0) and (posx <= (self.board_size-1)) and (posy >= 0) and (posy <= (self.board_size-1)):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if board[posx][posy] == -1:
                            return False, 0
                        if board[posx][posy] == self.my_color:
                            return True, opp_stones_inverted
                    opp_stones_inverted += 1

        return False, 0
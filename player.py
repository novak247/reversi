import copy,random
class MyPlayer():
    '''Template Docstring for MyPlayer, look at the TODOs''' # TODO a short description of your player

    def __init__(self, my_color,opponent_color, board_size=10):
        self.name = 'essence_of_qui' #TODO: fill in your username
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size

    def move(self,board):
        maxvalue = -64
        finalmove = ()
        moves = self.get_all_valid_potential_moves(board,self.my_color) 
        possible_moves = self.choose_n_moves(moves,7)
        if possible_moves is not None:    
            for move in moves:
                if move in [(0,0),(0,self.board_size-1),(self.board_size-1,0),(self.board_size-1,self.board_size-1)]:
                    return move
            for pmove in possible_moves:    
                '''covered= self.coverage(board)
                if covered < 0.40:
                    depth = 3
                elif covered < 0.75:
                    depth = 4  
                else:
                    depth = 5'''
                depth = 5
                if finalmove == ():
                    finalmove = pmove
                pboard = self.play_move(move,self.opponent_color,copy.deepcopy(board))
                value = self.alphabeta(copy.deepcopy(pboard),-64,64,depth,self.opponent_color)
                if value >= maxvalue:
                    maxvalue = value
                    finalmove = pmove
            return finalmove
        return ()
    
    def turned(self,board):
        min_inverted = self.board_size**2
        min_move = ()
        for move in self.get_all_valid_potential_moves(board,self.my_color):
            dx = [-1, -1, -1, 0, 1, 1, 1, 0]
            dy = [-1, 0, 1, 1, 1, 0, -1, -1]
            for i in range(len(dx)):
                if self.__confirm_direction(move, dx[i], dy[i], board)[0]:
                    inverted = self.__confirm_direction(move,dx[i],dy[i],board)[1]
            if inverted < min_inverted:
                min_inverted = inverted
                min_move = move
            if min_move ==():   
                min_move = move
        return min_move
    
    def choose_n_moves(self,moves,n):
        if len(moves) <= n:
            return moves
        else:
            return random.sample(moves,n)
    def coverage(self,board):
        occupied = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == self.my_color or board[i][j] == self.opponent_color:
                    occupied += 1
        return occupied/(self.board_size**2)
        

    def eval(self,board):
        (my_score,opp_score) = (1,1)
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == self.my_color:
                    if i == self.board_size -1 or i == 0 or j == self.board_size -1 or j == 0:
                        my_score += 3
                    else:
                        my_score +=1
                elif board[i][j] == self.opponent_color: 
                    if i == self.board_size -1 or i == 0 or j == self.board_size -1 or j == 0:
                        opp_score += 3
                    else:
                        opp_score += 1
        return my_score-opp_score
    
    def alphabeta(self,board,alpha,beta,depth,color):
        if depth == 0:
            return self.eval(board)
        if color == self.my_color:
            value = -64
            potential_value = value
            possible_moves = self.get_all_valid_potential_moves(board,self.my_color)
            if possible_moves is not None:    
                for move in possible_moves:
                    if move in [(0,0),(0,self.board_size-1),(self.board_size-1,0),(self.board_size-1,self.board_size-1)]:   # i wanna play stones in the corner
                        return (self.board_size)**2*2
                    if move in [(1,1),(1,0),(0,1),(1,self.board_size-2),(2,self.board_size-2),(2,self.board_size-1),(self.board_size-2,0),(self.board_size-2,1),(self.board_size-1,1),
                                (self.board_size-2,self.board_size-2),(self.board_size-2,self.board_size-1),(self.board_size-1,self.board_size-2)]:
                        continue
                    pboard = self.play_move(move,self.my_color,board)
                    value = max(value,self.alphabeta(copy.deepcopy(pboard),alpha,beta,depth-1,self.opponent_color))
                    if value > beta:
                        break
                    alpha = max(alpha,value)
            return value
        else:
            value = 64
            potential_value = value
            possible_moves = self.get_all_valid_potential_moves(board,self.opponent_color) 
            if possible_moves is not None:    
                for move in possible_moves:
                    if move in [(0,0),(0,self.board_size-1),(self.board_size-1,0),(self.board_size-1,self.board_size-1)]:         # the same logic goes for minimizing player, just reversed numbers
                        return -(self.board_size)**2*2
                    if move in [(1,1),(1,0),(0,1),(1,self.board_size-2),(2,self.board_size-2),(2,self.board_size-1),(self.board_size-2,0),(self.board_size-2,1),(self.board_size-1,1),
                                (self.board_size-2,self.board_size-2),(self.board_size-2,self.board_size-1),(self.board_size-1,self.board_size-2)]:
                        continue
                    pboard = self.play_move(move,self.opponent_color,board)
                    value = min(value,self.alphabeta(copy.deepcopy(pboard),alpha,beta,depth-1,self.my_color))
                    if value < alpha:
                        break
                    beta = min(beta,value)
            return value

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
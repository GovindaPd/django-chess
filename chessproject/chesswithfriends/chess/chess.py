from .chessbase import ChessBase
from .chessmixin import ChessMixin
from .chessman_moves import *
from copy import deepcopy
#import multiprocessing


class Chess(ChessBase,ChessMixin):
    def __init__(self, turn : str, board : dict, castle : dict, flag : bool = False):
        #here flag define in self.get_both_data what we want in data like only moves data or all other data included
        self.for_who, self.for_opp = ('W','B') if turn=='W' else ('B','W')
        self.chessboard = board
        self.castle = castle
        self.my,self.opp = self.get_both_data(self.for_who, self.chessboard, self.castle, flag)
        # self.count()

    @classmethod
    def count(cls):
        #count hou many time objecct is created (function called)
        cls.loopcount +=1

    @classmethod
    def play(cls, chessboard : dict, castle : dict, turn : str, cur_depth=3, alpha=-900, beta=900, best_move=None, depth=1, maximiser=True):
        #here =>depth is used for getting the current depth level increment order
    
        if not cls.is_valid(chessboard): 
            print("error chessboard is not valid")
            return (None,0)
        else:
            obj = cls(turn, chessboard, castle, False) if cur_depth !=0 else cls(turn, chessboard, castle, True)
            #below line for if error occure in code
            if obj.my == None and obj.opp == None:
                print("error in code from play method")
                return (None, 0)
            
            if cur_depth ==0 or obj.is_checkmate() or obj.is_stalemate():
                if obj.is_checkmate() or obj.is_stalemate():
                    return (None, -900 +10*depth) if maximiser else (None, 900-10*depth)
                # elif obj.is_stalemate():
                #     return (None, -900+10*depth) if maximiser else (None, 900-10*depth)
                else:
                    return (None, +(obj.statistics())) if maximiser else (None, -(obj.statistics()))
            else:
                all_moves = [(man, obj.my['chessmans_positions'][man], move) for man,moves in obj.my['legal_moves'].items() for move in moves]
                                
                if maximiser==False:  #minimiser
                    mineval = 900
                    for man, cur_box_id, next_box_id in all_moves:
                        boardcopy = obj.chessboard.copy()
                        castlecopy = obj.castle.copy()
                        Chess.push(obj.for_who, boardcopy, castlecopy, cur_box_id, next_box_id, man)
                                                
                        m, points = cls.play(boardcopy, castlecopy, obj.for_opp, cur_depth-1, alpha, beta, depth+1, True)
                        
                        if points < mineval:
                            mineval = points
                            best_move = (man, cur_box_id, next_box_id,)
                        
                        beta = min(beta, mineval)
                        if beta <= alpha:
                            break
                    return best_move, mineval
                
                else:   #maximiser
                    maxeval = -900
                    for man, cur_box_id, next_box_id in all_moves:

                        boardcopy = obj.chessboard.copy()
                        castlecopy = obj.castle.copy()
                        Chess.push(obj.for_who, boardcopy, castlecopy, cur_box_id, next_box_id, man)
                        m,points = cls.play(boardcopy, castlecopy, obj.for_opp, cur_depth-1, alpha, beta, depth+1, maximiser=False,)

                        if points > maxeval:
                            maxeval = points
                            best_move = (man, cur_box_id, next_box_id,)

                        alpha = max(alpha, maxeval)
                        if beta <= alpha:
                            break
                    return best_move, maxeval

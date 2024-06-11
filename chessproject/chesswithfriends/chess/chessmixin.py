from .chessman_moves import *

class ChessMixin:
    """should't be instaiate without child class """
    def __init__(self):
        pass

    def is_checkmate(self):     #if opponent is in check and does not have any legal moves
        if (self.my['kp'] in self.opp['all_moves'] and len(self.my['legal_moves'])==0):return True
        else:return False
       
    def is_stalemate(self):
        return True if (self.my['kp'] not in self.opp['all_moves'] and len(self.my['legal_moves'])==0) else False
       
    def is_insufficient_piece(self):
        if len(self.chessboard.values())==2: return True
        elif len(self.chessboard.values())==3:
            for piece in self.chessboard.values():
                if piece[1]!='K': return True if piece[1]=='H' or piece[1]=='C' else False
        else:return False

    @classmethod
    def print_chessboard(cls, chessboard=None):
        """ this method print chessoard in console. """
        board = chessboard if chessboard!=None else cls.chessboard
        index=0
        print("+-+-+-+-+-+-+-+-+")
        for i in chessboard.values():
            if i=='':
                print("| ",end="")
            else:
                print("|"+cls.gui_text[i[:2]], end='')

            if index==7:
                index=0
                print("|\n+-+-+-+-+-+-+-+-+")
            else:
                index += 1
    
    @classmethod
    def in_check(cls, kp, opp_all_moves):
        return True if kp in opp_all_moves else False

    @classmethod
    def is_valid(cls,chessboard):
        return True if cls.WK in chessboard.values() and cls.BK in chessboard.values() else False    
        
    @classmethod
    def checkmate(cls,kp,legal_moves,opp_all_moves,):
        return True if kp in opp_all_moves and len(legal_moves)==0 else False
    
    @classmethod
    def stalemate(cls,kp,legal_moves,opp_all_moves,):
        return True if kp not in opp_all_moves and len(legal_moves)==0 else False

    @classmethod
    def insufficient_piece(cls,chessboard):
        avail_chessmans = [i for i in chessboard.values() if i!='']
        if len(avail_chessmans)==2: return True

        elif len(avail_chessmans)==3:
            return all([True if piece[1]=='K' or piece[1]=='C' or piece[1]=='H' else False for piece in avail_chessmans])
        
        else: return False

    @classmethod
    def one_side_has_insufficient_piece(cls, for_, chessboard):
        avail_chessmans = [i for i in chessboard.values() if i!='' and i[0]==for_ ]
        if len(avail_chessmans)==1: return True
        elif len(avail_chessmans)==2:
            return all([ True if piece[1]=='K' or piece[1]=='C' or piece[1]=='H' else False for piece in avail_chessmans ])
        else: return False

    @classmethod
    def push(cls, for_my,board, castle, from_, to_, man):
        promoting_row,for_opp = (0,'W') if for_my == 'B' else (7,'B')
        if man[1]=='S' and int(to_[0])==promoting_row:#promot pawn
            man = man[0]+'Q'+man[2:]

        if man[1] in ['K','E']:   # or (board[to_]!='' and board[to_][1] in ['K','E']):
            cls.castle_handle(board,castle,from_,to_,man)

        if board[to_]!='' and board[to_][1]=='E' and castle[for_opp]['km']==False:
            if castle[for_opp]['lem']==False and board[to_][3]=='0':    #left
                castle[for_opp]['lem']=True
                if castle[for_opp]['rem']==True:
                    castle[for_opp]['km']=True
            if castle[for_opp]['rem']==False and board[to_][3]=='7':    #right
                castle[for_opp]['rem']=True
                if castle[for_opp]['lem']==True:
                    castle[for_opp]['km']=True

        board[to_] = man
        board[from_] = ''
    
    @classmethod
    def castle_handle(cls, board, castle, from_, to_, man):
        if castle[man[0]]['km']==False and (man[1]=='E' or man[1]=='K'):
            if man[1]=='K':
                if int(from_[1])-int(to_[1])==2:
                    castle[man[0]]['km'] = True
                    castle[man[0]]['lem'] = True
                    board[castle[man[0]]['lep']]=''
                    board[castle[man[0]]['lboxes'][0]]=castle[man[0]]['leid']
                elif int(from_[1])-int(to_[1])==-2:
                    castle[man[0]]['km'] = True
                    castle[man[0]]['rem'] = True
                    board[castle[man[0]]['rep']]=''
                    board[castle[man[0]]['rboxes'][0]]=castle[man[0]]['reid']
                else:
                    castle[man[0]]['km'] = True
            else:
                if man[3]=='0':
                    if castle[man[0]]['lem']==False:
                        castle[man[0]]['lem'] = True
                        if castle[man[0]]['rem'] == True:
                            castle[man[0]]['km'] = True
                else:
                    if castle[man[0]]['rem']==False:
                        castle[man[0]]['rem'] = True
                        if castle[man[0]]['lem'] == True:
                            castle[man[0]]['km'] = True

    
        # if self.in_check(self.my['kp'], self.opp['all_moves']):
        #     #blank check point = -0.1
        #     final_score += self.check_threats_danger()
        # else:
        #     final_score += self.tactial_moves()
        #     #well protected king can stop unnessary threats
        #     final_score += .50 if self.well_protected_king(int(self.my['kp'][0]), int(self.my['kp'][0]), self.for_who) else -0.50
        #     #final_score += .50 if self.well_protected_king(int(self.opp['kp'][0]),int(self.opp['kp'][0]),self.for_opp) else -0.50
                       
    def statistics(self):
        final_score = 0.0
        my_piece_score = 0.0
        my_board_score = 0.0
        opp_piece_score = 0.0
        opp_board_score = 0.0

        #fork and captur
        final_score += self.tactial_moves()
        
        if self.is_endgame():
            for i in self.my['avail_chessmans']:
                if i[1]!='k':
                    my_piece_score += self.chessman_points[i[1]]
                    my_board_score += self.EVAL[i[:2]][self.my['chessmans_positions'][i]] * 0.01
                else:
                    my_board_score += self.EVAL['EK'][self.opp['chessmans_positions'][i]] * 0.01
  
            for i in self.opp['avail_chessmans']:
                opp_piece_score += self.chessman_points[i[1]]
                if i[1]!='k':
                    my_piece_score += self.chessman_points[i[1]]
                    opp_board_score += self.EVAL[i[:2]][self.opp['chessmans_positions'][i]] * 0.01
                else:
                    #here EK meas End game king position evolution cause king has to be more active
                    opp_board_score += self.EVAL['EK'][self.opp['chessmans_positions'][i]] * 0.01
    
        else:
            final_score += .50 if self.well_protected_king(int(self.my['kp'][0]), int(self.my['kp'][0]), self.for_who) else -0.50
            
            for i in self.my['avail_chessmans']:
                my_piece_score += self.chessman_points[i[1]]
                my_board_score += self.EVAL[i[:2]][self.my['chessmans_positions'][i]] * 0.01

            for i in self.opp['avail_chessmans']:
                opp_piece_score += self.chessman_points[i[1]]
                opp_board_score += self.EVAL[i[:2]][self.opp['chessmans_positions'][i]] * 0.01

        #Material Advantage:
        final_score += my_piece_score-opp_piece_score
        #Scores for chessman positon on board 
        final_score += .20 if my_board_score > opp_board_score else -.20 if my_board_score!= opp_board_score else 0
        #control over center score
        final_score += self.control_over_center()
        #more active pices would get more points
        final_score += self.piece_activity()
        #a good pawn structur can lead a good game
        final_score += self.pawn_structure_score()
        
        return final_score

    #paset chect_threat danger here

    def tactial_moves(self):
        travers_chessmans = {}
        for man, threated_boxes in self.my['additional_data']['provide_threats_to_opp'].items():
            #fork
            if len(threated_boxes) > 1:
                for box in threated_boxes:
                    #here dp is temp vaiable dead points something 
                    dp = travers_chessmans.get(man, 0)
                    if len(self.opp['additional_data']['box_backups'].get(box,[])) == 0:
                        if self.chessboard[box][1] != 'K':
                            travers_chessmans.setdefault(man, dp+self.chessman_points[self.chessboard[box][1]])
                            # my_fork_points += chessman_points[self.chessboard[box][1]]
                        else: 
                            travers_chessmans.setdefault(man, dp+0.5)
                    else:
                        if self.chessboard[box][1] != 'K':
                            if self.chessboard[box][1] == 'S':  #opponent piece
                                op = self.pawn_points[abs(self.step[self.for_opp]-int(box[0]))]
                                if man[1] == 'S':
                                    #score according pawn current positon
                                    mp = self.pawn_points[abs(self.step[self.for_who]-int(self.my['chessmans_positions'][man][0]))]
                                    travers_chessmans.setdefault(man, dp+op-mp)
                                else:
                                    travers_chessmans.setdefault(man, dp+op-self.chessman_points[man[1]])
                            else:
                                travers_chessmans.setdefault(man, dp+self.chessman_points[self.chessboard[box][1]]-self.chessman_points[man[1]])
                        else:
                            travers_chessmans.setdefault(man, dp+0.5)

            #capture
            elif len(threated_boxes) == 1:
                dp = travers_chessmans.get(man, 0)
                if len(self.opp['additional_data']['box_backups'].get(threated_boxes[0],[])) == 0:
                    if self.chessboard[threated_boxes[0]][1] != 'K':
                        travers_chessmans.setdefault(man, dp+self.chessman_points[self.chessboard[threated_boxes[0]][1]])   #opponent chessman
                else:
                    if self.chessboard[threated_boxes[0]][1] != 'K':
                        if self.chessboard[threated_boxes[0]][1] == 'S':
                            op = self.pawn_points[abs(self.step[self.for_opp]-int(threated_boxes[0][0]))]
                            if man[1] == 'S':
                                mp = self.pawn_points[abs(self.step[self.for_who]-int(self.my['chessmans_positions'][man][0]))]
                                travers_chessmans.setdefault(man, dp+op-mp)
                            else:
                                travers_chessmans.setdefault(man, dp+op-self.chessman_points[man[1]])
                        else:
                            travers_chessmans.setdefault(man, dp+self.chessman_points[self.chessboard[threated_boxes[0]][1]]-self.chessman_points[man[1]])
  
        return max(travers_chessmans.values(),default=0) if len(travers_chessmans)>0 else 0

    
    def is_endgame(self):
        no_pawn = 0
        no_pieces = len(self.my['avail_chessmans']+self.opp['avail_chessmans'])
        no_queen = 0
        no_rook = 0
        piece_threshold = 8
        pawn_threshold = 5
        for i in self.my['avail_chessmans'] + self.opp['avail_chessmans']:
            if i[1]=='S':
                no_pawn += 1
            elif i[1]=='q':
                no_queen += 1
            elif i[1]=='r':
                no_rook += 1

        return no_pieces<=piece_threshold and no_pawn<=pawn_threshold and no_queen<=1 and no_rook<=2

    #control over center of board
    def control_over_center(self):
        center_pos = ['33','34','43','44']
        my_center_score = 0.0
        opp_center_score = 0.0
        for k,v in self.my['chessmans_positions'].items():
            if v in center_pos:
                my_center_score += self.center_control[k[0]][v]

        for k,v in self.opp['chessmans_positions'].items():
            if v in center_pos:
                opp_center_score += self.center_control[k[0]][v]
        
        return my_center_score-opp_center_score
        #return 0.20 if my_center_score>opp_center_score else -0.20 if my_center_score!=opp_center_score else 0.0

    def piece_activity(self):
        my_activity = sum(len(moves) for man,moves in self.my['legal_moves'].items())
        opp_activity = sum(len(moves) for man,moves in self.opp['legal_moves'].items())
        return (my_activity-opp_activity)*0.001
        #0.40 if my_activity>opp_activity else -0.40 if my_activity!=opp_activity else 0.0

    def pawn_structure_score(self):
        my_pawn_structure_score = 0.0
        opp_pawn_structure_score = 0.0
        for m,p in self.my['chessmans_positions'].items():
            if m[1]=='S':
                #Award points for pawns on advanced ranks and penalize isolated pawns.
                #-1 is default pown point that was already calculated in piece advantage
                my_pawn_structure_score += self.pawn_points[abs(self.step[self.for_who]-int(p[0]))] -1
                my_pawn_structure_score += -0.50 if self.is_isolated_pawn(int(p[0]), int(p[1]), m[0:2]) else 0.0

        for m,p in self.opp['chessmans_positions'].items():
            if m[1]=='S':
                opp_pawn_structure_score += self.pawn_points[abs(self.step[self.for_opp]-int(p[0]))] -1
                opp_pawn_structure_score += -0.50 if self.is_isolated_pawn(int(p[0]), int(p[1]), m[0:2]) else 0.0

        return my_pawn_structure_score - opp_pawn_structure_score
        # .50 if my_pawn_structure_score>opp_pawn_structure_score else -.50 if my_pawn_structure_score != opp_pawn_structure_score else 0.0

    def is_isolated_pawn(self,row,col,man):    #adjecent row and adjecent_column
        for ar,ac in [(row-1,col-1), (row-1,col+1), (row+1,col-1), (row+1,col+1)]:
            if 0 <= ar < 8 and 0 <= ac < 8 and self.chessboard[str(ar)+str(ac)] != '' and self.chessboard[str(ar)+str(ac)][0:2] == man:
                return False
        return True

    def well_protected_king(self,row,col,color):
        friendly_pieces = 0
        for ar,ac in [(row-1,col-1), (row-1,col+1), (row-1,col), (row+1,col-1), (row+1,col+1), (row+1,col), (row,col-1), (row,col+1)]:
            if 0 <= ar < 8 and 0 <= ac < 8 and self.chessboard[str(ar)+str(ac)] != '' and self.chessboard[str(ar)+str(ac)][0] == color:
                friendly_pieces += 1
        return True if friendly_pieces >= 2 else False

   #paste tactical move here


    @staticmethod
    def join_lists(mydict, *args, **kwargs):
        #return list of all availabe moves
        x= []
        for man,moves in mydict.items():
            if man[1] =='S':
                if len(args[0][man])>0: x.extend(args[0][man])
            else:
                if len(moves)>0:x.extend(moves)       
        return x

    @staticmethod
    def chessmans_can_move_to_box(block_possible_moves):
        """ this method return dictionary of number of chessmans can moves to a box(position) of one side(black or white)
        like box_backups-->{'45':['BP62','BP65','BC72']}""" 
        box_backups = {}
        for chessman,moves in block_possible_moves.items():
            if len(moves)>0:
                for m in moves:
                    if m in box_backups.keys(): 
                        box_backups[m].append(chessman)
                    else: 
                        box_backups[m] = [chessman]
        return box_backups

    @staticmethod
    def provide_threats_to_opp(my_chessmans_moves,opp_chessmans_positions):
        """ this function return dictionaries of opp chessman position if they are in my chessman possile moves.
        like: {'BQ75':[25,36,45]}   number of threats my chessman is providing""" 
        x = {}
        for k,v in  my_chessmans_moves.items():
            if len(v)>0:
                for _ in opp_chessmans_positions.values():
                    if _ in v:
                        if k in x.keys():
                            x[k].append(_)
                        else:
                            x.setdefault(k,[_])
        return x

    @classmethod
    def check_threats(cls, chessmans_positions, opponent_all_moves):
        """ this function return dictionary of chessman if they are in threats with loss points 
        in this method we included pawn different point for different case. """
        threats = {}
        for man,pos in chessmans_positions.items():
            if pos in opponent_all_moves:
                if man[1]=='S':
                    if abs(int(man[2])-int(pos[0])) == 6:
                        threats[man] = cls.chessman_points[man[1]]*6
                    elif abs(int(man[2])-int(pos[0])) == 5:
                        threats[man] = cls.chessman_points[man[1]]*2
                    elif abs(int(man[2])-int(pos[0])) == 4:
                        threats[man] = cls.chessman_points[man[1]]*1.5
                    else:
                        threats[man] = cls.chessman_points[man[1]]
                else:
                    if man[1]!='K':
                        threats[man] = cls.chessman_points[man[1]]
        return threats

    @classmethod
    def get_both_data(cls, for_who: str, board: dict, castle:dict, flag:bool=False):
        #here flag means we want all data or just my and opp moves
        for_opp = 'W' if for_who=='B' else 'B'
        my_pawn_include= {}
        opp_pawn_include= {}

        my = {'chessmans_moves':{},'chessmans_positions':{},'avail_chessmans':[],'block_possible_moves':{},
            'all_moves':[],'additional_data':{},'after_stop_moves':{},'btw_moves':{},
            'guarding_chessman_can_move':{},'legal_moves':{},'kp':None,'color':for_who}
        opp = {'chessmans_moves':{},'chessmans_positions':{},'avail_chessmans':[],'block_possible_moves':{},
            'all_moves':[],'additional_data':{},'after_stop_moves':{},'btw_moves':{},
            'guarding_chessman_can_move':{},'legal_moves':{},'kp':None,'color':for_opp}
        
        try:  
            for k,v in board.items():
                if v!='':
                    btw_moves = []; guard_man = {}
                    if v.startswith(for_who):
                        my['chessmans_moves'][v],my['block_possible_moves'][v],my['after_stop_moves'][v],btw_moves,\
                        guard_man,my_pawn_include[v] = chessman(board, for_who, int(k[0]), int(k[1]), for_who, v[1],[],[],[],[],[],[])
                        
                        my['chessmans_positions'][v] = k
                        my['avail_chessmans'].append(v)
                        
                        if len(btw_moves)>0:opp['btw_moves'][v]=btw_moves
                        if len(guard_man)>0:opp['guarding_chessman_can_move'][guard_man[0]]=guard_man[1]
                            
                    else:
                        opp['chessmans_moves'][v],opp['block_possible_moves'][v],opp['after_stop_moves'][v],btw_moves,\
                        guard_man,opp_pawn_include[v] = chessman(board, for_opp, int(k[0]), int(k[1]), for_opp, v[1],[],[],[],[],[],[])
                        
                        opp['chessmans_positions'][v] = k
                        opp['avail_chessmans'].append(v)
                        
                        if len(btw_moves)>0:my['btw_moves'][v]=btw_moves
                        if len(guard_man)>0:my['guarding_chessman_can_move'][guard_man[0]]=guard_man[1]
                            
            my['all_moves'] = ChessMixin.join_lists(my['chessmans_moves'],my_pawn_include)
            opp['all_moves'] = ChessMixin.join_lists(opp['chessmans_moves'],opp_pawn_include)

            my['additional_data']['box_backups'] = ChessMixin.chessmans_can_move_to_box(my['block_possible_moves']) 
            my['additional_data']['chessmans_can_move_to_box'] = ChessMixin.chessmans_can_move_to_box(my['chessmans_moves'])
            my['additional_data']['provide_threats_to_opp'] = ChessMixin.provide_threats_to_opp(my['chessmans_moves'],opp['chessmans_positions'])

            opp['additional_data']['box_backups'] = ChessMixin.chessmans_can_move_to_box(opp['block_possible_moves']) 
            opp['additional_data']['chessmans_can_move_to_box'] = ChessMixin.chessmans_can_move_to_box(opp['chessmans_moves'])
            opp['additional_data']['provide_threats_to_opp'] = ChessMixin.provide_threats_to_opp(opp['chessmans_moves'],my['chessmans_positions'])

            my['kp'],opp['kp'] = (my['chessmans_positions'][cls.BK], opp['chessmans_positions'][cls.WK]) if for_who \
                                == 'B' else (my['chessmans_positions'][cls.WK], opp['chessmans_positions'][cls.BK])
            
            my['legal_moves'] = legalMoveGen(board,my['kp'],my['chessmans_moves'],my['btw_moves'],my['guarding_chessman_can_move'],\
                                            opp['all_moves'],opp['chessmans_positions'],opp['additional_data'],opp['after_stop_moves'],castle)
            opp['legal_moves'] = legalMoveGen(board,opp['kp'],opp['chessmans_moves'],opp['btw_moves'],opp['guarding_chessman_can_move'],\
                                            my['all_moves'],my['chessmans_positions'],my['additional_data'],my['after_stop_moves'],castle)
        
            if flag==False:
                return (
                {'legal_moves':my['legal_moves'], 'chessmans_positions':my['chessmans_positions'], 'kp':my['kp'], 'all_moves':my['all_moves']},
                {'legal_moves':opp['legal_moves'], 'chessmans_positions':opp['chessmans_positions'], 'kp':opp['kp'], 'all_moves':opp['all_moves']}
                )
            else:
                return (my,opp)
        except:
            print("error occured in chessmixi.py file in except block")
            return (None, None)
        """
        #'all_block_possible_moves':[],'before_move_threats':{},
        # my['before_move_threats'] = ChessMixin.check_threats(my['chessmans_positions'],opp['all_moves'],)
        # opp['before_move_threats'] = ChessMixin.check_threats(opp['chessmans_positions'],my['all_moves'],)
        """
"""
    @classmethod
    def get_datas(cls,for_who,board,castle):
        for_opp = 'W' if for_who=='B' else 'B'
        
        my_pawn_include= {}
        opp_pawn_include= {}
        
        my_chessmans_moves = {}
        my_chessmans_positions = {}
        my_my_avail_chessmans = []
        my_block_possible_moves = {}
        my_all_moves = []
        my_additional_data = {}
        my_after_stop_moves = {}
        my_btw_moves = {}
        my_guarding_chessman_can_move = {}
        my_legal_moves = {}
        my_kp = None
        my_color = for_who

        opp_chessmans_moves = {}
        opp_chessmans_positions = {}
        opp_avail_chessmans = []
        opp_block_possible_moves = {}
        opp_all_moves = []
        opp_additional_data = {}
        opp_after_stop_moves = {}
        opp_btw_moves = {}
        opp_guarding_chessman_can_move = {}
        opp_legal_moves = {}
        opp_kp = None
        opp_color = for_who

        for k,v in board.items():
            if v!='':
                btw_moves = []; guard_man = {}
                if v.startswith(for_who):
                    my_chessmans_moves[v],my_block_possible_moves[v],my_after_stop_moves[v],btw_moves,\
                    guard_man,my_pawn_include[v] = chessman(board, for_who, int(k[0]), int(k[1]), for_who, v[1],[],[],[],[],[],[])
                    
                    my_chessmans_positions[v] = k
                    my_avail_chessmans.append(v)
                    
                    if len(btw_moves)>0: opp_btw_moves[v]=btw_moves
                    if len(guard_man)>0: opp_guarding_chessman_can_move[guard_man[0]]=guard_man[1]
                        
                else:
                    opp_chessmans_moves[v],opp_block_possible_moves[v],opp_after_stop_moves[v],btw_moves,\
                    guard_man,opp_pawn_include[v] = chessman(board, for_opp, int(k[0]), int(k[1]), for_opp, v[1],[],[],[],[],[],[])
                    
                    opp_chessmans_positions[v] = k
                    opp_avail_chessmans.append(v)
                    
                    if len(btw_moves)>0:my_btw_moves[v]= btw_moves
                    if len(guard_man)>0:my_guarding_chessman_can_move[guard_man[0]]=guard_man[1]
                        
        my_all_moves = ChessMixin.join_lists(my_chessmans_moves,my_pawn_include)
        opp_all_moves = ChessMixin.join_lists(opp_chessmans_moves,opp_pawn_include)

        my_additional_data['box_backups'] = ChessMixin.chessmans_can_move_to_box(my_block_possible_moves) 
        my_additional_data['chessmans_can_move_to_box'] = ChessMixin.chessmans_can_move_to_box(my_chessmans_moves)
        my_additional_data['provide_threats_to_opp'] = ChessMixin.provide_threats_to_opp(my_chessmans_moves,opp_chessmans_positions)

        opp_additional_data['box_backups'] = ChessMixin.chessmans_can_move_to_box(opp_block_possible_moves) 
        opp_additional_data['chessmans_can_move_to_box'] = ChessMixin.chessmans_can_move_to_box(opp_chessmans_moves)
        opp_additional_data['provide_threats_to_opp'] = ChessMixin.provide_threats_to_opp(opp_chessmans_moves,my_chessmans_positions)

        my_kp,opp_kp = (my_chessmans_positions[cls.BK],opp_chessmans_positions[cls.WK]) if for_who==\
                        'B' else (my_chessmans_positions[cls.WK],opp_chessmans_positions[cls.BK])
        
        my_legal_moves = legalMoveGen(board,my_kp,my_chessmans_moves,my_btw_moves,my_guarding_chessman_can_move,\
                                        opp_all_moves,opp_chessmans_positions,opp_additional_data,opp_after_stop_moves,castle)
        opp_legal_moves = legalMoveGen(board,opp_kp,opp_chessmans_moves,opp_btw_moves,opp_guarding_chessman_can_move,\
                                        my_all_moves,my_chessmans_positions,my_additional_data,my_after_stop_moves,castle)
        
        #return (my,opp)
        return (
            {'legal_moves':my_legal_moves, 'chessmans_positions':my_chessmans_positions, 'kp':my_kp, 'all_moves':my_all_moves},
            {'legal_moves':opp_legal_moves, 'chessmans_positions':opp_chessmans_positions, 'kp':opp_kp, 'all_moves':opp_all_moves},
            )
"""

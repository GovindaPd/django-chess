def forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,*args,**kwargs):
    if turn ==chessman_color:

        if chessman_short_id=='Q' or chessman_short_id=='E':
            flag = 0;discard = [];#guarding chessman can only move btw(king and threating chessman)blocks(include threating chessman and king pos)
            for i in range(1,8,1):
                cond,r,c = (row-i >= 0, row-i, col) if chessman_color=='B' else (row+i <= 7, row+i, col)

                if cond:    ##check forward move is not out of chessboard length for white
                    if flag==0:
                        if chessboard[str(r)+str(c)] != '':    #check forward box is not empty then proceed
                            blocker_id = chessboard[str(r)+str(c)]
                            blocker_color = blocker_id[0]
                            if blocker_color != turn:   #check blocker person is not similar to this person color if not then append in possible moves of possible_moves else break
                                possible_moves.append(str(r)+str(c))
                                discard.append(str(r)+str(c))
                                discard.append(str(row)+str(col))   #chessman current position
                                if blocker_id[1] == 'K':btw_moves.extend(discard)
                            else:
                                block_possible_moves.append(str(r)+str(c))
                            after_stop.append(str(r)+str(c))
                            flag = 1

                        else:   #if forward box is empty then append in possible moves of possible_moves
                            possible_moves.append(str(r)+str(c))
                            discard.append(str(r)+str(c))

                    else:
                        after_stop.append(str(r)+str(c))
                        discard.append(str(r)+str(c))
                        if chessboard[str(r)+str(c)] != '':
                            if chessboard[str(r)+str(c)][1]=='K' and chessboard[str(r)+str(c)][0]!=turn:
                                guarding_chessman_can_move.append(blocker_id)
                                guarding_chessman_can_move.append(discard)
                            break

        if chessman_short_id=='S':     #check if it is pawn then proceed
            cond,r,c,start_pos,symbol = (row-1>= 0, row-1, col, 6, -1) if chessman_color=='B' else (row+1 <= 7, row+1, col, 1, +1)
            if cond:        # checking pawn forward moves is not out of board length for white
                if row==start_pos:         #check if it is at default position then check 2 forward steps
                    if chessboard[str(r)+str(col)] != '':    #check if forward box is not empty then leave(stop)
                        pass 
                    else:   #if 1st place is empty then append box id in possible moves(possible_moves) and check for 2nd step
                        possible_moves.append(str(r)+str(col))
                        if chessboard[str(row+(symbol*2))+str(col)] != '': #check for 2nd step if forward box is not empty then leave(stop) 
                            pass
                        else:   #if 2nd place is empty then append box id in possible moves(possible_moves)
                            possible_moves.append(str(row+(symbol*2))+str(col))
                else:   #if pawn is not at it default position then check 1 step forward move possibility
                    #if step forward is not possible
                    if chessboard[str(r)+str(col)] != '': #check if forward box is not empty then leave(stop)
                        pass
                    else:   #if step forward box is possible then store its box id in possible moves(possible_moves) 
                        possible_moves.append(str(r)+str(col))

        #check if it is king then proceed
        if chessman_short_id=='K':
            # checking pawn forward moves is not out of board length for white
            cond,r,c = (row-1 >= 0, row-1, col) if chessman_color=='B' else (row+1 <= 7, row+1, col)
            if cond:
                #check if forward box is not empty then proceed
                if chessboard[str(r)+str(c)] != '':
                    blocker_id = chessboard[str(r)+str(c)]
                    blocker_color = blocker_id[0]
                    #check blocker person is not similar to this person color if not then append in possible moves of possible_moves else break
                    if blocker_color != turn:
                        possible_moves.append(str(r)+str(c))
                    else:
                        block_possible_moves.append(str(r)+str(c))
                #if step forward box is possible then store its box id in possible moves(possible_moves)
                else:
                    possible_moves.append(str(r)+str(c))

#backward move
def backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,*args,**kwargs):
    if turn==chessman_color:  
        if chessman_short_id=='Q' or chessman_short_id=='E':
            flag = 0;discard = []
            for i in range(1,8,1):
                cond,r,c = (row+i <= 7, row+i, col) if chessman_color=='B' else (row-i >= 0, row-i, col)
                if cond:
                    if flag ==0:
                        if chessboard[str(r)+str(c)] != '': #frist stop
                            blocker_id = chessboard[str(r)+str(c)]
                            blocker_color = blocker_id[0]
                            if blocker_color != turn:
                                possible_moves.append(str(r)+str(c))
                                discard.append(str(r)+str(c))
                                discard.append(str(row)+str(col))
                                if blocker_id[1] == 'K':
                                    btw_moves.extend(discard)
                            else:
                                block_possible_moves.append(str(r)+str(c))
                            after_stop.append(str(r)+str(c))
                            flag = 1
                        else:
                           possible_moves.append(str(r)+str(c))
                           discard.append(str(r)+str(c))
                    else:
                        after_stop.append(str(c)+str(c))
                        discard.append(str(r)+str(c))
                        if chessboard[str(r)+str(c)] != '':
                            #using discard variable here cause ig btw_moves work then guarding_chessman_can_move don't 
                            #work or vise vers(opposite)
                            if chessboard[str(r)+str(c)][1]=='K' and chessboard[str(r)+str(c)][0]!=turn:    #second stop
                                guarding_chessman_can_move.append(blocker_id)
                                guarding_chessman_can_move.append(discard)
                            break

        if chessman_short_id=='K':
            cond,r,c = (row+1 <= 7, row+1, col) if chessman_color=='B' else (row-1 >= 0, row-1, col)
            if cond:        
                if chessboard[str(r)+str(c)] != '':
                    blocker_id = chessboard[str(r)+str(c)]
                    blocker_color = blocker_id[0]
                    if blocker_color != turn: 
                        possible_moves.append(str(r)+str(c)) 
                    else:
                        block_possible_moves.append(str(r)+str(c))
                else:
                    possible_moves.append(str(r)+str(c))

#left forward move
def left_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,*args,**kwargs):
    if turn==chessman_color:
        if chessman_short_id=='Q' or chessman_short_id=='C':  #check if it is ROOK or QUEEN then proceed
           flag = 0;discard = []
           for i in range(1,8,1):
                cond,r,c = (row-i>=0 and col-i>=0, row-i, col-i) if chessman_color=='B' else (row+i<=7 and col-i>=0, row+i, col-i)
                if cond:
                    if flag==0:
                        if chessboard[str(r)+str(c)] != '':
                            blocker_id = chessboard[str(r)+str(c)]
                            blocker_color = blocker_id[0]
                            if blocker_color != turn:
                                possible_moves.append(str(r)+str(c))
                                discard.append(str(r)+str(c))
                                discard.append(str(row)+str(col))
                                if blocker_id[1] == 'K':
                                    btw_moves.extend(discard)
                            else:
                                block_possible_moves.append(str(r)+str(c))
                            after_stop.append(str(r)+str(c))
                            flag = 1
                        else:
                            possible_moves.append(str(r)+str(c))
                            discard.append(str(r)+str(c))
                    else:
                        after_stop.append(str(r)+str(c))
                        discard.append(str(r)+str(c))
                        if chessboard[str(r)+str(c)] != '':
                            if chessboard[str(r)+str(c)][1]=='K' and chessboard[str(r)+str(c)][0]!=turn:
                                guarding_chessman_can_move.append(blocker_id)
                                guarding_chessman_can_move.append(discard) 
                            break

        if chessman_short_id=='S':     #check if it is pawn then proceed
            cond,r,c = (row-1>=0 and col-1>=0, row-1, col-1) if chessman_color=='B' else (row+1<=7 and col-1>=0, row+1, col-1)       
            if cond:
                    if chessboard[str(r)+str(c)] != '':
                        blocker_id = chessboard[str(r)+str(c)]
                        blocker_color = blocker_id[0]
                        if blocker_color != turn:
                            possible_moves.append(str(r)+str(c))
                            args[0].append(str(r)+str(c))
                        else:
                            block_possible_moves.append(str(r)+str(c))
                    else:
                        args[0].append(str(r)+str(c))
                    
        if chessman_short_id=='K':
            cond,r,c = (row-1>=0 and col-1>=0, row-1, col-1) if chessman_color=='B' else (row+1<=7 and col-1>=0, row+1, col-1)       
            if cond:
                if chessboard[str(r)+str(c)] != '':
                    blocker_id = chessboard[str(r)+str(c)]
                    blocker_color = blocker_id[0]
                    if blocker_color != turn: 
                        possible_moves.append(str(r)+str(c))
                    else:
                        block_possible_moves.append(str(r)+str(c))
                else:
                    possible_moves.append(str(r)+str(c))

#right forward move
def right_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,*args,**kwargs):
    if turn==chessman_color:    #check if it is black then proceed
        if chessman_short_id=='Q' or chessman_short_id=='C':  #check if it is ROOK or QUEEN then proceed
            flag = 0;discard = []
            for i in range(1,8,1):
                cond,r,c = (row-i>=0 and col+i<=7, row-i, col+i) if chessman_color=='B' else (row+i<=7 and col+i<=7, row+i, col+i)
                if cond:
                    if flag==0:
                        if chessboard[str(r)+str(c)] != '':
                            blocker_id = chessboard[str(r)+str(c)]
                            blocker_color = blocker_id[0]
                            if blocker_color != turn:
                                possible_moves.append(str(r)+str(c))
                                discard.append(str(r)+str(c))
                                discard.append(str(row)+str(col))
                                if blocker_id[1] == 'K':
                                    btw_moves.extend(discard)
                            else:
                                block_possible_moves.append(str(r)+str(c))
                            after_stop.append(str(r)+str(c))
                            flag = 1
                        else:
                            possible_moves.append(str(r)+str(c))
                            discard.append(str(r)+str(c))
                    else:
                        after_stop.append(str(r)+str(c))
                        discard.append(str(r)+str(c))
                        if chessboard[str(r)+str(c)] != '':
                            if chessboard[str(r)+str(c)][1]=='K' and chessboard[str(r)+str(c)][0]!=turn:
                                guarding_chessman_can_move.append(blocker_id)
                                guarding_chessman_can_move.append(discard) 
                            break

        if chessman_short_id=='S':     #check if it is pawn then proceed 
            cond,r,c = (row-1>=0 and col+1<=7, row-1, col+1) if chessman_color=='B' else (row+1<=7 and col+1<=7, row+1, col+1)
            if cond:
                    if chessboard[str(r)+str(c)] != '':
                        blocker_id = chessboard[str(r)+str(c)]
                        blocker_color = blocker_id[0]
                        if blocker_color != turn:
                            possible_moves.append(str(r)+str(c))
                            args[0].append(str(r)+str(c))
                        else:
                            block_possible_moves.append(str(r)+str(c))
                    else:
                        args[0].append(str(r)+str(c))
        
        if chessman_short_id=='K':
            cond,r,c = (row-1>=0 and col+1<=7, row-1, col+1) if chessman_color=='B' else (row+1<=7 and col+1<=7, row+1, col+1)
            if cond:
                if chessboard[str(r)+str(c)] != '':
                    blocker_id = chessboard[str(r)+str(c)]
                    blocker_color = blocker_id[0]
                    if blocker_color != turn: 
                        possible_moves.append(str(r)+str(c))
                    else:
                        block_possible_moves.append(str(r)+str(c))
                else:
                    possible_moves.append(str(r)+str(c))

#check left moves
def left_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,*args,**kwargs):
    if turn==chessman_color:
        if chessman_short_id=='Q' or chessman_short_id=='E':
            flag = 0;discard = [];
            for i in range(1,8,1):
                cond,r,c = (col-i>=0, row, col-i)
                if cond:
                    if flag==0:
                        if chessboard[str(r)+str(c)] != '':
                            blocker_id = chessboard[str(r)+str(c)]
                            blocker_color = blocker_id[0]
                            if blocker_color != turn:
                                possible_moves.append(str(r)+str(c))
                                discard.append(str(r)+str(c))
                                discard.append(str(row)+str(col))
                                if blocker_id[1] == 'K':
                                    btw_moves.extend(discard)
                            else:
                                block_possible_moves.append(str(r)+str(c))
                            after_stop.append(str(r)+str(c))
                            flag = 1
                        else:
                            possible_moves.append(str(r)+str(c))
                            discard.append(str(r)+str(c))
                    else:
                        after_stop.append(str(r)+str(c))
                        discard.append(str(r)+str(c))
                        if chessboard[str(r)+str(c)] != '':
                            if chessboard[str(r)+str(c)][1]=='K' and chessboard[str(r)+str(c)][0]!=turn:
                                guarding_chessman_can_move.append(blocker_id)
                                guarding_chessman_can_move.append(discard) 
                            break
        
        if chessman_short_id=='K':
            cond,r,c = (col-1>=0, row, col-1)
            if col-1 >= 0:
                if chessboard[str(r)+str(c)] != '':
                    blocker_id = chessboard[str(r)+str(c)]
                    blocker_color = blocker_id[0]
                    if blocker_color != turn:
                        possible_moves.append(str(r)+str(c))
                    else:
                        block_possible_moves.append(str(r)+str(c))
                else:
                    possible_moves.append(str(r)+str(c))

#right moves
def right_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,*args,**kwargs):
    if turn==chessman_color:
        if chessman_short_id=='Q' or chessman_short_id=='E':
            flag = 0;discard = []
            for i in range(1,8,1):
                cond,r,c = (col+i<=7, row, col+i)
                if cond:
                    if flag==0:
                        if chessboard[str(r)+str(c)] != '':
                            blocker_id = chessboard[str(r)+str(c)]
                            blocker_color = blocker_id[0]
                            if blocker_color != turn:
                                possible_moves.append(str(r)+str(c))
                                discard.append(str(r)+str(c))
                                discard.append(str(row)+str(col))#chessman current postion
                                if blocker_id[1] == 'K':
                                    btw_moves.extend(discard)
                            else:
                                block_possible_moves.append(str(r)+str(c))
                            after_stop.append(str(r)+str(c))
                            flag = 1
                        else:
                            possible_moves.append(str(r)+str(c))
                            discard.append(str(r)+str(c))
                    else:
                        after_stop.append(str(r)+str(c))
                        discard.append(str(r)+str(c))
                        if chessboard[str(r)+str(c)] != '':
                            if chessboard[str(r)+str(c)][1]=='K' and chessboard[str(r)+str(c)][0]!=turn:
                                guarding_chessman_can_move.append(blocker_id)
                                guarding_chessman_can_move.append(discard) 
                            break

        if chessman_short_id=='K':
            cond,r,c = (col+1<= 7, row, col+1)
            if cond:
                if chessboard[str(r)+str(c)] != '':
                    blocker_id = chessboard[str(r)+str(c)]
                    blocker_color = blocker_id[0]
                    if blocker_color != turn:
                        possible_moves.append(str(r)+str(c))
                    else:
                        block_possible_moves.append(str(r)+str(c))
                else:
                    possible_moves.append(str(r)+str(c))

#left bckward move
def left_backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,*args,**kwargs):
    if turn == chessman_color:    #check if it is black then proceed
        if chessman_short_id=='Q' or chessman_short_id=='C':  #check if it is ROOK or QUEEN then proceed
            flag = 0;discard = []
            for i in range(1,8,1):
                cond,r,c = (row+i<=7 and col-i>=0, row+i, col-i) if chessman_color=='B' else (row-i>=0 and col-i>=0, row-i, col-i)
                if cond:
                    if flag==0:
                        if chessboard[str(r)+str(c)] != '':
                            blocker_id = chessboard[str(r)+str(c)]
                            blocker_color = blocker_id[0]
                            if blocker_color != turn:
                                possible_moves.append(str(r)+str(c))
                                discard.append(str(r)+str(c))
                                discard.append(str(row)+str(col))
                                if blocker_id[1] == 'K':
                                    btw_moves.extend(discard)
                            else:
                                block_possible_moves.append(str(r)+str(c))
                            after_stop.append(str(r)+str(c))
                            flag = 1
                        else:
                            possible_moves.append(str(r)+str(c))
                            discard.append(str(r)+str(c))
                    else:
                        after_stop.append(str(r)+str(c))
                        discard.append(str(r)+str(c))
                        if chessboard[str(r)+str(c)] != '':
                            if chessboard[str(r)+str(c)][1]=='K' and chessboard[str(r)+str(c)][0]!=turn:
                                guarding_chessman_can_move.append(blocker_id)
                                guarding_chessman_can_move.append(discard)
                            break

        if chessman_short_id=='K':
            cond,r,c = (row+1<=7 and col-1>=0, row+1, col-1) if chessman_color=='B' else (row-1>=0 and col-1>=0, row-1, col-1)
            if cond:
                if chessboard[str(r)+str(c)] != '':
                        blocker_id = chessboard[str(r)+str(c)]
                        blocker_color = blocker_id[0]
                        if blocker_color != turn:
                            possible_moves.append(str(r)+str(c))
                        else:
                            block_possible_moves.append(str(r)+str(c))
                else:
                    possible_moves.append(str(r)+str(c))

#right bckward move
def right_backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,*args,**kwargs):
    if turn == chessman_color:    #check if it is black then proceed
        if chessman_short_id=='Q' or chessman_short_id=='C':  #check if it is ROOK or QUEEN then proceed
            flag = 0;discard = []
            for i in range(1,8,1):
                cond,r,c = (row+i<=7 and col+i<=7, row+i, col+i) if chessman_color=='B' else (row-i>=0 and col+i<=7, row-i, col+i)
                if cond:
                    if flag==0:
                        if chessboard[str(r)+str(c)] != '':
                            blocker_id = chessboard[str(r)+str(c)]
                            blocker_color = blocker_id[0]
                            if blocker_color != turn:
                                possible_moves.append(str(r)+str(c))
                                discard.append(str(r)+str(c))
                                discard.append(str(row)+str(col))
                                if blocker_id[1] == 'K':
                                    btw_moves.extend(discard)
                            else:
                                block_possible_moves.append(str(r)+str(c))
                            after_stop.append(str(r)+str(c))
                            flag = 1
                        else:
                            possible_moves.append(str(r)+str(c))
                            discard.append(str(r)+str(c))
                    else:
                        after_stop.append(str(r)+str(c))
                        discard.append(str(r)+str(c))
                        if chessboard[str(r)+str(c)] != '':
                            if chessboard[str(r)+str(c)][1]=='K' and chessboard[str(r)+str(c)][0]!=turn:
                                guarding_chessman_can_move.append(blocker_id)
                                guarding_chessman_can_move.append(discard)
                            break

        if chessman_short_id=='K':
            cond,r,c = (row+1<=7 and col+1<=7, row+1, col+1) if chessman_color=='B' else (row-1>=0 and col+1<=7, row-1, col+1)
            if cond:
                if chessboard[str(r)+str(c)] != '':
                        blocker_id = chessboard[str(r)+str(c)]
                        blocker_color = blocker_id[0]
                        if blocker_color != turn: 
                            possible_moves.append(str(r)+str(c))
                        else:
                            block_possible_moves.append(str(r)+str(c))
                else:
                    possible_moves.append(str(r)+str(c))

def knight(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves):
    if turn==chessman_color:
        knight_opt = []
        if chessman_color=='B':
            knight_opt.append((row-2 >= 0 and col-1 >= 0, row-2, col-1))#(condition, row ,col)-->forward left move
            knight_opt.append((row-2 >= 0 and col+1 <= 7, row-2, col+1))#forward right move
            knight_opt.append((row-1 >= 0 and col-2 >= 0, row-1, col-2))#left forward move
            knight_opt.append((row-1 >= 0 and col+2 <= 7, row-1, col+2))#right forward move
            knight_opt.append((row+1 <= 7 and col+2 <= 7, row+1, col+2))#right backward move
            knight_opt.append((row+1 <= 7 and col-2 >= 0, row+1, col-2))#left backward move
            knight_opt.append((row+2 <= 7 and col-1 >= 0, row+2, col-1))#backward left move
            knight_opt.append((row+2 <= 7 and col+1 <= 7, row+2, col+1))#backward right move
        else:
            knight_opt.append((row+2 <= 7 and col-1 >= 0, row+2, col-1))#forward left move -->(condition, row ,col)
            knight_opt.append((row+2 <= 7 and col+1 <= 7, row+2, col+1))#forward right move
            knight_opt.append((row+1 <= 7 and col-2 >= 0, row+1, col-2)) #left forward move
            knight_opt.append((row+1 <= 7 and col+2 <= 7, row+1, col+2))#right forward move
            knight_opt.append((row-1 >= 0 and col+2 <= 7, row-1, col+2))#right backward move
            knight_opt.append((row-1 >= 0 and col-2 >= 0, row-1, col-2))#left backward move
            knight_opt.append((row-2 >= 0 and col-1 >= 0, row-2, col-1))#backward left move
            knight_opt.append((row-2 >= 0 and col+1 <= 7, row-2, col+1))#backward right move
        
        for cond,r,c in knight_opt:
            if cond:
                if chessboard[str(r)+str(c)] !='':
                    blocker_id = chessboard[str(r)+str(c)]
                    blocker_color = blocker_id[0]
                    if blocker_color != turn:
                        possible_moves.append(str(r)+str(c))
                    else:
                        block_possible_moves.append(str(r)+str(c))
                else:
                    possible_moves.append(str(r)+str(c))

def chessman(chessboard,turn,row,col,chessman_color,chessman_short_id,\
            possible_moves=[],block_possible_moves=[],after_stop=[],btw_moves=[],guarding_chessman_can_move=[],pawn_include=[]):
    if chessman_short_id=='S':
        pawn(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,pawn_include)
    elif chessman_short_id=='H':
        knight(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves)
    elif chessman_short_id=='Q':
        queen(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    elif chessman_short_id=='E':
        rook(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    elif chessman_short_id=='C':
        bishop(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    elif chessman_short_id=='K':
        king(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    else:
        pass
    return possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,pawn_include

def pawn(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,pawn_include):
    forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)#temp
    left_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,pawn_include)
    right_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move,pawn_include)

def rook(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move):
    forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    left_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    right_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)

def bishop(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move):
    left_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    right_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    left_backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    right_backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)

def queen(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move):
    forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    left_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)    
    right_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    left_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    right_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    left_backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    right_backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)

def king(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move):
    forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    left_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    right_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    left_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    right_forward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    left_backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)
    right_backward_move(chessboard,turn,row,col,chessman_color,chessman_short_id,possible_moves,block_possible_moves,after_stop,btw_moves,guarding_chessman_can_move)

def castle_move(chessboard,castle,for_,opp_all_moves,possible_moves):
    if castle[for_]['km'] == False:
        if castle[for_]['lem'] == False:
            flag = True
            for index,i in enumerate(castle[for_]['lboxes']):
                if index <=1:
                    if (chessboard[i]!='' or i in opp_all_moves):
                        flag = False
                        break
                else:
                    if chessboard[i] != '': flag=False
            if flag:
                possible_moves.append(castle[for_]['lboxes'][1])

        if castle[for_]['rem'] == False:
            flag = True
            for index,i in enumerate(castle[for_]['rboxes']):
                if index <=1:
                    if (chessboard[i]!='' or i in opp_all_moves):
                        flag = False
                        break
                else:
                    if chessboard[i] != '': flag = False
            if flag:
                possible_moves.append(castle[for_]['rboxes'][1])


def legalMoveGen(chessboard, my_kp, my_chessmans_moves, my_btw_moves, my_guarding_chessman_can_move,\
    opp_all_moves, opp_chessmans_positions, opp_additional_data, opp_after_stop_moves, castle):
    
    legal_moves = {}
    my_king = chessboard[my_kp]
    
    if my_kp in opp_all_moves:  #if king is in check
        threatning_chessmans = []   #[(threatning_Chessman_pos, threatning_Chessman_id ), ...]
        tempb_= {}  #dict of chessman and there position who can kill the king like : {'WH07:':'07'}
        #number of chessman can move to my king or kill my king
        for man in opp_additional_data['chessmans_can_move_to_box'][my_kp]:
            threatning_chessmans.append((opp_chessmans_positions[man], man))
            tempb_[man] = opp_chessmans_positions[man]

        if len(threatning_chessmans)>1:  #more then one piece threats to  my_king then only king will move cause we can't block two piece at one time
            temp = []
            if len(my_chessmans_moves[my_king])>0:     # if my_king has possible moves
                for i in my_chessmans_moves[my_king]:  #loop through my_king moves
                    if i not in opp_all_moves:
                        x=[]
                        if chessboard[i] != '': ##if moving into box is not empty
                            if len(opp_additional_data['box_backups'].get(i, []))==0:  #check opp has no backup for moving box_chessman
                                if i in tempb_.values():
                                    for j in tempb_.keys():
                                        if i != tempb_[j]:
                                            if i not in opp_after_stop_moves.get(j, []): x.append(True)
                                            else: x.append(False)
                                        else: x.append(True)
                                    if len(x)>0 and all(x): temp.append(i)
                                else:
                                    temp.append(i)

                        else:   #if moving into box is empty
                            for j in tempb_.keys():
                                #here checking is in moving box is still not in threating chessman opp_after_stop_moves
                                if i not in opp_after_stop_moves.get(j, []): x.append(True)
                                else: x.append(False)
                            if len(x)>0 and all(x):temp.append(i)
                if len(temp)>0:
                    legal_moves[my_king] = temp
            return legal_moves
        
        #if only one check to my king
        else:
            for man,moves in my_chessmans_moves.items():
                if len(moves)>0:
                    temp=[]
                    if man[1]!='K':
                        if man not in my_guarding_chessman_can_move.keys():
                            if threatning_chessmans[0][1][1] in ['S','H','K']:#this pices threat from one step
                                if threatning_chessmans[0][0] in moves:
                                    temp.append(threatning_chessmans[0][0])
                            else:   #if threatning_chessmans[0][1] in ['Q','E','C']:
                                for i in moves:
                                    if i in my_btw_moves.get(threatning_chessmans[0][1],[]): temp.append(i)
                    else:
                        for i in moves:
                            if i not in opp_all_moves:
                                if chessboard[i] != '':
                                    if len(opp_additional_data['box_backups'].get(i,[]))==0:
                                        if threatning_chessmans[0][0] != i:
                                            if i not in opp_after_stop_moves.get(threatning_chessmans[0][1],[]):
                                                temp.append(i)
                                        else: temp.append(i)    
                                else:
                                    if i not in opp_after_stop_moves.get(threatning_chessmans[0][1], []):
                                        temp.append(i)
                    if len(temp)>0:
                        legal_moves[man] = temp
            return legal_moves
    
    #if my king is not in threat then my chessmans possible moves
    else:
        for man,moves in my_chessmans_moves.items():
            if len(moves)>0:
                temp=[]
                if man[1]!='K':
                    if man in my_guarding_chessman_can_move.keys():   #case where peice btw king and opp_chessman
                        for i in moves:
                            if i in my_guarding_chessman_can_move[man]:temp.append(i); 
                        if len(temp)>0:legal_moves[man] = temp;     
                    else:legal_moves[man] = moves;                    #if pice not in btw king and opp_chessman
                else:   #if moving pice is king
                    for i in moves:
                        if i not in opp_all_moves:
                            if chessboard[i] != '':
                                if len(opp_additional_data['box_backups'].get(i,[]))==0: temp.append(i)
                            else:temp.append(i)
                    #castle_move
                    castle_move(chessboard,castle,my_king[0],opp_all_moves,temp)
                    if len(temp)>0: legal_moves[man] = temp
        return legal_moves
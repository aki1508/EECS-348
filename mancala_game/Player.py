# File: Player.py
# Author(s) names AND netid's: Upasna Madhok (umu583), Akshay Batra (abz233)
# Date: 4/16/2016
# Group work statement: "All group members were present and contributing during all work on this project"
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """

        move = -1 #Initialize move we will return to -1
        turn = self #Monitors players turn
        score = -INFINITY #Intialize score we will return to -Infinty -> will be updated
        alpha = -INFINITY #Alpha (max) and beta(min) initializing
        beta = INFINITY

        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over

            #Testing different options avalaible to player
            nb = deepcopy(board) #make a new board
            nb.makeMove(self, m) #try the move
            opp = Player(self.opp, self.type, self.ply) #and see what the opponent would do next
            s = opp.MINValue(nb, ply-1, turn, alpha, beta)
            #if the result is better than our best score so far, save that move,score
            if s > score:
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def MAXValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player while using AlphaBetaPruning
        at a given board configuation. Returns score."""

        #If you can't make a move then the game is over
        if board.gameOver():
            return turn.score(board)
        v = -INFINITY #Score to keep track of max
        for m in board.legalMoves(self):
            #if we're at ply 0, we need to call our eval function & return
            if ply == 0:
                return turn.score(board)
            opponent = Player(self.opp, self.type, self.ply) # make a new player to play the other side
            nextBoard = deepcopy(board) # Copy the board so that we don't ruin it

            #Testing different options available to player
            nextBoard.makeMove(self, m)
            s = opponent.MINValue(nextBoard, ply-1, turn, alpha, beta)

            # Update the max score
            if s > v:
                v = s
            # If v (score) greater than beta stop as min will never choose
            if v >= beta:
                return v
            # If new move is best move then make it alpha
            if v > alpha:
                alpha = v
        return v

    def MINValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player while utilizing alpha beta pruning
            at a given board configuation. Returns score."""

        #If you can't make a move then the game is over
        if board.gameOver():
            return turn.score(board)
        v = INFINITY #Score to keep track of min
        for m in board.legalMoves(self):
            #if we're at ply 0, we need to call our eval function & return
            if ply == 0:
                return turn.score(board)
            opponent = Player(self.opp, self.type, self.ply) # make a new player to play the other side
            nextBoard = deepcopy(board) # Copy the board so that we don't ruin it

            #Testing different options available to player
            nextBoard.makeMove(self, m)
            s = opponent.MAXValue(nextBoard, ply-1, turn, alpha, beta)

            #Update min score
            if s < v:
                v = s
            #If v(score) lower than alpha then stop as max will never choose
            if v <= alpha:
                return v
            #If new move is best move then make it beta
            if beta > v:
                beta = v
        return v

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.alphaBetaMove(board, 9)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class umu583(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        player_number = self.num # getting player number
        stateScore = 0 # initializing statescore to 0
        stateScore += board.scoreCups[0] - board.scoreCups[1] # setting stateScore to be the difference of Mancala's in Player 1's favor
        stateScore += sum(board.P1Cups) - sum(board.P2Cups) # setting stateScore to be the difference of stones on each side in Player 1's favor
        if player_number == 1:
            for index in range(len(board.P1Cups)):
                # Checking whether stealing is possible
                if board.P1Cups[index] == 0 and board.P2Cups[5 - index] != 0: #Sees if hole on your side is empty and hole opposite is not
                    stateScore += 1
                # Checking to see whether you can be stolen from
                if board.P1Cups[index] != 0 and board.P2Cups[5 - index] == 0: #Sees if hole on opponents side is empty and hole opposite is not
                    stateScore -= 1
            if board.P1Cups[4] > 4 or board.P1Cups[5] > 4: #rewarding you for stockpiling stones at end of board to prevent you from moving it to other side
                stateScore += 1
            return stateScore * 10 #multiplying by 10 just cause I feel like it and like big numbers
        else: #If player number 2
            stateScore = stateScore * (-1) #Inverting earlier logic so that we're doing player 2 cups - player 1 cups
            for index in range(len(board.P2Cups)):
                # Checking whether stealing is possible
                if board.P2Cups[index] == 0 and board.P1Cups[5 - index] != 0: #Sees if hole on your side is empty and hole opposite is not
                    stateScore += 1
                # Checking to see whether you can be stolen from
                if board.P2Cups[index] != 0 and board.P1Cups[5 - index] == 0: #Sees if hole on opponents side is empty and hole opposite is not
                    stateScore -= 1
                if board.P2Cups[4] > 4 or board.P2Cups[5] > 4: #rewarding you for stockpiling stones at end of board to prevent you from moving it to other side
                    stateScore += 1
            return stateScore * 10 #multiplying by 10 just cause I feel like it and like big numbers

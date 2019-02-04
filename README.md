# Othello
In this assignment an AI player implemented for the game Reversi, also known as Othello. 

#Book 
Artificial Intelligence: A Modern Approach - Third Edition has been taken as reference.

All functions added to AI_Assignment-3.py to build AI player. Rest of it provided; othello_game, othello_gui, othello_shared and randy_ai.

#Part I. Minimax
Implemented Minimax recursively by writing two functions minimax_max_node(board, color) and minimax_min_node(board, color). Other functions provided for implementing the Othello agent.

#Part II. α-β Pruning
The simple Minimax approach becomes infeasible for boards larger than 4x4. This speeds up decisions for the AI.

#Part III. Caching states
Created a dictionary in AI player that maps board states to their minimax value.

#Part IV. Node ordering heuristic
α-β-pruning works better if nodes that lead to a better utility are explored first.

#Part V. Depth Limit
Modified the α-β-pruning functions so that the algorithm only explores a limited number of levels, rather than the entire search tree.

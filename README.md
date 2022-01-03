# ConnectFour
3 different Connect Four games. There is a 2 player, basic AI, and MiniMax AI game. All games use numpy and pygame.

The first game is a basic 2 player Connect Four game that ends when either player gets 4 in a row or the board is filled.

The second game is a 1 player Connect Four game that uses a basic AI. The AI uses a point system to determine where to place it's piece. The highest points are given to moves which create 4 in a row for the AI and the lowest points are given to a move which allows the player to create 4 in a row.

The third game is a 1 player ocnnect Four game that uses the MiniMax algorithm as well as the point system in the second game. Together they create a more sophisticated (but still a basic) AI which makes it's move based on predictions 4 moves in advanced.

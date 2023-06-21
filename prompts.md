I have created a class of BackGammon with following methods and properties:
- board property, which is an array of tuples where the second element is (0,1,None) which represents if player 0 or 1's pieces are at that place. First element of tuple is number of pieces of the player at that position. LEngth of array is 24. For example, initial state of tuple is [(2, 1), (0, None), (0, None), (0, None), (0, None), (5, 0), (0, None), (3, 0), (0, None), (0, None), (0, None), (5, 1), (5, 0), (0, None), (0, None), (0, None), (3, 1), (0, None), (5, 1), (0, None), (0, None), (0, None), (0, None), (2, 0)].
- get_valid_moves method which returns a list of valid moves possible given a player and dice roll.
- there are more methods that are needed for the game which are already implemented.
    
BackGammon class takes care of all the logic of how the game should be played. What I want is code for training a bot which uses Q Learning and Neural network which can play the game.

Please, do not give the code directly. Let us discuss the approach. Wait till my command before proceeding with the code. No code until then. Just discussing.





What we need to do is initialize BackGammon class, create two BotPlayers and ask them the choice/action they take given the state. BotPlayer uses exploratin/exploitation and Neural network to make the decision. After the action happens, we ask BAckGammon if there is a winner or of any specific state we are interested in. Then based on response, we assign a reward to BotPlayer. I am not sure where this reward function goes to. We keep on continuing the game until someone wins or else particular number of steps are exceeded. Does the skeleton you gave take into account of these assumptions.

Also, we need to train on multiple games. But let us initially focus on having on completing one game with two BotPlayers. Later we can add other details.
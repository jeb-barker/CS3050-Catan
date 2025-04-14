# CS3050-Catan

## How to run the program
When running main.py, a screen with the default catan board setup will appear in the middle of the screen.

## Initial Setup
Four players are currently added to the game, with the red player's (the User) hand being displayed on the bottom left of the screen. The red player starts with no resources, but during the course of the game, resources will be added to their hand.

## The Bank
The bank is shown on the right side of the screen, and shows the number of each resource currently available in the bank. Note that during the course of a game, the bank can run out of resources and will simply not give any more out to the players until they are returned.

## Player Info
Below the bank, a player information section is shown. For each player, their colored box contains the number of victory points they currently have (this defaults to 0 since no settlements have been played). In order to right, the numbers above the cards represent the number of cards that player has, the number of development cards that player has, the number of knights the player has already played (-1 as of right now), and the length of that player's longest road (-1 to begin). These values automatically update throughout the game.

## Playing the Game
The game is divided into two parts, the initial phase, and the main phase. During the initial phase, each player places a settlement, then a road in a location of their choosing. during the player's turn they may press the 'build settlement' button (top left of the cluster of red buttons), and buttons will appear showing where a settlement can be placed.

Then the player may press the 'build road' button (top right in the cluster of red buttons), and press two buttons to place a road between two vertices.

Upon placing both a road and settlement, the player's turn is over, and the User may choose to press the bottom right button to let the AI play its turn. Once every other AI player has placed 2 settlements, the User places another settlement and road, and receives the resources surrounding this settlement. This concludes the initial phase.

In the main phase, the player should 1. roll the dice, 2. place as many roads, settlements, cities, etc. as they choose, then press the bottom left button to end their turn, then press the bottom right button to let each AI take its turn.


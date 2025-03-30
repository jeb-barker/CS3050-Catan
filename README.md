# CS3050-Catan
When running main.py, a screen with the default catan board setup will appear in the middle of the screen. If your screen is too small, this may result in parts of the game overflowing off of your screen currently (WIP).

Three players are currently added to the game, with the red player's hand being displayed on the bottom left of the screen. The red player starts with one of each resource.

The bank is shown on the right side of the screen, and shows the number of each resource currently available in the bank. Note that during the course of a game, the bank can run out of resources and will simply not give any more out to the players until they are returned.

Below the bank, a player information section is shown. For each player, their colored box contains the number of victory points they currently have (this defaults to 0 since no settlements have been played). In order to right, the numbers above the placeholder cards (WIP) represent the number of cards the player has, the number of development cards the player has, the number of knights the player has already played (-1 as of right now), and the length of that player's longest road (-1 as of right now).

In the top right of the screen, a red button can be pressed (as many times as you wish), and will roll the dice. Based on the outcome of the dice roll, certain resource tiles will generate their resources and give their resources to each player (WIP: This is temporary, and will become more complex once players are able to place buildings)

There is also a very small button in the bottom-middle of the screen that will give the red player (current player 1) a Wood resource from the bank. This is a temporary button used for administration and testing purposes.

Note: this project requires the pyglet package to run.


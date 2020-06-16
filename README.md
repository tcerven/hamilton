# hamilton
Playing card services

## background
Did you ever need a deck of cards but didn't have one? This is the dilemma that inspired the creation of an app that allows someone to use their computing device to simulate a deck of cards.
## single use cases
* Draw cards from the deck and arrange them in your hand
* Remove cards from the board one at a time
* Return all cards to deck
* Shuffle the deck
* Create a player
* Draw a card and put it in a player's hand

## multiuser functionaltity
The project's backend is called the ***dealer*** and it is a service that responses to requests from the frontend.
## requests


Name  | Description | Parameters | Response
------------- | ------------- | -------------| -------------
SingleDeck  | Creates a shuffled, deck with the standard 52 cards | None | The ***ID*** of the deck
AddPlayer  | Attaches a player to a deck | The ***ID*** of the deck and the ***Name*** of the player | The ID of the player
	Draw  | Removes a card from the deck and transfers to a hand | The ***ID*** of the deck and the ***ID*** of the player | The ***Card***
ShowHands  | The ID of the deck | The ID of the deck | An array of Hands

### cards
Cards are encoded


## multi use cases
	1. The person who sends the SingleDeck request first must setup the game
		* Add players
		* Draw cards for players
	2. Each person adds themself to an existing deck and everyone draws their own cards

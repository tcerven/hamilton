import json
import random

suits = ["H", "D", "S", "C"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

class Dealer:

    def __init__(self):
        self.numDecks = 0
        self.decks = {}      # (deck ID, deck[])
        self.players = {}    # (deck ID, players[])
        self.hands = {}      # (deck ID, (player ID, hand[]))

    def singleDeck(self):
        newDeck = []
        for s in suits:
            for r in ranks:
                newDeck.append((r, s))

        random.shuffle(newDeck) 

        self.decks[self.numDecks] = newDeck                           # numDeck serves as the ID of newDeck
        self.players[self.numDecks] = []
        self.hands[self.numDecks] = {}
        self.numDecks += 1

        return (self.numDecks - 1)

    def addPlayer(self, deckID, playerName):
        playerID = len(self.players[deckID])
        self.players[deckID].append(playerName)
        self.hands[deckID][playerID] = []
        return  (len(self.players[deckID]) - 1)                          # player's ID is deck-specific (its position in the deck's player array)

    def draw(self, deckID, playerID):
        index = random.randrange(0, len(self.decks[deckID]))
        card = self.decks[deckID].pop(index)                     # (rank, suit)
        self.hands[deckID][playerID].append(card)
        return card

    def showHands(self, deckID):
        return self.hands[deckID]


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    try:
        cmd = event["request"]
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print("Error: invalid request")

        raise e

    # depending on what "cmd" is, make appropriate calls to dealer functions, then use return values in JSON below

    return {
        "statusCode": 200,
        "body": json.dumps({
            "suit": s,
            "rank": r
        }),
    }

import json
import random
from pprint import pprint

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

def formatResponse(statusCode,response):
    return {
        "statusCode": statusCode,
        "body": json.dumps(response)
        # "isBase64Encoded": False
    }

dealer = Dealer()
sanity = 0

def lambda_handler(event, context):
    pprint(event)
    """Dealer lambda

    """
    global sanity,dealer
    sanity += 1
    print(sanity)
    cmd = None

    # depending on what "cmd" is, make appropriate calls to dealer functions, then use return values in JSON below
    try:
        if event['httpMethod']=='GET':
            cmd = event['queryStringParameters']['cmd']
        elif event['httpMethod']=='POST':
            cmd = json.loads(event['body'])['cmd']
        else:
            errmsg = f'Bad method {event["httpMethod"]}'
            return formatResponse(400,{"error": errmsg})

    except (KeyError,TypeError) as e:
        return formatResponse(400,{"error": "Bad request","e":str(e)})
    except Exception as e:
        return formatResponse(500,{"error": "Unknown","e":str(e)})
    print(cmd)

    if cmd=='SingleDeck':
        return formatResponse(200,{"cmd": "SingleDeck", "deck": dealer.singleDeck()})
    elif cmd=='AddPlayer':
        deckID = event['queryStringParameters']['deckID']
        playerName = event['queryStringParameters']['playerName']
        return formatResponse(200,{"cmd": "AddPlayer", "player": dealer.addPlayer(deckID, playerName)})
    elif cmd=='Draw':
        deckID = event['queryStringParameters']['deckID']
        playerID = event['queryStringParameters']['playerID']
        return formatResponse(200,{"cmd": "Draw", "card": dealer.draw(deckID, playerID)})
    elif cmd=='ShowHands':
        deckID = event['queryStringParameters']['deckID']
        return formatResponse(200,{"cmd": "ShowHands", "hands": dealer.showHands(deckID)})

    return formatResponse(200,{"cmd": cmd})

def main():
    print("Dealer test")
    while True:
        print("Type 1 for SingleDeck")
        print("Type 2 for AddPlayer")
        print("Type x to Exit")
        cmd_num = input('> ')
        print(type(cmd_num))
        if str(cmd_num)=='x':
            break
        event = {
            "httpMethod": "GET",
            "queryStringParameters": {}
        }
        if cmd_num=='1':
            print('Shuffling a single deck')
            event['queryStringParameters']['cmd']="SingleDeck"
            print(lambda_handler(event,{}))
        if cmd_num=='2':
            deckID=input('deckID')
            playerName=input('playerName')
            print(f'Adding {playerName} to deck {deckID}')
            event['queryStringParameters']['cmd']="AddPlayer"
            event['queryStringParameters']['deckID']=deckID
            event['queryStringParameters']['playerName']=playerName
            print(lambda_handler(event,{}))

    print('Goodbye')



if __name__ == "__main__":
    # execute only if run as a script
    main()

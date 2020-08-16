import json
import random
import string
from pprint import pprint

suits = ["H", "D", "S", "C"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

class Player:

    def __init__(self, playerName):
        self.name = playerName
        self.hand = []

class Dealer:

    def __init__(self):
        self.numDecks = 0
        self.decks = {}      # (deck ID, deck[])
        self.players = {}    # (deck ID, players[])

    def singleDeck(self):
        newDeck = []
        for s in suits:
            for r in ranks:
                newDeck.append((r, s))

        random.shuffle(newDeck)

        self.decks[self.numDecks] = newDeck                           # numDecks serves as the ID of newDeck
        self.players[self.numDecks] = []
        self.numDecks += 1

        return (self.numDecks - 1)

    def addPlayer(self, deckID, playerName):
        player = Player(playerName)
        playerID = len(self.players[deckID])
        self.players[deckID].append(player)
        return playerID                          # player's ID is deck-specific (its position in the deck's player array)

    def draw(self, deckID, playerID):
        index = random.randrange(0, len(self.decks[deckID]))
        card = self.decks[deckID].pop(index)                     # (rank, suit)
        self.players[deckID][playerID].hand.append(card)
        return card

    def showHands(self, deckID):
        hands = {}
        for p in self.players[deckID]:
            cards = [] # strings
            for card in p.hand:
                # card[0] is the denomination, card[1] is the suit
                cards.append(""+card[0]+card[1])
            hands[p.name] = cards
        return hands

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
            errmsg = 'Bad method {event["httpMethod"]}'
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
        print("Type 3 for Draw")
        print("Type 4 for ShowHands")
        print("Type x to Exit")
        cmd_num = input('> ')
        print(type(cmd_num))
        if cmd_num=='x':
            break
        event = {
            "httpMethod": "GET",
            "queryStringParameters": {}
        }
        if str(cmd_num)=='1':
            print('Shuffling a single deck')
            event['queryStringParameters']['cmd']="SingleDeck"
            pprint(lambda_handler(event,{}))

        if str(cmd_num)=='2':
            deckID=int(input('deckID: '))
            print(type(deckID))
            playerName=str(input('playerName: '))
            print(type(playerName))
            print('Adding {playerName} to deck {deckID}')
            event['queryStringParameters']['cmd']="AddPlayer"
            event['queryStringParameters']['deckID']=deckID
            event['queryStringParameters']['playerName']=playerName
            pprint(lambda_handler(event,{}))

        if str(cmd_num)=='3':
            deckID=int(input('deckID: '))
            print(type(deckID))
            playerID=int(input('playerID: '))
            print(type(playerID))
            print('Adding {playerID} to deck {deckID}')
            event['queryStringParameters']['cmd']="Draw"
            event['queryStringParameters']['deckID']=deckID
            event['queryStringParameters']['playerID']=playerID
            pprint(lambda_handler(event,{}))

        if str(cmd_num)=='4':
            deckID=int(input('deckID: '))
            print(type(deckID))
            print("Showing hands for deck {deckID}")
            event['queryStringParameters']['cmd']="ShowHands"
            event['queryStringParameters']['deckID']=deckID
            pprint(lambda_handler(event,{}))


    print('Goodbye')



if __name__ == "__main__":
    # execute only if run as a script
    main()

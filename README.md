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


Name  | Description | Query Parameters | Response
------------- | ------------- | -------------| -------------
SingleDeck  | Creates a shuffled, deck with the standard 52 cards | `cmd=SingleDeck` | `{"cmd": "SingleDeck", "deck": 0}`
AddPlayer  | Attaches a player to a deck | `cmd=AddPlayer&deckID=0&playerName=Jack` | `{"cmd": "AddPlayer", "player": 0}`
Draw  | Removes a card from the deck and transfers to a hand | `cmd=Draw&deckID=0&playerID=0` | `{"cmd": "Draw", "card": "6C"}`
ShowHands  | Display all cards in all hands in addition to player names | `cmd=ShowHands&deckID=0` | `{"cmd": "ShowHands", "hands": {"Jack": ["6C"]}}`
Discard (TBD) | Removes a card from a hand | Deck ID, Player ID and Card | A card from the deck, e.g. `4H`

### cards
Cards are encoded


## multi use cases
	1. The person who sends the SingleDeck request first must setup the game
		* Add players
		* Draw cards for players
	2. Each person adds themself to an existing deck and everyone draws their own cards

## build and deploy back-end
Use the SAM CLI to build and deploy the back-end

1. `sam build` or `sam build --use-container`. Each will update the requirements.txt file and pull the appropriate packages. As in all pythobn apps, there is no syntax checking until the app is run. You can run the app locally with this command `sam local invoke -e events/event.json`


2. Run `sam package --s3-bucket hamilton-deploy --output-template-file dealer-deploy-cfn.json` to upload the app


3. Run `sam deploy --template-file dealer-deploy-cfn.json --stack-name dealer-lambda --capabilities CAPABILITY_IAM` to deploy the app. Note the APIGateway endpoint for testing.

## testing

### using the test harness
There is a simple test harness in a main() function in app.py. This makes it easy to test the lambda_handler without needing to use any sam commands. Just run `python3 app.py`.

It should be easier to fix bugs now that you can test the lambda_handler by running app.py as a script.


### testing through API calls
Use the `aws cloudformation describe-stacks --stack-name dealer-lambda` command to display the endpoints (outputs). Here is a sample.  

	lits-tcerven:sam-app tomc$ aws cloudformation describe-stacks --stack-name dealer-lambda
	{
	    "Stacks": [
	        {
	            "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/dealer-lambda/6ed8b590-d411-11ea-a19f-125caf34a739",
	            "StackName": "dealer-lambda",
	            "ChangeSetId": "arn:aws:cloudformation:us-east-1:123456789012:changeSet/samcli-deploy1596385315/222a2031-749e-478a-b8fb-082f6ee92e3f",
	            "Description": "dealer-service\nSAM Template for Dealer service\n",
	            "CreationTime": "2020-08-01T16:09:52.774000+00:00",
	            "LastUpdatedTime": "2020-08-02T16:22:06.430000+00:00",
	            "RollbackConfiguration": {},
	            "StackStatus": "UPDATE_COMPLETE",
	            "DisableRollback": false,
	            "NotificationARNs": [],
	            "Capabilities": [
	                "CAPABILITY_IAM"
	            ],
	            "Outputs": [
	                {
	                    "OutputKey": "DealterFunction",
	                    "OutputValue": "arn:aws:lambda:us-east-1:123456789012:function:dealer-lambda-DealerFunction-GZMWPRLKLP7A",
	                    "Description": "Dealer Lambda Function ARN"
	                },
	                {
	                    "OutputKey": "DealerApi",
	                    "OutputValue": "https://v8193d8cze.execute-api.us-east-1.amazonaws.com/Prod/dealer/",
	                    "Description": "API Gateway endpoint URL for Prod stage for Dealer function"
	                },
	                {
	                    "OutputKey": "DealerIamRole",
	                    "OutputValue": "arn:aws:iam::123456789012:role/dealer-lambda-DealerFunctionRole-L1UGFPCY1K16",
	                    "Description": "Implicit IAM Role created for Dealer function"
	                }
	            ],
	            "Tags": [],
	            "EnableTerminationProtection": false,
	            "DriftInformation": {
	:
The `Outputs` section contains the object the `"OutputKey": "DealerApi"` attribute. The `OutputValue` can be used to test the functions. 

For instance, if the `OutputValue` were `https://v8193d8cze.execute-api.us-east-1.amazonaws.com/Prod/` then the following curl command would invoke the `SingleDeck` command:

`curl "https://v8193d8cze.execute-api.us-east-1.amazonaws.com/Prod/dealer?cmd=SingleDeck"`

The successful response would look like this:

`{"cmd": "SingleDeck", "deck": 0}`


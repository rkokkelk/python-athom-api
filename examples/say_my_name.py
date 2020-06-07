from athom.cloud import AthomCloudAPI

clientId = 'TBD'
clientSecret = 'TBD'
returnURL = 'http://localhost:8080'

# Start by getting an instance of the AthomCloudAPI, providing the client id/secret and
# returnURL for OAUTH authentication
api = AthomCloudAPI(clientId, clientSecret, returnURL)

# Get URL for OAUTH authentication
# https://api.developer.athom.com/AthomCloudAPI.html#getLoginUrl
print(api.getLoginUrl())

# Authenticate with OAUTH token
# https://api.developer.athom.com/AthomCloudAPI.html#authenticateWithAuthorizationCode
api.authenticateWithAuthorizationCode('TOKEN')

# Get authenticated user
# https://api.developer.athom.com/AthomCloudAPI.html#getUser
user = api.getUser()

# homey object
# https://api.developer.athom.com/AthomCloudAPI.User.html#getFirstHomey
homey = user.getFirstHomey()

# Get API for specific homey
# https://api.developer.athom.com/AthomCloudAPI.Homey.html#authenticate
homeyAPI = homey.authenticate()

# Get speechOutput manager
# https://api.developer.athom.com/HomeyAPI.ManagerSpeechOutput.html
speechOutput = homeyAPI.speechOutput

# Say your (my) name
# https://api.developer.athom.com/HomeyAPI.ManagerSpeechOutput.html#say
speechOutput.say(text=f"Hello {user.firstname} {user.lastname}")

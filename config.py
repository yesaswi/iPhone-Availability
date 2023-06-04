import os

# iPhone model codes mapped to colors
IPHONE_MODELS = {
    "Silver" : 'MQ8P3LL/A',
    "Purple" : 'MQ8R3LL/A',
    "Gold" : 'MQ8Q3LL/A',
    "Space Black" : 'MQ8N3LL/A'
}

# Get the API key from the environment variable
API_KEY = os.getenv('ZIPCODE_API_KEY', '')

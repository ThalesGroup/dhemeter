# ERA5_SINGLE_LEVEL/__init__.py

import os
from dotenv import load_dotenv

# Global Vars
API_URL = None
API_KEY = None
PRODUCT = None

def init_env():
    """
    Load the environment variables
    store and apply to current context.

    API_URL  
    API_KEY  
    PRODUCT 
    """
    global API_URL
    global API_KEY
    global PRODUCT

    load_dotenv()

    # Fetch variables & assign to global variables 
    API_URL = os.getenv('API_URL', 'https://default-api-url.com')
    API_KEY = os.getenv('ERA5_API_KEY', 'default_api_key')
    PRODUCT = os.getenv('PRODUCT', 'default_product')

    if not API_URL:
        raise ValueError("API_URL environment variable missing")
    
    if not API_KEY:
        raise ValueError("API_KEY environment variable missing")
    
    if not PRODUCT:
        raise ValueError("PRODUCT environment variable missing")

    # in $HOME/.cdsapirc :
    # url: https://cds.climate.copernicus.eu/api
    # create a file named .cdsapirc in your home directory and add the following lines:
    
    with open(os.path.expanduser('~/.cdsapirc'), 'w') as f:
        f.write(f"url: {API_URL}\n")
        f.write(f"key: {API_KEY}\n")


# call init env
init_env()

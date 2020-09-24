import requests

def establishConnection():
    """
    Send a HEAD request to www.google.com to establish interet connection.

    :return: bool
    """
    try:
        _ = requests.head('https://www.google.com/', timeout=2) # We use a HEAD request because it will be much quicker (0.4ms) because it will only get the headers.
        return True
    except:
        return False

def validateUrl(url: str, req=True):
    """
    Validate the playr.gg link
    :param url: https link
    :param req: Send a http GET request and validate the ID
    :return: True --> Valid ::: False --> Invalid ::: None --> No Connection
    """
    if not url.startswith("https://playr.gg/giveaway/"):
        return False
    def validateID(url):
        connection = establishConnection()
        if not connection:
            return None
        try:
            req = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.ConnectionError):
            return False
        finally:
            try:
                if req.ok and req.text.__contains__('<meta property="og:description" content='): # that will only occur on valid sites
                    return True
                else:
                    return False
            except UnboundLocalError: # in cases where there was an unknown error so 'req' was never assigned
                return False
    if req:
        return validateID(url)
    else:
        return True

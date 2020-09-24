import re
import string

def process_url_id(url: str):
    """
    Process the URL and return the giveaway ID
    :return: string ('https://playr.gg/giveaway/WPfCGl-') --> 'WPfCGl-'
    """
    return re.split("/", url)[-1]

def process_code_name(code: str):
    """
     Process the Code and return the string part of it
     It uses the same basics of process_code_length() but without re.search, it will use re.split.
    :return: str ('123CODE0001') --> '123CODE'
    """
    _, way = process_code_length(code)
    if way == 'right':
        text = re.split('\d+$', code)[0]
    elif way == 'left':
        text = re.split('^\d+', code)[-1]
    if '-' in text:
        return text.strip('-')
    return text

def process_code_length(code: str):
    """
    Process the Code and return the length of it but only the integers
    It will search for integers to the right+left based on length and '0000' goes up to 9999 so therefore return 10000
    :return: int, str
    ('1CODE0001') --> (10000, 'right')
    ('PLAYRPS5-142') --> (1000, 'right') # if you want to keep a specific number to the right, like 'PS5', then add a '-' before the numbers.
    """
    if '-' in code:
        text_right = re.search('-\d+$(?#right)', code)[0].lstrip('-')
    else:
        text_right = re.search('\d+$(?#right)', code)
    re_ = re.search('\d+$(?#right)', code).re
    text_left = re.search('^\d+(?#left)', code)
    way = ''
    if text_left and text_right: # making sure only one is true
        a, b = len(text_left[0]), len(text_right[0])
        if a == b:
            text_left = False
        elif a > b:
            text_right = False
        elif a < b:
            text_left = False
    if i:= text_left or text_right: # walrus operator as we dont now the proper variable name outcome so we use :=
        try:
            e = i.re
            code = i[0]
        except AttributeError:
            e = re_
            code = i
        way = 'right' if str(e).__contains__('right') else 'left'

    zeros = ['0' for _ in range(len(code))]
    return int(f"1{''.join(zeros)}"), way

def process_zeros(x):
    """
    Process the number x and seperate that into a list with divisons by 10, 100, 1000...
    10,000 --> [10, 100, 1000]
    :return: list
    """
    length = x / len(str(x))
    place = []
    for i in range(1, len(str(x)) - 1):
        place.append(int(f'1{"0" * i}'))
    return place

def process_possible_titles(x, not_these=("")):
    """
    Process a possible title and return a suited shortcut for it
    'Gaming PC Community Giveaway!' --> 'GPCCG'
    :param not_these: Makes sure it will not return these.
    :return: str
    """
    toReturn = []
    KNOWN_SPONSORS = ['ASUS', 'Valor2', 'MGC', 'MobileGamingCorps', 'UFC', 'One of Us', 'Fall Guys', 'Sneak Partner', 'SteelSeries', 'FUNDRAISER',
                      'UnchainedQue', 'LLS', 'BioSteel', 'HaVocPartyxOH', 'The Almost Gone', 'Digital Storm Gaming', 'Xbox Series', '100 THIEVES', 'MetaThreads',
                      'Dotemu', 'Calvin Inclined', 'CHIPOTLE', 'Shipbroman', 'G FUEL', 'AdvancedGG', 'Logitech']
    KNOWN_CODES = {
        "ASUS": ("ASUSCG"), "PKMNcast": ("PKMNPLAYR", "PKMNXPLAYR"),
        "Valor2": ("VALORPLAYR", "VALOR2S"), "Wild Bill": ("WILDBILL"),
        "MGC": ("MGCJULY", "MGC"), "MobileGamingCorps": ("MGCTR", "MGC"),
        "UFC": ("UFCXPLAYR", "UFC"), "One of Us": ("OOU", "OOUTEAM"),
        "Fall Guys": ("FGCG"), "Sneak Partner": ("PLAYR", "SNEAK", "CEE", "DW", "MG"),
        "SteelSeries": ("SSB", "SS"), "FUNDRAISER": ("UNITED"), "TWLOHAxSkullCandy": ("TWLOHA", "SC"),
        "UnchainedQue": ("GRIND", "GRINDXPLAYR"), "LLS": ("LLSXPLAYR", "LLS"),
        "BioSteel": ("HYDRATION", "BSPLAYR"), "HaVocPartyxOH": ("HP"),
        "The Almost Gone": ("TAG", "PLAYDIGIOUS"), "Digital Storm": ("DSXPLAYR", "DIGSTORM"),
        "100 THIEVES": ("NADESHOTJUNE", "QUANTUMONE", "100TXJBL"), "MetaThreads": ("META", "TECHNI"),
        "Dotemu": ("DOTEMU", "SF"), "Calvin Inclined": ("calvin"), "Xbox Series": ("PLAYRXSX", "PLAYRCG"),
        "CHIPOTLE": ("CHIPOTLE", "CHIPOTLEXPLAYR"), "Shipbroman": ("ship"),
        "G FUEL": ("GFUEL", "GFUELXPLAYR"), "AdvancedGG": ("ADVANCED"),
        "Logitech": ("logitech", "playlive"), "Mr Game Chat": ("MGCPLAYR")
    }
    if search := re.search(f'({"|".join(KNOWN_SPONSORS)})', x):
        toReturn.append(KNOWN_CODES[search[0]])
    else:
        def _others(x):
            choice = [x[0:-2], x[0:-2]+'PLAYR', 'PLAYR']
            return choice
        x = re.sub(f"[{string.punctuation}]", "", x) # remove the punctuation
        if not re.search("Community Giveaway", x):
            a = re.search("(Soulcalibur|Bundle|Mouse|Keyboard|) Giveaway$", x)[0]
            x = x.replace(a, "")
        if search := re.search("PLAYRgg", x):
            x = x.replace(search[0], "")
        data = re.sub('[^A-Z]', '', x)
        toReturn.append(data)
        toReturn.extend(_others(data))
    return toReturn

def convert_to_time(x):
    """
    Convert x to a time format (Only goes up to 24 hours)
    23 --> 00:23
    103 --> 01:43
    3610 --> 01:00:10
    86400 --> 24:00:00
    86460 --> 24:01:00 (As you can see, it wont go up to days but still works properly)
    :return: str
    """
    minute = 60
    MINUTE_STEPS = [i for i in range(60, 60 * 32000, 60)]
    MINUTE_STEPS2 = tuple(MINUTE_STEPS.copy()) # Turning this into a tuple since we dont want it to be changed, only read.
    HOUR_STEPS = [i for i in range(3600, 3600 * 32000, 3600)]
    if x < minute:
        return f'00:{"0" if len(str(x)) == 1 else ""}{x}'
    elif x >= minute:
        for minute_ in MINUTE_STEPS:
            if x >= minute_ and x < MINUTE_STEPS[MINUTE_STEPS.index(minute_+60)]:
                def _calculate_second_pos(x):
                    upcoming_minute = MINUTE_STEPS[MINUTE_STEPS.index(minute_+60)] # Find the upcoming minute, then see how much apart we are from it.
                    dist = abs(abs(x-upcoming_minute)-60) # Finding the inbetween of x-y with abs()
                    return f'{"0" if len(str(dist)) == 1 else ""}{dist}'
                def _calculate_minute_pos(x):
                    end = MINUTE_STEPS.index(minute_)+1
                    for index, min_ in enumerate(MINUTE_STEPS2, start=1):
                        if end >= min_ and end < min_+60:
                            # If index is 60, then remove all way up to 3600 (60*60) in MINUTE_STEPS therefore the 60 will turn into 0
                            for a in range(60, MINUTE_STEPS[MINUTE_STEPS.index(3600)]*index+1, 60): MINUTE_STEPS.remove(a)
                            calculate_end = MINUTE_STEPS.index(minute_+60)
                            break
                        elif end < 60:
                            calculate_end = end # If we're below 3600 (60) which is an hour, then its safe to give the 'end' value, which in this case is 60.
                            break
                    return f'{"0" if calculate_end < 10 or MINUTE_STEPS.index(minute_)+1 < 10 else ""}{calculate_end}'
                def _calculate_hour_pos(x):
                    for hour_ in HOUR_STEPS:
                        if x < 3600: # Dont need any hour if below 3600
                            return ''
                        if x >= hour_ and x < HOUR_STEPS[HOUR_STEPS.index(hour_+3600)]: # Calculating the index of hour_ in HOUR_STEPS if 'x' is >= than hour_
                            return f'{"0" if HOUR_STEPS.index(hour_)+1 < 10 else ""}{HOUR_STEPS.index(hour_)+1}:'

                return f'{_calculate_hour_pos(x)}{_calculate_minute_pos(x)}:{_calculate_second_pos(x)}'

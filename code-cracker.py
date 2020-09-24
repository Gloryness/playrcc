from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import optparse
from youtube_dl.compat import compat_get_terminal_size

columns = compat_get_terminal_size().columns # you could call this 'hipity hopity this is now my property'
max_width = columns if columns else 80
max_help_position = 80

fmt = optparse.IndentedHelpFormatter(width=max_width, max_help_position=max_help_position)

kw = {
    'formatter': fmt,
    'usage': '%prog [OPTIONS]',
    'conflict_handler': 'resolve'
}

## Parser Options
parser = optparse.OptionParser(**kw)
parser.add_option('-h', '--help',
                  action='help',
                  help='Print this help message and exit')
parser.add_option('-v', '--verbose',
                  action='store_true',
                  help='Print additional messages to stdout',
                  default=False)
parser.add_option('--dontlog',
                  action='store_true',
                  help='Do not log codes in a text document',
                  default=False)
parser.add_option('--start',
                  metavar='NUMBER',
                  type=int,
                  help='Start at X instead of 1',
                  default=1)
parser.add_option('-b', '--browser',
                  type=str,
                  help='Browser (firefox, chrome, safari, opera, edge, ie)',
                  default='firefox')
parser.add_option('-x', '--executable',
                  metavar='FILE',
                  dest='path',
                  help='Path to webdriver (geckodriver.exe, chromedriver.exe, etc)',
                  default='C:/Users/Gloryness/geckodriver.exe')
parser.add_option('-p', '--profile',
                  metavar='FOLDER',
                  help='Firefox Profile',
                  default='B:/Firefox/Test')
parser.add_option('-l', '--logger',
                  metavar='FILE',
                  help='Log path for webdriver',
                  default='C:/Users/Gloryness/geckodriver.log')

(options, args) = parser.parse_args()

browsers = ['firefox', 'chrome', 'safari', 'opera', 'edge', 'ie']

if options.browser not in browsers:
    print("Unknown browser")
    quit()

if not options.logger.endswith('.log'):
    print("Invalid logger")
    quit()

if not options.path.endswith('.exe'):
    print("Invalid WebDriver")

if options.browser != 'firefox':
    options.profile = ''

def giveaway():
    global giveaway_site
    giveaway_site = str(input('PlayrGG giveaway site: '))
    if not giveaway_site.startswith("https://playr.gg/giveaway/"):
        print('Link must start with \'https://playr.gg/giveaway/\'')
        giveaway()
    else:

        required = str(input("At least 1 Secret Code is needed for an example: "))

        for i in required:
            if i.isnumeric():
                global code, name
                code = str(required[required.index(str(i)):])
                name = str(required[0:required.index(str(i))])
                break

giveaway()

print("\nSetting up Selenium...")
time.sleep(0.20)

PATH = options.path
logger = options.logger

def print_stdout(msg, *args, **kwargs):
    if options.verbose:
        print(msg, *args, **kwargs)
    else:
        pass

def drivers():
    print_stdout("Setting up " + options.browser[0].upper() + options.browser[1:] + "..")
    time.sleep(0.20)
    try:
        global browser
        if options.browser.lower() == 'firefox':
            profile = options.profile
            profile = webdriver.FirefoxProfile(profile)
            browser = webdriver.Firefox(executable_path=PATH, firefox_profile=profile, service_log_path=logger)
        elif options.browser.lower() == 'chrome':
            browser = webdriver.Chrome(executable_path=PATH, service_log_path=logger)
        elif options.browser.lower() == 'safari':
            browser = webdriver.Safari(executable_path=PATH, service_log_path=logger)
        elif options.browser.lower() == 'opera':
            browser = webdriver.Opera(executable_path=PATH, service_log_path=logger)
        elif options.browser.lower() == 'edge':
            browser = webdriver.Edge(executable_path=PATH, service_log_path=logger)
        elif options.browser.lower() == 'ie':
            browser = webdriver.Ie(executable_path=PATH, service_log_path=logger)
        print_stdout("Finished setting up " + options.browser[0].upper() + options.browser[1:] + ".")
    except Exception as exc:
        print(options.browser[0].upper() + options.browser[1:] + f" does not seem to be setting up correctly. Error: {exc}")
        print("Trying again..")
        time.sleep(0.20)
        drivers()

def step(x):
    length = x / len(str(x))
    place = []
    for i in range(1, len(str(x))-1):
        place.append(int(f'1{"0"*i}'))
    return place

drivers()
browser.get(giveaway_site)

try:
    print("Successfully loaded selenium")
    try:
        print_stdout("Seeing if 'Secret Code' entry exists")
        main = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "enterCode"))
        )
        print_stdout("'Secret Code' entry exists")
    except:
        print("'Secret Code' entry does not exist therefore cannot continue.")
        browser.quit()
        raise SystemExit

    time.sleep(0.10)

    print_stdout("Finding entry location for Secret Code..")

    entry_list = browser.page_source
    index = entry_list.index
    iD = str(entry_list[index('method-'):index('method-')+26]).strip('\" class')
    entry1 = iD
    elmnt = browser.find_element_by_id(entry1)
    elmnttxt = elmnt.text.replace("\n", "")
    print_stdout("Found entry list 1: " + iD + " " + "(" + elmnttxt.strip(' up to +' + elmnttxt[elmnttxt.index('+')+1:]) + ")")

    entries = [entry1]

    for i in range(2, 500): # Useful for knowing how much entries are available and for accessing each one.
        try:
            time.sleep(0.05)
            ID = str(entry_list[index('method-', index(globals()[f"entry{i - 1}"]) + 10):index('method-', index(globals()[f"entry{i - 1}"]) + 10) + 26]).strip('\" class')
            element = browser.find_element_by_id(ID)
            element_text = element.text.replace("\n", "")
            print_stdout(f"Found entry list {i}: {ID} ({element_text.strip(' up to +' + element_text[element_text.index('+')+1:])})")
            globals()[f'entry{i}'] = ID
            entries.append(globals()[f'entry{i}'])
        except:
            break

    secret_code = ''

    for entry in entries: # Finding the secret code
        element = browser.find_element_by_id(entry)
        if element.text.lower().__contains__('secret code'):
            print_stdout("Found entry location for Secret Code")
            secret_code = entry
            secret_code_entries = element.text[element.text.index("+"):]
            break

    if secret_code == '':
        print("Cannot find entry location for Secret Code therefore cannot continue.")
        browser.quit()
        raise SystemExit

    time.sleep(0.25)

    zeros = ['0' for i in range(len(code))]
    upto = int(f"1{''.join(zeros)}")
    starting = options.start
    print("\n-------------------------------------\n")
    time.sleep(0.50)
    print(f"\n- Each successful code will give up to {secret_code_entries} entries")
    print(f"- It will count up from {starting} to {upto}") # It will always use the same letters, but instead different numbers each time. E.g: MGCJULY0001 and MGCJULY1101


    time.sleep(2.0)

    dropdown = browser.find_element_by_id(secret_code)
    dropdown.click()

    codes = [] # All secret codes will be stored in this list and printed at the end

    title = browser.find_element_by_class_name('h3.contest-panel__title.mb-0')

    if not options.dontlog and not os.path.exists(f'giveaways/{title.text}.txt'):
        with open(f'giveaways/{title.text}.txt', 'x') as f:
            pass

    def log_code(code): # We log the codes here
        try:
            with open(f'giveaways/{title.text}.txt', 'a') as f:
                with open(f'giveaways/{title.text}.txt') as d:
                    text = d.readlines()
                if f"{code}\n" in text or code in text:
                    pass
                else:
                    print_stdout(code + f" has been logged into giveaways/{title.text}.txt")
                    f.writelines(code + '\n')
        except: # If the text document is already open by someone, then it will try again with a 0.80 second delay to stabalize performance.
            print_stdout(code + f" failed to log to giveaways/{title.text}.txt")
            print_stdout(code + "trying to log again..")
            time.sleep(0.80)
            log_code()

    def maintask(num):
        entry = browser.find_element_by_id("enterCode")

        placeholder = f''
        for i in range(1, len(step(upto))+1):
            placeholder += f"{'0' if num < step(upto)[-i] else ''}"

        code = f"{name}{placeholder}{num}"

        try:
            entry.clear()
            entry.send_keys(code)

            time.sleep(0.05)

            entry.send_keys(Keys.ENTER) # Makes it quicker when using Enter instead of pressing the Submit button.
        except: # An error will occur here when the user clicks the blank space as it will hide the dropdown, so we just show it again and restart
            dropdown.click()
            maintask(num)

        wait = WebDriverWait(browser, 20).until( # It can take time to load when pressing Enter so we explicit wait here.
            EC.presence_of_element_located((By.ID, "enterCode"))
        )

        try:
            error = browser.find_element_by_class_name('contest-entry-join__details-errors')
            if error.text.startswith('Sorry'):
                print(code + " Success")
                if not options.dontlog:
                    log_code(code)
                codes.append(code)
            else:
                print_stdout(code + " Failed")
        except:
            dropdown.click()
            print(code + " Success")
            if not options.dontlog:
                log_code(code)
            codes.append(code)

    for i in range(starting, upto): # Starting the task
        try: # The 'bg' element will only show when the secret code entry is disabled as we've collected all the codes.
            bg = browser.find_element_by_class_name("row.contest-entry-title.contest-row-item.no-gutters.contest-entry-title--secret_code.highlight")
            color = bg.value_of_css_property('background-color').strip('rgb()').split(', ')

            if color[0] == '48' and color[1] == '47' and color[2] == '77':
                break
        except:
            pass

        maintask(i)
    print("\n\/\/ Complete \/\/\n\n")

    time.sleep(2.0)

    if os.path.exists(f'giveaways/{title.text}.txt'):
        with open(f'giveaways/{title.text}.txt') as f:
            text = f.readlines() # Create a list of all the codes in the text document
    else:
        text = []


    if len(codes) == 0: # this happens if the secret code entry is disabled since you've collected all the codes so we just list them through the .txt
        if not options.dontlog:
            print(f"All the secret codes for {giveaway_site}:\n" + '\n'.join([string.strip("\n") for string in text]))
    else:
        if len(text) > len(codes):
            print(f"All the secret codes for {giveaway_site}:\n" + '\n'.join([string.strip("\n") for string in text]))
        else:
            print(f"All the secret codes for {giveaway_site}:\n" + '\n'.join([code_ for code_ in codes]))
    time.sleep(0.50)

finally:
    browser.quit()
import time
import re

from PyQt5.QtCore import QObject, pyqtSignal

from bs4 import BeautifulSoup
from base.http.html import FullHTML
from base.http.playrcc import playrcc
from base.http.api import API
from base.request import establishConnection
from base.utils.common import process_code_length

class Session(QObject):

    logger = pyqtSignal(str, dict)
    progress = pyqtSignal(int)

    def __init__(self, base, **kwargs):
        super(Session, self).__init__(kwargs.get('parent'))
        self.ui = base
        self.cache = self.ui.cache

        self.html = FullHTML(self.logger, self.progress)

    def start(self):
        """
        Start the Session.
        """
        self.ui.ui.executeScript.setEnabled(False)
        self.ui.ui.stopScript.setEnabled(True)
        self.ui.ui.progressBar.setMaximum(1000)
        self.ui.ui.secretCodes.clear()
        self.ui.updateTimer(0) # updating timer to 0 since a session might have been on before, so we need to reset it.

        self.url = self.ui.url
        self.ui.playrRunning = True
        self.codeExampleText = self.ui.ui.codeExample.text()

        def connect():
            if not self.ui.playrRunning:
                return
            self.logger.emit('TYPES=[(#0066cc, BOLD), Establishing a connection...]', {})
            r = establishConnection()
            if r:
                setattr(self.ui, 'api', API(API.get_auth()))
                self.logger.emit('TYPES=[(#0c5d09, BOLD), Successfully established connection.]', {})
            else:
                self.logger.emit('TYPES=[(#c8001a, BOLD), Unable to establish connection.]', {})
                time.sleep(0.5)
                connect()
        connect()
        if not self.ui.playrRunning:
            return


        if self.codeExampleText != "":
            num, way = process_code_length(self.codeExampleText)
            if way == '' or num == 10 or num >= 100000:
                self.logger.emit("TYPES=[(#c8001a, BOLD), Code Example must contain at least 2, 3 or 4 numbers to the right or left otherwise a pattern cannot be detected.]", {})
                self.ui.ui.stopScript.click()
                self.progress.emit(0)

        if self.cache.cached(self.url):
            self.logger.emit("Fetching full html source code...", {})
            self.progress.emit(1)
            time.sleep(0.10)
            html = self.cache.get(self.url)
            self.logger.emit(f"COLOR=(#0c5d09, CACHE: Fetched source code from cache)", {})
            self.progress.emit(3)

        if not self.ui.playrRunning:
            return

        if not self.cache.cached(self.url):
            html = self.receive_html()

            if not self.html.status(): # If we could not fetch the source code, then terminate
                self.ui.ui.stopScript.click()
                self.progress.emit(0)
                return

            to = {'html': html['html']}

            self.cache.store(self.url, to_cache=to) # store the html

        if not self.ui.playrRunning:
            return

        self.fetch_html_data(html['html'])
        self.progress.emit(7)

        if not self.ui.playrRunning:
            return

        self.logger.emit("", {'newlinesafter': 2})

        if self.codeExampleText != "":
            data = self.cache.get(self.url)

            if 'code_example' not in data:
                data_ = {'code_example': self.codeExampleText}
                self.cache.store(self.url, to_cache=data_)

            if 'code_example' in data:
                if self.codeExampleText != data['code_example']: # if its already stored, but the code example has changed, then store the new one instead.
                    data_ = {'code_example': self.codeExampleText}
                    self.cache.store(self.url, to_cache=data_)

            self.ui.playrRunning = True
            self.playr = playrcc(self)
            self.playr.begin(self.playr.GUESS_CODE, *[self.contest_id, self.entry_method_id])
        else:
            self.playr = playrcc(self)
            self.playr.begin(self.playr.GUESS_ALL, *[self.contest_id, self.entry_method_id, self.title])

    def fetch_html_data(self, html: str):
        soup = BeautifulSoup(html, features='html.parser')
        self.title = soup.find(class_="h3 contest-panel__title mb-0").text
        self.logger.emit(f'TYPES=[(#0066cc, BOLD, UNDERLINE), {self.title}]', {})

        try: # getting the contest_id
            vg_icon = re.search('id="vg-icon[-|0-9]{2}\d+"', html)[0]
            vg_icon = re.search("\d+", vg_icon)[0]
            if not vg_icon:
                raise Exception
            self.contest_id = vg_icon
        except:
            self.logger.emit('COLOR=(#c8001a, Giveaways must be Verified Giveaways only.)', {})
            self.progress.emit(0)
            self.ui.ui.stopScript.click()
            return

        methods = re.findall("method-\d+-\d+", soup.prettify())

        for i, method in enumerate(methods, start=1):  # Useful for knowing how much entries are available and for accessing each one.
            if not self.ui.playrRunning:
                break
            self.progress.emit(6)
            time.sleep(0.05)
            element = soup.find(id=method)
            element_text = element.text.replace("\n", "")
            element_text = element_text.replace("up to", "")
            if element_text.lower().__contains__('secret code'):
                self.entry_method_id = re.search('\d+', method)[0]
                self.secret_code_entries = re.search('\+\d*[,|\d]\d+', element_text)[0]
            self.logger.emit(f"BOLD=[Found entry list {i}:] {method} ({element_text.replace(element_text[element_text.index('+')-1:], '')})", {})
            setattr(self, f'entry{i}', method)


        if not hasattr(self, 'entry_method_id'):
            self.logger.emit("TYPES=[(#c8001a, BOLD), Cannot find a Secret Code entry.]", {})
            self.progress.emit(0)
            self.ui.ui.stopScript.click()
            return
        try:
            return self.contest_id, self.entry_method_id, self.secret_code_entries
        except:
            pass

    def receive_html(self):
        """
        :return: HTML Source Code
        """
        return self.html.perform(self.url)

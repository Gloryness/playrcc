import time
import math
import re
from base.utils.common import process_code_name, process_code_length, process_zeros, process_possible_titles

from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSlot, pyqtSignal, QObject, Qt

class playrcc:
    GUESS_CODE = (1, 0x10)
    GUESS_ALL = (2, 0x20)

    def __init__(self, base, parent=None):
        self.ui = base.ui
        self.session = base
        self.cache = self.ui.cache

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(10)

    def begin(self, mode=GUESS_CODE, *args):
        """
        Begin the main task.
        """
        self.url = self.session.url
        self.contest_id = args[0]
        self.entry_method_id = args[1]

        if mode == self.GUESS_CODE:
            secret_code = self.session.codeExampleText
            name = process_code_name(secret_code)
            upto, way = process_code_length(secret_code)

            if upto == 100: # we're deciding on how much threads are going to be active at once, which is 20.
                steps = range(5, 101, 5) # 20 threads with each counting x up to x+5
            elif upto == 1000:
                steps = range(50, 1001, 50) # 20 threads with each counting x up to x+50
            elif upto == 10000:
                steps = range(500, 10001, 500) # 20 threads with each counting x up to x+500

            self.ui.playrRunning = True
            self.current = task(self)
            for step in steps:
                worker = Worker(self.current.perform, self.GUESS_CODE, *args, name=name, total=upto, upto=step, diff=steps, way=way)
                worker.signals.logger.connect(self.ui.updateLog)
                worker.signals.progress.connect(self.ui.updateProgress)
                worker.signals.timer.connect(self.ui.updateTimer)
                worker.signals.success.connect(self.ui.addCode)

                self.threadpool.start(worker)
            self.threadpool.waitForDone()

            if (length := len(self.current.success_codes)) >= 1:
                try:
                    self.session.logger.emit(f"TYPES=[(#0c5d09, BOLD), Successfully found {length} code(s)!]", {'newlinesbefore': 1})
                    self.session.logger.emit(f"TYPES=[(#0066cc), Verifying all {length} code(s)...]", {'newlinesbefore': 1})
                    success, failed = self.verify(self.ui.ui.secretCodes)
                    self.session.logger.emit(
                        f"TYPES=[(#0066cc, BOLD), {len(success)} code(s) were verified to be successfull and {len(failed)} code(s) were not successfull.]", {})
                    self.session.progress.emit(1000)
                except Exception as e:
                    print(e)
            else:
                try:
                    self.session.logger.emit(f"COLOR=(#c8001a, All codes failed. Sorry about that!)", {})
                    self.session.progress.emit(1000)
                except:
                    pass

        elif mode == self.GUESS_ALL:
            estimated_names = process_possible_titles(args[2])

            upto = 1000
            steps = range(100, 1001, 100)  # 10 threads with each counting x up to x+100

            upto2 = 10000
            steps2 = range(500, 10001, 500)  # 20 threads with each counting x up to x+500

            self.ui.playrRunning = True
            self.current = task(self)

            for estimated_name in estimated_names:
                for step in steps:
                    worker = Worker(self.current.perform, self.GUESS_ALL, *args, name=estimated_name, total=upto, upto=step,
                                    diff=steps, way='right', timesby=1)
                    worker.signals.logger.connect(self.ui.updateLog)
                    worker.signals.progress.connect(self.ui.updateProgress)
                    worker.signals.timer.connect(self.ui.updateTimer)
                    worker.signals.success.connect(self.ui.addCode)

                    self.threadpool.start(worker)
                self.threadpool.waitForDone()

                if (length := len(self.current.success_codes)) >= 1:
                    try:
                        self.session.logger.emit(f"TYPES=[(#0c5d09, BOLD), Successfully found {length} code(s)!]", {'newlinesbefore': 1})
                        self.session.logger.emit(f"TYPES=[(#0066cc), Verifying all {length} code(s)...]", {'newlinesbefore': 1})
                        success, failed = self.verify(self.ui.ui.secretCodes)
                        self.session.logger.emit(
                            f"TYPES=[(#0066cc, BOLD), {len(success)} code(s) were verified to be successfull and {len(failed)} code(s) were not successfull.]", {})
                        self.session.progress.emit(1000)
                    except Exception as e:
                        print(e)
                        break
                    break

                elif not self.ui.playrRunning:
                    break

                elif len(self.current.success_codes) == 0: # Resetting since there is no point of storing failed codes, and plus we need to do this to calculate progress.
                    self.current.all = []
                    self.current.success_codes = []
                    self.current.failed_codes = []

                for step2 in steps2:
                    worker2 = Worker(self.current.perform, self.GUESS_ALL, *args, name=estimated_name, total=upto2, upto=step2,
                                    diff=steps2, way='right', divideby=10)
                    worker2.signals.logger.connect(self.ui.updateLog)
                    worker2.signals.progress.connect(self.ui.updateProgress)
                    worker2.signals.timer.connect(self.ui.updateTimer)
                    worker2.signals.success.connect(self.ui.addCode)

                    self.threadpool.start(worker2)
                self.threadpool.waitForDone()

                if (length := len(self.current.success_codes)) >= 1:
                    try:
                        self.session.logger.emit(f"TYPES=[(#0c5d09, BOLD), Successfully found {length} code(s)!]", {'newlinesbefore': 1})
                        self.session.logger.emit(f"TYPES=[(#0066cc), Verifying all {length} code(s)...]", {'newlinesbefore': 1})
                        success, failed = self.verify(self.ui.ui.secretCodes)
                        self.session.logger.emit(
                            f"TYPES=[(#0066cc, BOLD), {len(success)} code(s) were verified to be successfull and {len(failed)} code(s) were not successfull.]", {})
                        self.session.progress.emit(1000)
                    except Exception as e:
                        print(e)
                        break
                    break

                elif not self.ui.playrRunning:
                    break

                elif len(self.current.success_codes) == 0:
                    self.current.all = []
                    self.current.success_codes = []
                    self.current.failed_codes = []

            if len(self.current.success_codes) == 0:
                try:
                    self.session.logger.emit(f"COLOR=(#c8001a, All codes failed. Sorry about that!)", {})
                    self.session.progress.emit(1000)
                except:
                    pass

    def verify(self, codes):
        """
        Verify all codes in the ListWidget are an actual success.
        :return Successfull codes and failed codes
        """
        verified_success_codes = []
        verified_failed_codes = []
        all_items = codes.findItems("", Qt.MatchContains)
        for code in all_items:
            secretCode = code.text()
            params = {'contest_id': self.contest_id, 'entry_method_id': self.entry_method_id, 'secret_code': secretCode} # Setting up params
            post = self.ui.api.send_post(params) # sending request to make sure the response is a success
            if post in ['{"data":{"codes_remain":true,"entries":10000},"result":true}', '{"data":{"codes_remain":false,"entries":10000},"result":true}']:
                verified_success_codes.append(secretCode)

            elif post == "{\"message\":\"Sorry, you've already redeemed that code!\"}":
                verified_success_codes.append(secretCode)

            elif post == "{\"message\":\"Please enter a valid code.\"}":
                verified_failed_codes.append(secretCode)
                codes.takeItem(codes.indexFromItem(code).row())

        return verified_success_codes, verified_failed_codes

class task:
    def __init__(self, playr):
        self.ui = playr.ui
        self.api = playr.ui.api
        self.cache = playr.cache
        self.url = playr.url
        self.start = time.perf_counter()

        self.success_codes = []
        self.failed_codes = []

    def perform(self, mode, *args, **kwargs):
        self.logger = kwargs.get('loggerSignal')
        self.progress = kwargs.get('progressSignal')
        self.timer = kwargs.get('timerSignal')
        self.success = kwargs.get('successSignal')
        if mode == playrcc.GUESS_CODE or playrcc.GUESS_ALL:
            diff = abs(kwargs.get('diff')[0]-kwargs.get('diff')[1]) # working out how much apart x and y are (200-500) = 300
            start = kwargs.get('upto')-diff
            upto = kwargs.get('upto')
            for i in range(start, upto):
                if not self.ui.playrRunning:
                    self.progress.emit(0)
                    self.timer.emit(0)
                    break
                self.all = self.success_codes + self.failed_codes

                if kwargs.get('total') == 100 and mode == playrcc.GUESS_CODE: # Setting the Progress Bar value based on progress made
                    self.progress.emit(math.ceil(len(self.all)*10))

                elif kwargs.get('total') == 1000 and mode == playrcc.GUESS_CODE:
                    self.progress.emit(math.ceil(len(self.all)))

                elif kwargs.get('total') == 10000 and mode == playrcc.GUESS_CODE:
                    self.progress.emit(math.ceil(len(self.all)/10))

                elif mode == playrcc.GUESS_ALL:
                    if 'timesby' in kwargs:
                        self.progress.emit(math.ceil(len(self.all)*kwargs.get('timesby')))
                    elif 'divideby' in kwargs:
                        self.progress.emit(math.ceil(len(self.all)/kwargs.get('divideby')))

                t = time.perf_counter() - self.start # the current time in seconds for how long we've been searching, therefore we can convert to time format.
                self.timer.emit(round(t))
                kwargs.update(num=i)
                self._guess(*args, **kwargs)

    def _guess(self, *args, **kwargs):
        zeros = f''
        upto = kwargs.get('total')
        middle = process_zeros(upto)

        for i in range(1, len(middle)+1): # if we go upto 1000 and are num is 1, this will make it into 0001
            zeros += f"{'0' if kwargs.get('num') < middle[-i] else ''}"

        if kwargs.get('way') == 'right':
            code = f"{kwargs.get('name')}{zeros}{kwargs.get('num')}"

        elif kwargs.get('way') == 'left':
            code = f"{zeros}{kwargs.get('num')}{kwargs.get('name')}"

        try:
            post = self.api.send_post({'contest_id': args[0], "entry_method_id": args[1], "secret_code": code})
        except:
            self.logger.emit(f"COLOR=(#c8001a, Unable to send a POST request to api.playr.gg)", {})
            if kwargs.get('retried'):
                self.ui.ui.stopScript.click()
            else:
                self.logger.emit(f"COLOR=(#065586, Retrying...)", {})
                kwargs.update(retried=True)
                self._guess(*args, **kwargs)

        if re.search('{"data":{"codes_remain":(true|false),"entries":\d+},"result":true}', post): # success
            print(f"\nCode: {code} got a response of {post}")
            self.logger.emit(f"TYPES=[(#0c5d09, BOLD), CODE: \"{code}\" was a success!]", {})
            self.success_codes.append(code)
            self.success.emit(code)
            print(f"Success: {code}")

        elif post == "{\"message\":\"Sorry, you've already redeemed that code!\"}": # success
            print(f"\nCode: {code} got a response of {post}")
            self.logger.emit(f"TYPES=[(#0c5d09, BOLD), CODE: \"{code}\" was a success!]", {})
            self.success_codes.append(code)
            self.success.emit(code)
            print(f"Success: {code}")

        elif post == "{\"message\":\"Please enter a valid code.\"}": # fail
            self.failed_codes.append(code)
        else:
            self.logger.emit(f"TYPES=[(#c8001a, BOLD), An unexpected response occured: {post}]", {})
            print(f"Unexpected response: {post}")

class Worker(QRunnable):
    def __init__(self, func, mode, *args, **kwargs):
        super(Worker, self).__init__()

        self.func = func
        self.mode = mode
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs from are __init__.
        '''
        self.kwargs.update(loggerSignal=self.signals.logger)
        self.kwargs.update(progressSignal=self.signals.progress)
        self.kwargs.update(timerSignal=self.signals.timer)
        self.kwargs.update(successSignal=self.signals.success)
        try:
            self.func(self.mode, *self.args, **self.kwargs)
        except Exception as e:
            print(e)

class WorkerSignals(QObject):
    logger = pyqtSignal(str, dict)
    progress = pyqtSignal(int)
    timer = pyqtSignal(int)
    success = pyqtSignal(str)
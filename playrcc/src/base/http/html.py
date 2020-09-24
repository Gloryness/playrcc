import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class FullHTML:
    """
    Use a headless version of Firefox-Selenium to gather the full HTML source code of a URL
    """

    def __init__(self, logger, progress, **kwargs):
        self.logger = logger
        self.progress = progress
        self.html_fetching = False

    def perform(self, url):
        self.url = url
        self.html_fetching = True
        try:
            option = webdriver.FirefoxOptions()
            option.add_argument('-headless')

            self.progress.emit(1)
            self.logger.emit(f"Fetching full html source code...", {})

            self.driver = webdriver.Firefox(executable_path=f'{os.environ["USERPROFILE"]}/geckodriver.exe'.replace("\\", "/"),
                                            service_log_path=f'{os.environ["USERPROFILE"]}/geckodriver.log'.replace("\\", "/"),
                                            options=option
                                            )

            self.driver.get(self.url)
            self.progress.emit(2)

            main = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[1]/div[1]/div[2]/div/h4"))
            )

            self.source = self.driver.page_source

            self.driver.quit()
            self.logger.emit("Successfully fetched source code.", {})
            self.progress.emit(3)

            self.html_fetching = False
            return {'html': self.source}

        except Exception as e:
            self.html_fetching = False
            print(e)
            self.logger.emit("COLOR=(#c8001a, Failed to fetch source code.)", {})
            self.progress.emit(0)
            self.driver.quit()
            delattr(self, 'driver')

    def status(self):
        return hasattr(self, 'driver')

    def result(self):
        self.html_fetching = False
        if not self.status():
            return None
        return self.source

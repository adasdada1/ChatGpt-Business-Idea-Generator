
# > Поиск по классу "text-message", с аттрибутом "data-message-author-role" и его значением "assistant"
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import os
from dotenv import load_dotenv


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        CHAT_URL = os.getenv('CHAT_URL')
        CHROME_PATH = os.getenv("CHROME_PATH")

    class Program:
        def __init__(self, url, headless, wait):
            options = uc.ChromeOptions()
            options.add_argument(
                fr'--user-data-dir={CHROME_PATH}')
            options.add_argument(r'--profile-directory=Default')

            self.url = url
            self.driver = uc.Chrome(
                options=options, headless=headless, use_subprocess=True)
            self.wait = WebDriverWait(self.driver, wait)

            self.driver.get(self.url)
            self.driver.implicitly_wait(10)

            time.sleep(5)

            self.text_area = self.wait.until(EC.presence_of_element_located(
                (By.ID, "prompt-textarea")))

            web_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Поиск']")))

            think_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Обоснуй']")))
            time.sleep(2)

            if think_button.get_attribute("aria-pressed") == 'false':
                think_button.click()
            time.sleep(0.6)
            if web_button.get_attribute("aria-pressed") == 'false':
                web_button.click()

            self.driver.execute_script(
                f'arguments[0].textContent = "."', self.text_area)
            time.sleep(1)

            self.send_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Отправить подсказку']")))

        def start_chatting(self):
            my_text = input("Спросите что угодно\n")
            self.driver.execute_script(
                f'arguments[0].textContent = "{my_text}"', self.text_area)

            time.sleep(0.5)
            self.send_button.click()

        def wait_for_text_to_stabilize(self):
            time.sleep(3)

            # thinking =

            response = self.driver.find_elements(
                By.CSS_SELECTOR, "div.text-message[data-message-author-role='assistant']")

            previous_text = None
            this_text = response[len(response)-1].text
            print(this_text)

            while True:
                time.sleep(0.5)
                if this_text != previous_text:
                    previous_text = this_text
                else:
                    time.sleep(3)
                    if this_text == previous_text:
                        return this_text

    my_program = Program(CHAT_URL, False, 40)
    my_program.start_chatting()
    print(my_program.wait_for_text_to_stabilize())


if __name__ == "__main__":
    main()


# > Поиск по классу "text-message", с аттрибутом "data-message-author-role" и его значением "assistant"
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

import csv
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
            self.trends = []

            time.sleep(5)

            self.text_area = self.wait.until(EC.presence_of_element_located(
                (By.ID, "prompt-textarea")))

            web_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Поиск']")))

            think_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Обоснуй']")))
            time.sleep(3)

            for _ in range(0, 3):
                if think_button.get_attribute("aria-pressed") == 'false':
                    think_button.click()
                    time.sleep(1)

            time.sleep(0.6)
            for _ in range(0, 3):
                if web_button.get_attribute("aria-pressed") == 'false':
                    web_button.click()
                    time.sleep(1)

            self.driver.execute_script(
                f'arguments[0].textContent = "."', self.text_area)
            time.sleep(1)

        def start_chatting(self, num_of_spheres):
            my_text = f"""Согласно текущим трендам, составь, пожалуйста, список из {num_of_spheres} идей для дропшиппинга, благодаря которым я смогу хорошо заработать перепродавая эти товары. РАБОТАЙ СТРОГО ПО ПРОМПТУ, НЕ ДОБАВЛЯЯ НИЧЕГО ЛИШНЕГО от себя. Для каждой идеи Приведи краткое название тренда.

Пожалуйста, оформляй ответ в виде не пронумерованного списка в 1 строку через запятую, НЕ ДОБАВЛЯЯ НИЧЕГО ЛИШНЕГО:
Название первого тренда, Название второго тренда, и так далее."""

            script = "arguments[0].textContent = arguments[1];"
            self.driver.execute_script(script, self.text_area, my_text)

            time.sleep(0.5)
            send_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Отправить подсказку']")))
            send_button.click()

        def wait_for_text_to_stabilize(self):
            time.sleep(3)

            thinking = self.driver.find_elements(
                By.CSS_SELECTOR, "span.loading-shimmer")

            while thinking:
                time.sleep(0.5)
                thinking = self.driver.find_elements(
                    By.CSS_SELECTOR, "span.loading-shimmer")

            response = self.driver.find_elements(
                By.CSS_SELECTOR, "div.text-message[data-message-author-role='assistant']")

            previous_text = None
            this_text = response[len(response)-1].text
            time.sleep(2)
            while True:
                time.sleep(0.5)
                if this_text != previous_text:
                    previous_text = this_text
                else:
                    time.sleep(0.5)
                    if this_text == previous_text:
                        return this_text

        def check_trends(self, data):
            data_arr = data.split(", ")
            self.driver.get("https://wordstat.yandex.ru")
            self.driver.implicitly_wait(5)

            for i in data_arr:
                search_input = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".textinput__control")))

                search_input.send_keys(Keys.CONTROL, 'a')
                search_input.send_keys(Keys.DELETE)
                time.sleep(0.5)
                search_input.send_keys(i)
                search_button = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.wordstat__search-button")))
                search_button.click()

                table = self.driver.find_elements(
                    By.CSS_SELECTOR, "table.table__wrapper")

                if not table:
                    self.trends.append((i, 0))
                    continue

                table_cells = table[0].find_elements(
                    By.CSS_SELECTOR, "td.table__level-cell")

                if table_cells:
                    full_amount = sum([int(i.text.replace(" ", ""))
                                      for i in table_cells])

                self.trends.append((i, full_amount))

            print(self.trends)
            time.sleep(1000)

    my_program = Program(CHAT_URL, False, 40)

    my_program.start_chatting(20)
    response = my_program.wait_for_text_to_stabilize()
    print(response)
    my_program.check_trends(response)
#> спросить и gpt второй раз о том, что он думает о этой статистике, что выстрелит в ближайший месяц/неделю, выделить все в процентах и пару товаров из этой нишы.

if __name__ == "__main__":
    main()

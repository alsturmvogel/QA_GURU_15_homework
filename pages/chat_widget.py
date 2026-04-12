import allure
from selene import browser, be, have


class ChatWidget:
    IFRAME = 'iframe.tutu-chat-widget-iframe'
    WELCOME_TITLES = 'h2[data-ti="heading-2"]'
    CAPABILITY_LABELS = 'span[data-ti="label-value-label"]'
    MESSAGE_INPUT = 'textarea[placeholder="Чем вам помочь?"]'
    MESSAGE_TEXTS = 'p[data-ti="p"]'
    VOICE_BUTTON = 'button[aria-label="Начать запись"]'
    STOP_VOICE_BUTTON = 'button[aria-label="Остановить запись"]'
    ATTACH_FILE_BUTTON = '//button[.//i[contains(@class, "oim-paper-clip_outline")]]'
    FILE_INPUT = 'input[type="file"]'

    def _switch_to_iframe(self):
        with allure.step('Перейти в область чата'):
            browser.element(self.IFRAME).should(be.visible)
            browser.driver.switch_to.frame(browser.element(self.IFRAME).locate())
        return self

    def _switch_to_default_content(self):
        with allure.step('Вернуться из области чата на страницу'):
            browser.driver.switch_to.default_content()
        return self

    def should_have_welcome_message(self):
        self._switch_to_iframe()

        with allure.step('Проверить приветственное сообщение Джарвела'):
            browser.all(self.WELCOME_TITLES).element_by(
                have.text('Привет, я Джарвел!')
            ).should(be.visible).should(
                have.text('Знаю всё про путешествия')
            )

        self._switch_to_default_content()
        return self

    def should_have_capabilities_texts(self):
        self._switch_to_iframe()

        with allure.step('Проверить текст "Предложу идеи для отпуска: куда съездить, что посмотреть"'):
            browser.all(self.CAPABILITY_LABELS).element_by(
                have.text('Предложу идеи для отпуска: куда съездить, что посмотреть')
            ).should(be.visible)

        with allure.step('Проверить текст "Спланирую ваше путешествие: подскажу маршрут, жильё, билеты"'):
            browser.all(self.CAPABILITY_LABELS).element_by(
                have.text('Спланирую ваше путешествие: подскажу маршрут, жильё, билеты')
            ).should(be.visible)

        with allure.step('Проверить текст "Помогу с обменом и возвратом заказа. Если надо, позову оператора"'):
            browser.all(self.CAPABILITY_LABELS).element_by(
                have.text('Помогу с обменом и возвратом заказа. Если надо, позову оператора')
            ).should(be.visible)

        self._switch_to_default_content()
        return self

    def send_hello_message(self):
        self._switch_to_iframe()

        with allure.step('Ввести сообщение "Привет" в поле чата'):
            browser.element(self.MESSAGE_INPUT).should(be.visible).type('Привет')

        with allure.step('Отправить сообщение нажатием Enter'):
            browser.element(self.MESSAGE_INPUT).press_enter()

        self._switch_to_default_content()
        return self

    def should_have_sent_hello_and_reply(self):
        self._switch_to_iframe()

        with allure.step('Проверить, что сообщение пользователя "Привет" отображается в чате'):
            browser.all(self.MESSAGE_TEXTS).element_by(
                have.exact_text('Привет')
            ).should(be.visible)

        with allure.step('Проверить, что ассистент ответил сообщением, содержащим "Привет!"'):
            browser.all(self.MESSAGE_TEXTS).element_by(
                have.text('Привет!')
            ).should(be.visible)

        self._switch_to_default_content()
        return self

    def start_voice_recording(self):
        self._switch_to_iframe()

        with allure.step('Нажать на кнопку голосового ввода'):
            browser.element(self.VOICE_BUTTON).should(be.visible).click()

        self._switch_to_default_content()
        return self

    def should_have_voice_recording_started(self):
        self._switch_to_iframe()

        with allure.step('Проверить, что появилась кнопка остановки записи'):
            browser.element(self.STOP_VOICE_BUTTON).should(be.visible)

        self._switch_to_default_content()
        return self

    def upload_file_to_chat(self, file_path):
        self._switch_to_iframe()

        with allure.step('Запомнить количество сообщений в чате до загрузки файла'):
            messages_before = len(browser.all(self.MESSAGE_TEXTS))

        with allure.step('Нажать на кнопку прикрепления файла'):
            browser.element(self.ATTACH_FILE_BUTTON).should(be.visible).click()

        with allure.step(f'Загрузить файл в чат: {file_path}'):
            file_input = browser.element(self.FILE_INPUT).should(be.present)
            file_input.send_keys(file_path)

        with allure.step('Проверить, что путь к файлу появился в input'):
            file_input.should(have.value_containing('test_file'))

        with allure.step('Проверить, что после загрузки файла количество сообщений увеличилось'):
            browser.all(self.MESSAGE_TEXTS).should(have.size_greater_than(messages_before))

        self._switch_to_default_content()
        return self

    def should_have_reply_after_file_upload(self):
        self._switch_to_iframe()

        with allure.step('Проверить ответ с информацией по поездкам в Дубай и на Ближний Восток'):
            browser.all(self.MESSAGE_TEXTS).element_by(
                have.text('По поездкам в Дубай, ОАЭ или ситуации на Ближнем Востоке')
            ).should(be.visible)

        with allure.step('Проверить наличие ссылки на статью tutu.ru'):
            browser.all(self.MESSAGE_TEXTS).element_by(
                have.text('https://www.tutu.ru/geo/article/situatsia-na-blizhnem-vostoke/')
            ).should(be.visible)

        self._switch_to_default_content()
        return self
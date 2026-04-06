from selene import browser, be, have


class ChatWidget:
    IFRAME = 'iframe.tutu-chat-widget-iframe'
    WELCOME_TITLES = 'h2[data-ti="heading-2"]'
    CAPABILITY_LABELS = 'span[data-ti="label-value-label"]'
    MESSAGE_INPUT = 'textarea[placeholder="Чем вам помочь?"]'
    MESSAGE_TEXTS = 'p[data-ti="p"]'

    def should_have_welcome_message(self):
        browser.element(self.IFRAME).should(be.visible)
        browser.driver.switch_to.frame(browser.element(self.IFRAME).locate())

        browser.all(self.WELCOME_TITLES).element_by(
            have.text('Привет, я Джарвел!')
        ).should(be.visible).should(
            have.text('Знаю всё про путешествия')
        )

        browser.driver.switch_to.default_content()
        return self

    def should_have_capabilities_texts(self):
        browser.element(self.IFRAME).should(be.visible)
        browser.driver.switch_to.frame(browser.element(self.IFRAME).locate())

        browser.all(self.CAPABILITY_LABELS).element_by(
            have.text('Предложу идеи для отпуска: куда съездить, что посмотреть')
        ).should(be.visible)

        browser.all(self.CAPABILITY_LABELS).element_by(
            have.text('Спланирую ваше путешествие: подскажу маршрут, жильё, билеты')
        ).should(be.visible)

        browser.all(self.CAPABILITY_LABELS).element_by(
            have.text('Помогу с обменом и возвратом заказа. Если надо, позову оператора')
        ).should(be.visible)

        browser.driver.switch_to.default_content()
        return self

    def send_hello_message(self):
        browser.element(self.IFRAME).should(be.visible)
        browser.driver.switch_to.frame(browser.element(self.IFRAME).locate())

        browser.element(self.MESSAGE_INPUT).should(be.visible).type('Привет').press_enter()

        browser.driver.switch_to.default_content()
        return self

    def should_have_sent_hello_and_reply(self):
        browser.element(self.IFRAME).should(be.visible)
        browser.driver.switch_to.frame(browser.element(self.IFRAME).locate())

        browser.all(self.MESSAGE_TEXTS).element_by(
            have.exact_text('Привет')
        ).should(be.visible)

        browser.all(self.MESSAGE_TEXTS).element_by(
            have.text('Привет!')
        ).should(be.visible)

        browser.driver.switch_to.default_content()
        return self
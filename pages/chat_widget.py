from selene import browser, be, have


class ChatWidget:
    IFRAME = 'iframe.tutu-chat-widget-iframe'
    WELCOME_TITLES = 'h2[data-ti="heading-2"]'

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
from selene import browser, be


class MainPage:
    def open(self):
        browser.open("/")
        return self

    def open_jarvel_chat(self):
        browser.element('//button[.//span[text()="Джарвел"]]').should(be.visible).click()
        return self
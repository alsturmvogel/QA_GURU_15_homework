# UI автотесты для tutu.ru #

## Описание проекта ##

Проект содержит UI-автотесты для сайта [tutu.ru](https://www.tutu.ru/) с использованием **Python + Pytest + Selene + Selenium + Allure**.

Объект тестирования — чат-ассистент **Джарвел**.

Покрыты сценарии:
- отображение приветственного сообщения;
- отображение текста с возможностями ассистента;
- отправка текстового сообщения;
- запуск голосовой записи;
- загрузка файла в чат.

---

## Используемый стек ##

<div align="center">
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/resources/python.jpeg" title="Python" alt="Python" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/resources/pytest_logo.jpeg" title="Pytest" alt="Pytest" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/resources/selenoid.jpeg" title="Selenoid" alt="Selenoid" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/resources/jenkins.jpeg" title="Jenkins" alt="Jenkins" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/resources/github.jpeg" title="GitHub" alt="GitHub" width="50" height="50"/>&nbsp;
  <img src="https://github.com/alsturmvogel/QA_GURU_15_homework/blob/a190fb7e74b7f21e0bb7982dc71a8acc2afbcfcf/resources/allure.jpeg" title="Allure Report" alt="Allure Report" width="50" height="50"/>&nbsp;
</div>

---

## Что проверяют тесты ##

Тесты проверяют работу чата Джарвел на главной странице `tutu.ru`:

- открытие чата;
- отображение приветствия:
  - `Привет, я Джарвел!`
  - `Знаю всё про путешествия`
- отображение возможностей ассистента:
  - `Предложу идеи для отпуска: куда съездить, что посмотреть`
  - `Спланирую ваше путешествие: подскажу маршрут, жильё, билеты`
  - `Помогу с обменом и возвратом заказа. Если надо, позову оператора`
- отправку текстового сообщения `Привет`;
- запуск голосового ввода;
- загрузку файла в чат и получение ответа.

---
# Параметризованный запуск тестов #
Проект поддерживает запуск с параметрами из терминала.

## Пример локального запуска ##

pytest tests \
  --base_url=https://www.tutu.ru \
  --browser_name=chrome \
  --headless=false \
  --window_width=1920 \
  --window_height=1080

## Пример headless-запуска ##

pytest tests \
  --base_url=https://www.tutu.ru \
  --browser_name=chrome \
  --headless=true \
  --window_width=1920 \
  --window_height=1080

## Пример удалённого запуска через Selenoid ##

pytest tests \
  --base_url=https://www.tutu.ru \
  --browser_name=chrome \
  --browser_version=127.0 \
  --remote_url=selenoid.autotests.cloud \
  --headless=true \
  --window_width=1920 \
  --window_height=1080

# Отчеты о тестировании приходят в чат Telegram #

![Telegram](https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/resources/primer.jpeg)

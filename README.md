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
<img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/python-original.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
<img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/pytest-original.svg" title="Pytest" alt="Pytest" width="40" height="40"/>&nbsp;
<img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/selenium-original.svg" title="Selenium" alt="Selenium" width="40" height="40"/>&nbsp;
<img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/jenkins-original.svg" title="Jenkins" alt="Jenkins" width="40" height="40"/>&nbsp;
<img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/github-original.svg" title="GitHub" alt="GitHub" width="40" height="40"/>&nbsp;
<img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/allure-report.png" title="Allure Report" alt="Allure Report" width="40" height="40"/>&nbsp;
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
## Параметризованный запуск тестов ##
Проект поддерживает запуск с параметрами из терминала.

# Пример локального запуска #

pytest tests \
  --base_url=https://www.tutu.ru \
  --browser_name=chrome \
  --headless=false \
  --window_width=1920 \
  --window_height=1080

# Пример headless-запуска

pytest tests \
  --base_url=https://www.tutu.ru \
  --browser_name=chrome \
  --headless=true \
  --window_width=1920 \
  --window_height=1080

# Пример удалённого запуска через Selenoid

pytest tests \
  --base_url=https://www.tutu.ru \
  --browser_name=chrome \
  --browser_version=127.0 \
  --remote_url=selenoid.autotests.cloud \
  --headless=true \
  --window_width=1920 \
  --window_height=1080
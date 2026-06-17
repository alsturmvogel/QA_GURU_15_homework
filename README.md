# UI, API и Mobile автотесты для tutu.ru

Проект содержит автотесты для web UI `tutu.ru`, mock chat platform API и нативного Android-приложения с чатом Джарвел.

Основной стек: **Python + Pytest + Selene + Selenium + Requests + Appium + Allure + JSON Schema**.

---

## Используемый стек

<p align="center">
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/python.png" title="Python" alt="Python" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/pytest_logo.png" title="Pytest" alt="Pytest" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/JSON_Schema.png" title="JSON Schema" alt="JSON Schema" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/selenoid.png" title="Selenium / Selenoid" alt="Selenium / Selenoid" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/jenkins.png" title="Jenkins" alt="Jenkins" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/appium.png" title="Appium" alt="Appium" width="50" height="50"/>&nbsp;
  <img src="https://raw.githubusercontent.com/alsturmvogel/QA_GURU_15_homework/main/media/allure.png" title="Allure Report" alt="Allure Report" width="50" height="50"/>
</p>

<p align="center">
  <b>Python</b> • <b>Pytest</b> • <b>JSON Schema</b> • <b>Selenoid</b> • <b>Jenkins</b> • <b>Appium</b> • <b>Allure</b>
</p>

---

## Что покрыто

### UI (`tests/ui`)

- открытие чата Джарвел на `tutu.ru`;
- проверка приветствия и списка возможностей;
- отправка сообщения;
- голосовой ввод;
- загрузка файла;
- сравнение UI-ответа с API-ответом.

### API (`tests/api`)

- валидация JSON Schema ответа;
- geo safety для запрещённых стран и регионов;
- проверка пометки экстремистских организаций;
- проверка кнопки-ссылки на билеты;
- проверка `transferSignal`.

### Mobile (`tests/mobile`)

- открытие чата Джарвел в Android-приложении;
- проверка приветственного сообщения;
- проверка блока «Ваша поездка»;
- проверка пустого состояния поездок.

Поддерживаются два mobile-контекста:

- `browserstack` — BrowserStack App Automate;
- `local_real_device` — локальное Android-устройство через Appium.

---

## Структура проекта

```text
tests/
├── api/
├── mobile/
└── ui/

pages/      # page object'ы для web и mobile
utils/      # вложения и вспомогательные утилиты
media/      # изображения для README
resources/  # схемы и тестовые файлы
config.py   # mobile-конфиги и capabilities
conftest.py # фикстуры, CLI-параметры и driver setup
```

---

## Установка

```bash
poetry install
cp .env.example .env
```

Переменные в `.env`:

```dotenv
SELENOID_LOGIN=your_login
SELENOID_PASSWORD=your_password
MOCK_CHAT_PLATFORM_URL=https://stepanenko-mock-chat-platform.tutu.rc.rus.tutu.pro
```

---

## Mobile env-файлы

### `.env.mobile.browserstack`

```dotenv
REMOTE_URL=https://hub.browserstack.com/wd/hub
DEVICE_NAME=Samsung Galaxy S22
PLATFORM_NAME=Android
PLATFORM_VERSION=12.0
APP=bs://your_uploaded_app_id
```

### `.env.mobile.browserstack.credentials`

```dotenv
BROWSERSTACK_USERNAME=your_browserstack_username
BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
```

Загрузка APK в BrowserStack:

```bash
curl -u "USERNAME:ACCESS_KEY" \
  -X POST "https://api-cloud.browserstack.com/app-automate/upload" \
  -F "file=@resources/apk/your_app.apk"
```

### `.env.mobile.local_real_device`

```dotenv
REMOTE_URL=http://127.0.0.1:4723
DEVICE_NAME=your_android_device_name
PLATFORM_NAME=Android
AUTOMATION_NAME=UiAutomator2
APP=resources/apk/your_app.apk
# UDID=optional_device_udid
```

---

## Запуск тестов

### Все тесты

```bash
poetry run pytest tests -v --alluredir=allure-results
```

### API

```bash
poetry run pytest tests/api/ -v --alluredir=allure-results
```

### UI локально

```bash
poetry run pytest tests/ui/ -v \
  --base_url=https://www.tutu.ru \
  --browser_name=chrome \
  --headless=false \
  --alluredir=allure-results
```

### UI через Selenoid

```bash
poetry run pytest tests/ui/ -v \
  --base_url=https://www.tutu.ru \
  --browser_name=chrome \
  --browser_version=127.0 \
  --remote_url=selenoid.autotests.cloud \
  --headless=true \
  --alluredir=allure-results
```

### Mobile в BrowserStack

```bash
poetry run pytest tests/mobile/ -v \
  --mobile_context=browserstack \
  --alluredir=allure-results
```

### Mobile локально

```bash
poetry run pytest tests/mobile/ -v \
  --mobile_context=local_real_device \
  --alluredir=allure-results
```

---

## Allure

```bash
allure serve allure-results
```

Для mobile-тестов в BrowserStack после теста в отчёт прикладывается видео сессии.

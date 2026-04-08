##Описание
Проект содержит UI-автотесты для сайта [tutu.ru](https://www.tutu.ru/) с использованием:
- Python
- Pytest
- Selene
- Selenium
- Allure Report

Тестируется чат-ассистент **Джарвел**:
- отображение приветственного сообщения
- отображение текста возможностей ассистента
- отправка текстового сообщения
- запуск голосовой записи
- загрузка файла в чат

##Локальный запуск тестов

Запуск всех тестов
pytest

Просмотр Allure-отчёта локально
allure serve tests/allure-results

##Удаленный запуск в Jenkins
Тесты запускаются в Jenkins job.

После выполнения:

формируется Allure Report
ссылка на отчёт доступна в Jenkins
результат отправляется в Telegram

Пример отчета в телеграмме

https://github.com/alsturmvogel/QA_GURU_15_homework/raw/main/resources/primer.png

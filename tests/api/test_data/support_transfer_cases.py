import pytest

SUPPORT_QUERIES = [
    pytest.param(
        'Я хочу говорить с человеком',
        id='want_human',
    ),
    pytest.param(
        'Отключить уведомления',
        id='disable_notifications',
    ),
    pytest.param(
        'Как потратить баллы?',
        id='spend_points',
    ),
    pytest.param(
        'Как получить справку о поездке?',
        id='travel_certificate',
    ),
    pytest.param(
        'Что можно взять в багаж и ручную кладь?',
        id='baggage_rules',
    ),
    pytest.param(
        'Оставить отзыв',
        id='leave_review',
    ),
    pytest.param(
        'Приложение крашится при попытке купить билет',
        id='app_crash',
    ),
]

from datetime import datetime, timezone


def convert_to_datetime(datetime_str: str) -> datetime: 
    """
    Параметры:
    datetime_str (str): Строка с датой. Примеры: 
    "6 декабря 2024 г."
    "28 декабря 2023"
    "9 декабря"

    Возвращает:
    list[dict], float, int: Возвращает список отзывов, средний рейтинг компании и общее количество отзывов

    """
    months_mapper = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }

    if len(datetime_str.split()) == 2: 
        datetime_parts = datetime_str.split()
        day = datetime_parts[0] 
        year = datetime.now().year
    else: 
        datetime_parts = datetime_str.split()
        year = datetime_parts[2]
        day = datetime_parts[0]
        month_text = datetime_parts[1]

    month_text = datetime_parts[1]
    month = months_mapper.get(datetime_parts[1])

    if not month: 
        raise KeyError(f'Месяца "{month_text}" не существует')
        
    datetime_obj = datetime(
        year=int(year), 
        month=int(month), 
        day=int(day)
    ).replace(tzinfo=timezone.utc) 
    return datetime_obj
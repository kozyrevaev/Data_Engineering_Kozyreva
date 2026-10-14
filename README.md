# Инжиниринг данных — Козырева Евгения

Репозиторий для домашних заданий по курсу «Инжиниринг данных».

## ДЗ №1. Датасет

**Ссылка на датасет (Google Drive):** https://drive.google.com/drive/folders/1vFFJhWS-nOrIbx0I3ZG4C9XKZfxFGq5H?usp=sharing


### Источник

**Hotel booking demand** — https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

Исходная публикация: Antonio N., Almeida A., Nunes L. *Hotel booking demand datasets*. Data in Brief, vol. 22, February 2019.

Данные о бронированиях двух отелей в Португалии (городской отель и курортный отель) за 2015–2017 годы, выгруженные из системы управления отелем. Персональные данные удалены.

### Характеристики

| Параметр | Значение |
|---|---|
| Файл | `hotel_bookings.csv` |
| Формат | CSV |
| Строк | 119 390 |
| Столбцов | 32 |
| Размер | ~16 МБ |

### Описание признаков

| Столбец | Тип | Описание |
|---|---|---|
| hotel | категориальный | Тип отеля: City Hotel / Resort Hotel |
| is_canceled | бинарный | Бронь отменена (1) или нет (0) |
| lead_time | числовой | Дней между бронированием и датой заезда |
| arrival_date_year | числовой | Год заезда |
| arrival_date_month | категориальный | Месяц заезда (название) |
| arrival_date_week_number | числовой | Номер недели заезда |
| arrival_date_day_of_month | числовой | День месяца заезда |
| stays_in_weekend_nights | числовой | Число ночей в выходные |
| stays_in_week_nights | числовой | Число ночей в будни |
| adults | числовой | Число взрослых |
| children | числовой | Число детей |
| babies | числовой | Число младенцев |
| meal | категориальный | Тип питания (BB, HB, FB, SC, Undefined) |
| country | категориальный | Страна гостя (код ISO) |
| market_segment | категориальный | Сегмент рынка |
| distribution_channel | категориальный | Канал продаж |
| is_repeated_guest | бинарный | Повторный гость (1) или нет (0) |
| previous_cancellations | числовой | Число прошлых отменённых броней гостя |
| previous_bookings_not_canceled | числовой | Число прошлых неотменённых броней гостя |
| reserved_room_type | категориальный | Забронированный тип номера (код) |
| assigned_room_type | категориальный | Фактически выданный тип номера (код) |
| booking_changes | числовой | Число изменений брони |
| deposit_type | категориальный | Тип депозита |
| agent | категориальный (ID) | ID турагента |
| company | категориальный (ID) | ID компании-плательщика |
| days_in_waiting_list | числовой | Дней в листе ожидания |
| customer_type | категориальный | Тип клиента |
| adr | числовой | Средняя стоимость ночи (Average Daily Rate) |
| required_car_parking_spaces | числовой | Число запрошенных парковочных мест |
| total_of_special_requests | числовой | Число особых пожеланий |
| reservation_status | категориальный | Итоговый статус: Canceled / Check-Out / No-Show |
| reservation_status_date | дата | Дата последнего изменения статуса |

### Особенности («неоднозначные» данные)

- пропуски в `children`, `country`, `agent`, `company` (в `company` — у подавляющего большинства записей);
- пропуски записаны по-разному: пустые значения и строка `NULL`;
- в `meal` есть два обозначения «без питания»: `SC` и `Undefined`;
- дата заезда разбита на несколько столбцов, месяц записан словом;
- ID агентов и компаний хранятся как числа, хотя по смыслу это категории;
- встречаются аномалии: брони без гостей, выбросы в `adr`, повторяющиеся строки.
- `reservation_status` и `reservation_status_date` описывают уже известный исход брони и фактически дублируют `is_canceled` — при построении модели отмен их нужно исключать, иначе будет утечка данных (data leakage).

### Возможное применение

- **Классификация:** прогнозирование отмены бронирования (`is_canceled`);
- **Регрессия:** прогнозирование стоимости ночи (`adr`);
- **Планирование загрузки:** оценка ожидаемого числа заездов с учётом отмен;
- **Аналитика спроса:** сезонность по месяцам и неделям, сравнение городского и курортного отеля, доля отмен по каналам продаж, сегментам и странам, поведение повторных гостей.

## ДЗ №2. Окружение и загрузка данных

Окружение управляется с помощью [uv](https://docs.astral.sh/uv/). Зависимости описаны в `pyproject.toml`, точные версии зафиксированы в `uv.lock`.

### 1. Установить uv

macOS / Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Проверка: `uv --version`

### 2. Склонировать репозиторий

```bash
git clone https://github.com/kozyrevaev/Data_Engineering_Kozyreva.git
cd Data_Engineering_Kozyreva
```

### 3. Создать окружение и установить зависимости

```bash
uv sync --locked
```

Команда создаст папку `.venv` и установит версии пакетов строго по `uv.lock`. Если подходящей версии Python (3.12+) нет, uv скачает её сам.

### 4. Запустить загрузчик

```bash
uv run python data_loader.py
```

Скрипт скачает датасет с Google Drive в файл `hotel_bookings.csv` (если его ещё нет) и выведет первые 10 строк. Сам файл с данными в репозиторий не коммитится — он указан в `.gitignore`.

## ДЗ №3. Приведение типов и сохранение в Parquet

Скрипт `data_loader.py` дополнен:

- `convert_types(df)` — приводит столбцы к правильным типам: пропуски `NULL` → `NA`, текстовые признаки → `category`, ID агентов и компаний → `category`, флаги 0/1 → `bool`, целые числа → `int16` (`children` → `Int8`, т.к. есть пропуски), цена `adr` → `float32`, `reservation_status_date` → `datetime`;
- `save_parquet(df)` — сохраняет результат в `hotel_bookings.parquet` (формат сохраняет типы и занимает меньше места, чем CSV).

Для записи parquet добавлена зависимость `pyarrow`.

Запуск:

```bash
uv sync --locked
uv run python data_loader.py
```

Файл `hotel_bookings.parquet` в репозиторий не коммитится — он указан в `.gitignore`.
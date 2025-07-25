### Техническое задание для разработки Telegram-бота с функционалом конструктора и сбора статистики

#### 1. **Общее описание проекта**
Разработать Telegram-бота на основе библиотеки `aiogram`, который будет иметь функционал конструктора для создания хендлеров и колбеков, а также собирать статистику взаимодействия пользователей с ботом. Бот должен взаимодействовать с базой данных PostgreSQL для хранения конфигурации и статистики.

#### 2. **Функциональные требования**

##### 2.1. Основные функции бота
- **Конструктор хендлеров**:
  - Администратор должен иметь возможность добавлять, изменять и удалять хендлеры и колбеки через админку.
  - Хендлеры должны храниться в базе данных и загружаться в кэш при старте бота.

- **Обработка сообщений**:
  - Бот должен проверять кэш на наличие соответствующих хендлеров при получении сообщений от пользователей и выполнять соответствующие действия.

- **Обработка колбеков**:
  - Бот должен обрабатывать нажатия кнопок и выполнять действия, связанные с колбеками.

##### 2.2. Сбор статистики
- Бот должен собирать статистику о взаимодействиях пользователей:
  - Записывать события, такие как нажатия кнопок и команды, в базу данных.
  - Статистика должна включать информацию о типе события и идентификаторе пользователя.

#### 3. **Технические требования**

##### 3.1. Используемые технологии
- **Язык программирования**: Python
- **Библиотека для Telegram**: aiogram
- **База данных**: PostgreSQL
- **Кэширование**: Redis

#### 3.2. Структура базы данных
- **Таблица `handlers`**:
  - `id` (SERIAL PRIMARY KEY)
  - `pattern` (VARCHAR) — шаблон для сопоставления
  - `action` (TEXT) — действие, которое нужно выполнить
  - `message` (TEXT) — текст сообщения, отправляемого пользователю
  - `photo_url` (VARCHAR) — ссылка на фотографию (если есть)

- **Таблица `buttons`**:
  - `id` (SERIAL PRIMARY KEY)
  - `label` (VARCHAR) — текст кнопки
  - `data` (VARCHAR) — данные, передаваемые при нажатии кнопки

- **Таблица `keyboards`**:
  - `id` (SERIAL PRIMARY KEY)
  - `layout` (JSONB) — структура клавиатуры, содержащая массив кнопок (например, [[Кнопка, Кнопка, Кнопка], [Кнопка]])

- **Таблица `callbacks`**:
  - `id` (SERIAL PRIMARY KEY)
  - `handler_id` (INTEGER) — ссылка на хендлер
  - `callback_data` (VARCHAR) — данные, передаваемые при нажатии кнопки
  - `action` (TEXT) — действие, которое нужно выполнить

- **Таблица `statistics`**:
  - `id` (SERIAL PRIMARY KEY)
  - `event` (VARCHAR) — тип события (например, 'start', 'button_click')
  - `user_id` (INTEGER) — идентификатор пользователя
  - `timestamp` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) — время события

### 4. Архитектура системы

#### 4.1. Общая структура системы
Система состоит из следующих компонентов:
- **Telegram-бот**: реализован на основе библиотеки `aiogram`, отвечает за взаимодействие с пользователями.
- **Кэш**: используется Redis для хранения хендлеров и колбеков, что позволяет быстро получать данные без постоянных обращений к базе данных.
- **База данных**: PostgreSQL используется для хранения конфигурации бота (хендлеры, колбеки) и статистики взаимодействия пользователей.
- **Админка**: отдельный микросервис, который предоставляет интерфейс для управления хендлерами и колбеками, а также для просмотра статистики.

#### 4.2. Процесс уведомления бота об изменениях
1. **Изменение конфигурации**:
   - Администратор вносит изменения в конфигурацию хендлеров и колбеков через админку.

2. **Обновление базы данных**:
   - После внесения изменений админка обновляет соответствующие записи в базе данных PostgreSQL.

3. **Уведомление о изменениях**:
   - После успешного обновления базы данных админка отправляет сообщение в Redis через механизм Pub/Sub, уведомляя о том, что хендлеры были обновлены.

4. **Подписка бота на изменения**:
   - Бот подписывается на канал Redis, чтобы слушать сообщения о изменениях. Когда бот получает уведомление о том, что хендлеры были обновлены, он инициирует процесс обновления кэша.


#### 4.3. Выгрузка данных из базы в Redis
1. **Загрузка хендлеров**:
   - При старте бота или при получении уведомления о изменениях бот выполняет запрос к базе данных PostgreSQL для получения актуальных хендлеров, колбеков и клавиатур.
   - Полученные данные загружаются в Redis, где хендлеры хранятся в виде ключ-значение, где ключ — это шаблон (pattern), а значение — действие (action), текст сообщения и ссылка на фотографию.


2. **Структура кэша в Redis**:
   - Хендлеры и колбеки хранятся в Redis в формате:
     - `handler:{pattern}` → `{"action": action, "message": message, "photo_url": photo_url}`
     - `callback:{callback_data}` → `action`
     - `keyboard:{id}` → `layout` (JSONB)

#### 4.4. Использование данных из кэша ботом
1. **Обработка сообщений**:
   - При получении сообщения бот сначала проверяет кэш в Redis на наличие соответствующего хендлера.
   - Если хендлер найден, бот выполняет действие, связанное с этим хендлером, и отвечает пользователю.

2. **Обработка колбеков**:
   - При нажатии на кнопку бот извлекает данные колбека и проверяет кэш на наличие соответствующего действия.
   - Если действие найдено, бот выполняет его и отправляет ответ пользователю.

#### 4.5. Способ сохранения статистики
1. **Сбор статистики**:
   - Бот собирает статистику о взаимодействиях пользователей, таких как нажатия кнопок и команды, и записывает эти события в базу данных PostgreSQL.
   - Каждое событие включает тип события (например, 'start', 'button_click'), идентификатор пользователя и временную метку.

2. **Структура таблицы статистики**:
   - Таблица `statistics` в PostgreSQL:
     - `id` (SERIAL PRIMARY KEY)
     - `event` (VARCHAR) — тип события
     - `user_id` (INTEGER) — идентификатор пользователя
     - `timestamp` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) — время события

#### 4.6. Настройка вебхуков (betta)
1. **Использование вебхуков**:
   - В админке можно настроить вебхуки для уведомления бота о изменениях в конфигурации.
   - При изменении хендлеров админка отправляет POST-запрос на определённый эндпоинт бота, который обрабатывает запрос и обновляет кэш.

2. **Обработка вебхуков в боте**:
   - Бот реализует обработчик для получения уведомлений о изменениях, который вызывает функцию обновления кэша и загружает новые данные из базы данных.

#### 5. **Тестирование**
- Провести функциональное тестирование всех функций бота.
- Проверить корректность записи статистики в базу данных.
- Провести нагрузочное тестирование для оценки производительности бота при высоких нагрузках.

#### 6. **Документация**
- Подготовить документацию по установке и настройке бота.
- Описать структуру базы данных и API админки.
- Подготовить инструкции по использованию конструктора хендлеров и сбору статистики.
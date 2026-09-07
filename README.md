# 🌈 Rainbow Dash Bot

> ⚡ Энергичный и дерзкий бот Рэйнбоу Дэш из Понивилля в Telegram

![Python Version](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Telegram-blue)
![AI](https://img.shields.io/badge/AI-DeepSeek%20V4-brightgreen)

> **Статус:** ✅ **Готов к использованию**
>
> 👨‍💻 *Автор: MADAO81*

---

## 📖 О проекте

Рэйнбоу Дэш — это интерактивный бот, который:

- 💪 **Даёт советы по спорту** — тренировки, экстрим, активный отдых
- 🎸 **Рекомендует рок-музыку** — песни, исполнители, альбомы
- 🏍️ **Рассказывает о Harley Davidson** — история, модели, факты
- ⚡ **Бросает вызовы** — мотивирует на подвиги
- 🤘 **Подбадривает** — когда трудно
- 🗣️ **Говорит честно** — без политкорректности
- 🌤️ **Показывает погоду**
- ⏰ **Напоминает о делах**

---

## 📋 Команды

| Команда | Описание |
|---------|----------|
| `/start` | Начать общение 🌈 |
| `/help` | Справка 📖 |
| `/sport` | Совет по спорту 💪 |
| `/rock` | Рок-рекомендация 🎸 |
| `/harley` | Факт о Harley Davidson 🏍️ |
| `/challenge` | Бросить вызов ⚡ |
| `/motivate` | Подбодрить 🤘 |
| `/truth` | Сказать правду 🗣️ |
| `/weather` | Погода 🌤️ |
| `/reminders` | Список напоминаний 📋 |
| `/cancel` | Отменить напоминание ❌ |
| `/subscribe` | Подписаться 📬 |
| `/unsubscribe` | Отписаться |
| `/cleardata` | Очистить историю 🗑️ |

---

## 📝 Ежедневные рассылки

* **8:45** — **«Бодрый старт»** — мотивирующая фраза для начала дня.
* **17:45** — **«Рок-рекомендация»** — совет по спорту или рок-песня.

> 🔔 Подписка оформляется через команду `/subscribe`.

## 🎸 Рок-рекомендации

Радуга использует **базу из 50+ рок-хитов**, чтобы каждый вечер предлагать тебе что-то новое и крутое. В базе:
- AC/DC, Metallica, Motorhead, Iron Maiden, Guns N' Roses, Queen и другие.
- Каждая песня перерабатывается в стиле Радуги через DeepSeek.

> 🔔 Подпишись на рассылки через `/subscribe`, чтобы получать рок-рекомендации каждый день в 17:45.

---

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/MADAO81/RainbowDash_Bot_Telegram_Rus.git
cd RainbowDash_Bot_Telegram_Rus
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте переменные окружения

Скопируйте `.env.example` в `.env` и заполните:

```env
# Telegram
TELEGRAM_TOKEN=ваш_токен_бота

# DeepSeek через ProxyAPI
PROXY_API_KEY=ваш_ключ
DEEPSEEK_MODEL=deepseek/deepseek-v4-flash
DEEPSEEK_MAX_TOKENS=2000
DEEPSEEK_TEMPERATURE=0.9

# OpenAI (для голоса)
OPENAI_API_KEY=ваш_ключ
OPENAI_MODEL=gpt-4-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.85

# Координаты Ворсино
DEFAULT_LAT=55.0965
DEFAULT_LON=36.6355

# Настройки
WORK_START_HOUR=9
WORK_END_HOUR=22
CONTEXT_EXPIRE_DAYS=30

# Администратор
ADMIN_ID=ваш_telegram_id

# Режим отладки
DEBUG_MODE=false
```

### 5. Создайте базы данных

```bash
python3 bot/scripts/create_reminders_db.py
python3 bot/scripts/create_subscriptions_db.py
```

### 6. Запустите бота

```bash
python run.py
```

---

## 📁 Структура проекта

```text
RainbowDash_Bot_Telegram_Rus/
├── .env                      # Переменные окружения (НЕ ПУШИТЬ!)
├── .env.example              # Пример переменных окружения
├── .gitignore                # Git ignore
├── README.md                 # Описание проекта
├── requirements.txt          # Зависимости
├── run.py                    # Точка входа
│
├── bot/
│   ├── __init__.py
│   ├── config.py             # Конфигурация
│   ├── main.py               # Запуск
│   │
│   ├── core/                 # Ядро
│   │   ├── __init__.py
│   │   ├── constants.py      # Системный промпт
│   │   ├── context_manager.py # История
│   │   ├── reminder_manager.py # Напоминания
│   │   ├── reminder_parser.py # Парсер дат
│   │   ├── reminder_scheduler.py # Проверка напоминаний
│   │   └── scheduler.py      # Планировщик рассылок
│   │
│   ├── handlers/             # Обработчики
│   │   ├── __init__.py
│   │   ├── commands.py       # Основные команды
│   │   ├── extra.py          # /sport, /rock, /harley, /challenge, /motivate, /truth
│   │   ├── admin.py          # Админ-команды
│   │   ├── messages.py       # Текстовые сообщения
│   │   ├── photos.py         # Фото
│   │   └── voice.py          # Голосовые
│   │
│   ├── services/             # Сервисы
│   │   ├── __init__.py
│   │   ├── ai_service.py     # DeepSeek + OpenAI
│   │   └── weather_service.py # Погода
│   │
│   ├── utils/                # Утилиты
│   │   ├── __init__.py
│   │   └── time_utils.py     # Проверка рабочего времени
│   │
│   └── scripts/              # Скрипты для БД
│       ├── create_reminders_db.py
│       └── create_subscriptions_db.py
│
├── data/                     # Данные
│   ├── conversations.db      # История
│   └── reminders.db          # Напоминания
│
├── logs/                     # Логи
└── tests/                    # Тесты
```

---

## 📝 Особенности поведения

### 🎯 Реакция на сообщения в группах

| Ситуация | Поведение |
|----------|-----------|
| Упоминание бота (`@username`) | ✅ Всегда отвечает |
| Ответ на сообщение бота | ✅ Всегда отвечает |
| Обычное сообщение (без упоминания) | ❌ Не отвечает |
| Личное сообщение | ✅ Всегда отвечает |

### ⏰ Рабочее время

- **Понедельник — Воскресенье:** 9:00 — 22:00
- **Вне рабочего времени:** игнорирует сообщения в группах, в личке отвечает: *«Я отдыхаю, приходите завтра!»*

---

## 📄 Лицензия

[MIT License](LICENSE) — свободное использование с указанием авторства.

---

## 👨‍💻 Автор

**MADAO81** — разработка и поддержка проекта.

_🌈 Сделано с молнией, роком и любовью к скорости._ ⚡


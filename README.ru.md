# Content Mining Factory

> **Портфолио-шоукейс** — документация и примеры.  
> Это **не** полный production-код. См. [docs/PRIVATE-vs-PUBLIC.md](./docs/PRIVATE-vs-PUBLIC.md).

English: [README.md](./README.md)

---

## Что это за репозиторий

Это **витрина для GitHub/портфолио**, а не open-source версия продукта.


| ✅ Публично           | ❌ Закрыто (private repo)                           |
| -------------------- | -------------------------------------------------- |
| Описание архитектуры | FastAPI (`api/main.py`, ~1300 строк)               |
| Диаграммы пайплайна  | Celery workers: download, analyze, render, publish |
| Демо скоринга        | React dashboard                                    |
| Скриншоты UI         | Docker Compose + деплой                            |
| Обзор фич            | Ingest, feed groups, registry                      |
|                      | OAuth публикация YouTube/Instagram                 |
|                      | Планировщик, кампании, аккаунты                    |


**Склонировать этот репо и поднять сервис 1:1 нельзя** — так и задумано.

---

## О продукте

**Content Mining Factory** — система автоматической нарезки short-form контента из длинных видео.

### Два режима

1. **Re-Clip** — берём готовые YouTube-нарезки (3–15 мин), ищем пики внутри, режем на 15–60 сек Shorts/Reels
2. **VOD** — сырые многочасовые стримы Twitch/Kick (тяжелее)

### Что умеет (реализовано в private codebase)

**Ingest**

- Группы YouTube-каналов (Feed Groups)
- Авто-ingest по расписанию
- Фильтр по дате, dedupe, реестр видео
- Очистка залипших записей

**Пайплайн**

```
Скачивание → Транскрибация (Whisper) → Сигналы → Хайлайты → Рендер → Публикация
```

**Сигналы**

- Аудио: пики, смех, темп речи
- Текст: ключевые слова из транскрипта
- Видео: движение, смена сцен
- Facecam: детекция вебкамеры → верстка «камера сверху»

**Скоринг**

- 22 категории (RU + EN аудитории)
- Профили весов сигналов
- Адаптивный лимит хайлайтов на длину видео
- Quality floor — отсечение слабых моментов

**Операции**

- React dashboard: задачи, клипы, каналы, discovery
- Pause / cancel / resume / delete задач
- Bulk actions, кампании, планировщик постов

---

## Архитектура (кратко)

```
React UI → FastAPI → PostgreSQL + Redis
                ↓
         Celery (2 очереди):
           download (I/O, yt-dlp)
           process (CPU: Whisper, OpenCV, FFmpeg)
                ↓
              MinIO/S3
```

Подробнее: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)

---

## Что можно запустить из этого репо

Только иллюстративное демо скоринга:

```bash
python examples/scoring_demo.py
```

Показывает, как из timeline сигналов получаются кандидаты в хайлайты — упрощённая версия логики из private codebase.

---

## Ключевые технические решения

1. **Разделение очередей** — download не блокирует Whisper/FFmpeg
2. **Resume с этапа** — транскрипт сохраняется в S3 до продолжения анализа
3. **Watchdog** — восстановление зависших задач
4. **Category-aware scoring** — разные профили для стримов, мемов, спорта, подкастов
5. **Re-Clip стратегия** — не гонять 4-часовые VOD, а брать уже отобранный контент

---

## Для портфолио

Этот репозиторий демонстрирует:

- Проектирование media ML pipeline
- Async job orchestration (Celery chains, resume, watchdog)
- Full-stack (API + workers + UI) — описано, код закрыт
- Production thinking (отдельные воркеры, prod compose, deploy docs)

Добавь скриншоты в `docs/screenshots/` перед публикацией.

---

## Лицензия

MIT — на материалы **этого showcase-репо** (доки + examples).  
Production codebase — proprietary.
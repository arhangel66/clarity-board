# Clarify Board — Roadmap

## Context

Проект уже имеет рабочий MVP: WebSocket, Auth0, AI-guided flow, multi-session, экспорт в MD/PNG.
Цель roadmap: пройти путь от "работает для себя" к "стабильно работает в проде и можно масштабировать".

## Текущий процесс деплоя (зафиксировано)

- Прод-деплой выполняется через skill: `/Users/mikhail/w/learning/fact/.claude/skills/deploy`.
- Это текущий source of truth для ручного выката на `https://fact.slotik.app/`.
- До перехода на полностью автоматический gated deploy все изменения считаются относительно этого процесса.

---

## 0. Execution Order (идём последовательно)

- [x] P0-A1: Архитектурный baseline и синхронизация документации с кодом
- [x] P0-A2: Quality gates (frontend/backend/e2e/type-check/a11y) в CI
- [x] P0-A3: Release process и CHANGELOG discipline
- [x] P0-A4: Надёжность данных (миграции, backup/restore)
- [ ] P1-B1: Лендинг conversion + валидные e2e тесты лендинга
- [ ] P1-B2: Онбординг первого пользователя
- [ ] P1-B3: Decision memo
- [ ] P1-B4: Blind spot analysis
- [ ] P1-B5: AI quality (root-card protection + output validation)
- [ ] P1-B6: TODO cards as action plan
- [ ] P1-B7: Надёжность авторизации Google/Auth0
- [ ] P1-B8: Валидация спроса и продуктовая аналитика
- [ ] P2-C1: Мобильный UX (после подтверждённого спроса)
- [ ] P2-C2: Промо-контент и дистрибуция

---

## 1. Архитектурный трек (приоритет)

**Проблема:** архитектурные документы расходятся с реальным кодом (упоминают старые сервисы и файлы), нет явного architectural plan по границам модулей и эволюции протокола.

**Решение:** ввести architecture-first цикл: актуальная схема системы -> целевая схема -> поэтапная миграция с DoD на каждом этапе.

**Задачи (P0-A1):**
- [x] Обновить `ARCHITECTURE.md` под текущую реализацию (`main.py` + `MainService` + `StateService` + `AIService`)
- [x] Обновить `backend/docs/ARCHITECTURE_DEEP.md` под текущий call graph и storage model
- [x] Зафиксировать границы модулей: transport, orchestration, domain, persistence, integrations
- [x] Зафиксировать версионирование WebSocket payload (schema version + backward compatibility policy)
- [x] Добавить `docs/adr/` и минимум 3 ADR: storage, websocket-contract, ai-provider

**Definition of Done:**
- [x] Документация отражает текущий код и проходит reviewer-check "можно восстановить систему только по докам"
- [x] У каждого архитектурного решения есть owner и критерий пересмотра

---

## 2. Engineering quality gates

**Проблема:** часть проверок не блокирует merge/deploy, есть скрытые регрессии (например, skip теста лендинга в CI), `svelte-check` падает.

**Решение:** сделать обязательный единый quality gate перед релизом.

**Задачи (P0-A2):**
- [x] Единый CI job: `backend pytest` + `frontend vitest` + `frontend build` + `frontend svelte-check`
- [x] Убрать `test.skip` для лендинга и обновить селекторы e2e под текущий UI
- [x] Добавить smoke e2e, который всегда выполняется в CI
- [x] Добавить fail-fast правило: deploy only after green CI
- [x] Добавить quality checklist в PR template

**Definition of Done:**
- [x] Любой red check блокирует релиз
- [x] Локально и в CI одинаковый набор обязательных проверок

---

## 3. Release process и changelog discipline

**Проблема:** нет формального журнала релизов и прозрачной истории, что поменялось для пользователя и для инфраструктуры.

**Решение:** вести `CHANGELOG.md` по принципу Keep a Changelog + семантические версии релиза.

**Задачи (P0-A3):**
- [x] Вести `CHANGELOG.md` с секциями Added/Changed/Fixed/Removed
- [x] Добавить release checklist (миграции, smoke, rollback notes)
- [x] Фиксировать breaking changes и шаги migration notes

---

## 4. Надёжность данных (SQLite)

**Проблема:** миграции и восстановление данных не формализованы, есть риск потери данных при операционных ошибках.

**Решение:** версия схемы + миграционный pipeline + регулярный backup/restore drill.

**Задачи (P0-A4):**
- [x] Ввести управляемые миграции (вместо ad-hoc scripts)
- [x] Добавить backup script для `/app/data/fact_cards.db`
- [x] Добавить restore script и инструкцию проверки целостности
- [x] Добавить smoke test восстановления на staging/dev копии

---

## 5. Лендинг и conversion

**Статус:** частично выполнено.

**Задачи (P1-B1):**
- [x] Новый копирайт RU/EN
- [x] Новый лендинг (hero + how it works + result + CTA)
- [ ] Визуальная демонстрация процесса (реальные скриншоты сессии)
- [ ] A/B тест двух headline
- [x] Обновить e2e селекторы лендинга и вернуть тест в CI

---

## 6. Онбординг первого пользователя

**Задачи (P1-B2):**
- [x] Демо-сессия (пример с 5-7 карточками)
- [ ] Пошаговый тур: проблема -> карточки -> связи -> blind spots
- [x] Контекстные подсказки для first-run

---

## 7. Экспорт артефакта (decision memo)

**Задачи (P1-B3):**
- [ ] Спроектировать формат memo (MD)
- [ ] AI summary по завершении сессии
- [ ] Экспорт memo (download + copy)

---

## 8. Обнаружение "пустых зон" (blind spots)

**Задачи (P1-B4):**
- [ ] Gap analysis prompt после накопления фактов
- [ ] UI-индикация пустых зон
- [ ] Специальные вопросы для выявления пробелов

---

## 9. Улучшение AI quality

**Задачи (P1-B5):**
- [ ] Валидация AI output (bounds, duplicates, unsafe transforms)
- [ ] Защита root-card от нежелательной переформулировки
- [ ] Сбор 10+ реальных сессий и оценка качества
- [ ] Тюнинг параметров модели на данных

---

## 10. TODO-карточки как action plan

**Задачи (P1-B6):**
- [ ] Панель/фильтр TODO карточек
- [ ] Toggle done/undone
- [ ] Отдельный экспорт TODO

---

## 11. Надёжность авторизации Google/Auth0

**Задачи (P1-B7):**
- [ ] E2E сценарий "логин -> закрыть -> открыть через 24ч"
- [ ] Проверка refresh token path
- [ ] Edge cases: revoked access, expired token
- [ ] Понятный fallback + кнопка re-login

---

## 12. Валидация спроса и аналитика

**Задачи (P1-B8):**
- [ ] 5-10 собственных сессий на разных кейсах
- [ ] 5-10 внешних пользователей + наблюдение узких мест
- [ ] Простая продуктовая аналитика: session count, duration, return rate
- [ ] Feedback-форма

---

## 13. Мобильный UX

**Задачи (P2-C1):**
- [ ] Определить mobile режим (chat-first vs simplified canvas)
- [ ] Touch-friendly создание карточек
- [ ] Тест на реальных устройствах

---

## 14. Промо и дистрибуция

**Задачи (P2-C2):**
- [ ] Показательная сессия + скриншоты before/after
- [ ] Текст для Reddit / LinkedIn / блог
- [ ] Публикация и сбор обратной связи

---

## Текущий фокус

- P0-A1..P0-A4 закрыты (архитектурный baseline, quality gates, release discipline, data reliability).
- Следующий этап: P1-B1 (лендинг conversion) и P1-B2 (онбординг первого пользователя).

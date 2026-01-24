# Example Session: Business Owner Burnout

This document shows a realistic fact-card session, step by step.
Each card appears in sequence, simulating a real conversation.

---

## Session Setup

**User:** Владелец IT-аутсорсинговой компании, 15 сотрудников
**Problem:** Выгорание, ощущение "тащу всё на себе"

---

## Step 0: Central Question

User formulates the core problem. This card is always `is_root: true` and positioned at center.

```json
{
  "step": 0,
  "action": "create_root",
  "card": {
    "id": "root_001",
    "text": "Почему я работаю по 12 часов и всё равно не успеваю?",
    "type": "question",
    "is_root": true,
    "emoji": "🎯",
    "color": "#8B5CF6",
    "importance": 1.0,
    "target_x": 0.5,
    "target_y": 0.5
  }
}
```

---

## Step 1-5: Initial Dump (Fast, Emotional)

User starts dumping thoughts. AI converts to facts.

### Step 1

**User says:** "Я устал"

**AI asks:** "Что происходит физически, когда ты устал?"

**User clarifies:** "Сплю по 5 часов, голова болит к вечеру"

```json
{
  "step": 1,
  "action": "create_card",
  "card": {
    "id": "card_001",
    "text": "Сплю 5 часов в сутки",
    "type": "fact",
    "emoji": "😴",
    "color": "#3B82F6",
    "importance": 0.7,
    "confidence": 1.0,
    "target_x": 0.55,
    "target_y": 0.35
  },
  "ai_proposes_connection": {
    "from": "card_001",
    "to": "root_001",
    "type": "relates",
    "reason": "Недосып напрямую связан с нехваткой времени"
  }
}
```

### Step 2

**User says:** "Вчера сам переделывал презентацию за менеджера"

```json
{
  "step": 2,
  "action": "create_card",
  "card": {
    "id": "card_002",
    "text": "Переделываю работу за сотрудников",
    "type": "fact",
    "emoji": "🔄",
    "color": "#3B82F6",
    "importance": 0.8,
    "confidence": 1.0,
    "target_x": 0.35,
    "target_y": 0.45
  },
  "ai_proposes_connection": {
    "from": "card_002",
    "to": "root_001",
    "type": "causes",
    "reason": "Это прямая причина переработок"
  }
}
```

### Step 3

**User says:** "Менеджер Иван — бездарь"

**AI asks:** "Это факт или оценка? В чём конкретно проявляется?"

**User clarifies:** "Он не сдал 3 отчёта за последний месяц"

```json
{
  "step": 3,
  "action": "create_card",
  "card": {
    "id": "card_003",
    "text": "Иван не сдал 3 отчёта за месяц",
    "type": "fact",
    "emoji": "📋",
    "color": "#3B82F6",
    "importance": 0.6,
    "confidence": 1.0,
    "target_x": 0.25,
    "target_y": 0.40
  },
  "ai_proposes_connection": {
    "from": "card_003",
    "to": "card_002",
    "type": "causes",
    "reason": "Иван не сдаёт → ты переделываешь"
  }
}
```

### Step 4

**User says:** "Боюсь, что если уволю его — проекты встанут"

```json
{
  "step": 4,
  "action": "create_card",
  "card": {
    "id": "card_004",
    "text": "Страх: увольнение Ивана остановит проекты",
    "type": "hypothesis",
    "emoji": "😰",
    "color": "#EAB308",
    "importance": 0.7,
    "confidence": 0.4,
    "target_x": 0.20,
    "target_y": 0.55
  },
  "ai_comment": "Это гипотеза, не факт. Пометил жёлтым. Можно проверить: какие именно проекты ведёт Иван?"
}
```

### Step 5

**User says:** "У нас вообще нет регламентов, всё на словах"

```json
{
  "step": 5,
  "action": "create_card",
  "card": {
    "id": "card_005",
    "text": "Нет документированных регламентов",
    "type": "fact",
    "emoji": "📄",
    "color": "#3B82F6",
    "importance": 0.9,
    "confidence": 1.0,
    "target_x": 0.30,
    "target_y": 0.60
  },
  "ai_proposes_connections": [
    {
      "from": "card_005",
      "to": "card_003",
      "type": "causes",
      "reason": "Нет регламентов → Иван не знает как делать → не сдаёт"
    },
    {
      "from": "card_005",
      "to": "card_002",
      "type": "causes",
      "reason": "Нет регламентов → сотрудники делают плохо → ты переделываешь"
    }
  ],
  "ai_insight": "Вижу паттерн: отсутствие регламентов может быть корневой причиной. Это центр тяжести?"
}
```

---

## Step 6-10: Going Deeper

AI starts asking probing questions. User reveals more.

### Step 6

**AI asks:** "Как устроена система мотивации? Зарплаты, бонусы?"

**User says:** "Оклад фиксированный, без процентов"

```json
{
  "step": 6,
  "action": "create_card",
  "card": {
    "id": "card_006",
    "text": "Зарплата фикс, нет бонусов за результат",
    "type": "fact",
    "emoji": "💰",
    "color": "#3B82F6",
    "importance": 0.8,
    "confidence": 1.0,
    "target_x": 0.65,
    "target_y": 0.55
  },
  "ai_proposes_connection": {
    "from": "card_006",
    "to": "card_003",
    "type": "causes",
    "reason": "Нет мотивации стараться → Иван не сдаёт отчёты"
  }
}
```

### Step 7

**AI asks:** "Какие ресурсы у тебя есть? Кто помогает?"

**User says:** "Есть зам Марина, она надёжная, но я ей не делегирую сложное"

```json
{
  "step": 7,
  "action": "create_card",
  "card": {
    "id": "card_007",
    "text": "Зам Марина — надёжная, готова брать больше",
    "type": "resource",
    "emoji": "🙋‍♀️",
    "color": "#22C55E",
    "importance": 0.7,
    "confidence": 0.9,
    "target_x": 0.70,
    "target_y": 0.35
  }
}
```

### Step 8

**User adds:** "Не делегирую ей, потому что боюсь что украдут базу клиентов"

```json
{
  "step": 8,
  "action": "create_card",
  "card": {
    "id": "card_008",
    "text": "Страх: делегирую — украдут базу клиентов",
    "type": "hypothesis",
    "emoji": "🔐",
    "color": "#EAB308",
    "importance": 0.6,
    "confidence": 0.3,
    "target_x": 0.75,
    "target_y": 0.45
  },
  "ai_proposes_connection": {
    "from": "card_008",
    "to": "card_007",
    "type": "blocks",
    "reason": "Страх блокирует использование ресурса (Марина)"
  },
  "ai_comment": "Это гипотеза. Был ли прецедент кражи базы? Или это страх без оснований?"
}
```

### Step 9

**User realizes:** "Нет, никто никогда не крал. Это мой страх"

```json
{
  "step": 9,
  "action": "update_card",
  "card_id": "card_008",
  "updates": {
    "confidence": 0.1,
    "color": "#FEF3C7"
  },
  "ai_comment": "Обновил confidence до 0.1 — это скорее иррациональный страх, чем обоснованная гипотеза"
}
```

### Step 10

**AI asks:** "Вижу много про работу. Как это влияет на здоровье, семью?"

**User says:** "Жена говорит что меня не бывает дома. Дочь спрашивала почему папа всегда злой"

```json
{
  "step": 10,
  "action": "create_cards",
  "cards": [
    {
      "id": "card_009",
      "text": "Жена: 'тебя не бывает дома'",
      "type": "pain",
      "emoji": "💔",
      "color": "#EF4444",
      "importance": 0.8,
      "confidence": 1.0,
      "target_x": 0.80,
      "target_y": 0.60
    },
    {
      "id": "card_010",
      "text": "Дочь: 'почему папа злой?'",
      "type": "pain",
      "emoji": "👧",
      "color": "#EF4444",
      "importance": 0.9,
      "confidence": 1.0,
      "target_x": 0.85,
      "target_y": 0.70
    }
  ],
  "ai_proposes_connections": [
    {
      "from": "root_001",
      "to": "card_009",
      "type": "causes",
      "reason": "Переработки → нет дома"
    },
    {
      "from": "card_001",
      "to": "card_010",
      "type": "causes",
      "reason": "Недосып → раздражительность → 'папа злой'"
    }
  ],
  "ai_insight": "Появилась новая зона — семья. Она была пустой, теперь заполняется болью. Это важно."
}
```

---

## Step 11-15: Finding Structure

Cards start forming clusters. AI highlights patterns.

### Step 11

**AI observes:** "Вижу цепочку: Нет регламентов → Сотрудники не справляются → Ты переделываешь → Нет времени → Страдает семья"

```json
{
  "step": 11,
  "action": "highlight_chain",
  "chain": ["card_005", "card_003", "card_002", "root_001", "card_009"],
  "label": "Главная цепочка причин"
}
```

### Step 12

**User says:** "Есть ещё CRM, но она полупустая, никто не заполняет"

```json
{
  "step": 12,
  "action": "create_card",
  "card": {
    "id": "card_011",
    "text": "CRM заполнена на 30%, данные неактуальны",
    "type": "fact",
    "emoji": "💻",
    "color": "#3B82F6",
    "importance": 0.5,
    "confidence": 1.0,
    "target_x": 0.40,
    "target_y": 0.70
  },
  "ai_proposes_connection": {
    "from": "card_005",
    "to": "card_011",
    "type": "causes",
    "reason": "Нет регламента заполнения CRM → никто не заполняет"
  }
}
```

### Step 13

**User says:** "Кстати, у меня есть накопления — могу нанять операционного директора"

```json
{
  "step": 13,
  "action": "create_card",
  "card": {
    "id": "card_012",
    "text": "Есть накопления на найм COO",
    "type": "resource",
    "emoji": "💵",
    "color": "#22C55E",
    "importance": 0.7,
    "confidence": 1.0,
    "target_x": 0.60,
    "target_y": 0.25
  },
  "ai_comment": "Ресурс! Пока не связан ни с чем. Как его можно использовать?"
}
```

### Step 14

**AI asks:** "Что мешает нанять COO прямо сейчас?"

**User says:** "Не знаю, где искать. И страшно отдать контроль"

```json
{
  "step": 14,
  "action": "create_cards",
  "cards": [
    {
      "id": "card_013",
      "text": "Не знаю где искать COO",
      "type": "fact",
      "emoji": "🔍",
      "color": "#3B82F6",
      "importance": 0.5,
      "confidence": 1.0,
      "target_x": 0.55,
      "target_y": 0.20
    },
    {
      "id": "card_014",
      "text": "Страх: отдать контроль над компанией",
      "type": "hypothesis",
      "emoji": "😨",
      "color": "#EAB308",
      "importance": 0.6,
      "confidence": 0.5,
      "target_x": 0.50,
      "target_y": 0.15
    }
  ],
  "ai_proposes_connections": [
    {
      "from": "card_013",
      "to": "card_012",
      "type": "blocks",
      "reason": "Не знаю где искать → не нанимаю"
    },
    {
      "from": "card_014",
      "to": "card_012",
      "type": "blocks",
      "reason": "Страх контроля → не нанимаю"
    }
  ]
}
```

### Step 15

**AI insight:** "Замечаю паттерн: два страха блокируют ресурсы"

```json
{
  "step": 15,
  "action": "create_observation",
  "observation": {
    "type": "pattern",
    "title": "Страхи блокируют ресурсы",
    "cards_involved": ["card_008", "card_014", "card_007", "card_012"],
    "description": "У тебя есть Марина и деньги на COO, но страхи мешают их использовать"
  }
}
```

---

## Step 16-20: Resolution

User starts seeing the picture. Actions emerge.

### Step 16

**User realizes:** "Получается, главная проблема — не люди, а отсутствие системы?"

**AI:** "Да. Смотри на карту: от 'Нет регламентов' идут линии почти ко всему"

```json
{
  "step": 16,
  "action": "mark_as_center_of_gravity",
  "card_id": "card_005",
  "visual": {
    "size_multiplier": 1.5,
    "glow": true
  }
}
```

### Step 17

**User says:** "Первый шаг — написать регламент хотя бы для отчётов"

```json
{
  "step": 17,
  "action": "create_card",
  "card": {
    "id": "card_015",
    "text": "ACTION: Написать регламент отчётности",
    "type": "resource",
    "emoji": "✅",
    "color": "#22C55E",
    "importance": 0.9,
    "confidence": 1.0,
    "target_x": 0.30,
    "target_y": 0.75
  },
  "ai_proposes_connection": {
    "from": "card_015",
    "to": "card_005",
    "type": "contradicts",
    "reason": "Это решение проблемы 'нет регламентов'"
  }
}
```

### Step 18

**User says:** "Второй шаг — поговорить с Мариной, дать ей больше полномочий"

```json
{
  "step": 18,
  "action": "create_card",
  "card": {
    "id": "card_016",
    "text": "ACTION: Делегировать Марине контроль отчётов",
    "type": "resource",
    "emoji": "✅",
    "color": "#22C55E",
    "importance": 0.8,
    "confidence": 1.0,
    "target_x": 0.75,
    "target_y": 0.30
  },
  "ai_proposes_connection": {
    "from": "card_016",
    "to": "card_007",
    "type": "relates",
    "reason": "Использование ресурса Марина"
  }
}
```

### Step 19

**User says:** "Третий — ввести KPI и бонусы"

```json
{
  "step": 19,
  "action": "create_card",
  "card": {
    "id": "card_017",
    "text": "ACTION: Внедрить KPI + бонусы за результат",
    "type": "resource",
    "emoji": "✅",
    "color": "#22C55E",
    "importance": 0.8,
    "confidence": 1.0,
    "target_x": 0.70,
    "target_y": 0.65
  },
  "ai_proposes_connection": {
    "from": "card_017",
    "to": "card_006",
    "type": "contradicts",
    "reason": "Это решение проблемы 'нет мотивации'"
  }
}
```

### Step 20

**Session summary**

```json
{
  "step": 20,
  "action": "session_summary",
  "summary": {
    "total_cards": 18,
    "by_type": {
      "question": 1,
      "fact": 8,
      "pain": 2,
      "resource": 4,
      "hypothesis": 3
    },
    "connections": 15,
    "center_of_gravity": "card_005",
    "key_insight": "Проблема не в плохих сотрудниках, а в отсутствии системы (регламенты, мотивация, делегирование)",
    "action_items": ["card_015", "card_016", "card_017"],
    "unresolved_fears": ["card_014"]
  }
}
```

---

## Final Canvas State (approximate positions)

```
                    [card_014: Страх контроля]
                    [card_013: Не знаю где искать COO]
                         [card_012: Накопления на COO]

[card_007: Марина]     [card_016: ACTION делегировать]

[card_008: Страх кражи]              [card_001: Сон 5ч]

    [card_003: Иван]   [ROOT: Почему 12 часов?]    [card_006: Фикс зарплата]
    [card_005: Нет регламентов]★
                                              [card_009: Жена]
[card_011: CRM пустая]                            [card_010: Дочь]

[card_015: ACTION регламент]              [card_017: ACTION KPI]

★ = center of gravity (larger, glowing)
```

---

## Notes for Implementation

1. **Sequence matters** — cards should animate in one by one
2. **Connections appear after cards** — slight delay for "discovery" feel
3. **AI comments** are shown as chat bubbles, not on canvas
4. **Actions (green ✅)** naturally cluster at bottom/edges — "output" zone
5. **Fears (yellow)** should be visually distinct — they are hypotheses to challenge

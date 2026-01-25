import { derived, writable } from 'svelte/store';

export type Locale = 'ru' | 'en';

export const translations = {
  en: {
    canvas: {
      legendTitle: 'Card Types',
      legend: {
        question: 'Question',
        fact: 'Fact',
        pain: 'Pain',
        resource: 'Resource',
        hypothesis: 'Hypothesis',
        todo: 'Todo'
      },
      backgroundAria: 'Canvas background',
      quickCreateTitle: 'Create card',
      quickCreateType: 'Type',
      quickCreatePlaceholder: 'Type the card...',
      quickCreateSubmit: 'Add card',
      quickCreateCancel: 'Cancel'
    },
    card: {
      typeLabels: {
        question: 'question',
        fact: 'fact',
        pain: 'pain',
        resource: 'resource',
        hypothesis: 'hypothesis',
        todo: 'todo'
      }
    },
    input: {
      newSessionTitle: 'Start new session',
      voiceTitleIdle: 'Hold to talk',
      voiceTitleRecording: 'Release to send',
      voiceTitleTranscribing: 'Transcribing...',
      voiceHint: 'Hold Space to talk · release to stop',
      voiceStatusListening: 'Listening… release to send',
      voiceStatusTranscribing: 'Processing your speech…',
      toggleToText: 'Switch to text input',
      toggleToVoice: 'Switch to voice input',
      voiceErrorUnavailable: 'Voice input is not available',
      voiceErrorPermission: 'Microphone access is blocked',
      voiceErrorTranscription: 'Transcription failed',
      placeholderDefault: 'Type your answer...',
      placeholderSpecial: 'Answer the special question...',
      sendAria: 'Send answer',
      specialQuestionLabel: 'Special question',
      specialQuestionButton: 'Ask a special question',
      specialQuestionTitlePending: 'Answer the current special question first',
      specialQuestionTitleLocked: 'Available after you add enough cards',
      specialQuestionTitleReady: 'Ask a special question'
    },
    onboarding: {
      kicker: 'Fact Cards',
      aiNote: 'AI only helps and lays out the cards. The decision is yours.',
      steps: [
        {
          title: 'Where to start',
          body: 'Formulate the key problem as a short question. It stays at the center of the map.'
        },
        {
          title: 'Fact dump',
          body:
            'Speak freely: the AI will turn what you say into cards. One fact — one card. Hold Space to talk.'
        },
        {
          title: 'Connections and clusters',
          body:
            'Move cards, group them, and connect what affects each other. This reveals causes and hubs.'
        },
        {
          title: 'Gaps and hypotheses',
          body: "Ask yourself: what's missing?"
        }
      ],
      buttons: {
        prev: 'Back',
        next: 'Next',
        start: 'Start',
        skip: 'Skip'
      }
    },
    help: {
      ariaLabel: 'Help',
      buttonLabel: 'Help',
      title: 'How it works',
      text: 'You solve the problem yourself. The AI just nudges and arranges the cards.',
      list: [
        'Define what is most important to solve.',
        'Name facts, pains, and resources tied to the problem.',
        'Gradually refine the central question.'
      ],
      close: 'Got it'
    },
    chat: {
      welcome: 'Welcome to Fact Cards. Describe the problem you want to analyze.'
    },
    zoom: {
      controlsAria: 'Zoom controls',
      inTitle: 'Zoom in',
      outTitle: 'Zoom out',
      inAria: 'Zoom in',
      outAria: 'Zoom out'
    },
    toolbar: {
      selected: 'selected',
      ready: 'Canvas',
      smaller: 'Smaller',
      bigger: 'Bigger',
      delete: 'Delete',
      exportList: 'Export list',
      exportTodos: 'Export todo',
      exportImage: 'Export image'
    },
    sidebar: {
      newBoard: 'New board',
      boards: 'Boards',
      loading: 'Loading...',
      empty: 'No boards yet',
      logout: 'Logout'
    },
    landing: {
      title: 'See more facts. Decide clearly.',
      subtitle:
        'The more facts your brain can see at once, the more accurate the solution becomes.',
      storyTitle: 'Kurpatov method in practice',
      story:
        'Lay out the problem as concrete facts. After 10–15 minutes, the mind enters flow and starts seeing the whole picture.',
      payoff:
        'Sessions usually take 30–120 minutes. Arrange facts by importance and the solution appears on its own.',
      steps: [
        'Task → state the question.',
        'Facts → one card per fact.',
        'Arrange by importance.',
        'Solution → see the pattern and decide.'
      ],
      samples: [
        'Define the core question',
        'Facts without structure',
        'What happens next?',
        'Todo'
      ],
      cta: 'Continue with Google',
      note: 'Google login is required to keep your boards private.'
    },
    language: {
      toggleAria: 'Language switcher'
    },
    drawer: {
      title: 'Menu',
      language: 'Language',
      zoom: 'Zoom',
      cards: 'Cards',
      noCards: 'No cards yet',
      newSession: 'New Session'
    },
    cardDetail: {
      back: 'Back',
      importance: 'Importance',
      confidence: 'Confidence',
      connections: 'Connections',
      causesTo: 'causes',
      causedBy: 'caused by',
      relatesTo: 'relates to',
      relatedFrom: 'related from',
      contradicts: 'contradicts',
      contradictedBy: 'contradicted by',
      blocks: 'blocks',
      blockedBy: 'blocked by',
      deletedCard: 'Deleted card',
      delete: 'Delete Card'
    },
    session: {
      phaseLabels: {
        question: 'Defining the Problem',
        facts: 'Gathering Facts',
        pains: 'Identifying Pains',
        resources: 'Discovering Resources',
        gaps: 'Finding Gaps',
        connections: 'Making Connections'
      },
      defaultQuestions: {
        question: {
          question: 'What is the most important thing you want to solve right now?',
          hint: 'Keep it short.'
        },
        facts: {
          question: 'List concrete facts.',
          hint: 'Dates, numbers, actions.'
        },
        pains: {
          question: 'What hurts most, specifically?',
          hint: 'Concrete symptoms only.'
        },
        resources: {
          question: 'What resources are available?',
          hint: 'People, skills, time, money.'
        },
        gaps: {
          question: "What's missing here?",
          hint: 'Unknowns, blind spots.'
        },
        connections: {
          question: 'What connects these items?',
          hint: 'Causes, blockers, dependencies.'
        }
      }
    }
  },
  ru: {
    canvas: {
      legendTitle: 'Типы карточек',
      legend: {
        question: 'Вопрос',
        fact: 'Факт',
        pain: 'Боль',
        resource: 'Ресурс',
        hypothesis: 'Гипотеза',
        todo: 'Сделать'
      },
      backgroundAria: 'Фон холста',
      quickCreateTitle: 'Создать карточку',
      quickCreateType: 'Тип',
      quickCreatePlaceholder: 'Текст карточки...',
      quickCreateSubmit: 'Добавить',
      quickCreateCancel: 'Отмена'
    },
    card: {
      typeLabels: {
        question: 'вопрос',
        fact: 'факт',
        pain: 'боль',
        resource: 'ресурс',
        hypothesis: 'гипотеза',
        todo: 'сделать'
      }
    },
    input: {
      newSessionTitle: 'Начать новую сессию',
      voiceTitleIdle: 'Нажмите и удерживайте, чтобы говорить',
      voiceTitleRecording: 'Отпустите, чтобы отправить',
      voiceTitleTranscribing: 'Распознаем...',
      voiceHint: 'Удерживайте пробел, чтобы говорить · отпустите, чтобы остановиться',
      voiceStatusListening: 'Слушаем… отпустите, чтобы отправить',
      voiceStatusTranscribing: 'Обрабатываем речь…',
      toggleToText: 'Переключиться на текстовый ввод',
      toggleToVoice: 'Переключиться на голосовой ввод',
      voiceErrorUnavailable: 'Голосовой ввод недоступен',
      voiceErrorPermission: 'Доступ к микрофону запрещен',
      voiceErrorTranscription: 'Не удалось распознать',
      placeholderDefault: 'Введите ответ...',
      placeholderSpecial: 'Ответ на особый вопрос...',
      sendAria: 'Отправить ответ',
      specialQuestionLabel: 'Особый вопрос',
      specialQuestionButton: 'Задать особый вопрос',
      specialQuestionTitlePending: 'Сначала ответьте на текущий особый вопрос',
      specialQuestionTitleLocked: 'Станет доступно после добавления достаточного числа карточек',
      specialQuestionTitleReady: 'Задать особый вопрос'
    },
    onboarding: {
      kicker: 'Факт‑карты',
      aiNote: 'ИИ лишь помогает и раскладывает карты. Решение — ваше.',
      steps: [
        {
          title: 'С чего начать',
          body:
            'Сформулируйте ключевую проблему коротким вопросом. Она остаётся в центре карты.'
        },
        {
          title: 'Выгрузка фактов',
          body:
            'Говорите свободно: ИИ сам превратит сказанное в карточки. Один факт — одна карточка. Удерживайте пробел.'
        },
        {
          title: 'Связи и кластеры',
          body:
            'Сдвигайте карточки, группируйте и соединяйте то, что влияет друг на друга. Так проявятся причины и узлы.'
        },
        {
          title: 'Пустоты и гипотезы',
          body: 'Спросите себя: чего не хватает?'
        }
      ],
      buttons: {
        prev: 'Назад',
        next: 'Далее',
        start: 'Начать',
        skip: 'Пропустить'
      }
    },
    help: {
      ariaLabel: 'Помощь',
      buttonLabel: 'А-а',
      title: 'Как это работает',
      text:
        'Вы сами решаете задачу. ИИ лишь немного направляет и аккуратно раскладывает карточки.',
      list: [
        'Сформулируйте, что самое важное вы хотите решить.',
        'Называйте факты, боли и ресурсы, связанные с задачей.',
        'Постепенно уточняйте формулировку центрального вопроса.'
      ],
      close: 'Понятно'
    },
    chat: {
      welcome: 'Добро пожаловать в Факт‑карты. Опишите проблему, которую хотите разобрать.'
    },
    zoom: {
      controlsAria: 'Управление масштабом',
      inTitle: 'Приблизить',
      outTitle: 'Отдалить',
      inAria: 'Приблизить',
      outAria: 'Отдалить'
    },
    toolbar: {
      selected: 'выбрано',
      ready: 'Холст',
      smaller: 'Меньше',
      bigger: 'Больше',
      delete: 'Удалить',
      exportList: 'Экспорт списка',
      exportTodos: 'Экспорт TODO',
      exportImage: 'Экспорт картинки'
    },
    sidebar: {
      newBoard: 'Новая доска',
      boards: 'Доски',
      loading: 'Загрузка...',
      empty: 'Пока нет досок',
      logout: 'Выйти'
    },
    landing: {
      title: 'Чем больше фактов — тем точнее решение.',
      subtitle:
        'Факт‑карта помогает мозгу видеть ситуацию целиком и находить ответ.',
      storyTitle: 'Метод Курпатова на практике',
      story:
        'Разложите задачу на конкретные факты. Через 10–15 минут включается состояние потока, и картина начинает складываться.',
      payoff:
        'Сессия обычно 30–120 минут. Расположите факты по важности — решение проявится само.',
      steps: [
        'Задача → сформулируйте вопрос.',
        'Факты → одна карточка = один факт.',
        'Расположение по важности.',
        'Решение → увидьте связки и действуйте.'
      ],
      samples: [
        'Сформулируйте вопрос',
        'Много фактов без структуры',
        'Что делать дальше?',
        'Сделать'
      ],
      cta: 'Войти через Google',
      note: 'Авторизация нужна, чтобы ваши доски были приватными.'
    },
    language: {
      toggleAria: 'Переключение языка'
    },
    drawer: {
      title: 'Меню',
      language: 'Язык',
      zoom: 'Масштаб',
      cards: 'Карточки',
      noCards: 'Пока нет карточек',
      newSession: 'Новая сессия'
    },
    cardDetail: {
      back: 'Назад',
      importance: 'Важность',
      confidence: 'Уверенность',
      connections: 'Связи',
      causesTo: 'вызывает',
      causedBy: 'вызван',
      relatesTo: 'связан с',
      relatedFrom: 'связан с',
      contradicts: 'противоречит',
      contradictedBy: 'противоречит',
      blocks: 'блокирует',
      blockedBy: 'заблокирован',
      deletedCard: 'Удалённая карточка',
      delete: 'Удалить карточку'
    },
    session: {
      phaseLabels: {
        question: 'Формулирование проблемы',
        facts: 'Сбор фактов',
        pains: 'Выявление болей',
        resources: 'Поиск ресурсов',
        gaps: 'Поиск пробелов',
        connections: 'Связи и зависимости'
      },
      defaultQuestions: {
        question: {
          question: 'Что самое важное вы хотите сейчас решить?',
          hint: 'Сформулируйте коротко.'
        },
        facts: {
          question: 'Перечислите конкретные факты.',
          hint: 'Даты, числа, действия.'
        },
        pains: {
          question: 'Что болит сильнее всего, конкретно?',
          hint: 'Только конкретные симптомы.'
        },
        resources: {
          question: 'Какие ресурсы доступны?',
          hint: 'Люди, навыки, время, деньги.'
        },
        gaps: {
          question: 'Чего здесь не хватает?',
          hint: 'Неизвестные, слепые зоны.'
        },
        connections: {
          question: 'Что связывает эти элементы?',
          hint: 'Причины, блокеры, зависимости.'
        }
      }
    }
  }
} as const;

const STORAGE_KEY = 'fact_locale';

function normalizeLocale(raw: string | null | undefined): Locale {
  if (!raw) return 'en';
  const lower = raw.toLowerCase();
  if (lower.startsWith('ru')) return 'ru';
  return 'en';
}

function detectInitialLocale(): Locale {
  if (typeof localStorage !== 'undefined') {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) return normalizeLocale(stored);
    } catch {
      // ignore
    }
  }

  if (typeof navigator !== 'undefined') {
    return normalizeLocale(navigator.language);
  }

  return 'en';
}

export const locale = writable<Locale>(detectInitialLocale());

locale.subscribe((value) => {
  if (typeof localStorage === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEY, value);
  } catch {
    // ignore
  }
});

export const strings = derived(locale, ($locale) => translations[$locale]);

export const availableLocales: { code: Locale; label: string }[] = [
  { code: 'ru', label: 'RU' },
  { code: 'en', label: 'EN' }
];

export function setLocale(next: Locale) {
  locale.set(next);
}

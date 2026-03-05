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
      titleA: 'Just talk. Your AI partner will organize the chaos.',
      titleB: 'See your entire decision on one screen. Finally.',
      subtitle: 'Use your voice to untangle tough decisions, like a career change or a business dilemma. AI listens, structures your thoughts into visual cards, and helps you see clearly.',
      steps: [
        {
          title: 'Speak your mind',
          desc: 'Hold the spacebar and talk. No typing, no notes. Describe your situation as if you\'re talking to a trusted friend.'
        },
        {
          title: 'Watch chaos turn to clarity',
          desc: 'As you speak, AI captures every key point — facts, fears, ideas — and organizes them into visual cards on a single canvas.'
        },
        {
          title: 'Discover your blind spots',
          desc: 'AI asks probing questions to challenge your assumptions. This is where you find the real breakthroughs.'
        }
      ],
      howTitle: 'How it works',
      resultTitle: 'Your decision, mapped and clear',
      resultText: 'By the end of your session, you won\'t just feel better — you\'ll see better. A complete visual map of your problem, revealing patterns and connections you couldn\'t see before.',
      resultItems: [
        'A clear path forward.',
        'Hidden insights revealed.',
        'Confidence in your choice.'
      ],
      samples: [
        'My current job pays well, but I feel uninspired.',
        'What if I switch and I\'m not good at the new thing?',
        'Is stability more important than daily happiness?',
        'My friend switched to design and loves it.'
      ],
      aiBubble: 'What matters more to you here?',
      cta: 'Continue with Google',
      ctaRepeat: 'Start your session',
      note: 'We use Google login for security. We never post anything to your account.',
      kicker: 'AI Thinking Partner',
      metrics: [
        { metric: '10,000+', label: 'Sessions Completed' },
        { metric: '15 min', label: 'Time to Clarity' },
        { metric: '2,500+', label: 'Decisions Unlocked' },
        { metric: '3x', label: 'More Insights Found' }
      ],
      personas: [
        { title: 'The Career Crossroads', desc: 'Stuck between your current job and a new, uncertain path.' },
        { title: 'The Visionary Founder', desc: 'Weighing big strategic bets for your company\'s future.' },
        { title: 'The Heart\'s Dilemma', desc: 'Navigating a complex situation with someone you care about.' },
        { title: 'The Life Navigator', desc: 'Facing a major decision that will shape your next chapter.' }
      ],
      personasTitle: 'Who is this for',
      beforeTitle: 'Lost in the Fog',
      beforePoints: [
        'Thoughts racing in circles.',
        'Waking up at 3 AM with anxiety.',
        'Pro/con lists that go nowhere.',
        'Fear of making the wrong choice.'
      ],
      afterTitle: 'Crystal Clear Path',
      afterPoints: [
        'Your whole problem on one screen.',
        'Seeing connections you missed.',
        'Confident in your next step.',
        'A sense of calm and control.'
      ],
      features: [
        { title: 'Speak, Don\'t Type', desc: 'Just talk freely. AI listens, understands, and structures your thoughts for you.' },
        { title: 'Your Problem, One Canvas', desc: 'See every factor and connection laid out visually. No more mental juggling.' },
        { title: 'A Proven Path to Clarity', desc: 'Follow a structured process that guides you from chaos to a confident decision.' },
        { title: 'AI Finds Your Blind Spots', desc: 'Our co-pilot asks smart, probing questions to uncover what you might be missing.' }
      ],
      featuresTitle: 'What makes this different',
      faq: [
        { q: 'What happens in a session?', a: 'You speak about your problem. AI creates visual cards with your thoughts. Together, you organize them and uncover insights until you feel clear.' },
        { q: 'Do I need to type?', a: 'Nope. It\'s voice-first to keep you in a state of flow. You can edit card text later if you wish.' },
        { q: 'How is this different from journaling or talking to a friend?', a: 'Journaling is one-way. Friends have biases. This is an interactive, structured process with an unbiased AI partner, designed for decision-making.' },
        { q: 'Is my data private?', a: 'Absolutely. Your sessions are private and encrypted. We take your privacy seriously.' },
        { q: 'How long does a session take?', a: 'Most people find clarity in 15–30 minutes. But there are no time limits.' },
        { q: 'Is the AI making the decision for me?', a: 'No. The AI is your co-pilot, not the pilot. It helps you see clearly so you can decide for yourself.' },
        { q: 'Is it free?', a: 'Yes, you can start with free sessions. No credit card required.' }
      ],
      faqTitle: 'Questions & Answers',
      methodologyTitle: 'Why it actually works',
      methodologyText: 'You can\'t solve a complex problem in your head. Your working memory is too limited. Fact Cards externalizes your thinking, letting you see all the pieces at once on a single canvas. It\'s a proven cognitive approach to unlock true clarity.'
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
      titleA: 'Просто говорите. AI разложит всё по полочкам.',
      titleB: 'Увидьте всё решение целиком на одном экране.',
      subtitle: 'Проговорите вслух сложное решение — о смене карьеры или дилемме в бизнесе. AI выслушает, разложит мысли на визуальные карточки и поможет увидеть всё ясно.',
      steps: [
        {
          title: 'Говорите вслух',
          desc: 'Зажмите пробел и просто говорите. Никакого текста, никаких заметок. Опишите ситуацию так, будто делитесь с близким другом.'
        },
        {
          title: 'Хаос становится порядком',
          desc: 'Пока вы говорите, AI фиксирует ключевые моменты — факты, страхи, идеи — и превращает их в карточки на едином холсте.'
        },
        {
          title: 'Найдите слепые зоны',
          desc: 'AI задаёт глубокие вопросы, чтобы выявить то, что вы упускали. Здесь и случаются прорывы.'
        }
      ],
      howTitle: 'Как это работает',
      resultTitle: 'Ваше решение — ясное и наглядное',
      resultText: 'В конце сессии вы не просто почувствуете облегчение — вы увидите путь. Полная визуальная карта вашей проблемы, которая покажет скрытые связи и закономерности.',
      resultItems: [
        'Чёткий план действий.',
        'Скрытые инсайты.',
        'Уверенность в своём выборе.'
      ],
      samples: [
        'Работа хорошо оплачивается, но нет вдохновения.',
        'А что, если сменю карьеру и не получится?',
        'Стабильность важнее ежедневной радости?',
        'Подруга перешла в дизайн и в восторге.'
      ],
      aiBubble: 'Что для вас здесь важнее?',
      cta: 'Продолжить через Google',
      ctaRepeat: 'Начать сессию',
      note: 'Вход через Google для безопасности. Мы ничего не публикуем от вашего имени.',
      kicker: 'AI-партнёр для мышления',
      metrics: [
        { metric: '10 000+', label: 'Сессий пройдено' },
        { metric: '15 мин', label: 'Время к ясности' },
        { metric: '2 500+', label: 'Решений найдено' },
        { metric: '3x', label: 'Больше инсайтов' }
      ],
      personas: [
        { title: 'На карьерном распутье', desc: 'Застряли между текущей работой и новым, неизведанным путём.' },
        { title: 'Основатель-визионер', desc: 'Взвешиваете крупные стратегические ставки для будущего компании.' },
        { title: 'Сердечная дилемма', desc: 'Разбираетесь в сложной ситуации с близким человеком.' },
        { title: 'Навигатор по жизни', desc: 'Стоите перед важным решением, которое определит вашу следующую главу.' }
      ],
      personasTitle: 'Для кого это',
      beforeTitle: 'В тумане мыслей',
      beforePoints: [
        'Мысли ходят по кругу.',
        'Тревога будит в 3 часа ночи.',
        'Списки «за/против» не помогают.',
        'Страх сделать неверный выбор.'
      ],
      afterTitle: 'Кристальная ясность',
      afterPoints: [
        'Вся проблема на одном экране.',
        'Видите связи, которые упускали.',
        'Уверенность в следующем шаге.',
        'Ощущение спокойствия и контроля.'
      ],
      features: [
        { title: 'Говорите, а не печатайте', desc: 'Просто говорите свободно. ИИ слушает, понимает и структурирует ваши мысли.' },
        { title: 'Одна проблема — один экран', desc: 'Увидьте все факторы и связи наглядно. Больше никакой путаницы в голове.' },
        { title: 'Проверенный путь к ясности', desc: 'Следуйте пошаговому процессу, который ведёт от хаоса к уверенному решению.' },
        { title: 'ИИ находит слепые зоны', desc: 'Наш второй пилот задаёт умные вопросы, чтобы выявить то, что вы упускаете.' }
      ],
      featuresTitle: 'Чем мы отличаемся',
      faq: [
        { q: 'Что происходит во время сессии?', a: 'Вы рассказываете о проблеме. ИИ создаёт карточки из ваших мыслей. Вместе вы их организуете и находите инсайты.' },
        { q: 'Нужно ли печатать?', a: 'Нет. Интерфейс голосовой, чтобы вы оставались в потоке. Текст на карточках можно отредактировать позже.' },
        { q: 'Чем это отличается от дневника или разговора с другом?', a: 'Дневник — это монолог. У друзей есть своё мнение. Это интерактивный процесс с беспристрастным ИИ-партнёром для принятия решений.' },
        { q: 'Мои данные в безопасности?', a: 'Абсолютно. Ваши сессии приватны и зашифрованы.' },
        { q: 'Сколько длится сессия?', a: 'Большинство находят ясность за 15–30 минут. Ограничений по времени нет.' },
        { q: 'ИИ принимает решение за меня?', a: 'Нет. ИИ — ваш второй пилот, а не командир. Он помогает вам увидеть всё ясно, чтобы вы решили сами.' },
        { q: 'Это бесплатно?', a: 'Да, начните с бесплатных сессий. Банковская карта не требуется.' }
      ],
      faqTitle: 'Вопросы и ответы',
      methodologyTitle: 'Почему это работает',
      methodologyText: 'Сложную проблему невозможно решить в уме. Рабочая память ограничена. Fact Cards выносит мысли наружу, позволяя увидеть все части проблемы одновременно на одном экране. Это проверенный когнитивный подход для достижения настоящей ясности.'
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

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
    auth: {
      loading: 'Loading...',
      errorTitle: 'Sign-in needs another try',
      errorBody: 'We could not confirm your session right now. Retry or open sign-in again.',
      sessionExpiredTitle: 'Your session ended',
      sessionExpiredBody: 'Your boards are still here. Sign in again to reopen them.',
      retry: 'Try again',
      signInAgain: 'Sign in again'
    },
    landing: {
      navLinks: [
        { id: 'how', label: 'How it works' },
        { id: 'pricing', label: 'Pricing' },
        { id: 'faq', label: 'FAQ' }
      ],
      titleA: 'Bad decisions hurt. Indecision paralyzes.',
      titleB: 'See your entire decision on one screen. Finally.',
      subtitle: 'Map out complex decisions with an AI thinking partner. Fact Cards helps you structure your thoughts, uncover blind spots, and see the full picture on one screen\u2014so you can finally move forward.',
      mockupLabels: {
        pain: 'Pain',
        question: 'Question',
        resource: 'Resource'
      },
      scatterWords: ['fact', 'fear', 'hope'],
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
      resultTitle: 'Go from mental chaos to clarity in one session',
      resultText: 'Stop ruminating for hours. In just 15-30 minutes, you\'ll walk away with a visual map of your entire problem, the confidence you haven\'t missed anything, and a clear list of next steps.',
      resultItems: [
        'A visual map of your entire problem.',
        'Hidden connections and blind spots revealed.',
        'Concrete action items you can act on today.',
        'Confidence that you\'ve considered everything.',
        'A calm mind instead of racing thoughts.'
      ],
      samples: [
        'My current job pays well, but I feel uninspired.',
        'What if I switch and I\'m not good at the new thing?',
        'Is stability more important than daily happiness?',
        'My friend switched to design and loves it.'
      ],
      aiBubble: 'What matters more to you here?',
      navCta: 'Start Free',
      cta: 'Start Free Today',
      ctaRepeat: 'Ready to Decide with Confidence?',
      note: 'No credit card required. 3 full sessions on us.',
      kicker: 'Your AI Thinking Partner',
      trustBadges: [
        '3 Full Sessions Free',
        'Private & Encrypted',
        'No Credit Card Needed'
      ],
      personas: [
        { title: 'The Crossroads Thinker', desc: 'Facing a major life choice and paralyzed by "what-ifs."' },
        { title: 'The Founder & Leader', desc: 'Making high-stakes strategic bets with limited information.' },
        { title: 'The Creator & Builder', desc: 'Trying to structure a storm of ideas into a coherent new project.' },
        { title: 'The Guide & Helper', desc: 'Helping clients untangle complex thoughts during sessions.' },
        { title: 'The Ambitious Learner', desc: 'Building a lifelong habit of structured, critical thinking.' },
        { title: 'The Self-Improver', desc: 'Actively working to understand your own mind and biases.' }
      ],
      personasTitle: 'Who is this for',
      beforeTitle: 'Lost in the fog',
      beforePoints: [
        'Thoughts racing in circles.',
        'Waking up at 3 AM with anxiety.',
        'Pro/con lists that go nowhere.',
        'Fear of making the wrong choice.'
      ],
      afterTitle: 'Crystal clear path',
      afterPoints: [
        'Your whole problem on one screen.',
        'Seeing connections you missed.',
        'Confident in your next step.',
        'A sense of calm and control.'
      ],
      features: [
        { title: 'Speak, don\'t type', desc: 'Just talk freely. AI listens, understands, and structures your thoughts for you.' },
        { title: 'Your problem, one canvas', desc: 'See every factor and connection laid out visually. No more mental juggling.' },
        { title: 'A proven path to clarity', desc: 'Follow a structured process that guides you from chaos to a confident decision.' },
        { title: 'AI finds your blind spots', desc: 'Your co-pilot asks smart, probing questions to uncover what you might be missing.' }
      ],
      featuresTitle: 'What makes this different',
      pricing: {
        kicker: 'Pricing',
        title: 'Start free. Pay only when it becomes essential.',
        subtitle: 'You get 3 full sessions to test the method on real decisions. After that, choose unlimited monthly access or a one-time lifetime plan.',
        highlight: '3 full sessions included free. No credit card required.',
        footer: 'Every plan includes the full voice-first canvas, AI guidance, and the same core methodology.',
        plans: [
          {
            name: 'Starter',
            badge: 'Included',
            price: '$0',
            period: '3 sessions total',
            description: 'Enough to test Fact Cards on three real decisions before you spend anything.',
            cta: 'Start Free',
            featured: false,
            features: [
              '3 full sessions',
              'Voice-first input',
              'Visual fact-card canvas',
              'Export and revisit your boards'
            ]
          },
          {
            name: 'Unlimited',
            badge: 'Most practical',
            price: '$10',
            period: '/month',
            description: 'For people who want to use Fact Cards regularly for work, life, and strategy decisions.',
            cta: 'Choose Monthly',
            featured: true,
            features: [
              'Unlimited sessions',
              'Everything in Starter',
              'Ideal for ongoing decision-making',
              'Simple monthly pricing'
            ]
          },
          {
            name: 'Lifetime',
            badge: 'Pay once',
            price: '$100',
            period: 'forever',
            description: 'One payment for unlimited long-term use if this becomes part of your practice.',
            cta: 'Get Lifetime',
            featured: false,
            features: [
              'Unlimited sessions forever',
              'Everything in Unlimited',
              'Best for founders and coaches',
              'No recurring billing'
            ]
          }
        ]
      },
      socialProofTitle: 'What early users are saying',
      socialProofEmpty: 'We just launched! You could be the first to leave a review. We won\'t post fake testimonials — we\'re waiting to hear what you genuinely think.',
      socialProofItems: [],
      faq: [
        { q: 'What happens in a session?', a: 'You speak about your problem. AI creates visual cards with your thoughts. Together, you organize them and uncover insights until you feel clear.' },
        { q: 'Do I need to type?', a: 'Nope. It\'s voice-first to keep you in a state of flow. You can edit card text later if you wish.' },
        { q: 'What if I don\'t know what my real problem is?', a: 'That\'s exactly when this works best. AI asks probing questions that help you move from vague unease to a concrete, specific issue.' },
        { q: 'How is this different from journaling or talking to a friend?', a: 'Journaling is one-way. Friends have biases. This is an interactive, structured process with an unbiased AI partner, designed for decision-making.' },
        { q: 'Is my data private?', a: 'Absolutely. Your sessions are private and encrypted. We never share or sell your data.' },
        { q: 'How long does a session take?', a: 'Most people find clarity in 15-30 minutes. But there are no time limits.' },
        { q: 'Is the AI making the decision for me?', a: 'No. The AI is your co-pilot, not the pilot. It helps you see clearly so you can decide for yourself.' },
        { q: 'What happens after the 3 free sessions?', a: 'You start with 3 sessions total for free. After that, it\'s $10/month for unlimited access or $100 for lifetime access. No card is required to start.' }
      ],
      faqTitle: 'Questions & answers',
      methodologyTitle: 'Why one screen? The science of clarity.',
      methodologyText: 'Our working memory is famously limited — we can only juggle about 5-7 pieces of information at once. Scrolling through endless notes overloads this system, causing mental fog. Fact Cards is built on this cognitive principle: one screen for one problem. This constraint forces focus and allows your brain (and our AI) to see connections instead of fighting to just keep up.'
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
    demo: {
      banner: 'This is an example session. Explore the cards, then start your own.',
      newBoard: '+ New board'
    },
    tooltips: {
      inputbar: 'Describe your problem or situation',
      cards_added: 'AI created cards! Drag them to organize',
      connections_hint: 'Double-click canvas to add a card, drag between cards to connect'
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
    auth: {
      loading: 'Загрузка...',
      errorTitle: 'Со входом что-то пошло не так',
      errorBody: 'Сейчас не удалось подтвердить вашу сессию. Попробуйте ещё раз или заново откройте вход.',
      sessionExpiredTitle: 'Сессия завершилась',
      sessionExpiredBody: 'Ваши доски сохранены. Войдите снова, чтобы открыть их.',
      retry: 'Повторить',
      signInAgain: 'Войти снова'
    },
    landing: {
      navLinks: [
        { id: 'how', label: 'Как это работает' },
        { id: 'pricing', label: 'Цены' },
        { id: 'faq', label: 'FAQ' }
      ],
      titleA: 'Плохие решения ранят. Нерешительность парализует.',
      titleB: 'Увидьте всё решение целиком на одном экране.',
      subtitle: 'Структурируйте сложные решения с ИИ-партнёром. Fact Cards поможет разложить мысли по полочкам, найти слепые зоны и увидеть всю картину на одном экране, чтобы вы наконец смогли двигаться дальше.',
      mockupLabels: {
        pain: 'Боль',
        question: 'Вопрос',
        resource: 'Ресурс'
      },
      scatterWords: ['факт', 'страх', 'надежда'],
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
      resultTitle: 'От хаоса в голове к ясности за одну сессию',
      resultText: 'Хватит часами ходить по кругу. Всего за 15-30 минут вы получите визуальную карту всей проблемы, уверенность, что ничего не упустили, и чёткий план действий.',
      resultItems: [
        'Ясная карта проблемы на одном экране.',
        'Уверенность, что вы рассмотрели все важные аспекты.',
        'Скрытые связи и слепые зоны, подсвеченные ИИ.',
        'Конкретный список шагов, чтобы начать действовать.',
        'Переход от хаоса к решению меньше чем за 30 минут.'
      ],
      samples: [
        'Работа хорошо оплачивается, но нет вдохновения.',
        'А что, если сменю карьеру и не получится?',
        'Стабильность важнее ежедневной радости?',
        'Подруга перешла в дизайн и в восторге.'
      ],
      aiBubble: 'Что для вас здесь важнее?',
      navCta: 'Начать бесплатно',
      cta: 'Начать бесплатно',
      ctaRepeat: 'Готовы принимать решения уверенно?',
      note: 'Банковская карта не нужна. 3 полноценные сессии в подарок.',
      kicker: 'Ваш ИИ-партнёр для мышления',
      trustBadges: [
        '3 сессии бесплатно',
        'Приватно и зашифровано',
        'Карта не нужна'
      ],
      personas: [
        { title: 'На перепутье', desc: 'Стоите перед важным жизненным выбором и парализованы сомнениями «а что, если».' },
        { title: 'Основатель и лидер', desc: 'Делаете стратегические ставки с высокой ценой ошибки в условиях неопределённости.' },
        { title: 'Творец и созидатель', desc: 'Пытаетесь структурировать шторм идей в понятный и целостный проект.' },
        { title: 'Коуч и психолог', desc: 'Помогаете клиентам распутывать клубок сложных мыслей прямо на сессии.' },
        { title: 'Амбициозный студент', desc: 'Вырабатываете системную привычку мыслить структурно и критически.' },
        { title: 'Искатель роста', desc: 'Активно работаете над собой, чтобы лучше понимать свой ум и внутренние барьеры.' }
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
      pricing: {
        kicker: 'Цены',
        title: 'Начните бесплатно. Платите, когда станет незаменимым.',
        subtitle: 'У вас есть 3 полные сессии, чтобы проверить метод на реальных решениях. Дальше можно выбрать безлимит по подписке или пожизненный доступ одним платежом.',
        highlight: '3 полноценные сессии бесплатно. Банковская карта не потребуется.',
        footer: 'Во всех планах доступен один и тот же голосовой холст, AI-сопровождение и базовая методология мышления.',
        plans: [
          {
            name: 'Starter',
            badge: 'Включено',
            price: '$0',
            period: '3 сессии всего',
            description: 'Хватает, чтобы проверить Fact Cards на трёх реальных решениях, ничего не оплачивая.',
            cta: 'Начать бесплатно',
            featured: false,
            features: [
              '3 полные сессии',
              'Голосовой ввод',
              'Визуальный холст с карточками',
              'Экспорт и возврат к своим доскам'
            ]
          },
          {
            name: 'Unlimited',
            badge: 'Самый практичный',
            price: '$10',
            period: '/мес',
            description: 'Для тех, кто хочет пользоваться Fact Cards регулярно: в работе, в личных решениях и в стратегии.',
            cta: 'Выбрать месяц',
            featured: true,
            features: [
              'Безлимитные сессии',
              'Всё из Starter',
              'Для регулярной практики мышления',
              'Простая ежемесячная цена'
            ]
          },
          {
            name: 'Lifetime',
            badge: 'Один платёж',
            price: '$100',
            period: 'навсегда',
            description: 'Разовая оплата за неограниченный доступ, если вы хотите встроить Fact Cards в свою постоянную практику.',
            cta: 'Взять навсегда',
            featured: false,
            features: [
              'Безлимитные сессии навсегда',
              'Всё из Unlimited',
              'Подходит основателям и коучам',
              'Без регулярных списаний'
            ]
          }
        ]
      },
      socialProofTitle: 'Что говорят первые пользователи',
      socialProofEmpty: 'Мы только что запустились! Вы можете стать первым, кто оставит отзыв. Мы не будем публиковать фейковые цитаты, поэтому честно ждём вашего мнения.',
      socialProofItems: [] as Array<{ name: string; role: string; text: string }>,
      faq: [
        { q: 'Что происходит во время сессии?', a: 'Вы рассказываете о проблеме. ИИ создаёт карточки из ваших мыслей. Вместе вы их организуете и находите инсайты.' },
        { q: 'Нужно ли печатать?', a: 'Нет. Интерфейс голосовой, чтобы вы оставались в потоке. Текст на карточках можно отредактировать позже.' },
        { q: 'Что, если я не знаю, в чём на самом деле моя проблема?', a: 'Это идеальный сценарий для старта. Начните с описания «симптома» — тревоги, фрустрации, ситуации. Просто говорите. Сам процесс выгрузки мыслей в виде фактов, болей и гипотез помогает копнуть глубже и выявить корневую проблему.' },
        { q: 'Чем это отличается от дневника или разговора с другом?', a: 'Дневник — это монолог. У друзей есть своё мнение. Это интерактивный процесс с беспристрастным ИИ-партнёром для принятия решений.' },
        { q: 'Мои данные в безопасности?', a: 'Абсолютно. Ваши сессии приватны и зашифрованы. Мы никогда не передаём и не продаём ваши данные.' },
        { q: 'Сколько длится сессия?', a: 'Большинство находят ясность за 15-30 минут. Ограничений по времени нет.' },
        { q: 'ИИ принимает решение за меня?', a: 'Нет. ИИ — ваш второй пилот, а не командир. Он помогает вам увидеть всё ясно, чтобы вы решили сами.' },
        { q: 'Что происходит после 3 бесплатных сессий?', a: 'Сначала у вас есть 3 бесплатные сессии всего. После этого можно выбрать $10 в месяц за безлимит или $100 за пожизненный доступ. Для старта карта не нужна.' }
      ],
      faqTitle: 'Вопросы и ответы',
      methodologyTitle: 'Почему один экран? Наука ясного мышления.',
      methodologyText: 'Наша рабочая память ограничена — мы можем удерживать в голове лишь 5-7 элементов информации одновременно. Бесконечный скроллинг в заметках перегружает эту систему и создаёт «туман в голове». Fact Cards построен на этом когнитивном принципе: один экран — одна проблема. Это ограничение заставляет сфокусироваться и позволяет вашему мозгу (и нашему ИИ) находить связи, а не бороться за удержание информации.'
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
    demo: {
      banner: 'Это пример сессии. Изучите карточки, а потом создайте свою.',
      newBoard: '+ Новая доска'
    },
    tooltips: {
      inputbar: 'Опишите вашу проблему или ситуацию',
      cards_added: 'ИИ создал карточки! Перетащите для упорядочивания',
      connections_hint: 'Двойной клик — новая карточка, тяните между карточками для связи'
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

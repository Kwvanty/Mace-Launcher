import os
from flask import Flask, render_template, send_from_directory, request

app = Flask(
    __name__,
    template_folder='tamplate',
    static_folder='static'
)

TRANSLATIONS = {
    'en': {
        'title': 'Mace Launcher',
        'nav_features': 'Features',
        'nav_customization': 'FULL CUSTOMIZATION',
        'nav_modloaders': 'Modloaders',
        'nav_compare': 'Compare',
        'nav_updates': 'Updates',
        'nav_faq': 'FAQ',
        'theme_light': '☀️ Light Theme',
        'theme_dark': '🌙 Dark Theme',
        'hero_title': 'Mace Launcher',
        'hero_desc': 'Next-generation fast, convenient, and powerful Minecraft launcher.',
        'btn_download': 'Download Installer',
        'btn_learn_more': 'Learn More',
        'features_title': 'Launcher Features',
        'feat_1_title': '⚡ High Performance',
        'feat_1_desc': 'Optimized launch speed and minimal system resource consumption.',
        'feat_2_title': '🧩 Mod Support',
        'feat_2_desc': 'Convenient management of modpacks, mods, and tweaks in one click.',
        'feat_3_title': '🛡️ Reliability',
        'feat_3_desc': 'Stable updates and total security for your data.',
        
        # Customization Section
        'custom_title': 'FULL CUSTOMIZATION',
        'custom_desc': 'Customize every pixel of your launcher for maximum comfort and style.',
        'custom_th_param': 'Option',
        'custom_th_desc': 'Feature Description',
        'custom_row1_title': 'Visual Themes',
        'custom_row1_desc': 'Full accent color control, custom dark/light modes, and background customization.',
        'custom_row2_title': 'Layout & Elements',
        'custom_row2_desc': 'Flexible interface scaling, hiding sidebars, and custom widgets.',
        'custom_row3_title': 'Personalization',
        'custom_row3_desc': 'Custom avatar frames, animated profile cards, and unique launch sounds.',

        # Module Layout Section (New for imglauncher4)
        'modules_title': 'Flexible Modular Interface',
        'modules_desc': 'Rearrange modules, change panel forms, and set up your perfect layout drag-and-drop style.',
        'mod_feat_1': '✨ Drag & Drop placement',
        'mod_feat_2': '📐 Resizable panel shapes',
        'mod_feat_3': '🎨 Module background opacity',

        # Modloaders & API
        'mod_title': 'Full Modpack & API Integration',
        'mod_desc': 'One-click installation for popular mod loaders and Modrinth modpacks.',
        
        # Comparison Table
        'comp_title': 'Why Choose Mace Launcher?',
        'comp_feature': 'Feature',
        'comp_mace': 'Mace Launcher',
        'comp_others': 'Other Launchers',
        'comp_row1': 'Launch Speed',
        'comp_row1_mace': '⚡ 1.5 seconds',
        'comp_row1_oth': '🐢 Slow / Medium',
        'comp_row2': 'System Telemetry (CPU/RAM)',
        'comp_row2_mace': '✅ Built-in',
        'comp_row2_oth': '❌ Missing',
        'comp_row3': 'Modrinth & Modpacks API',
        'comp_row3_mace': '✅ Direct Search & Install',
        'comp_row3_oth': '❌ Manual Installation',
        'comp_row4': 'Automatic Java Setup',
        'comp_row4_mace': '✅ Full Auto',
        'comp_row4_oth': '⚠️ Partial / Manual',

        # Security
        'sec_title': '100% Safe & Secure',
        'sec_1_title': 'No Malware',
        'sec_1_desc': 'Clean installer without third-party adware or bloatware.',
        'sec_2_title': 'Encrypted Sessions',
        'sec_2_desc': 'Your authorization tokens and account data stay locally encrypted.',

        # Patch Notes
        'patch_title': 'Recent Updates & Timeline',
        'patch_v103_title': 'Version 1.0.3 (Current)',
        'patch_v103_desc': 'Added language switching, expanded settings options, and fully integrated NeoForge modloader support.',
        'patch_v102_title': 'Version 1.0.2',
        'patch_v102_desc': 'Added Modrinth API search and hardware telemetry monitor.',
        'patch_v101_title': 'Version 1.0.1',
        'patch_v101_desc': 'Optimized resource caching, accelerated asset downloading, and fixed UI elements.',

        # How to start & FAQ
        'how_title': 'How to Start Playing in 3 Steps',
        'step_1_title': '1. Download',
        'step_1_desc': 'Get the official MaceInstaller.exe by clicking the button above.',
        'step_2_title': '2. Install',
        'step_2_desc': 'Run the installer and follow the simple setup wizard instructions.',
        'step_3_title': '3. Play',
        'step_3_desc': 'Choose your favorite version or modpack and jump right into the game!',
        'sys_title': 'System Requirements',
        'sys_os_title': 'Operating System',
        'sys_os_desc': 'Windows 10 / 11 (64-bit)',
        'sys_cpu_title': 'Processor',
        'sys_cpu_desc': 'Intel Core i3 / AMD Ryzen 3 or higher',
        'sys_ram_title': 'RAM Memory',
        'sys_ram_desc': '4 GB (8 GB recommended)',
        'sys_java_title': 'Java Environment',
        'sys_java_desc': 'Pre-built (Automatic setup)',
        'faq_title': 'Frequently Asked Questions',
        'faq_q1': 'Is Mace Launcher completely free?',
        'faq_a1': 'Yes, Mace Launcher is 100% free to use for all Minecraft players.',
        'faq_q2': 'Does it support popular mods and modloaders?',
        'faq_a2': 'Absolutely! Full support for Fabric, Forge, NeoForge, and custom modpacks is built right in.',
        'faq_q3': 'How do I allocate more RAM to the game?',
        'faq_a3': 'Open Launcher Settings -> Memory allocation -> Drag the slider to your desired RAM amount.',
        
        # Modal & Footer
        'modal_title': 'Thank you for downloading!',
        'modal_desc': 'Your download should start automatically. Open MaceInstaller.exe once complete.',
        'modal_close': 'Got it',
        'footer_rights': '© 2026 Mace Launcher. All rights reserved.',
        'footer_disclaimer': 'Mace Launcher is not an official Mojang product.',
        'footer_discord': 'Join our Discord'
    },
    'ru': {
        'title': 'Mace Launcher',
        'nav_features': 'Возможности',
        'nav_customization': 'ПОЛНАЯ КАСТОМИЗАЦИЯ',
        'nav_modloaders': 'Модлоадери',
        'nav_compare': 'Сравнение',
        'nav_updates': 'Обновления',
        'nav_faq': 'FAQ',
        'theme_light': '☀️ Светлая тема',
        'theme_dark': '🌙 Тёмная тема',
        'hero_title': 'Mace Launcher',
        'hero_desc': 'Быстрый, удобный и мощный лаунчер Minecraft нового поколения.',
        'btn_download': 'Скачать Инсталлятор',
        'btn_learn_more': 'Узнать больше',
        'features_title': 'Преимущества лаунчера',
        'feat_1_title': '⚡ Высокая скорость',
        'feat_1_desc': 'Оптимизированный запуск и минимальное потребление ресурсов системы.',
        'feat_2_title': '🧩 Поддержка модов',
        'feat_2_desc': 'Удобное управление сборками, модами и модификаторами в один клик.',
        'feat_3_title': '🛡️ Надёжность',
        'feat_3_desc': 'Стабильные обновления и полная безопасность ваших данных.',

        # Секция Кастомизации
        'custom_title': 'ПОЛНАЯ КАСТОМИЗАЦИЯ',
        'custom_desc': 'Настраивайте каждый пиксель лаунчера под свой стиль и удобство.',
        'custom_th_param': 'Параметр',
        'custom_th_desc': 'Описание возможности',
        'custom_row1_title': 'Темы оформления',
        'custom_row1_desc': 'Полная смена цветовой палитры, поддержка темной и светлой темы, пользовательские акценты.',
        'custom_row2_title': 'Виджеты и панель',
        'custom_row2_desc': 'Свободная настройка расположения элементов, скрытие лишних блоков и гибкий интерфейс.',
        'custom_row3_title': 'Персонализация',
        'custom_row3_desc': 'Загрузка собственных фонов, кастомные иконки профиля и уникальные эффекты переходов.',

        # Модульная сетка (imglauncher4)
        'modules_title': 'Гибкая модульная сетка',
        'modules_desc': 'Перетаскивайте блоки, изменяйте форму модулей и адаптируйте рабочий экран под свои задачи.',
        'mod_feat_1': '✨ Перенос блоков Drag & Drop',
        'mod_feat_2': '📐 Изменение формы и размера',
        'mod_feat_3': '🎨 Настройка прозрачности панелей',

        'mod_title': 'Интеграция с Modrinth и Модлоадерами',
        'mod_desc': 'Установка популярных загрузчиков и сборок с Modrinth в один клик.',

        'comp_title': 'Почему именно Mace Launcher?',
        'comp_feature': 'Возможность',
        'comp_mace': 'Mace Launcher',
        'comp_others': 'Другие лаунчеры',
        'comp_row1': 'Скорость запуска',
        'comp_row1_mace': '⚡ 1.5 секунды',
        'comp_row1_oth': '🐢 Медленно',
        'comp_row2': 'Телеметрия ПК (CPU/RAM)',
        'comp_row2_mace': '✅ Встроена',
        'comp_row2_oth': '❌ Отсутствует',
        'comp_row3': 'Поиск по Modrinth API',
        'comp_row3_mace': '✅ Прямо в лаунчере',
        'comp_row3_oth': '❌ Ручная установка',
        'comp_row4': 'Автонастройка Java',
        'comp_row4_mace': '✅ Полностью авто',
        'comp_row4_oth': '⚠️ Частично / Вручную',

        'sec_title': '100% Безопасность',
        'sec_1_title': 'Без вирусов',
        'sec_1_desc': 'Чистый инсталлятор без стороннего софта и рекламы.',
        'sec_2_title': 'Шифрование данных',
        'sec_2_desc': 'Токены авторизации и профили хранятся в зашифрованном виде.',

        'patch_title': 'История обновлений',
        'patch_v103_title': 'Версия 1.0.3 (Текущая)',
        'patch_v103_desc': 'Добавлена смена языка, расширенные настройки и полноценная работа модлоадера NeoForge.',
        'patch_v102_title': 'Версия 1.0.2',
        'patch_v102_desc': 'Добавлен поиск Modrinth API и мониторинг железных ресурсов.',
        'patch_v101_title': 'Версия 1.0.1',
        'patch_v101_desc': 'Оптимизировано кэширование, ускорена загрузка файлов и улучшен интерфейс.',

        'how_title': 'Как начать играть за 3 шага',
        'step_1_title': '1. Скачай',
        'step_1_desc': 'Загрузи официальный MaceInstaller.exe, нажав кнопку выше.',
        'step_2_title': '2. Установи',
        'step_2_desc': 'Запусти инсталлятор и следуй простым инструкциям установки.',
        'step_3_title': '3. Играй',
        'step_3_desc': 'Выбери любимую версию или сборку модов и погружайся в игру!',
        'sys_title': 'Системные требования',
        'sys_os_title': 'Операционная система',
        'sys_os_desc': 'Windows 10 / 11 (64-bit)',
        'sys_cpu_title': 'Процессор',
        'sys_cpu_desc': 'Intel Core i3 / AMD Ryzen 3 или лучше',
        'sys_ram_title': 'Оперативная память',
        'sys_ram_desc': '4 ГБ (рекомендуется 8 ГБ)',
        'sys_java_title': 'Среда Java',
        'sys_java_desc': 'Встроенная (Автоматическая настройка)',
        'faq_title': 'Часто задаваемые вопросы',
        'faq_q1': 'Является ли Mace Launcher бесплатным?',
        'faq_a1': 'Да, Mace Launcher абсолютно бесплатен для всех игроков.',
        'faq_q2': 'Поддерживает ли он моды и модлоадеры?',
        'faq_a2': 'Конечно! Встроена полная поддержка Fabric, Forge, NeoForge и кастомных сборок.',
        'faq_q3': 'Как выделить больше оперативной памяти игре?',
        'faq_a3': 'Зайди в Настройки лаунчера -> Выделение памяти -> Передвинь ползунок на нужный объём ОЗУ.',

        'modal_title': 'Спасибо за скачивание!',
        'modal_desc': 'Загрузка запустится автоматически. После окончания откройте MaceInstaller.exe.',
        'modal_close': 'Понятно',
        'footer_rights': '© 2026 Mace Launcher. Все права защищены.',
        'footer_disclaimer': 'Mace Launcher не является официальным продуктом Mojang.',
        'footer_discord': 'Наш Discord'
    },
    'uk': {
        'title': 'Mace Launcher',
        'nav_features': 'Особливості',
        'nav_customization': 'ПОВНА КАСТОМІЗАЦІЯ',
        'nav_modloaders': 'Модлоадери',
        'nav_compare': 'Порівняння',
        'nav_updates': 'Оновлення',
        'nav_faq': 'FAQ',
        'theme_light': '☀️ Світла тема',
        'theme_dark': '🌙 Темна тема',
        'hero_title': 'Mace Launcher',
        'hero_desc': 'Швидкий, зручний та потужний лаунчер Minecraft нового покоління.',
        'btn_download': 'Завантажити Інсталятор',
        'btn_learn_more': 'Дізнатися більше',
        'features_title': 'Переваги лаунчера',
        'feat_1_title': '⚡ Висока швидкість',
        'feat_1_desc': 'Оптимізований запуск і мінімальне споживання ресурсів системи.',
        'feat_2_title': '🧩 Підтримка модів',
        'feat_2_desc': 'Зручне керування збірками, модами та модифікаторами в один клік.',
        'feat_3_title': '🛡️ Надійність',
        'feat_3_desc': 'Стабільні оновлення та повна безпека ваших даних.',

        # Секція Кастомізації
        'custom_title': 'ПОВНА КАСТОМІЗАЦІЯ',
        'custom_desc': 'Налаштовуйте кожен піксель лаунчера під свій стиль та зручність.',
        'custom_th_param': 'Параметр',
        'custom_th_desc': 'Опис можливості',
        'custom_row1_title': 'Теми оформлення',
        'custom_row1_desc': 'Повна зміна колірної палітри, підтримка темної та світлої теми, користувацькі акценти.',
        'custom_row2_title': 'Віджети та панелі',
        'custom_row2_desc': 'Вільне налаштування розташування елементів, приховування зайвих блоків та гнучкий інтерфейс.',
        'custom_row3_title': 'Персоналізація',
        'custom_row3_desc': 'Завантаження власних фонів, кастомні іконки профілю та унікальні ефекти переходів.',

        # Модульна сітка (imglauncher4)
        'modules_title': 'Гнучка модульна сітка',
        'modules_desc': 'Перетягуйте блоки, змінюйте форму модулів та адаптуйте робочий простір під свої потреби.',
        'mod_feat_1': '✨ Перенесення блоків Drag & Drop',
        'mod_feat_2': '📐 Зміна форми та розміру',
        'mod_feat_3': '🎨 Налаштування прозорості панелей',

        'mod_title': 'Інтеграція з Modrinth та Модлоадерами',
        'mod_desc': 'Встановлення популярних завантажувачів та збірок з Modrinth в один клік.',

        'comp_title': 'Чому саме Mace Launcher?',
        'comp_feature': 'Можливість',
        'comp_mace': 'Mace Launcher',
        'comp_others': 'Інші лаунчери',
        'comp_row1': 'Швидкість запуску',
        'comp_row1_mace': '⚡ 1.5 секунди',
        'comp_row1_oth': 'Повільно',
        'comp_row2': 'Телеметрія ПК (CPU/RAM)',
        'comp_row2_mace': '✅ Вбудована',
        'comp_row2_oth': '❌ Відсутня',
        'comp_row3': 'Пошук по Modrinth API',
        'comp_row3_mace': '✅ Прямо в лаунчері',
        'comp_row3_oth': '❌ Ручне встановлення',
        'comp_row4': 'Автоналаштування Java',
        'comp_row4_mace': '✅ Повністю авто',
        'comp_row4_oth': '⚠️ Частково / Вручную',

        'sec_title': '100% Безпека',
        'sec_1_title': 'Без вірусів',
        'sec_1_desc': 'Чистий інсталятор без стороннього софту та реклами.',
        'sec_2_title': 'Шифрування даних',
        'sec_2_desc': 'Токени авторизації та профілі зберігаються в зашифрованому вигляді.',

        'patch_title': 'Історія оновлень',
        'patch_v103_title': 'Версія 1.0.3 (Поточна)',
        'patch_v103_desc': 'Додано зміну мови, розширено налаштування та підключено повноцінну роботу NeoForge.',
        'patch_v102_title': 'Версія 1.0.2',
        'patch_v102_desc': 'Додано пошук Modrinth API та моніторинг апаратних ресурсів.',
        'patch_v101_title': 'Версія 1.0.1',
        'patch_v101_desc': 'Оптимізовано кешування, прискорено завантаження файлів та покращено інтерфейс.',

        'how_title': 'Як почати грати за 3 кроки',
        'step_1_title': '1. Завантаж',
        'step_1_desc': 'Скачай офіційний MaceInstaller.exe за кнопкою вище.',
        'step_2_title': '2. Встанови',
        'step_2_desc': 'Запусти інсталятор та дотримуйся простих підказок.',
        'step_3_title': '3. Грай',
        'step_3_desc': 'Обирай улюблену версію чи збірку модів та поринай у гру!',
        'sys_title': 'Системні вимоги',
        'sys_os_title': 'Операційна система',
        'sys_os_desc': 'Windows 10 / 11 (64-bit)',
        'sys_cpu_title': 'Процесор',
        'sys_cpu_desc': 'Intel Core i3 / AMD Ryzen 3 або краще',
        'sys_ram_title': 'Оперативна пам\'ять',
        'sys_ram_desc': '4 ГБ (рекомендовано 8 ГБ)',
        'sys_java_title': 'Середовище Java',
        'sys_java_desc': 'Вбудована (Автоматичне налаштування)',
        'faq_title': 'Часті запитання',
        'faq_q1': 'Чи безкоштовний Mace Launcher?',
        'faq_a1': 'Так, Mace Launcher на 100% безкоштовний для всіх гравців.',
        'faq_q2': 'Чи підтримує він моди та модлоадери?',
        'faq_a2': 'Звісно! Вбудовано повну підтримку Fabric, Forge, NeoForge та кастомних збірок.',
        'faq_q3': 'Як виділити більше оперативної пам\'яті?',
        'faq_a3': 'Перейди в Налаштування лаунчера -> Виділення пам\'яті -> Посунь повзунок на потрібний обсяг ОЗП.',

        'modal_title': 'Дякуємо за завантаження!',
        'modal_desc': 'Завантаження розпочнеться автоматично. Після завершення відкрийте MaceInstaller.exe.',
        'modal_close': 'Зрозуміло',
        'footer_rights': '© 2026 Mace Launcher. Усі права захищено.',
        'footer_disclaimer': 'Mace Launcher не є офіційним продуктом Mojang.',
        'footer_discord': 'Наш Discord'
    }
}

LANGUAGES = {
    'en': {'name': 'English', 'flag': '🇬🇧'},
    'ru': {'name': 'Русский', 'flag': '🇷🇺'},
    'uk': {'name': 'Українська', 'flag': '🇺🇦'}
}

@app.route('/')
def index():
    theme = request.args.get('theme', 'black')
    lang = request.args.get('lang', 'en')
    
    if lang not in TRANSLATIONS:
        lang = 'en'

    css_file = 'stile-black-theme.css' if theme == 'black' else 'stile-light-theme.css'
    
    return render_template(
        'index.html',
        css_file=css_file,
        current_theme=theme,
        current_lang=lang,
        t=TRANSLATIONS[lang],
        languages=LANGUAGES
    )

@app.route('/download/installer/<path:filename>')
def download_installer(filename):
    installer_dir = os.path.join(app.root_path, 'Mace Installer')
    
    file_path = os.path.join(installer_dir, filename)
    if not os.path.exists(file_path):
        return f"File not found at: {file_path}", 404
        
    return send_from_directory(installer_dir, filename, as_attachment=True)

@app.route('/download/update/<path:filename>')
def download_update(filename):
    update_dir = os.path.join(app.root_path, 'update')
    return send_from_directory(update_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
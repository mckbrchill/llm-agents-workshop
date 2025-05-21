# ИИ-агенты в кибербезопасности - Воркшоп

Этот репозиторий демонстрирует практическое применение ИИ-агентов, с акцентом на их отдельные составляющие, в разрезе примера анализа нормализованных событий SIEM.

## Обзор проекта

Два варианта реализации практически аналогичной агентской схемы:

- **No Code workflow в n8n** 
- **Реализация на Python с использованием Autogen + Langchain в Jupyter Notebook**

## Структура репозитория

```
.
├── n8n/                    # Файлы рабочих процессов n8n
│   ├── mitre-example/      # n8n workflow example 1
│   │   ├── clean_data.py   # Скрипт предварительной обработки данных
│   │   ├── mitre_mapper.json
│   │   ├── norm_events_workflow.json
│   │   └── VT_resolver.json
│   └── websecscan/         # n8n workflow example 2
│       └── web_scan_workflow.json
├── notebooks/              # Реализация в Jupyter notebook
│   └── siem_events_workflow.ipynb
├── local-files/            # Файлы исходных данных
│   ├── cleaned_mitre_attack_data.json
│   ├── cleaned_mitre_attack_data_short.json
│   ├── mitre_attack_data.json
│   └── norm_events.json
├── qdrant_data/            # Данные векторной базы данных (загрузить)
├── docker-compose.yml      # Конфигурация Docker
├── .env.example            # Пример переменных окружения
└── requirements.txt        # Зависимости Python
```

## Технический стек

- **Компоненты ML**:
  - Autogen для реализации агентов
  - Langchain для работы с векторным хранилицем
  - Эмбеддинги для семантического поиска
  - LLM API для возможностей языковых моделей

- **Инфраструктура**:
  - n8n для no code демонтрации
  - Qdrant в качестве векторной базы данных
  - PostgreSQL для хранения данных n8n
  - Langfuse для Observability

## Quickstart

### (Вариант 1) Настройка рабочего процесса n8n

0. **Установите Docker и Docker compose**:
   - [Docker Engine](https://docs.docker.com/engine/install/)
   - [Docker Compose](https://docs.docker.com/compose/install/)
1. **Клонируйте репозиторий и подготовьте переменные окружения**:
   ```bash
   cp .env.example .env
   ```

2. **[Cкачайте данные](https://drive.google.com/file/d/15k18nlCsXIiWNBmc3SnAWt5p9VpJkpxz/view?usp=sharing) для векторной базы и разрхивируйте в корень репозитория (данные должны быть в директории qdrant_data)** 

3. **Запустите сервисы с помощью Docker**:
   ```bash
   docker compose up
   ```

4. **Откройте веб-интерфейс n8n**:
   - Откройте браузер и перейдите по адресу http://localhost:5678

5. **Импортируйте и запустите существующие рабочие процессы**:
   - Нажмите "..." и выберите "Import from File"
   - Выберите файл рабочего процесса из `./n8n/mitre-example/norm_events_workflow.json` (или скопируйте и вставьте содержимое JSON напрямую)
   - Настройте учетные данные во всех блоках - [Mistral Platform](https://admin.mistral.ai/plateforme/limits) и [VirusTotal](https://www.virustotal.com)
   - Нажмите "Test Workflow" для запуска

### (Вариант 2) Использование реализации в Jupyter Notebook

0. **Установите Miniconda**:
   - [Miniconda Installation](https://www.anaconda.com/docs/getting-started/miniconda/install)

1. **Создайте виртуальное окружение и активируйте**:
   ```bash
   conda create --name agents-wshp python=3.10.11
   ```

   ```bash
   conda activate agents-wshp
   ```

2. **Установите зависимости Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте переменные окружения**:
   - Используйте тот же файл `.env`, что и выше, или создайте новый для среды notebook

2. **Отредактируйте файл .env с необходимыми переменными**:
   - Укажите ключ LLM API (`MISTRAL_API_KEY`) - получите его на [Mistral Platform](https://admin.mistral.ai/plateforme/limits)
   - Укажите ключ VirusTotal API (`VT_API_KEY`) - создайте аккаунт на [VirusTotal](https://www.virustotal.com)
   - При необходимости настройте параметры базы данных

4. **(Опицонально) Разверните сервис langfuse для трейсинга**:
   ```bash
   docker compose -f ./lfuse/docker-compose.lfuse.yml up -d
   ```
5. **Откройте notebook в своем IDE или запустите ноутбук в Jupyter**:
   ```bash
   jupyter notebook notebooks/siem_events_workflow.ipynb
   ```


6. **Последовательно выполняйте ячейки notebook**, чтобы увидеть процесс анализа:
   - Чтение и обработка событий SIEM
   - Загрузка данных MITRE ATT&CK и создание векторного хранилища
   - Инициализация агентов и определение Tools
   - Выполнение анализа и генерация отчетов

## Объяснение схемы

Процесс анализа состоит из нескольких этапов:

1. **Сбор и фильтрация событий**: Чтение событий SIEM и извлечение ключевых полей
2. **Интеграция с MITRE ATT&CK**: Сопоставление событий с релевантными техниками MITRE с использованием векторного поиска в базе как Tool для агента
3. **Анализ угроз**: Проверка и анализ доменов через API VirusTotal как Tool для агента
4. **Пост процессинг**: Структурирование и агрегация результатов
5. **Генерация итоговых выводов**: Саммаризация, генерация отчета, перевод на русский

## Сервисы Docker

Web-UI сервисов:

- **n8n**: http://localhost:5678
- **Qdrant**: http://localhost:6333/dashboard
- **Langfuse**: http://localhost:3000
# 🎯 Scan Your QR!

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![UI](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)](https://github.com/TomSchimansky/CustomTkinter)

**Приложение для целевого поиска и распознавания QR-кодов в реальном времени**

---

## 📋 Навигация / Navigation
- [🇷🇺 Русская версия](#-описание-проекта-ru)
- [🇬🇧 English version](#-project-description-en)
- [📚 Документация](#-документация)
- [🏗 Архитектура](#-архитектура-приложения)

---

## 🇷🇺 Описание проекта (RU)

### 🎯 Цель проекта
Разработка кроссплатформенного приложения, которое в реальном времени обнаруживает, валидирует и обрабатывает **именно целевой QR-код**, игнорируя фоновые метки. Приложение интегрируется в интерактивные сценарии: квесты, музейные экспозиции, образовательные проекты.

### ✨ Ключевые возможности
- 🔍 **Фильтрация QR-кодов** — поиск конкретного кода по содержимому
- 📹 **Два режима работы** — сканирование видеофайлов или веб-камеры
- ⏸️ **Пауза и продолжение** — управление процессом сканирования без потери данных
- 🎨 **Предобработка** — улучшение качества распознавания в сложных условиях
- 🎯 **Визуализация** — цветовая индикация (зелёный = найден, красный = фон)
- ⚡ **Оптимизация** — пропуск кадров для повышения производительности

### 🛠 Технологический стек
| Компонент | Технология |
|-----------|------------|
| **Язык** | Python 3.10+ |
| **GUI** | CustomTkinter + CTkListbox |
| **Computer Vision** | OpenCV |
| **QR Detection** | QReader (YOLOv8 + Pyzbar) |
| **Neural Networks** | PyTorch, Ultralytics |
| **Image Processing** | NumPy, imutils |

### 📦 Установка и запуск
1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/LuminousLex/ScanURQR.git
   cd ScanURQR
   ```
2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Запустите приложение:**
   ```bash
   python main.py
   ```

### 🚀 Быстрый старт
1. Введите параметр поиска (содержимое целевого QR-кода)
2. Выберите режим: Видео или Веб-камера
3. Нажмите «СТАРТ!!!»
4. Наведите камеру на QR-коды
5. Зелёная рамка = целевой код найден! 🎉

### 📂 Структура проекта
```text
ScanURQR/
├── main.py                    # Главный модуль с GUI
├── QRDetecting.py             # Модуль обработки видеопотока
├── requirements.txt           # Зависимости проекта
├── qr_logo.ico                # Иконка приложения
├── ScanURQR.spec              # Конфигурация PyInstaller
├── DOCUMENTATION/             # Документация
│   ├── RUS/                   # Русская версия
│   └── ENG/                   # English version
├── diagram(схемы)/            # Архитектурные диаграммы
│   ├── Архитектура (краткая схема).png
│   ├── Архитектура (полная схема).png
│   └── Архитектура приложения в FlowChart
└── dist/                      # Готовый .exe файл + DLL
    ├── ScanURQR.exe
    ├── libiconv.dll
    └── libzbar-64.dll
```

### 🏗 Архитектура приложения
Приложение построено по модульному принципу с разделением ответственности:
1. **main.py** — графический интерфейс (CustomTkinter)
2. **QRDetecting.py** — обработка видео и распознавание (OpenCV + QReader)
3. **Многопоточность** — отдельный поток для обработки видео

### 📊 Краткая схема архитектуры
![Краткая схема](diagram%28%D1%81%D1%85%D0%B5%D0%BC%D1%8B%29/%D0%90%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0%20%28%D0%BA%D1%80%D0%B0%D1%82%D0%BA%D0%B0%D1%8F%20%D1%81%D1%85%D0%B5%D0%BC%D0%B0%29.png)

### 📚 Документация
+ 🇷 [RUS](ScanURQR-s/DOCUMENTATION/RUS)
+ 🇬🇧 [ENG](ScanURQR-s/DOCUMENTATION/ENG)

### 🎓 Образовательное применение
Приложение разработано в рамках выпускной квалификационной работы по направлению:
 + 01.03.02 Прикладная математика и информатика
 + Научный руководитель: Профессор, доктор наук Осипов Г.С.
 + Университет: Сахалинский государственный университет

## 🇬🇧 Project Description (EN)

### 🎯 Project Goal
Development of a cross-platform application that detects, validates, and processes specific target QR codes in real-time, ignoring background markers. The application integrates into interactive scenarios: quests, museum exhibitions, educational projects.

### ✨ Key Features
- 🔍 **QR Code Filtering** — search for specific code by content
- 📹 **Two Operating Modes** — сvideo file scanning or webcam
- ⏸️ **Pause and Resume** — scanning process control without data loss
- 🎨 **Preprocessing** — improved recognition in challenging conditions
- 🎯 **Visualization** — color coding (green = found, red = background)
- ⚡ **Optimization** — frame skipping for better performance

### 🛠 Technology Stack
| Component | Technology |
|-----------|------------|
| **Language** | Python 3.10+ |
| **GUI** | CustomTkinter + CTkListbox |
| **Computer Vision** | OpenCV |
| **QR Detection** | QReader (YOLOv8 + Pyzbar) |
| **Neural Networks** | PyTorch, Ultralytics |
| **Image Processing** | NumPy, imutils |

### 📦 Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/LuminousLex/ScanURQR.git
   cd ScanURQR
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   python main.py
   ```
### 🚀 Quick Start
1. Enter search parameter (target QR code content)
2. Select mode: Video or Webcam
3. Click «СТАРТ!!!»
4. Point camera at QR codes
5. Green rectangle = target code found! 🎉

### 📂 Project Structure
```text
ScanURQR/
├── main.py                    # Main GUI module
├── QRDetecting.py             # Video processing module
├── requirements.txt           # Project dependencies
├── qr_logo.ico                # Application icon
├── ScanURQR.spec              # PyInstaller configuration
├── DOCUMENTATION/             # Documentation
│   ├── RUS/                   # Russian version
│   └── ENG/                   # English version
├── diagram(схемы)/            # Architecture diagrams
│   ├── Architecture (brief).png
│   ├── Architecture (full).png
│   └── Application FlowChart
└── dist/                      # Ready .exe file + DLLs
    ├── ScanURQR.exe
    ├── libiconv.dll
    └── libzbar-64.dll
```

### 🏗 Application Architecture
The application follows a modular design with separation of concerns:
1. **main.py** — graphical interface (CustomTkinter)
2. **QRDetecting.py** — video processing and recognition (OpenCV + QReader)
3. **Multithreading** — separate thread for video processing

### 📊 Brief Architecture Diagram
![Short](diagram%28%D1%81%D1%85%D0%B5%D0%BC%D1%8B%29/%D0%90%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0%20%28%D0%BA%D1%80%D0%B0%D1%82%D0%BA%D0%B0%D1%8F%20%D1%81%D1%85%D0%B5%D0%BC%D0%B0%29.png)

### 📚 Documentation
+ 🇷 [RUS](ScanURQR-s/DOCUMENTATION/RUS)
+ 🇬🇧 [ENG](ScanURQR-s/DOCUMENTATION/ENG)

### 🎓 Educational Context
This application was developed as part of a graduation thesis in the field of:
 + 01.03.02 Applied Mathematics and Informatics
 + Scientific Supervisor: Professor, Dr. Osipov G.S.
 + University: Sakhalin State University

<div align="center">

⭐ If you like this project, give it a star!
Made with ❤️ using Python & CustomTkinter
</div>

#!/bin/bash

# Скрипт развертывания системы отчетности

echo "🚀 Запуск развертывания системы отчетности..."

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверка наличия Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

echo "✅ Docker и Docker Compose найдены"

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p data
mkdir -p .streamlit

# Проверка файлов конфигурации
if [ ! -f ".streamlit/config.toml" ]; then
    echo "⚠️  Файл конфигурации .streamlit/config.toml не найден"
    echo "📝 Создание базовой конфигурации..."
    
    cat > .streamlit/config.toml << EOL
[theme]
primaryColor = "#228B22"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f7fafc"
textColor = "#2d3748"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
EOL
fi

# Остановка существующих контейнеров
echo "🛑 Остановка существующих контейнеров..."
docker-compose down

# Сборка и запуск
echo "🔨 Сборка образа..."
docker-compose build

echo "🚀 Запуск приложения..."
docker-compose up -d

# Проверка статуса
echo "⏳ Ожидание запуска приложения..."
sleep 10

if docker-compose ps | grep -q "Up"; then
    echo "✅ Приложение успешно запущено!"
    echo "🌐 Доступно по адресу: http://localhost:8501"
    echo ""
    echo "📊 Система отчетности готова к работе!"
    echo ""
    echo "Для остановки используйте: docker-compose down"
    echo "Для просмотра логов: docker-compose logs -f"
else
    echo "❌ Ошибка при запуске приложения"
    echo "📋 Логи:"
    docker-compose logs
    exit 1
fi

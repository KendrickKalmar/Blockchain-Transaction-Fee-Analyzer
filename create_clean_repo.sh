#!/bin/bash

# Скрипт для создания чистого репозитория только для blockchain-fee-analyzer

echo "=========================================="
echo "Создание чистого репозитория"
echo "=========================================="

# Определяем пути
CURRENT_DIR=$(pwd)
PARENT_DIR=$(dirname "$CURRENT_DIR")
NEW_REPO_DIR="$PARENT_DIR/blockchain-fee-analyzer"

echo "Текущая директория: $CURRENT_DIR"
echo "Новая директория: $NEW_REPO_DIR"
echo ""

# Проверяем, существует ли уже папка
if [ -d "$NEW_REPO_DIR" ]; then
    echo "⚠️  Папка $NEW_REPO_DIR уже существует!"
    read -p "Удалить и создать заново? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$NEW_REPO_DIR"
    else
        echo "Отменено."
        exit 1
    fi
fi

# Создаем новую папку
echo "📁 Создаю новую папку..."
mkdir -p "$NEW_REPO_DIR"

# Копируем все файлы (кроме .git)
echo "📋 Копирую файлы проекта..."
rsync -av --exclude='.git' --exclude='results/*' --exclude='*.log' "$CURRENT_DIR/" "$NEW_REPO_DIR/"

# Переходим в новую папку
cd "$NEW_REPO_DIR"

# Инициализируем git
echo "🔧 Инициализирую git репозиторий..."
git init
git branch -M main

# Добавляем все файлы
echo "➕ Добавляю файлы в git..."
git add .

# Создаем первый коммит
echo "💾 Создаю первый коммит..."
git commit -m "Initial commit: Blockchain Transaction Fee Analyzer"

echo ""
echo "=========================================="
echo "✅ Готово!"
echo "=========================================="
echo ""
echo "Следующие шаги:"
echo "1. Создайте новый репозиторий на GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Затем выполните:"
echo "   cd $NEW_REPO_DIR"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "Новая папка: $NEW_REPO_DIR"


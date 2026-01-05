# Инструкция: Как запушить проект на GitHub

## Шаг 1: Подготовка файлов

```bash
cd /Users/aleksandrhohlov/projects/work/NFS_checker/blockchain-fee-analyzer

# Добавить все файлы (включая удаленные)
git add -A

# Проверить что будет в коммите
git status
```

## Шаг 2: Создать коммит

```bash
git commit -m "Initial commit: Blockchain Transaction Fee Analyzer"
```

## Шаг 3: Создать репозиторий на GitHub

1. Откройте https://github.com/new
2. Repository name: `blockchain-fee-analyzer` (или другое название)
3. Выберите Public или Private
4. **ВАЖНО:** НЕ добавляйте README, .gitignore или license (они уже есть)
5. Нажмите "Create repository"

## Шаг 4: Добавить remote и запушить

После создания репозитория GitHub покажет инструкции. Выполните:

```bash
# Замените YOUR_USERNAME на ваш GitHub username
git remote add origin https://github.com/YOUR_USERNAME/blockchain-fee-analyzer.git

# Или если используете SSH:
# git remote add origin git@github.com:YOUR_USERNAME/blockchain-fee-analyzer.git

# Проверить что remote добавлен
git remote -v

# Запушить код
git push -u origin main
```

## Готово! ✅

После этого ваш проект будет на GitHub.

## Если возникнут проблемы

### "Repository not found"
- Проверьте правильность URL репозитория
- Убедитесь что репозиторий создан на GitHub

### "Permission denied"
- Если используете HTTPS, может потребоваться Personal Access Token
- Или используйте SSH: `git remote set-url origin git@github.com:USERNAME/REPO.git`

### "Branch main does not exist"
- Убедитесь что вы на ветке main: `git branch`
- Если нет, переименуйте: `git branch -M main`


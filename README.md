# Django Template
Шаблон для быстрого и правильного развертывание Django проекта. Как я развертываю Django проекты.

## 1. Начало. Подготавливаем проект локально.
### Первым делом определяемся с именем проекта
```bash
$PROJECT_NAME="test_project"
```

### Подгатавливаем локальное рабочее окружение
```bash
mkdir ~/dev; cd ~/dev
python -m venv $PROJECT_NAME
cd $PROJECT_NAME
. bin/activate
pip install -U pip
mkdir src; cd src
```

### Клонируем данный репозиторий
```bash
git clone https://github.com/vitaldmit/django_template.git .
git remote set-url origin <YOUR_REPOSITORY> # Меняем на свой репозиторий
```

### Устанавливаем необходимые начальные пакеты
```python
pip install -r requirements.txt
```

### Запускаем, проверяем Django
```python
django-admin startproject project
cd project
python manage.py runserver
```

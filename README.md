# Django Template
Шаблон для быстрого и правильного развертывание Django проекта. Как мы развертываем и разрабатываем Django проекты. Сервер расчитан на размещение множества сайтов на `django`. Грубо говоря виртальный сервер.

Этот проект находится на стадии разработки пока не будут выполнены все пункты в [**issue**](https://github.com/vitaldmit/django_template/issues/1)

*Рекомендация: название проекта, имя пользователя, название репозитория должны быть одними и теми же*

## ❶ 🏁 Начало. Подготавливаем проект локально.
### Первым делом определяемся с именем проекта
```bash
PROJECT_NAME="test"
```

### Подгатавливаем локальное виртуальное окружение
```bash
python -m venv $PROJECT_NAME
cd $PROJECT_NAME
source bin/activate
python -m pip install --upgrade pip
```

### Клонируем текущий репозиторий
```bash
git clone https://github.com/vitaldmit/django_template.git src
cd src

# Заменяем django_template на имя проекта
find -type f -exec sed -i -e 's#django_template_project#${PROJECT_NAME}"_project"#g' {} \;
mv django_template_project ${PROJECT_NAME}'_project'

# Удаляем лишнее
rm contributors.md

# Начинаем git с чистого листа
rm -rf .git
git init
git branch -M main
```

```bash
# Адрес репозитория меняем на свой.
git remote add origin <YOUR_REPOSITORY>
```

### Устанавливаем, настраиваем Django
```bash
cp env.example .env
pip install -r requirements.txt

python manage.py makemigrations
python manage.py makemigrations main
python manage.py migrate
python manage.py createsuperuser
```

### Запускаем
```bash
python manage.py runserver
```


## ❷ 🗄️ Переходим на сервер.
### Первым делом настраиваем сам сервер. Под root'ом.
### Делается один раз при покупке сервера.
```bash
# Обновляем пакеты
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
# От пользователя можно перейти в root командой `su -`
apt install git python3 python3-pip python3-venv docker docker-compose -y
apt install nginx postgresql postgresql-contrib uwsgi gunicorn -y

# Настраиваем ssh
nano /etc/ssh/sshd_config
# Меняем sshd порт на 22222 или любой другой
# Добавляем в конец файла ClientAliveInterval 30
```

```bash
systemctl restart sshd
```

### Создаем пользователя. Каждый проект это новый пользователь
```bash
# Имя ему даем как название проекта
user=<PROJECT_NAME>
```

```bash
password=$(date +%s | sha256sum | base64 | head -c 5 ; echo)
echo "$user = $password " >> .users
# -c "comment", -s "shell", -m "create the user's home directory" -U "create a group with the same name as the user", 
useradd -c "$user" -s /bin/bash -m -U "$user"
echo "$user":"$password" | chpasswd

# Если надо будет удалить пользователя в будущем
# userdel -r "<USER_NAME>"

# Добавляем пользователя в группу docker
# чтобы мог работать с контейнерами
sudo usermod -aG docker $user # Пока под вопросом
```


### Логинимся под пользователем. Под user'ом
```bash
su - $user
# Создаем и активируем виртуальное окружение
python3 -m venv venv
source ~/venv/bin/activate

# Добавляем в конец файла .bashrc чтобы каждый раз при входе и выходе не набирать команды
echo PROJECT_NAME=$(whoami) >> .bashrc
echo "source ~/venv/bin/activate" >> .bashrc
echo "deactivate" >> .bash_logout
source .bashrc

# Обновляем pip
python -m pip install --upgrade pip
```

```bash
# Клонируем свой репозиторий с проектом в `src`
git clone <YOUR_REPOSITORY> src
```

```bash
cd src
```


### Подготавливаем проект к запуску
#### Есть два способа запустить проект:
- С помощью `docker`. Запускаем команду `docker-compose up --build` или `docker-compose up -d`
- Настроить непосредственно все службы на сервере: `Nginx`, `PostgreSQL`, `UWSGI` или `gunicorn`


## Структура проекта
```
/home/<PROJECT_NAME>/
    |- venv/ # Виртуальное окружение
    |- src/  # Исходники проекта
        |- apps/
        |- configs/
        |- logs/
        |- $PROJECT_NAME_project/
        |- manage.py
        |- requirements.txt
        |- ...
    |- ...
```

# Django Template
Шаблон для быстрого и правильного развертывание Django проекта. Как мы развертываем и разрабатываем Django проекты. Сервер расчитан на размещение множества сайтов на `django`. Грубо говоря виртальный сервер.

Этот проект находится на стадии разработки пока не будут выполнены все пункты в [**issue**](https://github.com/vitaldmit/django_template/issues/1)

*Рекомендация. Название проекта, имя пользователя, название репозитория должны быть одними и теми же*

## Начало. Подготавливаем проект на локальном компьютере.
### Первым делом определяемся с именем проекта
```bash
PROJECT_NAME="test"
```

### Подгатавливаем локальное виртуальное окружение
```bash
# Переходим в нужную диекторию
python -m venv $PROJECT_NAME
cd $PROJECT_NAME
. bin/activate
python -m pip install --upgrade pip
```

### Клонируем текущий репозиторий
```bash
git clone https://github.com/vitaldmit/django_template.git src
cd src
# Начинаем с чистого листа
rm -rf .git
git add --all
git commit -m "Initial commit"
git branch -M main
# Адрес меняем на свой
git remote add origin git@github.com:vitaldmit/$PROJECT_NAME.git
```

### Устанавливаем, настраиваем Django
```bash
pip install -r requirements.txt
django-admin startproject ${PROJECT_NAME}'_project' .
python manage.py migrate
python manage.py createsuperuser
```

### Создаем базовое приложение
```bash
# Приложения будут храниться в `apps`.
# Надо будет в `INSTALLED_APPS` и в файле `apps.py` 
# приложения добавить префикс `apps.` перед именем приложения.
mkdir apps; cd apps
python ../manage.py startapp base
cd ..
```

### Запускаем
```bash
python manage.py runserver
```


## Переходим на сервер.
### Первым делом настраиваем сервер. Под root'ом
```bash
# Обновляем пакеты
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
# От пользователя можно перейти в root командой `su -`
apt install git python3 python3-pip python3-venv docker docker-compose -y

# Настраиваем ssh
nano /etc/ssh/sshd_config
# Меняем порт на 22222 или любой другой
# Добавляем в конец файла ClientAliveInterval 30
systemctl restart sshd

# Устанавливаем Nginx
sudo apt install nginx
```

### Создаем пользователя. Каждый проект это новый пользователь
```bash
# Имя ему даем как название проекта
user=$PROJECT_NAME
```

```bash
password=$(date +%s | sha256sum | base64 | head -c 5 ; echo)
echo "$user = $password " >> .users && cat .users
# -c "comment", -s "shell", -m "create the user's home directory" -U "create a group with the same name as the user", 
useradd -c "$user" -s /bin/bash -m -U "$user"
echo "$user":"$password" | chpasswd

# Добавляем пользователя в группу docker
# чтобы мог работать с контейнерами
sudo usermod -aG docker $user # Пока под вопросом

# Если надо будет удалить пользователя в будущем
# userdel -r "<USER_NAME>"
```


### Логинимся под пользователем. Под user'ом
```bash
# Создаем и активируем виртуальное окружение
python3 -m venv venv

# Добавляем в конец файла .bashrc чтобы каждый раз при входе и выходе не набирать команды
echo PROJECT_NAME=$(whoami) >> .bashrc
echo "source ~/venv/bin/activate" >> .bashrc
echo "deactivate" >> .bash_logout
source .bashrc

# Обновляем pip
python -m pip install --upgrade pip
```

```bash
# Клонируем свой репозиторий с проектом
git clone <YOUR_REPOSITORY> src
cd src
```

```bash
# Директория для конфигов
cd $PROJECT_NAME
```


## Структура проекта
/home/$PROJECT_NAME/
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

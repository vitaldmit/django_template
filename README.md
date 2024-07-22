# Django Template
Шаблон для быстрого и правильного развертывание Django проекта. Как мы развертываем и разрабатываем Django проекты. Сервер расчитан на размещение множества сайтов на `django`. Грубо говоря виртальный сервер.

Этот проект находится на стадии разработки пока не будут выполнены все пункты в [**issue**](https://github.com/vitaldmit/django_template/issues/1)

*Рекомендация. Название проекта, имя пользователя, название репозитория должны быть одними и теми же*

## 1. Начало. Подготавливаем проект на локальном компьютере.
### Первым делом определяемся с именем проекта
```bash
PROJECT_NAME="test_project"
```


### Подгатавливаем локальное рабочее окружение
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
# Может project или "$PROJECT_NAME_project"?
django-admin startproject $PROJECT_NAME .
python manage.py migrate
python manage.py createsuperuser
```


### Создаем базовое приложение
```bash
mkdir apps; cd apps
python ../manage.py startapp base
cd ..
```


### Запускаем и далее разрабатываем проект
```bash
python manage.py runserver
```


## 5. Переходим на сервер. Настраиваем сервер.
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
# Добавляем ClientAliveInterval 30
systemctl restart sshd

# Устанавливаем Nginx
sudo apt install nginx
```

### Создаем пользователя. Каждый проект это новый пользователь
```bash
# Имя ему даем как название проекта
user="test_project"
```

```bash
password=$(date +%s | sha256sum | base64 | head -c 5 ; echo)
echo "$user = $password " >> .users && cat .users
# -c "comment", -s "shell", -m "create the user's home directory" -U "create a group with the same name as the user", 
useradd -c "$user" -s /bin/bash -m -U "$user"
echo "$user":"$password" | chpasswd

<<<<<<< HEAD
sudo usermod -aG docker $user
=======
# Если надо будет перейти к какому-либо пользователю
# su - "<USER_NAME>"
>>>>>>> c4ef18a3d5dd5dfd77b66394450d9142c9128e07

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
echo deactivate >> .bash_logout
source .bashrc

# Обновляем pip
pip install -U pip
```

```bash
# Клонируем репозиторий с проектом
git clone "<YOUR_REPOSITORY>"
```

```bash
# Директория для конфигов
cd $PROJECT_NAME
```
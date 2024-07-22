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
mkdir ~/dev; cd ~/dev
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

### Устанавливаем настраиваем Django
```bash
pip install -r requirements.txt
# Может project или "$PROJECT_NAME_project"?
django-admin startproject $PROJECT_NAME .
python manage.py migrate
python manage.py createsuperuser
```

### Запускаем проект на локальном сервере
```bash
python manage.py runserver
```

### Создаем базовое приложение
```bash
mkdir apps; cd apps
python ../manage.py startapp base
cd ..
```



## 5. Переходим на сервер. Настраиваем сервер. Делается один раз.
### Первым делом настраиваем сервер. Под root'ом
```bash
# Обновляем пакеты
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
# От пользователя можно перейти в root командой `su -`
apt install git python3 python3-pip python3-venv docker docker-compose -y

# Настраиваем ssh
# Меняем порт на 22222 или любой другой
# Добавляем ClientAliveInterval 30
nano /etc/ssh/sshd_config
systemctl restart sshd
```

```bash
# Добавляем пользователя. Имя ему даем как название проекта
# Каждый проект это новый пользователь
user="test_project"
```

```bash
password=$(date +%s | sha256sum | base64 | head -c 5 ; echo)
echo "$user = $password " >> .users && cat .users
# -c "comment", -s "shell", -m "create the user's home directory" -U "create a group with the same name as the user", 
useradd -c "$user" -s /bin/bash -m -U "$user"
echo "$user":"$password" | chpasswd

sudo usermod -aG docker $user

# Если надо будет удалить пользователя в будущем
# userdel -r "<USER_NAME>"
```

```bash
# Устанавливаем программы для 
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

# Клонируем репозиторий с проектом
git clone "<YOUR_REPOSITORY>"
cd $PROJECT_NAME
```
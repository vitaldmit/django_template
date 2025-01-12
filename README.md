# Django Template
Шаблон для быстрого и правильного развертывание `Django` проекта. Сервер расчитан на размещение множества сайтов на `Django`. Можно сказать виртальный сервер.

Этот проект находится на стадии разработки пока не будут выполнены все пункты в [**issue**](https://github.com/vitaldmit/django_template/issues/1)

**Рекомендация: следующие имена должны быть одинаковыми:**
- название проекта
- имя пользователя
- название репозитория


## ❶ 🏁 Начало. Подготавливаем проект локально.
### Первым делом определяемся с именем проекта
```bash
# Задаем название проекта вручную
PROJECT_NAME="test"
```

```bash
# Задаем доменное имя вручную
domain_name="test.ru"
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

# Меняем django_template_name на имя своего проекта
# Меняем название основной директории
mv django_template_project/ "${PROJECT_NAME}_project"
# Меняем все упоминания на свое имя
find . -type f \( -name "*.py" -o -name "*.yml" -o -name "*.conf" \) -exec sed -i "s#django_template_project#"${PROJECT_NAME}_project"#gi" {} \;
find . -type f \( -name "*.yml" -o -name "*.conf" \) -exec sed -i "s#django_template#"${PROJECT_NAME}"#gi" {} \;

# Надо еще заменить в env.example

# Заменим на наш домен в nginx.conf
sed -i "s#<DOMAIN_NAME>#"${domain_name}"#gi" configs/nginx.conf configs/nginx-ssl.conf
# Заменим путь для логирования в nginx.conf
sed -i "s#<PROJECT_NAME>#"${PROJECT_NAME}"#gi" configs/nginx.conf configs/nginx-ssl.conf

# Удаляем лишнее
rm contributors.md

# Начинаем git с чистого листа
rm -rf .git
git init --initial-branch=main
git add --all
git commit -m "First commit"
```

```bash
# Адрес репозитория вручную меняем на свой.
git remote add origin https://github.com/<YOUR_USER_NAME>/${PROJECT_NAME}.git
```

### Устанавливаем, настраиваем, запускаем Django
```bash
cp env.example .env
# Надо будет отредактировать `.env`
nano .env
```

```bash
pip install -r requirements.txt

python manage.py makemigrations main
python manage.py migrate
python manage.py createsuperuser
```

```bash
python manage.py test
python manage.py runserver
```


## ❷ 🗄️ Переходим на сервер.
### Первым делом настраиваем сам сервер. Под root'ом. Делается один раз, при покупке сервера.
```bash
# Обновляем пакеты
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
apt install git tree python3 python3-pip python3-venv -y
apt install nginx postgresql postgresql-contrib uwsgi gunicorn -y
apt install certbot python3-certbot-nginx -y

# Установим **официальный** Docker
# Add Docker's official GPG key:
apt update
apt install ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
# Add the repository to Apt sources:
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
# Install the latest version of Docker CE and containerd
apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Установим cсылку python на python3
ln -s /usr/bin/python3 /usr/bin/python

# Настраиваем SSH
nano /etc/ssh/sshd_config
# Меняем sshd порт на 22222 или любой другой

# Можно отключить вход из под root'а
# PermitRootLogin no
```

```bash
# Добавляем чтобы не отваливалось соединение
echo "ClientAliveInterval 60" >> /etc/ssh/sshd_config
echo "ClientAliveCountMax 3" >> /etc/ssh/sshd_config

systemctl restart sshd
```

### Создаем пользователя. Каждый проект это новый пользователь
```bash
# Вручную даем пользователю имя
user=<PROJECT_NAME>
```

```bash
password=$(date +%s | sha256sum | base64 | head -c 5 ; echo)
echo "$user - $password " >> .users && cat .users
# -c "comment", -s "shell", -m "create the user's home directory" -U "create a group with the same name as the user", 
useradd -c "$user" -s /bin/bash -m -U "$user"
echo "$user":"$password" | chpasswd

# Если надо будет удалить пользователя в будущем
# userdel -r "<USER_NAME>"

# Добавляем пользователя в группу docker
# чтобы мог работать с контейнерами
sudo usermod -aG docker $user
```


### Логинимся под user'ом
```bash
su - $user
# От пользователя можно перейти в root командой `su -`
```

```bash
# Задаем доменное имя вручную
domain_name="test.ru"
```

```bash
# Добавляем в конец файла .bashrc чтобы каждый раз при входе и выходе не набирать команды
echo domain_name=${domain_name} >> ~/.bashrc
echo PROJECT_NAME=$(whoami) >> .bashrc
echo "source ~/venv/bin/activate" >> .bashrc
echo "deactivate" >> .bash_logout
source .bashrc

# Создаем и активируем виртуальное окружение
python3 -m venv venv
source ~/venv/bin/activate

# Обновляем pip
python -m pip install --upgrade pip
```

```bash
# Клонируем ваш репозиторий с проектом в `src`
git clone <YOUR_REPOSITORY> src
```

```bash
cd src
### Подготавливаем проект к запуску
cp env.example .env

# Меняем DEBUG на False
sed -i "s/DEBUG = True/DEBUG = False/" .env

# Заменяем SECRET_KEY
generated_secret_key=$(python -c "import random; import string; print(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + '!@#$%^&*(-_=+)') for _ in range(50)))")
sed -i "s/SECRET_KEY = 'your_secret_key'/SECRET_KEY = '${generated_secret_key}'/" .env

# Добавляем домен в ALLOWED_HOSTS
sed -i "s/ALLOWED_HOSTS = \['127\.0\.0\.1', 'localhost'\]/ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '${domain_name}']/" .env

# Меняем адрес базы данных на свой
sed -i "s/django_template/${PROJECT_NAME}/" .env

# Если надо будет еще что-то менять.
# nano .env
```

### ❗ Есть два способа запустить проект:
#### 1. С помощью `Docker`
Для настройки Let's Encrypt выполним:
```bash
# Сначала останавливаем Nginx под root
# lsof -i :80
# nginx -s quit

# Запускаем контейнеры
docker compose up -d

# Так как docker "чистый" надо получить сертификаты:
# 1. Останвим контейнер с Nginx
docker compose stop ${PROJECT_NAME}_nginx
# 2. Запустим временный контейнер с простым веб-сервером для обработки запросов ACME challenge:
docker run -d --name temp_acme_challenge -p 80:80 -v ./certbot/www:/usr/share/nginx/html nginx:alpine
# 3. Получим сертификат с помощью webroot метода:
docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
  -d ${domain_name} \
  --email info@${domain_name} \
  --agree-tos \
  --no-eff-email" ${PROJECT_NAME}_certbot
# 4.После успешного получения сертификата, остановим и удалим временный контейнер:
docker stop temp_acme_challenge && docker rm temp_acme_challenge
# 5. Запустим Nginx контейнер:
docker compose up -d ${PROJECT_NAME}_nginx

# Создаем суперпользователя
docker exec -it src-${PROJECT_NAME}_web-1 python manage.py createsuperuser

# Полезные команды для docker
# docker exec -it <CONTAINER_NAME> /bin/bash
# docker logs <CONTAINER_NAME>
# docker inspect <CONTAINER_NAME>
# docker compose down -v; docker system prune
```

#### 2. С помощью традиционного метода. Надо будет настривать из под root'а
##### Настраиваем Lets Encrypt
```bash
# Получим сертификат, используя Certbot с плагином Nginx:
certbot certonly --webroot --webroot-path=/var/www/html --email "info@${domain_name}" --agree-tos --no-eff-email -d $domain_name
# Настроим автоматическое обновление сертификатов:
certbot renew --dry-run
# Добавим задачу в crontab для регулярного обновления:
crontab -e
# 0 12 * * * /usr/bin/certbot renew --quiet
```

###### Настраиваем Nginx
```bash
# Создаем ссылку на конфигурационный файл
ln -s /home/$user/src/configs/nginx.conf /etc/nginx/conf.d
# Проверяем работоспособность
nginx -t
# Перезапускаем Nginx
systemctl restart nginx
# Проверяем работоспособность
systemctl status nginx
```


#### Настраиваем PostgreSQL
```bash
# Загружаем переменные из файла .env. Пока это не работает. Надо подправить
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
    echo "Файл .env не найден. Убедитесь, что он существует в текущей директории."
    exit 1
fi

# Проверяем, что все необходимые переменные установлены
if [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ]; then
    echo "Ошибка: Не все необходимые переменные установлены в файле .env"
    exit 1
fi

# Создаем базу данных и пользователя
sudo -u postgres psql << EOF
CREATE DATABASE $POSTGRES_DB;
CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
ALTER ROLE $POSTGRES_USER SET client_encoding TO 'utf8';
ALTER ROLE $POSTGRES_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $POSTGRES_USER SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOF

echo "База данных $POSTGRES_DB и пользователь $POSTGRES_USER успешно созданы."
```


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

## Contributing
1. Перейдите по адресу https://github.com/vitaldmit/django_template.
2. Нажмите Fork, расположенный в правом верхнем углу страницы.
3. Снимите флажок «Копировать только ветку dev».
4. Нажмите кнопку Create fork.

Ваш форкнутый репозиторий CPython будет создан по адресу https://github.com/USERNAME/django_template.

```bash
# Склонируем репозиторий
git clone git@github.com:<username>/django_template.git
```
```bash
cd django_template
# Настрааиваем upstream репозиторий
git remote add upstream https://github.com/vitaldmit/django_template
# Настраиваем git для извлечения main из upstream remote
git config --local branch.dev.remote upstream
# Поскольку никогда не следует пытаться отправлять изменения в upstream, 
# настроим git так, чтобы он всегда отправлял изменения в источник
git remote set-url --push upstream git@github.com:<username>/django_template.git
```

```bash
# Проверяем удаленные репозитории
git remote -v

# Вывод должен быть таким:
origin git@github.com:<username>/django_template.git (fetch)
origin git@github.com:<username>/django_template.git (push)
upstream https://github.com/vitaldmit/django_template (fetch)
upstream git@github.com:<username>/django_template.git (push)
```

```bash
git config user.name "Ваше имя"
git config user.email your.email@example.com
```

Чтобы начать работу над проблемой, создайте новую ветку и переключитесь на нее.
```bash
git switch -c <branch-name> dev
```

Выполните необходимые изменения, добавьте их в коммиты и отправьте их в свой форк.
```bash
git push origin <branch-name>
```

Откройте запрос на слияние. Перейдите на https://github.com/vitaldmit/django_template.

1. Нажмите кнопку New pull request.
2. Нажмите ссылку Compare across forks.
3. Выберите базовый репозиторий: vitaldmit/django_template и базовую ветку: dev.
4. Выберите головной репозиторий: <username>/django_template и головную ветку: ветку, содержащую ваши изменения.
5. Нажмите кнопку Create pull request.

```bash
git switch -c <branch-name> dev
# Удаляем локльную ветку
git branch -D <branch-name>
# Удаляем удаленную ветку
git push origin -d <branch-name>
```

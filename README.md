# Кошачий благотворительный фонд (0.1.1)
## Команды развертывания
Клонируйте репозиторий к себе на компьютер при помощи команды:
```
git clone git@github.com:wArahh/cat_charity_fund.git
```

Создайте, активируйте виртуальное окружение и установите зависимости:
```
cd cat_charity_fund/
```
```
python -m venv venv
```
```
pip install -r requirements.txt
```
### создайте .env файл по примеру:
```
TITLE='Кошачий благотворительный фонд (0.1.0)'
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET='SECRET'
TYPE="service_account"
PROJECT_ID="PROJECT_ID"
PRIVATE_KEY_ID="PRIVATE_KEY_ID"
PRIVATE_KEY="PRIVATE_KEY"
CLIENT_EMAIL="user@gmail.com"
CLIENT_ID="CLIENT_ID"
AUTH_URI="https://accounts.google.com/o/oauth2/auth"
TOKEN_URI="https://oauth2.googleapis.com/token"
AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
CLIENT_X509_CERT_URL="https://www.googleapis.com/robot/v1/metadata/x509/warah-32%40practicum-435114.iam.gserviceaccount.com"
EMAIL='user@gmail.com'
```
### активируйте базу данных командой:
```
alembic upgrade head
```
### запустите проект командой
```
uvicorn app.main:app --reload
```
### Документацию вы можете посмотреть по адресу
[Swagger](http://127.0.0.1:8000/docs)

или тут

[ReDoc](http://127.0.0.1:8000/redoc)



## Стек
- Python
- FastApi
- fastapi-users[sqlalchemy] 
- SQLAlchemy
- aiogoogle
## Автор
- [Макаренко Никита](https://github.com/wArahh)

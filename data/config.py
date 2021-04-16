from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("IP")  # Тоже str, но для айпи адреса хоста

PG_USER = env.str('PG_USER')
PG_PASSWORD = env.str('PG_PASSWORD')
PG_HOST = env.str('PG_HOST')
PG_DB = env.str('PG_DB')

SMTP_PASSWORD = env.str('SMTP_PASSWORD')

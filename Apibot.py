import telebot
import requests

# Токен Telegram бота
API_TOKEN = 'ВАШ ТОКЕН'

# Ваш API ключ
API_KEY = 'ВАШ API КЛЮЧ'

# URL для API геолокації.
API_URL = f'https://ip-api.com/json/' # ТУТ Є URL ДЛЯ ГЕОЛОКАЦІЇ. ЯКЩО ЙОГО НЕМА ТО МОЖНА ЗАБУТИ ПРО 47 РЯДОК

bot = telebot.TeleBot(API_TOKEN)

# Дуже проста перевірка IP
def is_valid_ip(ip): # ТУТ ФУНКЦІЯ ЯКА ПЕРЕВІРЯЄ ЧИ IP ПРАВИЛЬНИЙ
    parts = ip.split('.')  # Разделяємо IP на части по точкам (.)
    if len(parts) != 4:  # Якщо частей не 4, значит це неправильный IP
        return False

    for part in parts:
        try:
            number = int(part)  # Робимо часть у число
            if number < 0 or number > 255:  # Якщо число меньше 0 та більше 225 то IP неправильний
                return False
        except ValueError:  # Якщо не вдаєтся преоброзувати у число (наприклад, якщо там букви), вертаємо False
            return False

    return True  # Якщо усі частини правильні, вертаємо True

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Надішліть мені IP-адресу, і я визначу твоє місцезнаходження з точними координатами.")

@bot.message_handler(func=lambda message: True)
def get_location(message):
    # Получаємо IP, котрий прислав користувач
    user_ip = message.text.strip()

    # Перевірка на правільність IP
    if is_valid_ip(user_ip):  # Якщо IP правильный
        # Запрос к API з іспользуванням API ключа
        response = requests.get(f'{API_URL}{user_ip}?key={API_KEY}')

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'fail': # ТУТ МИ ВИКОРИСТОВУЄМО 'ПОСИЛАННЯ' API_URL
                bot.reply_to(message, "Не вдалося знайти місцезнаходження для цього IP.")
            else:
                country = data.get('country', 'невідомо')
                city = data.get('city', 'невідомо')
                latitude = data.get('lat', 'невідомо')
                longitude = data.get('lon', 'невідомо')

                bot.reply_to(message,
                             f"Місцезнаходження для IP {user_ip}:\nМісто: {city}\nКраїна: {country}\nШирота: {latitude}\nДовгота: {longitude}")
        else:
            bot.reply_to(message, "Виникла помилка при отриманні даних про геолокацію. Перевірте правильність IP-адреси.")
    else:
        bot.reply_to(message, "Будь ласка, введіть правильну IP-адресу.")


bot.polling()

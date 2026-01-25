import telebot
from telebot import types
from logic import init_db, add_request, get_answer, FAQ
from config import TG_TOKEN

init_db()

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("FAQ", "Связаться со специалистом")
    bot.send_message(message.chat.id, "Добро пожаловать в техподдержку 'Продаем все на свете'!", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.lower() == "faq")
def show_faq(message):
    faq_text = "\n\n".join([f"Вопрос: {q}\nОтвет: {a}" for q, a in FAQ.items()])
    bot.send_message(message.chat.id, faq_text)

@bot.message_handler(func=lambda message: message.text.lower() == "связаться со специалистом")
def contact_specialist(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Продажи", "Программисты")
    bot.send_message(message.chat.id, "Выберите отдел:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["Продажи", "Программисты"])
def handle_department(message):
    department = message.text
    bot.send_message(message.chat.id, f"Опишите вашу проблему (отдел: {department}):")
    bot.register_next_step_handler(message, lambda m: handle_question(m, department))

def handle_question(message, department):
    if department:
        add_request(message.from_user.id, message.from_user.username, message.text, department)
        bot.send_message(message.chat.id, f"Ваш запрос отправлен в отдел {department}. Ожидайте ответа!")
    else:
        answer = get_answer(message.text)
        if answer:
            bot.send_message(message.chat.id, answer)
        else:
            bot.send_message(message.chat.id, "Извините, я не знаю ответа. Свяжитесь со специалистом.")

if __name__ == '__main__':
    bot.polling(none_stop=True)

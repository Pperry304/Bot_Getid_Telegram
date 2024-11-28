# -------------------------------------------------------------------------------------- KÍNH GỬI TRÙM PHI PHAI ------------------------------------------------------------------------------------------------------

import telebot
from telebot import types 

API_BOT = "7619364941:AAEM0SOrpC2onOE-5kwZ3P-gZaxGq3fE9kM" # API BOT ĐÃ THAY
bot = telebot.TeleBot(API_BOT)

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.username
    if not user_name :
        full_name = message.from_user.first_name + " " + message.from_user.last_name
    else:    
        full_name = user_name
    huong_dan_su_dung = telebot.types.InlineKeyboardButton("🧾 Hướng dẫn sử dụng", callback_data="hdsd")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(huong_dan_su_dung)
    bot.send_message(message.chat.id, f"<b>🙋 Chào mừng {full_name} đến với bot tính lương\nNhấp vào nút bên dưới để xem lệnh sử dụng</b>", parse_mode="HTML",reply_markup=keyboard)

def huong_dan_su_dung(message):
    huong_dan_su_dung = (
        "<b>HƯỚNG DẪN SỬ DỤNG\n\n"
        "Nhập lệnh /tl [số kim cương] [số xu]\n\n➤Bot sẽ trả kết quả lương !!!</b>"
    )    
    bot.send_message(message.chat.id, huong_dan_su_dung, parse_mode = "HTML")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query_game(call):
    if call.data == "hdsd":
        huong_dan_su_dung(call.message)

@bot.message_handler(commands=["tl"])
def tinhluong(message):
    user_name = message.from_user.username
    if not user_name :
        full_name = message.from_user.first_name + " " + message.from_user.last_name
    else:    
        full_name = user_name
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) != 3:
            huong_dan_su_dung = telebot.types.InlineKeyboardButton("🧾 Hướng dẫn sử dụng", callback_data="hdsd")
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(huong_dan_su_dung)
            bot.send_message(message.chat.id, f"<b>Vui lòng nhập theo mẫu /tl [số kim cương] [số xu]</b>", parse_mode="HTML", reply_markup=keyboard)
            return
        so_kim_cuong = int(parts[1])
        so_xu = int(parts[2])
        if (so_kim_cuong < 0 or so_kim_cuong >= 300000):
            huong_dan_su_dung = telebot.types.InlineKeyboardButton("🧾 Hướng dẫn sử dụng", callback_data="hdsd")
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(huong_dan_su_dung)
            bot.send_message(message.chat.id, f"<b>Vui lòng nhập theo mẫu /tl [số kim cương] [số xu]</b>", parse_mode="HTML", reply_markup=keyboard)
            return
        tien_luong = 0

        if so_kim_cuong < 60000:
            so_tien_dinh_dang = float(f"{(so_kim_cuong * 0.25 + so_xu * 0.15) / 1000:.2f}"[:-1])  
            tien_luong = (so_tien_dinh_dang * 23500)
        elif so_kim_cuong >= 60000 and so_kim_cuong < 150000:
            so_tien_dinh_dang = float(f"{(so_kim_cuong * 0.25 + so_xu * 0.15) / 1000:.2f}"[:-1])  
            tien_luong = (so_tien_dinh_dang * 23500) + 235000  
        elif so_kim_cuong >= 150000 and so_kim_cuong < 300000:
            so_tien_dinh_dang = float(f"{(so_kim_cuong * 0.25 + so_xu * 0.15) / 1000:.2f}"[:-1])
            tien_luong = (so_tien_dinh_dang * 23500) + 657000    
        so_kim_cuong_dinh_dang = f"{(so_kim_cuong):,.0f}"
        so_xu_dinh_dang = f"{(so_xu):,.0f}"   
        tien_luong_dinh_dang = f"{(tien_luong):,.0f}"     
        noi_dung_ket_qua = (
            f"<b>Tính lương Waha !!!</b>\n"
            f"<b>┏━━━━━━━━━━━━━━━━━━━━━\n"
            f"┣➤🪪 Tên: {full_name}\n"
            f"┣➤💎 Số kim cương: {so_kim_cuong_dinh_dang}\n"
            f"┣➤🪙 Số xu vàng: {so_xu_dinh_dang}\n"
            f"┣➤💸 Tiền định dạng: {so_tien_dinh_dang} VNĐ\n"
            f"┣➤💵 Tiền lương: {tien_luong_dinh_dang} VNĐ\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━</b>"
        )        
        bot.send_message(message.chat.id, noi_dung_ket_qua, parse_mode="HTML")  
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi: {e}</b>", parse_mode="HTML")      

@bot.message_handler(func=lambda message: True)
@bot.message_handler(content_types=['sticker','photo','video','document'])    
def tra_loi_ngoai_le(message):
    huong_dan_su_dung = telebot.types.InlineKeyboardButton("📝 Hướng dẫn sử dụng", callback_data="hdsd")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(huong_dan_su_dung)
    bot.send_message(message.chat.id, f"<b>❌ Sai lệnh. Vui lòng xem lại</b>", parse_mode='HTML',reply_markup=keyboard)

if __name__ == "__main__":
    try:
        print("Bot đang hoạt động ...")
        bot.infinity_polling()
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e} !")

# THE END 
            

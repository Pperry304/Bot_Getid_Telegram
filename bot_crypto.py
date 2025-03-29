# ! py
# Bot c_tradingview 
# Copyright by NTC

import os, http.client, sys
try:
    import numpy as np
    np.NaN = np.nan
except ImportError:
    os.system("pip install numpy==1.24.3")
    import numpy as np
    np.NaN = np.nan

libraries = [
    "requests", "telebot", "pandas", "matplotlib", "mplfinance", 
    "fpdf", "lequangminh", "pandas-ta", "panda_ta"
]
for lib in libraries:
    try:
        __import__(lib)
    except ImportError:
        os.system(f"pip install {lib}") 

import numpy as np
import requests, time, telebot, json, io
from telebot import types
import pandas as pd
import matplotlib
import mplfinance as mpf
from fpdf import FPDF
from lequangminh import *
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import pandas_ta as ta

try:
    import pandas_ta as ta
except Exception as e:
    print(f"Lỗi khi import pandas_ta: {e}")
    os.system("pip uninstall pandas-ta -y")
    os.system("pip install pandas-ta==0.3.14b0")
    import pandas_ta as ta

# Hàm tạo banner 
def Banner():
    os.system("cls" if os.name == "nt" else "clear") # xoá tất cả những thứ còn lại trên terminal
    title = "\nMọi thắc mắc xin liên hệ Telegram: @TruongChinh304 !" 
    banner = """\n
██████╗░░█████╗░████████╗   ░█████╗░██████╗░██╗░░░██╗██████╗░████████╗░█████╗░
██╔══██╗██╔══██╗╚══██╔══╝   ██╔══██╗██╔══██╗╚██╗░██╔╝██╔══██╗╚══██╔══╝██╔══██╗
██████╦╝██║░░██║░░░██║░░░   ██║░░╚═╝██████╔╝░╚████╔╝░██████╔╝░░░██║░░░██║░░██║
██╔══██╗██║░░██║░░░██║░░░   ██║░░██╗██╔══██╗░░╚██╔╝░░██╔═══╝░░░░██║░░░██║░░██║
██████╦╝╚█████╔╝░░░██║░░░   ╚█████╔╝██║░░██║░░░██║░░░██║░░░░░░░░██║░░░╚█████╔╝
╚═════╝░░╚════╝░░░░╚═╝░░░   ░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░╚════╝░
\n"""
    ban = Colorate.Vertical(Colors.DynamicMIX((Col.light_green, Col.light_gray)), Center.XCenter(title)) + Colorate.Vertical(Colors.DynamicMIX((Col.light_red, Col.light_blue)), Center.XCenter(banner.center(300)))
    for i in ban:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.001)

# Hàm nhập api bot telegram
'''def nhap_api_bot():
    while True:
        api_bot = input("\nNhập API bot telegram: ").strip()
        url = f"https://api.telegram.org/bot{api_bot}/getMe"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get("ok"):
                print(f"API: {api_bot} hợp lệ !")
                return api_bot
            else:
                print("API không hợp lệ! Vui lòng nhập lại.")
        except Exception as e:
            print(f"Lỗi : {e}")        
        except requests.RequestException:
            print("Lỗi kết nối! Kiểm tra internet và nhập lại.")'''

#Banner()
TOKEN_API_BOT = "6790339105:AAEKvcd-EmkC3mXI3IDAWVi9uIienb7B-DM"  
URL_API_BINANCE= 'https://api.binance.com/api/v3'
bot = telebot.TeleBot(TOKEN_API_BOT)
matplotlib.use('Agg') 

# Hàm lấy tỷ giá usd đổi sang vnd 
def lay_ty_gia_vnd():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')  # API tỷ giá tiền tệ
    data = response.json()
    return data['rates']['VND']
            
# Hàm lấy danh sách các đồng crypto
def lay_danh_sach_crypto():
    response = requests.get(f'{URL_API_BINANCE}/exchangeInfo')
    data = response.json()
    danh_sach = [s['symbol'] for s in data['symbols'] if s['quoteAsset'] == 'USDT']
    return danh_sach 

# Hàm lấy thông tin chi tiết của đồng crypto
def lay_thong_tin_crypto(ten_crypto):
    response = requests.get(f'{URL_API_BINANCE}/ticker/24hr', params={'symbol': ten_crypto})
    data = response.json()
    return data

def lay_thong_tin_gioi_han_crypto(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai):
    response = requests.get(f'{URL_API_BINANCE}/klines', params={
        'symbol': ten_crypto,
        'interval': '1m',  
        'startTime': timestamp_thoi_gian_muon_lay,
        'endTime': timestamp_hien_tai,
    })
    datas = response.json()
    return datas

# hàm lấy qrlink của sepay 
def qrlink(so_tai_khoan, ten_ngan_hang, so_tien, noi_dung, download):
    qrlink = f"https://qr.sepay.vn/img?acc={so_tai_khoan}&bank={ten_ngan_hang}&amount={so_tien}&des={noi_dung}&template=compact&download={download}"
    return qrlink

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
    bot.send_message(message.chat.id, f"<b>🙋 Chào mừng {full_name} đến với Pperry trading bot\nNhấp vào nút bên dưới để xem lệnh sử dụng.</b>", parse_mode="HTML",reply_markup=keyboard)
    
# Lệnh /list
@bot.message_handler(commands=['list'])
def gui_danh_sach_crypto(message):
    danh_sach = lay_danh_sach_crypto()
    noi_dung = 'Danh sách các đồng crypto:\n' + '\n'.join(danh_sach)
    file_path_list_crypto = "list_crypto.txt"
    if len(noi_dung) > 4096:
        with open(file_path_list_crypto, "w", encoding = "utf-8") as file:
            file.write(noi_dung)
        with open(file_path_list_crypto, "rb") as file:  
            bot.send_document(message.chat.id, file)
        os.remove(file_path_list_crypto)  

# Hàm hướng dẫn sử dụng         
def huong_dan_su_dung(message):
    huong_dan_su_dung = (
        "<b>HƯỚNG DẪN SỬ DỤNG\n"
        "Lệnh 1: /list (xem danh sách các đồng crypto)\n"
        #"Lệnh 2: /tpsl [tên coin] [giá chốt lời (TP)] [giá chốt lỗ (SL)] (xem thông tin coin đó)\n"
        #"Lệnh 3: /stop (ngưng theo dõi lệnh đang chạy)\n"
        "Lệnh 2: /gpi [tên coin] [khoảng thời gian muốn lấy thông tin (phút)]\n(Xem thông tin coin dưới dạng json)\n"
        "Lệnh 3: /about (xem thông tin account và bot)\n"
        "Lệnh 4: /finance [tên coin] [khoảng thời giaan (phút)] (xem nến)\n(Xem tất cả thông tin về coin + chỉ báo trong thời gian nhất định)\n"
        "Lệnh 5: /pfinance [chỉ báo] [tên coin] [khoảng thời gian (phút)]\n(Xem thông tin coin chứa chỉ báo và thời gian nhất định)</b>\n"
        "Lệnh 6: /qrbank [số tiền] [nội dung chuyển khoản]\n(Qr donut cho Admin :V)\n"
        #"Lưu ý:\n"
        #"Khi 1 lệnh đang chạy mà muốn thay TP/SL thì chỉ cần nhập như lệnh và thay đổi TP/SL muốn thay\n"
        #"Lệnh sẽ được update giá mới sau mỗi 3 giây\n"
        #"Nếu nhập lệnh mới bằng coin khác thì lệnh thông tin coin cũ sẽ dừng.</b>"
    )    
    bot.send_message(message.chat.id, huong_dan_su_dung, parse_mode = "HTML")

# Lệnh /stop
#@bot.message_handler(commands=['stop'])
def dung_theo_doi(message):
    global trang_thai_lenh
    if trang_thai_lenh['dang_chay']:
        trang_thai_lenh['dang_chay'] = False  # Đặt trạng thái dừng
        bot.send_message(message.chat.id, f"<b>Đã dừng theo dõi {trang_thai_lenh['ten_crypto']}</b>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "<b>Không có lệnh nào đang chạy</b>", parse_mode="HTML")

# Lệnh /about xem thông tin 
@bot.message_handler(commands=['about'])
def vai_dieu_muon_noi(message):  
    is_bot = message.from_user.is_bot
    if is_bot:
        is_bot_ans = "True"
    else:
        is_bot_ans = "False"
    user_id = message.from_user.id 
    user_first_name = message.from_user.first_name 
    user_last_name = message.from_user.last_name 
    user_language = message.from_user.language_code 
    user_name = message.from_user.username 
    full_name = user_first_name + " " + user_last_name    
    infor = (
        f"<b>👤 Thông tin bạn\n"
        f" ├ ID: {user_id}\n"
        f" ├ Là bot: {is_bot_ans}\n"
        f" ├ Tên đầu: {user_first_name}\n"
        f" ├ Tên cuối: {user_last_name}\n"
        f" ├ Tên người dùng: <a href='https://t.me/{user_name}'>{user_name}</a>\n"
        f" ├ Tên đầy đủ: {full_name}\n"
        f" └ Mã ngôn ngữ: {user_language} (-)</b>"
    )             
    bot.send_message(message.chat.id, f"<b>Chào {full_name.capitalize()} tôi là Pperry Tradingview Bot. Nhiệm vụ cuả tôi là gửi tín hiệu từ sàn mỗi 3 giây. Bên cạnh đó tôi còn có thể giúp bạn xem hết thông tin tất cả đồng Crypto hiện nay trên sàn 1 cách nhanh chóng.\n\nXem biểu đồ tại <a href='https://vn.tradingview.com/'>TradingView</a>\n\nVài điều lưu ý:\nHạn chế xem các đồng có giá trị quá nhỏ sẽ gây lỗi.Giá trị khi xem (Vnd) sẽ không chính xác vì 1 vài lý do\n\nSử dụng nếu có lỗi hãy nhắn cho <a href='https://t.me/Truongchinh304'>Admin</a>\n\nDưới đây là thông tin đầy đủ cuả bạn.</b>\n{infor}\n", parse_mode="HTML")
    
data_storage = {}
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query_game(call):
    if call.data == "hdsd":
        huong_dan_su_dung(call.message)
    elif call.data.startswith("gvf:"):
        unique_id = call.data.split(":")[1]
        # Lấy dữ liệu từ từ điển
        if unique_id in data_storage:
            data = data_storage[unique_id]
            ten_crypto = data["ten_crypto"]
            khoang_thoi_gian = data["khoang_thoi_gian"]
            all_noi_dung = data["all_noi_dung"]
            ghi_noi_dung_vao_file(ten_crypto, khoang_thoi_gian, all_noi_dung, call.message)
            # Xóa dữ liệu khỏi từ điển sau khi sử dụng
            del data_storage[unique_id]
    
trang_thai_lenh = {
    'ten_crypto': None,
    'nguong_chot_loi': None,
    'nguong_chot_lo': None,
    'nguong_chot_loi_vnd': None,
    'nguong_chot_lo_vnd': None,
    'dang_chay': False,
    'id_tin_nhan': None  # ID của tin nhắn để kiểm soát vòng lặp.
}

# Hàm tính trung bình 5 giá gần nhất 
def tinh_trung_binh_gia_gan_nhat(ten_crypto):
    thoi_gian_hien_tai = datetime.now()
    thoi_gian_5_phut_truoc = thoi_gian_hien_tai - timedelta(minutes=5)
    timestamp_5_phut_truoc = int(thoi_gian_5_phut_truoc.timestamp() * 1000)
    timestamp_hien_tai = int(thoi_gian_hien_tai.timestamp() * 1000)
    response = requests.get(f'{URL_API_BINANCE}/klines', params={
        'symbol': ten_crypto,
        'interval': '1m',  
        'startTime': timestamp_5_phut_truoc,
        'endTime': timestamp_hien_tai,
        'limit': 5 # Lấy 5 giá gần nhất 
    })
    datas = response.json()
    if datas:
        gia_dong_cua = [float(data[4]) for data in datas[-5:]] 
        gia_trung_binh = sum(gia_dong_cua) / 5  
        return gia_trung_binh 

# Hàm xem khối lượng giá 24h và tpsl     
#@bot.message_handler(commands=['tpsl'])
def gui_thong_tin_crypto_usd(message):
    global trang_thai_lenh
    try:
        ty_gia_vnd = lay_ty_gia_vnd()
        nhap_thong_tin = message.text.split()
        if len(nhap_thong_tin) != 4:
            bot.send_message(message.chat.id, "<b>Vui lòng nhập đúng định dạng: /tpsl [tên coin] [giá_chốt_lời (TP)] [giá_chốt_lỗ (SL)]</b>", parse_mode = "HTML")
            return
        ten_crypto = nhap_thong_tin[1].upper() + "USDT" 
        nguong_chot_loi = float(nhap_thong_tin[2])  # Giá chốt lời
        nguong_chot_lo = float(nhap_thong_tin[3])  # Giá chốt lỗ
        nguong_chot_loi_vnd = nguong_chot_loi * ty_gia_vnd
        nguong_chot_lo_vnd = nguong_chot_lo * ty_gia_vnd
        # Kiểm tra nếu lệnh đang chạy
        if trang_thai_lenh['dang_chay']:
            if trang_thai_lenh['ten_crypto'] == ten_crypto:
                trang_thai_lenh['nguong_chot_loi'] = nguong_chot_loi
                trang_thai_lenh['nguong_chot_lo'] = nguong_chot_lo
                trang_thai_lenh['nguong_chot_loi_vnd'] = nguong_chot_loi_vnd
                trang_thai_lenh['nguong_chot_lo_vnd'] = nguong_chot_lo_vnd
                bot.send_message(message.chat.id, f"<b>Đã cập nhật TP/SL mới cho {ten_crypto} USD\n[{nguong_chot_loi:,.6f} - {nguong_chot_lo:,.6f}]</b>", parse_mode = "HTML")
                bot.send_message(message.chat.id, f"<b>Đã cập nhật TP/SL mới cho {ten_crypto} VND\n[{nguong_chot_loi_vnd:,.2f} - {nguong_chot_loi_vnd:,.2f}]</b>", parse_mode = "HTML")
                return
            else:
                trang_thai_lenh['dang_chay'] = False
                bot.send_message(message.chat.id, f"<b>Ngưng theo dõi {trang_thai_lenh['ten_crypto']} và bắt đầu theo dõi {ten_crypto}</b>", parse_mode = "HTML")
        # Cập nhật trạng thái lệnh mới
        trang_thai_lenh['ten_crypto'] = ten_crypto
        trang_thai_lenh['nguong_chot_loi'] = nguong_chot_loi
        trang_thai_lenh['nguong_chot_lo'] = nguong_chot_lo
        trang_thai_lenh['nguong_chot_loi_vnd'] = nguong_chot_loi_vnd
        trang_thai_lenh['nguong_chot_lo_vnd'] = nguong_chot_lo_vnd
        trang_thai_lenh['dang_chay'] = True
        danh_sach = lay_danh_sach_crypto()
        if ten_crypto not in danh_sach:
            bot.send_message(message.chat.id, "<b>Đồng crypto không hợp lệ. Vui lòng nhập lại</b>", parse_mode = "HTML")
            return
        thong_tin = lay_thong_tin_crypto(ten_crypto)
        ngay_thoi_gian = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        ngay = datetime.now().strftime("%d-%m-%Y")
        # Tỷ giá USD gốc 
        gia_hien_tai = float(thong_tin['lastPrice'])
        gia_truoc_do = gia_hien_tai  # Giá trước đó bắt đầu bằng giá hiện tại ban đầu
        gia_tang_giam = float(thong_tin['priceChange'])
        gia_trung_binh = float(thong_tin['weightedAvgPrice'])
        gia_mo_cua = float(thong_tin['openPrice'])
        gia_dong_cua = float(thong_tin['prevClosePrice'])
        # Tỷ giá USD chuyển sang VND
        gia_hien_tai_vnd = gia_hien_tai * ty_gia_vnd
        gia_truoc_do_vnd = gia_truoc_do * ty_gia_vnd
        gia_tang_giam_vnd = gia_tang_giam * ty_gia_vnd
        gia_trung_binh_vnd = gia_trung_binh * ty_gia_vnd
        gia_mo_cua_vnd = gia_mo_cua * ty_gia_vnd 
        gia_dong_cua_vnd = gia_dong_cua * ty_gia_vnd
        noi_dung = (
            f"<b>📋 Thông tin coin {ten_crypto.replace('USDT','')}</b>\n"
            f"<b>⏱️ Thời gian:</b> {ngay_thoi_gian}\n\n"
            f"<b>💲 Đơn vị tiền tệ:</b> USD\n"
            f"<b>💸 Giá hiện tại:</b> {gia_hien_tai:,.5f}\n"
            f"<b>⏳ Giá trước đó:</b> {gia_truoc_do:,.5f}\n"
            f"<b>📈 Giá tăng/giảm:</b> {gia_tang_giam:,.5f}\n"
            f"<b>🔓 Giá mở cửa:</b> {gia_mo_cua:,.5f}\n"
            f"<b>🛡️ Giá đóng cửa:</b> {gia_dong_cua:,.5f}\n"
            f"<b>📊 Giá trung bình:</b> {gia_trung_binh:,.5f}\n\n"
            f"<b>💲 Đơn vị tiền:</b> VND\n"
            f"<b>💸 Giá hiện tại:</b> {gia_hien_tai_vnd:,.2f}\n"
            f"<b>⏳ Giá trước đó:</b> {gia_truoc_do_vnd:,.2f}\n"
            f"<b>📈 Giá tăng/giảm:</b> {gia_tang_giam_vnd:,.2f}\n"
            f"<b>🔓 Giá mở cửa:</b> {gia_mo_cua_vnd:,.2f}\n"
            f"<b>🛡️ Giá đóng cửa:</b> {gia_dong_cua_vnd:,.2f}\n"
            f"<b>📊 Giá trung bình:</b> {gia_trung_binh_vnd:,.2f}\n\n"
            f"<b>📎 TP/SL:</b> [{nguong_chot_loi:,.2f} - {nguong_chot_lo:,.2f}]\n"
            f"<b>📎 TP/SL:</b> [{nguong_chot_loi_vnd:,.2f} - {nguong_chot_lo_vnd:,.2f}]"
        )
        msg = bot.send_message(message.chat.id, noi_dung, parse_mode = "HTML")
        trang_thai_lenh['id_tin_nhan'] = msg.message_id  # Lưu lại ID của tin nhắn
        # Cập nhật tin nhắn sau mỗi 3 giây
        da_chot_loi = False 
        da_chot_lo = False 
        current_content = ""
        while trang_thai_lenh['dang_chay'] and trang_thai_lenh['id_tin_nhan'] == msg.message_id:
            ty_gia_vnd = lay_ty_gia_vnd()
            thong_tin = lay_thong_tin_crypto(ten_crypto)
            ngay_thoi_gian = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            thoi_gian = datetime.now().strftime("%H:%M:%S")
            so_luong_giao_dich = int(thong_tin['count'])
            gia_trung_binh_gan_nhat = tinh_trung_binh_gia_gan_nhat(ten_crypto)   
            # Tỷ giá USD
            gia_hien_tai = float(thong_tin['lastPrice'])
            gia_thay_doi = float(thong_tin['priceChange'])
            gia_trung_binh = float(thong_tin['weightedAvgPrice'])
            gia_mo_cua = float(thong_tin['openPrice'])
            gia_dong_cua = float(thong_tin['prevClosePrice'])
            gia_cao_nhat = float(thong_tin['highPrice'])  
            gia_thap_nhat = float(thong_tin['lowPrice'])  
            gia_ban = float(thong_tin['bidPrice'])
            gia_mua = float(thong_tin['askPrice'])
            khoi_luong_giao_dich = float(thong_tin['volume'])
            khoi_luong_ti_gia = float(thong_tin['quoteVolume'])
            phan_tram_gia_thay_doi = float(thong_tin['priceChangePercent'])
            nguong_chot_loi = trang_thai_lenh['nguong_chot_loi']
            nguong_chot_lo = trang_thai_lenh['nguong_chot_lo']
            # Tỷ giá VND
            gia_hien_tai_vnd = gia_hien_tai * ty_gia_vnd
            gia_truoc_do_vnd = gia_truoc_do * ty_gia_vnd
            gia_thay_doi_vnd = gia_thay_doi * ty_gia_vnd
            gia_trung_binh_vnd = gia_trung_binh * ty_gia_vnd
            gia_mo_cua_vnd = gia_mo_cua * ty_gia_vnd 
            gia_dong_cua_vnd = gia_dong_cua * ty_gia_vnd
            gia_cao_nhat_vnd = gia_cao_nhat * ty_gia_vnd
            gia_thap_nhat_vnd = gia_thap_nhat * ty_gia_vnd 
            gia_ban_vnd = gia_ban * ty_gia_vnd
            gia_mua_vnd = gia_mua * ty_gia_vnd 
            khoi_luong_giao_dich_vnd = khoi_luong_giao_dich * ty_gia_vnd
            khoi_luong_ti_gia_vnd = khoi_luong_ti_gia * ty_gia_vnd
            phan_tram_gia_thay_doi_vnd = (1 - (gia_hien_tai_vnd / gia_mo_cua_vnd)) * 100
            nguong_chot_loi_vnd = nguong_chot_loi * ty_gia_vnd
            nguong_chot_lo_vnd = nguong_chot_lo * ty_gia_vnd
            # Đặt điều kiện để edit tin nhắn mới 
            if gia_hien_tai != gia_truoc_do:
                noi_dung = (
                    f"<b>📋 <u>THÔNG TIN COIN {ten_crypto.replace('USDT','')}</u></b>\n"
                    f"<b>🛟 <u>Số lượng giao dịch:</u></b> {so_luong_giao_dich}\n\n"
                    f"<b>╭─────────────────────────⭓</b>\n"
                    f"<b>├➤</b><u><b>💲 Đơn vị tiền tệ: USD (USDollar)</b></u>\n"
                    f"<b>├➤💸 Giá hiện tại:</b> {gia_hien_tai:,.6f}\n"
                    f"<b>├➤⏳ Giá trước đó:</b> {gia_truoc_do:,.6f}\n"
                    f"<b>├➤📈 Giá tăng/giảm:</b> {gia_thay_doi:,.6f}\n"
                    f"<b>├➤🔎 Phần trăm tăng/giảm:</b> {phan_tram_gia_thay_doi:.2f}%\n"
                    f"<b>├➤🔓 Giá mở cửa:</b> {gia_mo_cua:,.6f}\n"
                    f"<b>├➤🛡️ Giá đóng cửa:</b> {gia_dong_cua:,.6f}\n"
                    f"<b>├➤📌 Giá cao nhất:</b> {gia_cao_nhat:,.6f}\n"
                    f"<b>├➤📌 Giá thấp nhất:</b> {gia_thap_nhat:,.6f}\n"
                    f"<b>├➤📌 Giá trung bình:</b> {gia_trung_binh:,.6f}\n"
                    f"<b>├➤🛒 Giá mua:</b> {gia_mua:,.6f}\n"
                    f"<b>├➤🛍️ Giá bán:</b> {gia_ban:,.6f}\n"
                    f"<b>├➤⚖️ Khối lượng giao dịch:</b> {khoi_luong_giao_dich:,.2f}\n"
                    f"<b>├➤⚖️ Khối lượng tỉ giá:</b> {khoi_luong_ti_gia:,.2f}\n"
                    f"<b>├────────────────────────</b>\n"
                    f"<b>├➤</b>           {ngay_thoi_gian}\n"
                    f"<b>├────────────────────────</b>\n"
                    f"<b>├➤</b><u><b>💲 Đơn vị tiền tệ: VND (VietNamDong)</b></u>\n"
                    f"<b>├➤💸 Giá hiện tại:</b> {gia_hien_tai_vnd:,.0f}\n"
                    f"<b>├➤⏳ Giá trước đó:</b> {gia_truoc_do_vnd:,.0f}\n"
                    f"<b>├➤📈 Giá tăng/giảm:</b> {gia_thay_doi_vnd:,.0f}\n"
                    f"<b>├➤🔎 Phần trăm tăng/giảm:</b> {phan_tram_gia_thay_doi_vnd:.2f}%\n"
                    f"<b>├➤🔓 Giá mở cửa:</b> {gia_mo_cua_vnd:,.0f}\n"
                    f"<b>├➤🛡️ Giá đóng cửa:</b> {gia_dong_cua_vnd:,.0f}\n"
                    f"<b>├➤📌 Giá cao nhất:</b> {gia_cao_nhat_vnd:,.0f}\n"
                    f"<b>├➤📌 Giá thấp nhất:</b> {gia_thap_nhat_vnd:,.0f}\n"
                    f"<b>├➤📌 Giá trung bình:</b> {gia_trung_binh_vnd:,.0f}\n"
                    f"<b>├➤🛒 Giá mua:</b> {gia_mua_vnd:,.0f}\n"
                    f"<b>├➤🛍️ Giá bán:</b> {gia_ban_vnd:,.0f}\n"
                    f"<b>├➤⚖️ Khối lượng giao dịch:</b> {khoi_luong_giao_dich_vnd:,.0f}\n"
                    f"<b>├➤⚖️ Khối lượng tỉ giá:</b> {khoi_luong_ti_gia_vnd:,.0f}\n"
                    f"<b>├────────────────────────</b>\n"
                    f"<b>├➤📎 TP/SL:</b> [<u>{nguong_chot_loi:,.2f} - {nguong_chot_lo:,.2f}</u>]\n"
                    f"<b>├➤📎 TP VND:</b> [<u>{nguong_chot_loi_vnd:,.2f}</u>]\n"
                    f"<b>├➤📎 SL VND:</b> [<u>{nguong_chot_lo_vnd:,.2f}</u>]\n"
                    f"<b>╰─────────────────────────⭓</b>\n"
                )
            if gia_hien_tai > nguong_chot_loi and not da_chot_loi:
                noi_dung_chot_loi = ( 
                    f"<b>╭───────────⭓</b>\n"
                    f"<b>├➤📎 Đã chốt lời [TP]</b>\n"
                    f"<b>├➤ Thời gian:</b> {thoi_gian}\n"
                    f"<b>├➤ Giá chốt lời:</b> [<u>{nguong_chot_loi:,.6f}</u>]\n"
                    f"<b>├➤ Giá lúc chốt lời:</b> [<u>{gia_hien_tai:,.6f}</u>]\n"
                    f"<b>├➤ Quy đổi VNĐ</b>\n"
                    f"<b>├➤ Giá chốt lời:</b> {nguong_chot_loi_vnd:,.2f}\n"
                    f"<b>├➤ Giá lúc chốt lời:</b> {gia_hien_tai_vnd:,.2f}\n"
                    f"<b>╰────────────────────────</b>\n"
                )
                bot.send_message(message.chat.id, noi_dung_chot_loi, parse_mode = "HTML")
                da_chot_loi = True  # Đánh dấu đã gửi thông báo chốt lời
            elif gia_hien_tai < nguong_chot_lo and not da_chot_lo:
                noi_dung_chot_lo = (
                    f"<b>╭───────────⭓</b>\n"
                    f"<b>├➤📎 Đã chốt lỗ [SL]</b>\n"
                    f"<b>├➤ Thời gian:</b> {thoi_gian}\n"
                    f"<b>├➤ Giá chốt lỗ:</b> [<u>{nguong_chot_lo:,.6f}</u>]\n"
                    f"<b>├➤ Giá lúc chốt lỗ:</b> [<u>{gia_hien_tai:,.6f}</u>]\n"
                    f"<b>├➤ Quy đổi VNĐ</b>\n"
                    f"<b>├➤ Giá chốt lỗ:</b> {nguong_chot_lo_vnd:,.2f}\n"
                    f"<b>├➤ Giá lúc chốt lỗ:</b> {gia_hien_tai_vnd:,.2f}\n"
                    f"<b>╰────────────────────────</b>\n"
                )
                bot.send_message(message.chat.id, noi_dung_chot_lo, parse_mode = "HTML")
                da_chot_lo = True  # Đánh dấu đã gửi thông báo chốt lời
            if gia_hien_tai > gia_trung_binh_gan_nhat:
                noi_dung += f"\n<b>Giá tăng nên mua {ten_crypto.replace('USDT', '')} lúc {thoi_gian}</b>"
            elif gia_hien_tai <= gia_trung_binh_gan_nhat:
                noi_dung += f"\n<b>Giá giảm nên bán {ten_crypto.replace('USDT', '')} lúc {thoi_gian}</b>"
            if noi_dung != current_content:
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=noi_dung, parse_mode="HTML")
                current_content = noi_dung    
            gia_truoc_do = gia_hien_tai
            gia_truoc_do_vnd = gia_hien_tai_vnd
            #print(f"➤ Lấy dữ liệu {ten_crypto.replace('USDT', '')} - {ngay_thoi_gian} thành công\n")
            time.sleep(10)
    except Exception as e:
        trang_thai_lenh['dang_chay'] = False
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi {e} !</b>", parse_mode = "HTML")

# Hàm lấy giá trong quá khứ
@bot.message_handler(commands=['gpi'])
def lay_gia_trong_khoang_thoi_gian(message):
    try:
        danh_sach = lay_danh_sach_crypto()
        nhap_thong_tin = message.text.split()
        if len(nhap_thong_tin) != 3:
            bot.send_message(message.chat.id, "<b>Vui lòng nhập đúng định dạng: /gpi [tên coin] [khoảng thời gian lấy data (m)]</b>", parse_mode="HTML")
            return 
        ten_crypto = nhap_thong_tin[1].upper() + "USDT"
        khoang_thoi_gian = int(nhap_thong_tin[2]) 
        if ten_crypto not in danh_sach:
            bot.send_message(message.chat.id, "<b>Đồng crypto không hợp lệ. Vui lòng nhập lại</b>", parse_mode="HTML")
            return 
        if khoang_thoi_gian < 1:
            bot.send_message(message.chat.id, "<b>Khoảng thời gian không hợp lệ. Vui lòng nhập lại</b>", parse_mode="HTML")    
            return 
        thoi_gian_hien_tai = datetime.now()
        thoi_gian_muon_lay = thoi_gian_hien_tai - timedelta(minutes=khoang_thoi_gian)
        timestamp_thoi_gian_muon_lay = int(thoi_gian_muon_lay.timestamp() * 1000)
        timestamp_hien_tai = int(thoi_gian_hien_tai.timestamp() * 1000)
        datas = lay_thong_tin_gioi_han_crypto(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai)
        if datas:
            danh_sach_noi_dung = []  # Lưu danh sách JSON hợp lệ
            for data in datas:
                thoi_gian = datetime.fromtimestamp(data[0] / 1000)  
                gia_mo_cua = data[1]
                gia_dong_cua = data[4]  
                gia_cao_nhat = data[2]
                gia_thap_nhat = data[3]
                khoi_luong = data[5]
                noi_dung = {
                    "Thời gian": thoi_gian.strftime("%Y-%m-%d %H:%M:%S"), 
                    "Giá mở cửa": gia_mo_cua,
                    "Giá đóng cửa": gia_dong_cua,
                    "Giá cao nhất": gia_cao_nhat,
                    "Giá thấp nhất": gia_thap_nhat,
                    "Khối lượng": khoi_luong
                }
                danh_sach_noi_dung.append(noi_dung)  
                all_noi_dung_json = json.dumps(danh_sach_noi_dung, indent=4, ensure_ascii=False)
            if len(all_noi_dung_json) < 4096:
                unique_id = str(message.chat.id) + "_" + str(datetime.now().timestamp())
                data_storage[unique_id] = {
                    "ten_crypto": ten_crypto,
                    "khoang_thoi_gian": khoang_thoi_gian,
                    "all_noi_dung": all_noi_dung_json
                }
                nut_ghi_vao_file = telebot.types.InlineKeyboardButton("📝 Ghi nội dung vào file", callback_data=f"gvf:{unique_id}")
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(nut_ghi_vao_file)
                bot.send_message(message.chat.id, f"```json\nGiá của {ten_crypto.replace('USDT', '')} trong {khoang_thoi_gian} phút đổ lại\n\n{all_noi_dung_json}```", parse_mode="MarkdownV2", reply_markup=keyboard)
            else:
                ghi_noi_dung_vao_file(ten_crypto, khoang_thoi_gian, danh_sach_noi_dung, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi {e} !</b>", parse_mode="HTML")


# Hàm ghi nội dung vào file đúng JSON
def ghi_noi_dung_vao_file(ten_crypto, khoang_thoi_gian, danh_sach_noi_dung, message):
    file_path_crypto = f"{ten_crypto}-{khoang_thoi_gian}.json"
    try:
        with open(file_path_crypto, "w", encoding="utf-8") as file:  # Ghi đè file mới
            json.dump(danh_sach_noi_dung, file, indent=4, ensure_ascii=False)
        with open(file_path_crypto, "rb") as file:
            bot.send_document(message.chat.id, file, caption="Hoàn thành gửi file!")     
        os.remove(file_path_crypto)  
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi {e} !</b>", parse_mode="HTML")


def lay_thong_tin_gioi_han_crypto_chart(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai, message):
    response = requests.get(f'{URL_API_BINANCE}/klines', params={
        'symbol': ten_crypto,
        'interval': '1m',  
        'startTime': timestamp_thoi_gian_muon_lay,
        'endTime': timestamp_hien_tai,
    })
    datas = response.json() 
    if datas:
        danh_sach = []
        for data in datas:
            thoi_gian = datetime.fromtimestamp(data[0] / 1000)  
            gia_mo_cua = data[1]
            gia_dong_cua = data[4]  
            gia_cao_nhat = data[2]
            gia_thap_nhat = data[3]
            khoi_luong = data[5]
            noi_dung = {
                "Thời gian": thoi_gian.strftime("%Y-%m-%d %H:%M:%S"), 
                "Giá mở cửa": gia_mo_cua,
                "Giá đóng cửa": gia_dong_cua,
                "Giá cao nhất": gia_cao_nhat,
                "Giá thấp nhất": gia_thap_nhat,
                "Khối lượng": khoi_luong
            }
            danh_sach.append(noi_dung)
        ghi_vao_file(ten_crypto, danh_sach)
    else :
        bot.send_message(message.chat.id, "<b>Không có dữ liệu theo yêu cầu</b>", parse_mode="HTML")   
        return None

def ghi_vao_file(ten_crypto, danh_sach_moi):
    file_path = f'{ten_crypto.upper()}.json'
    try:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                danh_sach_cu = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            danh_sach_cu = []
        danh_sach_cu.extend(danh_sach_moi)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(danh_sach_cu, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Đã xảy ra lỗi khi ghi vào file: {e}")

# Biểu đồ chỉ báo MA
def ve_bieu_do_nen_ma(message, ten_crypto):
    with open(f"{ten_crypto}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:  
        bot.send_message(message.chat.id, "<b>Dữ liệu rỗng, không thể vẽ biểu đồ</b>", parse_mode="HTML")
        return
    df = pd.DataFrame(data)
    df["Thời gian"] = pd.to_datetime(df["Thời gian"])
    df.rename(columns={
        "Thời gian": "Date",
        "Giá mở cửa": "Open",
        "Giá đóng cửa": "Close",
        "Giá cao nhất": "High",
        "Giá thấp nhất": "Low",
        "Khối lượng": "Volume"
    }, inplace=True)
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.set_index("Date", inplace=True)
    mpf.plot(
        df,
        type='candle', 
        style='charles', 
        title=f"Biểu đồ giá {ten_crypto}/USDT với MA",
        ylabel="Giá (USDT)",
        volume=True,  
        ylabel_lower="Khối lượng",
        mav=(5, 10),  # Thêm MA
        savefig='bieudo_ma.png'  
    )
    with open('bieudo_ma.png', 'rb') as file:
        thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bot.send_photo(message.chat.id, file, caption = f'<b>Biểu đồ nến MA của {ten_crypto} lúc: {thoi_gian_hien_tai}</b>', parse_mode="HTML")

# Biểu đồ chỉ báo BOLL 
def ve_bieu_do_nen_boll(message, ten_crypto):
    with open(f"{ten_crypto}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:  
        bot.send_message(message.chat.id, "<b>Dữ liệu rỗng, không thể vẽ biểu đồ</b>", parse_mode="HTML")
        return
    df = pd.DataFrame(data)
    df["Thời gian"] = pd.to_datetime(df["Thời gian"])
    df.rename(columns={
        "Thời gian": "Date",
        "Giá mở cửa": "Open",
        "Giá đóng cửa": "Close",
        "Giá cao nhất": "High",
        "Giá thấp nhất": "Low",
        "Khối lượng": "Volume"
    }, inplace=True)
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.set_index("Date", inplace=True)
    df['MA20'] = df['Close'].rolling(window=20).mean()  # Đường trung bình 20 phiên
    df['Upper'] = df['MA20'] + 2 * df['Close'].rolling(window=20).std()  # Dải trên
    df['Lower'] = df['MA20'] - 2 * df['Close'].rolling(window=20).std()  # Dải dưới
    apds = [
        mpf.make_addplot(df['MA20'], color='blue'),
        mpf.make_addplot(df['Upper'], color='red'),
        mpf.make_addplot(df['Lower'], color='green')
    ]
    mpf.plot(
        df,
        type='candle',
        style='charles',
        title=f"Biểu đồ giá {ten_crypto}/USDT với Bollinger Bands",
        ylabel="Giá (USDT)",
        volume=True,
        ylabel_lower="Khối lượng",
        addplot=apds,  # Thêm Bollinger Bands
        savefig='bieudo_boll.png'
    )
    with open('bieudo_boll.png', 'rb') as file:
        thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bot.send_photo(message.chat.id, file, caption = f'<b>Biểu đồ nến BOLL của {ten_crypto} lúc: {thoi_gian_hien_tai}</b>', parse_mode="HTML")

def ve_bieu_do_nen_ema(message, ten_crypto):
    with open(f"{ten_crypto}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:  
        bot.send_message(message.chat.id, "<b>Dữ liệu rỗng, không thể vẽ biểu đồ</b>", parse_mode="HTML")
        return
    df = pd.DataFrame(data)
    df["Thời gian"] = pd.to_datetime(df["Thời gian"])
    df.rename(columns={
        "Thời gian": "Date",
        "Giá mở cửa": "Open",
        "Giá đóng cửa": "Close",
        "Giá cao nhất": "High",
        "Giá thấp nhất": "Low",
        "Khối lượng": "Volume"
    }, inplace=True)
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.set_index("Date", inplace=True)
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()  # EMA20
    apds = [
        mpf.make_addplot(df['EMA20'], color='purple')  # Đường liền cho EMA20
    ]
    mpf.plot(
        df,
        type='candle',
        style='charles',
        title=f"Biểu đồ giá {ten_crypto}/USDT với EMA",
        ylabel="Giá (USDT)",
        volume=True,
        ylabel_lower="Khối lượng",
        addplot=apds,  # Thêm EMA vào biểu đồ
        savefig='bieudo_ema.png'
    )
    with open('bieudo_ema.png', 'rb') as file:
        thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bot.send_photo(message.chat.id, file, caption = f'<b>Biểu đồ nến EMA của {ten_crypto} lúc: {thoi_gian_hien_tai}</b>', parse_mode="HTML")    

def ve_bieu_do_nen_sar(message, ten_crypto):
    with open(f"{ten_crypto}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:
        bot.send_message(message.chat.id, "<b>Dữ liệu rỗng, không thể vẽ biểu đồ</b>", parse_mode="HTML")
        return
    df = pd.DataFrame(data)
    df["Thời gian"] = pd.to_datetime(df["Thời gian"])
    df.rename(columns={
        "Thời gian": "Date",
        "Giá mở cửa": "Open",
        "Giá đóng cửa": "Close",
        "Giá cao nhất": "High",
        "Giá thấp nhất": "Low",
        "Khối lượng": "Volume"
    }, inplace=True)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.set_index("Date", inplace=True)
    def calculate_sar(high, low, af=0.02, max_af=0.2):
        sar = [low[0]]  # Giá trị SAR ban đầu
        ep = high[0]  # Điểm cực trị (Extreme Point)
        trend = 1  # 1 = uptrend, -1 = downtrend
        af_step = af  # Hệ số tăng tốc ban đầu
        for i in range(1, len(high)):
            new_sar = sar[-1] + af_step * (ep - sar[-1])
            if trend == 1:  # Xu hướng tăng
                new_sar = min(new_sar, low[i - 1], low[i])
                if high[i] > ep:
                    ep = high[i]
                    af_step = min(af_step + af, max_af)
                if low[i] < new_sar:
                    trend = -1
                    af_step = af
                    ep = low[i]
            else:  # Xu hướng giảm
                new_sar = max(new_sar, high[i - 1], high[i])
                if low[i] < ep:
                    ep = low[i]
                    af_step = min(af_step + af, max_af)
                if high[i] > new_sar:
                    trend = 1
                    af_step = af
                    ep = high[i]
            sar.append(new_sar)
        return sar
    df["SAR"] = calculate_sar(df["High"].values, df["Low"].values)
    apds = [mpf.make_addplot(df["SAR"], color='red', marker='o', markersize=5, scatter=True)]
    mpf.plot(df, type='candle', style='charles',
             title=f"Biểu đồ SAR của {ten_crypto}/USDT",
             ylabel="Giá (USDT)", volume=True,
             addplot=apds, savefig='bieudo_sar.png')
    with open('bieudo_sar.png', 'rb') as file:
        bot.send_photo(message.chat.id, file, caption=f"<b>Biểu đồ SAR của {ten_crypto}</b>", parse_mode="HTML")

def ve_bieu_do_nen_avl(message, ten_crypto):
    with open(f"{ten_crypto}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:
        bot.send_message(message.chat.id, "<b>Dữ liệu rỗng, không thể vẽ biểu đồ</b>", parse_mode="HTML")
        return
    df = pd.DataFrame(data)
    df["Thời gian"] = pd.to_datetime(df["Thời gian"])
    df.rename(columns={
        "Thời gian": "Date",
        "Giá mở cửa": "Open",
        "Giá đóng cửa": "Close",
        "Giá cao nhất": "High",
        "Giá thấp nhất": "Low",
        "Khối lượng": "Volume"
    }, inplace=True)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.set_index("Date", inplace=True)
    df["AVL"] = df["Close"].rolling(window=10).mean()  # Lấy trung bình 10 phiên
    apds = [mpf.make_addplot(df["AVL"], color='blue')]
    mpf.plot(df, type='candle', style='charles',
             title=f"Biểu đồ AVL của {ten_crypto}/USDT",
             ylabel="Giá (USDT)", volume=True,
             addplot=apds, savefig='bieudo_avl.png')
    with open('bieudo_avl.png', 'rb') as file:
        bot.send_photo(message.chat.id, file, caption=f"<b>Biểu đồ AVL của {ten_crypto}</b>", parse_mode="HTML")

def du_doan_mua_ban(message, ten_crypto):
    try:
        with open(f"{ten_crypto}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        if not data:  
            bot.send_message(message.chat.id, "<b>Dữ liệu rỗng, không thể đưa ra dự đoán</b>", parse_mode="HTML")
            return
        df = pd.DataFrame(data)
        df["Thời gian"] = pd.to_datetime(df["Thời gian"])
        df.rename(columns={
            "Thời gian": "Date",
            "Giá mở cửa": "Open",
            "Giá đóng cửa": "Close",
            "Giá cao nhất": "High",
            "Giá thấp nhất": "Low",
            "Khối lượng": "Volume"
        }, inplace=True)
        df["Close"] = df["Close"].astype(float)
        df.set_index("Date", inplace=True)
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        rsi_latest = df['RSI'].iloc[-1]
        if rsi_latest < 30:
            du_doan = f"<b>RSI hiện tại: {rsi_latest:.2f}</b>\nQuá bán! Nên <b>MUA</b>."
        elif rsi_latest > 70:
            du_doan = f"<b>RSI hiện tại: {rsi_latest:.2f}</b>\nQuá mua! Nên <b>BÁN</b>."
        else:
            du_doan = f"<b>RSI hiện tại: {rsi_latest:.2f}</b>\nKhông có tín hiệu rõ ràng, nên <b>CHỜ</b>."
        #bot.send_message(message.chat.id, du_doan, parse_mode="HTML")
        noi_dung_du_doan = du_doan.replace("<b>", "").replace("</b>", "")
        return noi_dung_du_doan
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi khi dự đoán: {e}</b>", parse_mode="HTML")

def tao_pdf_tu_anh(ten_crypto, noi_dung_du_doan):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font("FreeSerif", '', "FreeSerif.ttf", uni=True)
    pdf.set_font("FreeSerif", size=14)
    pdf.cell(200, 10, txt=f"Biểu đồ phân tích {ten_crypto}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"{noi_dung_du_doan}")
    danh_sach_bieu_do = [
        "bieudo_ma.png",    # MA
        "bieudo_boll.png",  # Bollinger Bands
        "bieudo_ema.png",   # EMA
        "bieudo_sar.png",   # SAR
        "bieudo_avl.png"    # AVL
    ]
    for hinh in danh_sach_bieu_do:
        pdf.add_page()
        pdf.image(f'{hinh}', x=10, y=30, w=190)
    pdf_path = f"{ten_crypto}_chart_analysis.pdf"
    pdf.output(pdf_path)    
    return pdf_path

@bot.message_handler(commands=['finance'])
def finance(message):
    try:
        danh_sach = lay_danh_sach_crypto()
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, "<b>Nhập theo định dạng /finance [Tên coin] [Khoảng thời gian]</b>", parse_mode="HTML")
            return
        ten_crypto = parts[1].upper() + "USDT"
        khoang_thoi_gian_muon_lay = int(parts[2])
        if ten_crypto not in danh_sach:
            bot.send_message(message.chat.id, f"<b>{ten_crypto} không có trong danh sách tên coin</b>", parse_mode="HTML")
            return 
        if khoang_thoi_gian_muon_lay < 20 or khoang_thoi_gian_muon_lay > 400:
            bot.send_message(message.chat.id, "<b>Giới hạn thời gian trong khoảng 20 - 400 phút</b>", parse_mode="HTML")
            return
        thoi_gian_hien_tai = datetime.now()
        thoi_gian_muon_lay = thoi_gian_hien_tai - timedelta(minutes=khoang_thoi_gian_muon_lay)
        timestamp_thoi_gian_muon_lay = int(thoi_gian_muon_lay.timestamp() * 1000)
        timestamp_hien_tai = int(thoi_gian_hien_tai.timestamp() * 1000)
        lay_thong_tin_gioi_han_crypto_chart(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai, message)
        ve_bieu_do_nen_ma(message, ten_crypto)
        ve_bieu_do_nen_boll(message, ten_crypto)
        ve_bieu_do_nen_ema(message, ten_crypto)
        ve_bieu_do_nen_sar(message, ten_crypto)
        ve_bieu_do_nen_avl(message, ten_crypto)
        noi_dung_du_doan = du_doan_mua_ban(message, ten_crypto) 
        pdf_path = tao_pdf_tu_anh(ten_crypto, noi_dung_du_doan)
        with open(pdf_path, 'rb') as pdf_file:
            bot.send_document(message.chat.id, pdf_file, caption=f"<b>Phân tích biểu đồ {ten_crypto} trong {khoang_thoi_gian_muon_lay} phút</b>", parse_mode="HTML")
        os.remove(f'{ten_crypto.upper()}.json')    
        os.remove('bieudo_ma.png')
        os.remove('bieudo_boll.png')
        os.remove('bieudo_ema.png')
        os.remove('bieudo_sar.png')
        os.remove('bieudo_avl.png')
        os.remove(pdf_path)
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi: {e}</b>", parse_mode="HTML")        

@bot.message_handler(commands=['pfinance'])
def pfinance(message):
    try:
        danh_sach = lay_danh_sach_crypto()
        parts = message.text.split(maxsplit=3)
        if len(parts) < 4:
            bot.send_message(message.chat.id, "<b>Nhập theo định dạng /pfinance [Loại chỉ báo] [Tên coin] [Thời gian (m)]</b>", parse_mode="HTML")
            return 
        loai_chi_bao = parts[1].lower()
        loai_chi_bao_cho_phep = ["ma", "ema", "boll", "sar", "avl"]
        if loai_chi_bao not in loai_chi_bao_cho_phep:
            bot.send_message(message.chat.id, "<b>Chỉ báo cho phép là 'ma' 'ema' 'boll' 'sar' 'avl'</b>", parse_mode="HTML")
            return 
        ten_crypto = parts[2].upper() + "USDT"
        khoang_thoi_gian_muon_lay = int(parts[3])
        if ten_crypto not in danh_sach:
            bot.send_message(message.chat.id, f"<b>{ten_crypto} không có trong danh sách tên coin</b>", parse_mode="HTML")
            return 
        if khoang_thoi_gian_muon_lay < 20 or khoang_thoi_gian_muon_lay > 400:
            bot.send_message(message.chat.id, "<b>Giới hạn thời gian trong khoảng 20 - 400 phút</b>", parse_mode="HTML")
            return
        thoi_gian_hien_tai = datetime.now()
        thoi_gian_muon_lay = thoi_gian_hien_tai - timedelta(minutes=khoang_thoi_gian_muon_lay)
        timestamp_thoi_gian_muon_lay = int(thoi_gian_muon_lay.timestamp() * 1000)
        timestamp_hien_tai = int(thoi_gian_hien_tai.timestamp() * 1000)
        lay_thong_tin_gioi_han_crypto_chart(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai, message)
        if loai_chi_bao == "ma":
            ve_bieu_do_nen_ma(message, ten_crypto)
            os.remove("bieudo_ma.png")
        elif loai_chi_bao == "boll":
            ve_bieu_do_nen_boll(message, ten_crypto)
            os.remove("bieudo_boll.png")
        elif loai_chi_bao == "ema":    
            ve_bieu_do_nen_ema(message, ten_crypto)
            os.remove("bieudo_ema.png")
        elif loai_chi_bao == "sar":
            ve_bieu_do_nen_sar(message, ten_crypto)
            os.remove("bieudo_sar.png")
        else:
            ve_bieu_do_nen_avl(message, ten_crypto)
            os.remove("bieudo_avl.png")
        if os.path.exists(f"{ten_crypto}.json"):
            os.remove(f"{ten_crypto}.json")    
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi {e}</b>", parse_mode="HTML")        

filename = "QR_LINK_CODE.png"
def download_qr_image(url, noi_dung,  message):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        with open(filename, "rb") as file:    
            bot.send_photo(message.chat.id, file, caption = noi_dung, parse_mode = "HTML")
        os.remove(filename)    
        print(f"QR code đã được tải xuống thành công: {filename}")
    else:
        print("Không thể tải QR code. Vui lòng kiểm tra lại URL")

@bot.message_handler(commands=["qrbank"])
def lay_thong_tin(message):
    User_id = str(message.chat.id)
    bank_list = [
        "mbbank", "dongabank", "viettinbank", "vietcombank", "techcombank", 
        "bidv", "acb", "sacombank", "vpbank", "agribank",
        "hdbank", "tpbank", "shb", "eximbank", "ocb",
        "seabank", "bacabank", "pvcombank", "scb", "vib",
        "namabank", "abbank", "lpbank", "vietabank", "msb",
        "nvbank", "pgbank", "publicbank", "cimbbank", "uob"
    ]
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) != 3:
            bot.send_message(message.chat.id, "<b>Nhập theo định dạng /qrbank [Số tiền] [Nội dung chuyển khoản]</b>", parse_mode = "HTML")
            return 
        so_tien = int(parts[1])
        if not isinstance(so_tien, int):
            bot.send_message(message.chat.id, "<b>Tiền phải là số nguyên, nếu không muốn để số tiền thì nhập 0</b>", parse_mode = "HTML")
            return
        if so_tien < 10000:
            bot.send_message(message.chat.id, "<b>Tiền phải lớn hơn 10.000 VNĐ</b>", parse_mode = "HTML")
            return    
        so_tai_khoan = "1430042006"
        ma_ngan_hang = "techcombank"
        noi_dung = ""    
        noi_dung_nguoi_nhap = " ".join(parts[2:]) if len(parts) > 2 else ""
        if(noi_dung_nguoi_nhap == ""):
            noi_dung = "Chuyển khoản" 
        else:
            noi_dung = noi_dung_nguoi_nhap    
        link = qrlink(so_tai_khoan, ma_ngan_hang, so_tien, noi_dung, "true")
        dinh_dang_so_tien = f"{so_tien:,.0f}"
        dinh_dang_so_tien = dinh_dang_so_tien.replace(",", ".")
        noi_dung_thong_tin = (
            f"<b>➤ THÔNG TIN QRCODE !!!\n" 
            f"┏━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            f"┣➤ 💳 Số TK: <code>{so_tai_khoan}</code>\n"
            f"┣➤ 🏦 Bank: {ma_ngan_hang.upper()}\n"
            f"┣➤ 💵 Số tiền: {dinh_dang_so_tien} VNĐ\n"
            f"┣➤ 📋 Nội dung: <code>{noi_dung}</code>\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━━━┛</b>\n"
        )
        download_qr_image(link, noi_dung_thong_tin, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi: {e}</b>", parse_mode = "HTML")    

# Hàm trả lời ngoại lệ     
@bot.message_handler(func=lambda message: True)
@bot.message_handler(content_types=['sticker','photo','video','document'])    
def tra_loi_ngoai_le(message):
    huong_dan_su_dung = telebot.types.InlineKeyboardButton("📝 Hướng dẫn sử dụng", callback_data="hdsd")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(huong_dan_su_dung)
    bot.send_message(message.chat.id, f"<b>❌ Sai lệnh. Vui lòng xem lại</b>", parse_mode='HTML',reply_markup=keyboard)

def RUN_BOT_TRADINGVIEW():
    try:
        while True:
            if lay_thong_tin_crypto("BTCUSDT") and lay_ty_gia_vnd() and lay_danh_sach_crypto() and qrlink("00230042006", "mbbbank", "50000", "", "false"):
                print("Kết nối tất cả thành công")
                break    
        print("BOT ĐANG HOẠT ĐỘNG ...")         
        bot.infinity_polling(timeout=10)
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
    except http.client.HTTPException as http_err:
        print(f"Đã xảy ra lỗi HTTP: {http_err}")

if __name__ == "__main__": 
    RUN_BOT_TRADINGVIEW()

# The end

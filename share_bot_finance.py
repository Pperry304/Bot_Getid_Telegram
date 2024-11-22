import time, requests, json, telebot, os
import pandas as pd
import matplotlib
import mplfinance as mpf
from telebot import types
from datetime import datetime, timedelta

URL_API_BINANCE= 'https://api.binance.com/api/v3'
API_TOKEN_BOT = '6790339105:AAEKvcd-EmkC3mXI3IDAWVi9uIienb7B-DM'
bot = telebot.TeleBot(API_TOKEN_BOT)

matplotlib.use('Agg')
# Hàm lấy danh sách các đồng crypto
def lay_danh_sach_crypto():
    response = requests.get(f'{URL_API_BINANCE}/exchangeInfo')
    data = response.json()
    danh_sach = [s['symbol'] for s in data['symbols'] if s['quoteAsset'] == 'USDT']
    return danh_sach 

def lay_thong_tin_gioi_han_crypto(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai, message):
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
    file_path = f'D:\\Python\\{ten_crypto.upper()}.json'
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
    with open(f"D:\\Python\\{ten_crypto}.json", "r", encoding="utf-8") as file:
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
        title="Biểu đồ giá BTC/USDT",
        ylabel="Giá (USDT)",
        volume=True,  
        ylabel_lower="Khối lượng",
        mav=(5, 10),  # Thêm MA
        savefig='D:\\Python\\bieudo_ma.png'  
    )
    with open('D:\\Python\\bieudo_ma.png', 'rb') as file:
        thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bot.send_photo(message.chat.id, file, caption = f'<b>Biểu đồ nến MA lúc: {thoi_gian_hien_tai}</b>', parse_mode="HTML")

# Biểu đồ chỉ báo BOLL 
def ve_bieu_do_nen_boll(message, ten_crypto):
    with open(f"D:\\Python\\{ten_crypto}.json", "r", encoding="utf-8") as file:
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
        title="Biểu đồ giá BTC/USDT với Bollinger Bands",
        ylabel="Giá (USDT)",
        volume=True,
        ylabel_lower="Khối lượng",
        addplot=apds,  # Thêm Bollinger Bands
        savefig='D:\\Python\\bieudo_boll.png'
    )
    with open('D:\\Python\\bieudo_boll.png', 'rb') as file:
        thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bot.send_photo(message.chat.id, file, caption = f'<b>Biểu đồ nến BOLL lúc: {thoi_gian_hien_tai}</b>', parse_mode="HTML")

def ve_bieu_do_nen_ema(message, ten_crypto):
    with open(f"D:\\Python\\{ten_crypto}.json", "r", encoding="utf-8") as file:
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
        title="Biểu đồ giá BTC/USDT với EMA",
        ylabel="Giá (USDT)",
        volume=True,
        ylabel_lower="Khối lượng",
        addplot=apds,  # Thêm EMA vào biểu đồ
        savefig='D:\\Python\\bieudo_ema.png'
    )
    with open('D:\\Python\\bieudo_ema.png', 'rb') as file:
        thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bot.send_photo(message.chat.id, file, caption = f'<b>Biểu đồ nến EMA lúc: {thoi_gian_hien_tai}</b>', parse_mode="HTML")

@bot.message_handler(commands=['finance'])
def main(message):
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
        lay_thong_tin_gioi_han_crypto(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai, message)
        ve_bieu_do_nen_ma(message, ten_crypto)
        ve_bieu_do_nen_boll(message, ten_crypto)
        ve_bieu_do_nen_ema(message, ten_crypto)
        os.remove(f'D:\\Python\\{ten_crypto.upper()}.json')    
        os.remove('D:\\Python\\bieudo_ma.png')
        os.remove('D:\\Python\\bieudo_boll.png')
        os.remove('D:\\Python\\bieudo_ema.png')
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Đã xảy ra lỗi: {e}</b>", parse_mode="HTML")        

if __name__ == "__main__":
    print("Bot đang chạy")
    bot.infinity_polling()


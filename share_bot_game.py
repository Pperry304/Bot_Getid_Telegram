# ! py
# Bot game txcl
# Lưu ý: Không lưu database 
# Copyright by @Truongchinh304

import time 
import qrcode
import random
import telebot
import datetime
import threading
from datetime import datetime, timedelta    
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from collections import defaultdict, deque

# Token bot  
bot = telebot.TeleBot("THAY API BOT GAME")    #Bot game
bot1 = telebot.TeleBot("THAY API BOT THÔNG BÁO NẠP RÚT")   #Bot thông báo rút tiền 
print("\nBot đang hoạt động ...\n")        

# Thông tin / thời gian .
user_list = set()
admin_id = "5748482452" # id admin 
def thoi_gian_hien_tai():
    thoi_gian_hien_tai = datetime.now() + timedelta(hours=0)
    gio_phut_giay = thoi_gian_hien_tai.strftime("%H:%M:%S")
    ngay_hien_tai = thoi_gian_hien_tai.strftime("%d-%m-%Y")
    return ngay_hien_tai, gio_phut_giay

def cap_nhat_thoi_gian():
    global thoigian, ngay
    while True:
        ngay, thoigian = thoi_gian_hien_tai()
threading.Thread(target=cap_nhat_thoi_gian, daemon=True).start()

# Bắt đầu game (/start) 
@bot.message_handler(commands=['start'])
def start(message):
    global user_states, user_lsnaprut, user_lschoi, user_tongcuoc, user_lsnap, user_lsrut
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_list.add(user_id)
        user_states = {}    # Khởi tạo thông tin người dùng
        user_states = defaultdict(lambda: {'phien': 1,'phien_sn': 1,'phien_cl': 1,'phien_bc': 1,'phien_tx1xx': 1,'phien_tx10': 1,'phien_nxx': 1,'phien_qv': 1,'phien_bltx': 1,'phien_blcl': 1,'phien_nbl': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0})
        user_lsnap = defaultdict(lambda: deque(maxlen=15))
        user_lsrut = defaultdict(lambda: deque(maxlen=15))
        user_lschoi = defaultdict(lambda: deque(maxlen=20))
        user_lsnaprut = defaultdict(lambda: {'tongnap': 0,'tongrut': 0})
        user_tongcuoc = defaultdict(lambda: {'tongcuoc': 0,})
        bot.send_message(message.chat.id, "Hãy nhất vào nút 👤 Tài khoản để được kích hoạt")
    bot.send_message(message.chat.id , "MINIGAMES: Nhà cái top 1 trên nền tảng Telegram 🏆\n\n🎮 Đa dạng game hay trên Telegram\n🎮 An toàn bảo mật tuyệt đối\n🎮 Nạp rút nhanh chóng, tiện lợi\n\n🕹️ Chúc các bạn chơi game vui vẻ ! 🕹️",disable_web_page_preview=True)
    time.sleep(1)
    nut_start(message)
    



###################################################################################################
# NẠP - RÚT - CHUYỂN TIỀN - MUA GIFT- NHẬP GIFT - LSCHOI - TONGCUOC - LS NAP / RUT - TỔNG PHIÊN
# Các lệnh cho admin
# Nhắn cho users 
@bot.message_handler(commands=['nhan'])
def nhan(message):
    user_id = str(message.chat.id)
    if user_id != admin_id:
        bot.send_message(message.chat.id, "Bạn không có quyền sử dụng lệnh này.")
        return 
    if user_id not in user_list:
        user_list.add(user_id)
    msg_content = message.text[6:].strip()
    if msg_content:
        for user in user_list:
            if user != user_id:
                bot.send_message(user, f"{msg_content}")
    else:
        bot.send_message(message.chat.id, "Vui lòng nhập nội dung tin nhắn sau lệnh /nhan")
            
            
# Đổi điểm vip cuả users
@bot.message_handler(commands=['doidiemvip'])           
def doidiemvip(message):
    user_id = str(message.chat.id)
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.send_message(message.chat.id, "🚫 Sai cú pháp. Vui lòng dùng cú pháp: /doidiemvip [dấu cách] số điểm muốn đổi")
            return
        diemvip_chuyen = int(parts[1])    
        if user_states[user_id]['points'] < diemvip_chuyen:
            bot.send_message(message.chat.id, "❌ Không đủ điểm để đổi")
            return 
        if user_states[user_id]['points'] < 1:
            bot.send_message(message.chat.id, "❌ Điểm Vip không hợp lệ")
            return     
        tien_doi_diem_vip = diemvip_chuyen * 100
        user_states[user_id]['sodu'] += tien_doi_diem_vip
        user_states[user_id]['points'] -= diemvip_chuyen
        bot.send_message(message.chat.id, f"🧾 Đổi thành công {diemvip_chuyen} điểm Vip\n\n💰 Số dư mới: {user_states[user_id]['sodu']:,.0f}đ\n📋 Điểm vip còn lại: {user_states[user_id]['points']} điểm")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Số điểm không hợp lệ. Vui lòng nhập lại")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Có lỗi xảy ra: {str(e)}")
    
      
# Nạp tiền cho users
@bot.message_handler(commands=['naptien'])
def nap(message):
    global thoigiannap
    users_id = str(message.chat.id)
    if users_id != admin_id:
        bot.send_message(message.chat.id, "Bạn không có quyền sử dụng lệnh này.")
        return
    try:
        _, users_id, tiennap = message.text.split()
        tiennap = int(tiennap)
    except ValueError:
        bot.send_message(message.chat.id, "Vui lòng nhập đúng định dạng: /nap [users_id] [tiennap]")
        return

    if users_id in user_states:
        thoigiannap = thoigian + " " + ngay
        user_states[users_id]['sodu'] += tiennap
        user_lsnaprut[users_id]['tongnap'] += tiennap
        bot.send_message(message.chat.id, f"✅ Nạp thành công {tiennap:,.0f} đ vào tài khoản {users_id}\n💸 Số dư mới: {user_states[users_id]['sodu']:,.0f} đ")
        bot.send_message(users_id, f"💸 Bạn đã nạp thành công {tiennap:,.0f} đ vào tài khoản\n➤ Số dư mới: {user_states[users_id]['sodu']:,.0f} đ")
        user_lsnap[users_id].append({
            'nguoinap': 'Admin N-TC',
            'tiennap': tiennap,
            'thoigian': thoigiannap,
            'trangthai': 'Thành công'
        })            
    else:
        bot.send_message(message.chat.id, "ID người dùng không hợp lệ.")
        
        
# Rút tiền cho users
@bot.message_handler(commands=['ruttien'])
def rut(message):
    global thoigianrut
    users_id = str(message.chat.id)
    if users_id != admin_id:
        bot.send_message(message.chat.id, "Bạn không có quyền sử dụng lệnh này.")
        return
    try:
        _, users_id, tienrut = message.text.split()
        tienrut = int(tienrut)
    except ValueError:
        bot.send_message(message.chat.id, "Vui lòng nhập đúng định dạng: /rut [users_id] [tienrut]")
        return

    if users_id in user_states:
        thoigianrut = thoigian + " " + ngay
        user_states[users_id]['sodu'] -= tienrut
        user_lsnaprut[users_id]['tongrut'] += tienrut
        bot.send_message(message.chat.id, f"✅ Rút thành công {tienrut:,.0f} đ từ tài khoản {users_id}\n💸 Số dư mới: {user_states[users_id]['sodu']:,.0f} đ")
        bot.send_message(users_id, f"💸 Bạn đã rút thành công {tienrut:,.0f} đ từ tài khoản\n➤ Số dư mới: {user_states[users_id]['sodu']:,.0f} đ")
        user_lsrut[users_id].append({
            'nguoirut': 'Admin N-TC',
            'tienrut': tienrut,
            'thoigian': thoigianrut,
            'trangthai': 'Thành công'
        })            
    else:
        bot.send_message(message.chat.id, "ID người dùng không hợp lệ.")


# Chuyển tiền cho users        
@bot.message_handler(commands=['chuyen'])
def xu_ly_chuyen_tien(message):
    try:
        # Tách lệnh để lấy ID người nhận và số tiền muốn chuyển
        parts = message.text.split()
        if len(parts) != 3:
            bot.send_message(message.chat.id, "🚫 Sai cú pháp. Vui lòng dùng cú pháp: /chuyen [id người nhận] [số tiền muốn chuyển]")
            return
        user_id_chuyen = str(message.chat.id)
        user_id_nhan = parts[1]
        tienchuyen = int(parts[2])
        # Kiểm tra số dư của người gửi
        if user_states[user_id_chuyen]['sodu'] < tienchuyen:
            bot.send_message(message.chat.id, "❌ Số dư không đủ để chuyển tiền")
            return
        # Kiểm tra tính hợp lệ của ID người nhận
        if user_id_nhan not in user_states:
            bot.send_message(message.chat.id, "❌ ID người nhận không tồn tại")
            return
        # Thực hiện chuyển tiền
        user_states[user_id_chuyen]['sodu'] -= tienchuyen
        user_states[user_id_nhan]['sodu'] += tienchuyen
        # Thông báo kết quả
        bot.send_message(message.chat.id, f"✅ Đã chuyển {tienchuyen:,.0f}đ cho ID: {user_id_nhan}")
        bot.send_message(user_id_nhan, f"✅ Bạn đã nhận được {tienchuyen:,.0f}đ từ ID: {user_id_chuyen}")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Số tiền không hợp lệ. Vui lòng nhập lại")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Có lỗi xảy ra: {str(e)}")


# Mua giftcode 
giftcode_used_mua = []        #Giftcode đã mua
giftcode_used_da_dung = []    #Giftcode đã dùng

def noi_dung_mua_giftcode(message):
    noi_dung_mua_Giftcode = (
        """💝 Để mua Giftcode, vui lòng thực hiện theo cú pháp sau: ( hệ thống sẽ thu phí 10% trên tổng tiền mua )

/muagiftcode [dấu cách] số lượng giftcode [dấu cách] Số tiền mỗi giftcode

➡️ Vd:  /muagiftcode 10 5000 (mua 10 giftcode với trị giá mỗi giftcode là 5000đ)"""
    )            
    bot.send_message(message.chat.id, noi_dung_mua_Giftcode)

@bot.message_handler(commands=['muagiftcode'])
def mua_gift_code(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    ky_tu_giftcode = "ABCDEFGHIJKLMNPQRSTUVWXYZ1234567890"
    parts = message.text.split()
    if len(parts) < 3:
        bot.send_message(message.chat.id, "❌ Yêu cầu không đúng định dạng. Vui lòng nhập theo mẫu: /muagiftcode [dấu cách] Số giftcode muốn mua [dấu cách] Mệnh giá giftcode")
        return 
    so_gift_code_muon_mua = int(parts[1])
    menh_gia_gift_code = int(parts[2])
    tong_tien_mua_gift_code = (so_gift_code_muon_mua * menh_gia_gift_code)*(1+0.1)
    if tong_tien_mua_gift_code > user_state['sodu']:
        bot.send_message(message.chat.id, "❌ Không đủ tiền để mua giftcode")
        return
    else:
        bot.send_message(message.chat.id, f"🧾 Yêu cầu mua {so_gift_code_muon_mua} giftcode mệnh giá {menh_gia_gift_code} đồng đã được ghi nhận")
        user_state['sodu'] -= tong_tien_mua_gift_code
        for i in range(so_gift_code_muon_mua):
            gift_code_mua = "".join(random.choice(ky_tu_giftcode) for i in range(6))
            bot.send_message(message.chat.id, f"📋 Giftcode {i+1}: `{gift_code_mua}` với mệnh giá {menh_gia_gift_code} đồng", parse_mode='Markdown')
            giftcode_used_mua.append((gift_code_mua, menh_gia_gift_code))
        bot.send_message(message.chat.id, "📝 Nhập giftcode theo mẫu : /nhapgiftcode [dấu cách] giftcode của bạn")

def noi_dung_nhap_gift_code(message):
    bot.send_message(message.chat.id, "Nhập giftcode theo mẫu: /nhapgiftcode [dấu cách] giftcode của bạn")
    
@bot.message_handler(commands=['nhapgiftcode'])
def nhap_gift_code_mua(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    parts = message.text.split()
    if len(parts) < 2 :
        bot.send_message(message.chat.id, "Nhập giftcode theo mẫu: /nhapgiftcode [dấu cách] giftcode của bạn")
    else:
        gift_code_nhap = parts[1]
        for gift_code, menh_gia in giftcode_used_mua:
            if gift_code_nhap == gift_code:
                user_state['sodu'] += menh_gia
                bot.send_message(message.chat.id, f"🎁 Giftcode hợp lệ! Cộng {menh_gia} đồng vào tài khoản.")
                giftcode_used_mua.remove((gift_code, menh_gia))
                giftcode_used_da_dung.append(gift_code)
                return
        if gift_code_nhap in giftcode_used_da_dung:
            bot.send_message(message.chat.id, "❌ Giftcode này đã được sử dụng !")
        else:
            bot.send_message(message.chat.id, "❌ Giftcode không hợp lệ")
    
    
# Lịch sử chơi
@bot.message_handler(commands=['lschoi'])
def xem_lich_su_choi(message):
    user_id = str(message.chat.id)
    history = user_lschoi.get(user_id, [])
    if not history:
        bot.send_message(message.chat.id, "Chưa có lịch sử chơi.")
    else:
        history_text = "LỊCH SỬ 20 PHIÊN GẦN NHẤT\n\nThời gian | Game | Số tiền | Trạng thái\n"
        # Lấy 20 phiên gần nhất
        latest_history = history[:20] if len(history) > 20 else history
        # Duyệt qua từng phiên trong lịch sử và thêm số thứ tự
        for idx, record in enumerate(latest_history, start=1):
            history_text += (
                f"{idx}. {record['thoigian']} | "
                f"{record['game']} | "
                f"{record['tiencuoc']:,.0f} | "
                f"{record['trangthai']}\n"
            )
        bot.send_message(message.chat.id, history_text)


# Lịch sử nạp
@bot.message_handler(commands=['lsnap'])
def xem_lich_su_nap(message):        
    user_id = str(message.chat.id)
    lsnap = user_lsnaprut[user_id]
    history_nap = user_lsnap.get(user_id, [])
    if not lsnap  or int(user_lsnaprut[user_id]['tongnap']) <= 0 :
        bot.send_message(message.chat.id, "Chưa có lịch sử nạp.")
    else:
        history_text = "💸 LỊCH SỬ 15 PHIÊN NẠP GẦN NHẤT\n\nNgười nạp | Số tiền | Thời gian | Trạng thái\n"
        latest_history = history_nap[:20] if len(history_nap) > 20 else history_nap
        # Duyệt qua từng phiên trong lịch sử và thêm số thứ tự
        for idx, record in enumerate(latest_history, start=1):
            history_text += (
                f"{idx}. {record['nguoinap']} | "
                f"{record['tiennap']:,.0f} | "
                f"{record['thoigian']} | "
                f"{record['trangthai']}\n"
            )     
        bot.send_message(message.chat.id, history_text)     


# Lịch sử rút
@bot.message_handler(commands=['lsrut'])
def xem_lich_su_rut(message):        
    user_id = str(message.chat.id)
    lsrut = user_lsnaprut[user_id]
    history_rut = user_lsrut.get(user_id, [])
    if not lsrut or int(user_lsnaprut[user_id]['tongrut']) <= 0 :
        bot.send_message(message.chat.id, "Chưa có lịch sử rút.")
    else:
        history_text = "💸 LỊCH SỬ 15 PHIÊN RÚT GẦN NHẤT\n\nNgười rút | Số tiền | Thời gian | Trạng thái\n"
        latest_history = history_rut[:20] if len(history_rut) > 20 else history_rut
        # Duyệt qua từng phiên trong lịch sử và thêm số thứ tự
        for idx, record in enumerate(latest_history, start=1):
            history_text += (
                f"{idx}. {record['nguoirut']} | "
                f"{record['tienrut']:,.0f} | "
                f"{record['thoigian']} | "
                f"{record['trangthai']}\n"
            )     
        bot.send_message(message.chat.id, history_text)       


# Tổng cược 
@bot.message_handler(commands=['tc'])
def xem_tong_cuoc(message):        
    global tongphien 
    user_id = str(message.chat.id)    
    tongcuoc = user_tongcuoc[user_id]['tongcuoc']
    user_data = user_states[user_id]
    tongphien = (
        user_data['phien'] + user_data['phien_sn'] + user_data['phien_cl'] +
        user_data['phien_bc'] + user_data['phien_tx1xx'] + user_data['phien_tx10'] +
        user_data['phien_nxx'] + user_data['phien_qv'] + user_data['phien_bltx'] +
        user_data['phien_blcl'] + user_data['phien_nbl']
    )
    if not tongcuoc:
        bot.send_message(message.chat.id, "Chưa cược ván nào.")
    else:
        bot.send_message(message.chat.id, f"✅ ID: {user_id}\n✅ Bạn đã chơi {tongphien-11} lượt\n✅ Tổng tiền cược: {tongcuoc:,.0f}đ")


# Xếp hạng    
@bot.message_handler(func=lambda message: message.text == "🥇 Bảng xếp hạng")
@bot.message_handler(commands=['xephang'])
def xep_hang(message):
    user_id = str(message.chat.id)
    # Sắp xếp người dùng dựa trên tổng cược và loại bỏ những người có tổng cược bằng 0
    sorted_users = sorted(
        {uid: info for uid, info in user_tongcuoc.items() if info['tongcuoc'] > 0}.items(),
        key=lambda item: item[1]['tongcuoc'],
        reverse=True
    )
    top_20 = sorted_users[:20]

    # Tạo bảng xếp hạng
    ranking_text = f"🏆 Bảng xếp hạng ngày {ngay}\n\nTOP - ID - TỔNG CƯỢC\n"
    for rank, (uid, info) in enumerate(top_20, start=1):
        ranking_text += f"{rank} - {uid} - Tổng cược: {info['tongcuoc']:,.0f} đ\n"

    # Tìm thứ hạng của người dùng hiện tại
    user_rank = next((i for i, (uid, _) in enumerate(sorted_users, start=1) if uid == user_id), None)
    if user_rank is not None:
        if user_rank > 20 and user_rank <= 100:
            ranking_text += f"\nTổng cược của bạn là: {user_states[user_id]['tongcuoc']:,.0f}đ\n"
            ranking_text += f"Thứ hạng của bạn là: {user_rank}\n"
        elif user_rank > 100:
            ranking_text += f"\nTổng cược của bạn là: {user_states[user_id]['tongcuoc']:,.0f}đ\n"
            ranking_text += f"Thứ hạng của bạn là: Vô cực\n"
    else:
        ranking_text += "\nBạn chưa có cược nào để hiển thị trong bảng xếp hạng.\n"

    bot.send_message(message.chat.id, ranking_text)

    
# Tổng phiên
@bot.message_handler(commands=['tp'])   
def tongphien(message):
    bot.send_message(message.chat.id, f"Bạn đã chơi {tongphien-11} lượt All game !")


# Rút tiền momo
@bot.message_handler(commands=['rutmomo'])           
def xu_ly_rut_tien_momo(message):
    user_id = str(message.chat.id)
    user_name = message.from_user.username
    full_name = message.from_user.first_name + " " + message.from_user.last_name
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.send_message(message.chat.id, "🚫 Yêu cầu không đúng định dạng. Vui lòng nhập lại theo mẫu: /rutmomo [SĐT] [Số tiền muốn rút] [Nội dung]")
            return
        sdt = parts[1]
        tien_rut_momo = int(parts[2])  # Chuyển số tiền thành kiểu số nguyên
        noi_dung_momo = " ".join(parts[3:]) if len(parts) > 3 else ""
        if noi_dung_momo == "":
            noi_dung_momo = "không có"
        if tien_rut_momo > user_states[user_id]['sodu']:
            bot.send_message(message.chat.id, "❌ Không đủ tiền trong tài khoản để rút. Vui lòng nhập số tiền nhỏ hơn hoặc bằng số dư.")
            return
        if tien_rut_momo < 50000:
            user_states[user_id]['sodu'] -= tien_rut_momo + 2000
            bot.send_message(message.chat.id, f"➤ Yêu cầu rút tiền MoMo đã được ghi nhận.\n➤ SĐT: {sdt}\n➤ Số tiền: {(tien_rut_momo-2000):,.0f}đ\n➤ Nội dung: {noi_dung_momo}\n  ➤ Số dư mới sau khi rút {(user_states[user_id]['sodu']):,.0f}đ")
            bot1.send_message(message.chat.id, f"➤ Tên: {full_name}\n➤ Tên người dùng: {user_name}\n➤ Yêu cầu rút momo:\n  +Sđt: {sdt}\n  +Tiền muốn rút: {(tien_rut_momo-2000):,.0f}đ\n  +Nội dung: {noi_dung_momo}\n➤ Thời gian: {thoigian}")
        else:
            user_states[user_id]['sodu'] -= tien_rut_momo 
            bot.send_message(message.chat.id, f"➤ Yêu cầu rút tiền MoMo đã được ghi nhận.\n➤ SĐT: {sdt}\n➤ Số tiền: {(tien_rut_momo):,.0f} đồng\n➤ Nội dung: {noi_dung_momo}\n➤ Số dư mới sau khi rút {(user_states[user_id]['sodu']):,.0f}đ")    
            bot1.send_message(message.chat.id, f"➤ Tên: {full_name}\n➤ Tên người dùng: {user_name}\n➤ Yêu cầu rút momo:\n  +Sđt: {sdt}\n  +Tiền muốn rút: {(tien_rut_momo):,.0f} đồng\n  +Nội dung: {noi_dung_momo}\n➤ Thời gian: {thoigian}")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Số tiền không hợp lệ. Vui lòng nhập lại")
            
            
# Rút tiền ngân hàng
@bot.message_handler(commands=['rutbank'])
def xu_ly_rut_tien_bank(message):
    user_id = str(message.chat.id)
    user_name = message.from_user.username
    full_name = message.from_user.first_name + " " + message.from_user.last_name
    parts = message.text.split()
    if len(parts) < 4:
        bot.send_message(message.chat.id, "🚫 Yêu cầu không đúng định dạng. Vui lòng nhập lại theo mẫu: /rutbank [Số tiền] [Mã ngân hàng] [Số tài khoản] [Tên chủ tài khoản]")
        return
    tien_rut_ngan_hang = int(parts[1])
    ma_ngan_hang = parts[2]
    so_tai_khoan = parts[3]
    ten_chu_tai_khoan = " ".join(parts[4:]) if len(parts) > 4 else ""
    if tien_rut_ngan_hang > user_states[user_id]['sodu']:
        bot.send_message(message.chat.id, "❌ Không đủ tiền trong tài khoản để rút. Vui lòng nhập số tiền nhỏ hơn hoặc bằng tổng vốn.")
        return
    ma_ngan_hang_hop_le = ["VCB", "BIDV", "VTB", "TCB", "MBB", "AGR", "TPB", "SHB", "ACB", "MSB", "VIB", "STB", "VPB", "SAB", "SHIB", "EIB", "KLB", "DAB", "HDB", "LVPB", "VBB", "ABB", "PGB", "PVB", "BAB", "SCB", "VCCB", "SGB", "BVB", "OCB", "OJB"]
    if ma_ngan_hang not in ma_ngan_hang_hop_le:
        bot.send_message(message.chat.id, f"👉 Mã ngân hàng không hợp lệ. Vui lòng kiểm tra và nhập lại.")
        return
    user_states[user_id]['sodu'] -= tien_rut_ngan_hang    
    bot.send_message(message.chat.id, f"➤ Yêu cầu rút ngân hàng đã được ghi nhận.\n➤ Số tiền: {(tien_rut_ngan_hang):,.0f}đ\n➤ Mã ngân hàng: {ma_ngan_hang}\n➤ Số tài khoản: {so_tai_khoan}\n➤ Tên chủ tài khoản: {ten_chu_tai_khoan}\n➤ Số dư mới sau khi rút {(user_states[user_id]['sodu']):,.0f}đ")
    bot1.send_message(message.chat.id, f"➤ Tên: {full_name}\n➤ Tên người dùng: {user_name}\n➤ Yêu cầu rút bank:\n  +Tiền muốn rút: {(tien_rut_ngan_hang):,.0f}đ\n  +Mã ngân hàng: {ma_ngan_hang}\n  +Số tài khoản: {so_tai_khoan}\n  +Tên chủ ngân hàng: {ten_chu_tai_khoan}\n➤ Thời gian: {thoigian}")             


# Quà cho tân thủ
@bot.message_handler(func=lambda message: message.text == "🎁 Quà tặng cho tân thủ !!! 🎁")
def qua_tan_thu(message):
    giftcode = "MNTX"
    bot.send_message(message.chat.id, f"🎁 Chào mừng tân thủ nhập code `{giftcode}` để nhận phần quà 2000đ vào tài khoản\n\n👉 Nhập theo cú pháp /gift [dấu cách] mã giftcode", parse_mode='Markdown')


giftcode_tanthu_dadung = {}
# Nhập giftcode 
@bot.message_handler(commands=['gift'])
def nhap_gift_code_tan_thu(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    giftcode = message.text.split(" ")[1]  # Lấy phần mã giftcode từ tin nhắn
    if giftcode not in giftcode_tanthu_dadung or not giftcode_tanthu_dadung[giftcode]:
        if giftcode == "MNTX":
            user_state['sodu'] += 2000
            bot.send_message(message.chat.id, "🎁 Nhận thành công 2000đ vào tài khoản")
            giftcode_tanthu_dadung[giftcode] = True 
        else:
            bot.send_message(message.chat.id, "❌ Giftcode không hợp lệ")
    else:
         bot.send_message(message.chat.id, "❌ Giftcode này đã được sử dụng !")
         
    
    
    
#############################################################################################

# CÁC NÚT THAO TÁC                    
def nut_start(message):
    markup = InlineKeyboardMarkup()
    button0 = InlineKeyboardButton(text="🎮 Chiến thôi !!!", callback_data="chien_thoi")
    markup.add(button0)
    bot.send_message(message.chat.id, "Bạn đã sẵn sàng bùng nổ chưa ? 💣💣💣", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "chien_thoi")
def nut_main(call):
    handle_nut_main(call.message)
def handle_nut_main(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2)
    button0 = types.KeyboardButton(text="🎮 Danh sách game")
    button1 = types.KeyboardButton(text="👤 Tài khoản")
    button2 = types.KeyboardButton(text="📜 Event")
    button3 = types.KeyboardButton(text="🥇 Bảng xếp hạng")
    button4 = types.KeyboardButton(text="🧑‍💻 Vào nhóm")
    button5 = types.KeyboardButton(text="👥 Giới thiệu bạn bè")
    button6 = types.KeyboardButton(text="❔Thông tin❔")
    button7 = types.KeyboardButton(text="💬 Trung tâm hỗ trợ")
    button8 = types.KeyboardButton(text="🎁 Quà tặng cho tân thủ !!! 🎁")
    user_markup.add(button0, button1)
    user_markup.add(button2, button3)
    user_markup.add(button5, button4)
    user_markup.add(button6, button7)
    user_markup.add(button8)
    bot.send_message(message.chat.id, "Chọn 1 trong những nút bên dưới 👇", reply_markup=user_markup)
    
@bot.message_handler(func=lambda message: message.text == "🎮 Danh sách game")
def nut_the_loai_game(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2)
    buttontx = types.KeyboardButton(text="🎲 Xúc Xắc 🎲")
    buttonbl = types.KeyboardButton(text="🎳 Bowling 🎳")
    buttonvm = types.KeyboardButton(text="🕹️ Vận May 🕹️")
    buttonsx = types.KeyboardButton(text="🧾 Xổ Số 🧾")
    buttonxx = types.KeyboardButton(text="🛎️ Xốc Xốc 🛎️")
    buttonql = types.KeyboardButton(text="⬅️ Quay lại")
    buttontt = types.KeyboardButton(text="⏱️ Timestick ⏱️")
    buttonsl = types.KeyboardButton(text="🎰 Slot 777 🎰")
    #user_markup.add(buttontx)
    user_markup.add(buttontx, buttonbl, buttonvm, buttonsx, buttonxx, buttontt, buttonsl, buttonql)
    #user_markup.add(buttonql)
    photo_path = "/sdcard/download/fpt/bothotro.jpg"
    with open(photo_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Thể loại game muốn chơi 👇👇👇",reply_markup=user_markup)    

@bot.message_handler(func=lambda message: message.text == "🎲 Xúc Xắc 🎲")
def game_xuc_xac(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)    
    button0 = types.KeyboardButton(text="🎲 Tài xỉu 🎲")
    button1 = types.KeyboardButton(text="🎲 Tài xỉu 1xx 🎲")
    button2 = types.KeyboardButton(text="🎲 Ném xúc xắc 🎲")
    button3 = types.KeyboardButton(text="🎲 Tài xỉu 10s 🎲")
    button4 = types.KeyboardButton(text="⬅️ Quay lại menu")
    user_markup.add(button0, button1, button2, button3, button4)
    photo_path = "/sdcard/download/fpt/botxucxac.jpg"
    with open(photo_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Game xúc xắc muốn chơi 👇👇👇", reply_markup=user_markup)
    
    
@bot.message_handler(func=lambda message: message.text == "🎳 Bowling 🎳")
def game_bowling(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)    
    button0 = types.KeyboardButton(text="🎳 Bowling-TX 🎳")
    button1 = types.KeyboardButton(text="🎳 Bowling-CL 🎳")
    button2 = types.KeyboardButton(text="🎳 Ném Bowling 🎳")
    button3 = types.KeyboardButton(text="⬅️ Quay lại menu")
    user_markup.add(button0, button1, button2, button3)
    photo_path = "/sdcard/download/fpt/botbowling.jpg"
    with open(photo_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Game bowling bạn muốn chơi 👇👇👇",reply_markup=user_markup)     


@bot.message_handler(func=lambda message: message.text == "🕹️ Vận May 🕹️")
def game_van_may(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)    
    button0 = types.KeyboardButton(text="🎯 Đoán số 🎯")
    button1 = types.KeyboardButton(text="🪙 Sấp ngửa 🪙")
    button2 = types.KeyboardButton(text="☝️ Chẵn lẻ ✌️")
    button3 = types.KeyboardButton(text="⬅️ Quay lại menu")
    user_markup.add(button0, button1, button2, button3)
    photo_path = "/sdcard/download/fpt/botvanmay.jpg"
    with open(photo_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Game vận may bạn muốn chơi 👇👇👇",reply_markup=user_markup)           
    

@bot.message_handler(func=lambda message: message.text == "🛎️ Xốc Xốc 🛎️")
def game_xoc_xoc(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)    
    button0 = types.KeyboardButton(text="🦀 Bầu cua 🦀")
    button1 = types.KeyboardButton(text="🔴 Quân vị ⚪")
    button2 = types.KeyboardButton(text="⬅️ Quay lại menu")
    user_markup.add(button0, button1, button2)
    photo_path = "/sdcard/download/fpt/botxocxoc.jpg"
    with open(photo_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Game xóc xóc bạn muốn chơi 👇👇👇",reply_markup=user_markup)               
    
@bot.message_handler(func=lambda message: message.text == "⬅️ Quay lại menu")
def quay_lai_menu(message):
    return nut_the_loai_game(message)
    
def co_khong(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)    
    button0 = types.KeyboardButton(text="Có")
    button1 = types.KeyboardButton(text="Không")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "Bạn chơi lại chứ ? 👇👇👇",reply_markup=user_markup)               
    
def nut_nhap_doan_so(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button0 = types.KeyboardButton(text="1")
    button1 = types.KeyboardButton(text="2")
    button2 = types.KeyboardButton(text="3")
    button3 = types.KeyboardButton(text="4")
    button4 = types.KeyboardButton(text="5")
    button5 = types.KeyboardButton(text="6")
    user_markup.add(button0, button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, "Chọn số muốn đoán 👇", reply_markup=user_markup) 

def nut_nhap_tien_cuoc(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=3)
    button0 = types.KeyboardButton(text="1000")
    button1 = types.KeyboardButton(text="5000")
    button2 = types.KeyboardButton(text="10000")
    button3 = types.KeyboardButton(text="20000")
    button4 = types.KeyboardButton(text="50000")
    button5 = types.KeyboardButton(text="100000")
    button6 = types.KeyboardButton(text="200000")
    button7 = types.KeyboardButton(text="500000")
    button8 = types.KeyboardButton(text="1000000")
    button9 = types.KeyboardButton(text="2000000")
    button10 = types.KeyboardButton(text="5000000")
    user_markup.add(button0, button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)
    bot.send_message(message.chat.id, "💵 Chọn mệnh giá cược ", reply_markup=user_markup)      
      
#######################################################################    
# ALL GAME     


# Tài xỉu
# Chia điểm theo level 1-15 (mỗi level 50 điểm)
level_thresholds = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750]
@bot.message_handler(func=lambda message: message.text == "🎲 Tài xỉu 🎲")
def tai_xiu(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id,"🎲 Chào mừng bạn đến game tài xỉu ! 🎲\n\n🎮 LUẬT CHƠI :\nBot sẽ tung 3 xúc xắc với giá trị từ 1 đến 6 mỗi xúc xắc\n➤ TÀI : 11 - 18 nút\n➤ XỈU : 3 - 10 nút")
    tai_xiu_main(message)

def tai_xiu_main(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_tai_xiu(message)

def nut_tai_xiu(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button0 = types.KeyboardButton(text="TÀI")
    button1 = types.KeyboardButton(text="XỈU")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "👉 Vui lòng chọn 1 trong 2 nút bên dưới", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_tai_xiu)

def lua_chon_tai_xiu(message):
    user_id = str(message.chat.id)
    luachon = message.text.strip()
    if luachon in ["TÀI", "XỈU"]:
        user_states[user_id]['luachon'] = luachon
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_tx)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn TÀI hoặc XỈU")
        nut_tai_xiu(message)

def nhap_tien_cuoc_tx(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_tx = int(message.text.strip())
        if tiencuoc_tx > 0 and tiencuoc_tx <= sodu:
            user_state['sodu'] -= tiencuoc_tx
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_tx
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_tx(message, tiencuoc_tx)
        elif tiencuoc_tx > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_tx)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_tx)
    
def xu_ly_ket_qua_tx(message, tiencuoc_tx):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachon = user_state['luachon']
    phien_tx = user_state['phien']
    sodu = user_state['sodu']

    xucxac_1 = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    xucxac_2 = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    xucxac_3 = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    tong_xucxac = xucxac_1 + xucxac_2 + xucxac_3
    time.sleep(4)
    if tong_xucxac > 10:
        ket_qua_tx = "TÀI"
    else: 
        ket_qua_tx = "XỈU"
    if (tong_xucxac > 10 and luachon == "TÀI") or (tong_xucxac < 11 and luachon == "XỈU"):
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += int(tiencuoc_tx * 1.9)
        trangthai = "Thắng"
        
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_tx}  ➤ Cược: {luachon}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_tx:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: {int(tiencuoc_tx * 1.9):,.0f}đ\n" 
                                          f"┣➤ Tổng điểm: {xucxac_1} + {xucxac_2} + {xucxac_3} = {tong_xucxac}\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THẮNG\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_tx}  ➤ Cược: {luachon}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_tx:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: 0đ\n" 
                                          f"┣➤ Tổng điểm: {xucxac_1} + {xucxac_2} + {xucxac_3} = {tong_xucxac}\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THUA\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
        )                                 
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Tx',
        'tiencuoc': tiencuoc_tx,
        'trangthai': trangthai,
    })            
    user_state['phien'] += 1
    co_khong(message)
    bot.register_next_step_handler(message,choi_tiep)
    
def choi_tiep(message):
    user_id = str(message.chat.id)
    choi_tiep = message.text.lower()
    if choi_tiep == "có":
        tai_xiu_main(message)
    elif choi_tiep == "không":
        game_xuc_xac(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep)



# Đoán số
user_states = defaultdict(lambda: {'phien_ds': 1})
@bot.message_handler(func=lambda message: message.text == "🎯 Đoán số 🎯")
def doan_so(message):
    bot.send_message(message.chat.id, "🎯 Chào mừng bạn đến với game đoán số! 🎯\n\n🎮 LUẬT CHƠI:\nBot sẽ tung xúc xắc và nhiệm vụ bạn là đoán số nút của xúc xắc đó (1-6)\n")
    user_id = message.chat.id
    user_states[user_id] = {'phien_ds': 1, 'van_may': 0, 'so_lan_doan': 1}
    doan_so_main(message)

def doan_so_main(message):
    user_id = message.chat.id
    user_state = user_states[user_id]
    bot.send_message(message.chat.id, f"👉 Lượt thứ {user_state['so_lan_doan']}")
    nut_nhap_doan_so(message)
    bot.register_next_step_handler(message, xu_ly_ket_qua_ds)

def xu_ly_ket_qua_ds(message):
    user_id = message.chat.id
    user_state = user_states[user_id]
    so_lan_doan = user_state['so_lan_doan']
    van_may = user_state['van_may']
    so_can_doan = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    time.sleep(4)
    try:
        so_doan = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "👉 Vui lòng nhập một số từ 1 đến 6")
        nut_nhap_doan_so(message)
        bot.register_next_step_handler(message, xu_ly_ket_qua_ds)
        return
    if so_doan == so_can_doan:
        van_may += 20
        bot.send_message(message.chat.id, f"✅ Chúc mừng bạn đã đoán trúng {so_can_doan} nút")
    else:
        bot.send_message(message.chat.id, f"❌ Bạn đã đoán sai! Số nút cần đoán là {so_can_doan}")

    if so_lan_doan >= 5:
        bot.send_message(message.chat.id, f"➤ Phiên {user_state['phien_ds']}\n👉 Vận may của bạn là {van_may}/100 điểm")
        user_state['phien_ds'] += 1
        co_khong(message)
        bot.register_next_step_handler(message,choi_tiep_ds)
    else:
        so_lan_doan += 1
        user_state['so_lan_doan'] = so_lan_doan
        user_state['van_may'] = van_may
        bot.send_message(message.chat.id, f"👉 Lượt thứ {so_lan_doan}")
        nut_nhap_doan_so(message)
        bot.register_next_step_handler(message, xu_ly_ket_qua_ds)

def choi_tiep_ds(message):
    user_id = message.chat.id
    user_state = user_states[user_id]
    choi_tiep_ds = message.text.lower()
    if choi_tiep_ds == "có":
        user_state['so_lan_doan'] = 1
        user_state['van_may'] = 0
        doan_so_main(message)
    elif choi_tiep_ds == "không":
        game_van_may(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_ds)



# Sấp ngửa
@bot.message_handler(func=lambda message: message.text == "🪙 Sấp ngửa 🪙")
def sap_ngua(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_sn': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🪙 Chào mừng bạn đến game sấp ngửa ! 🪙\n\n🎮 LUẬT CHƠI :\nBot sẽ tung đồng xu gồm 2 mặt SẤP và NGỬA\n➤ SẤP : mặt sấp đồng xu\n➤ NGỬA : mặt ngửa đồng xu\n\nNhiệm vụ của bạn là đoán mặt của đồng xu !!!")
    sap_ngua_main(message)

def sap_ngua_main(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_sap_ngua(message)

def nut_sap_ngua(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button0 = types.KeyboardButton(text="SẤP")
    button1 = types.KeyboardButton(text="NGỬA")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "👉 Vui lòng chọn 1 trong 2 nút bên dưới", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_sap_ngua)

def lua_chon_sap_ngua(message):
    user_id = str(message.chat.id)
    luachonsn = message.text.strip()
    if luachonsn == "SẤP" or luachonsn == "NGỬA":
        user_states[user_id]['luachon'] = luachonsn
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_sn)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn SẤP hoặc NGỬA")
        nut_sap_ngua(message)

def nhap_tien_cuoc_sn(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_sn = int(message.text.strip())
        if tiencuoc_sn > 0 and tiencuoc_sn <= sodu:
            user_state['sodu'] -= tiencuoc_sn
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_sn
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_sn(message, tiencuoc_sn)
        elif tiencuoc_sn > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_sn)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_sn)
        
def xu_ly_ket_qua_sn(message, tiencuoc_sn):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachonsn = user_state['luachon']
    phien_sn = user_state['phien_sn']
    sodu = user_state['sodu']
    mat = random.choice(["SẤP", "NGỬA"])

    sent_message = bot.send_message(message.chat.id, "⏱️ Vui lòng chờ ... ⏱️")
    time.sleep(0.5)
    for i in range(3):
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Đang tung đồng xu 🪙")
        time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Đang tung đồng xu")
    bot.send_message(message.chat.id, "🪙")    
    time.sleep(3)
    if (mat == "SẤP" and luachonsn == "SẤP") or (mat == "NGỬA" and luachonsn == "NGỬA"):
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += int(tiencuoc_sn * 1.9)
        trangthai = "Thắng"
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=  f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                                                                                  f"┣➤ Phiên: {phien_sn}  ➤ Cược: {luachonsn}\n"
                                                                                                  f"┣➤ Tiền cược: {tiencuoc_sn:,.0f}đ\n" 
                                                                                                  f"┣➤ Tiền thắng: {int(tiencuoc_sn * 1.9):,.0f}đ\n" 
                                                                                                  f"┣➤ Kết quả: {mat}\n"
                                                                                                  f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                                                                                  f"┣➤ Trạng thái: THẮNG\n"
                                                                                                  f"┗━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
        )                                                                                          
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=  f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                                                                                  f"┣➤ Phiên: {phien_sn}  ➤ Cược: {luachonsn}\n"
                                                                                                  f"┣➤ Tiền cược: {tiencuoc_sn:,.0f}đ\n" 
                                                                                                  f"┣➤ Tiền thắng: 0đ\n" 
                                                                                                  f"┣➤ Kết quả: {mat}\n"
                                                                                                  f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                                                                                  f"┣➤ Trạng thái: THUA\n"
                                                                                                  f"┗━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
        )
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Sn',
        'tiencuoc': tiencuoc_sn,
        'trangthai': trangthai,
    })            
    user_state['phien_sn'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_sn)

def choi_tiep_sn(message):
    choi_tiep_sn = message.text.lower()
    if choi_tiep_sn == "có":
        sap_ngua_main(message)
    elif choi_tiep_sn == "không":
        game_van_may(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_sn)   



# Chẵn lẻ
@bot.message_handler(func=lambda message: message.text == "☝️ Chẵn lẻ ✌️")
def chan_le(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_cl': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "☝️ Chào mừng bạn đến game chẵn lẻ ! ✌️\n\n🎮 LUẬT CHƠI :\nBot sẽ tung 1 xúc xắc với giá trị từ 1 đến 6\n➤ LẺ : 1 - 2 - 3 nút\n➤ CHẴN : 2 - 4 - 6 nút")
    chan_le_main(message)    

def chan_le_main(message):   
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_chan_le(message)

def nut_chan_le(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)  # Đặt row_width thành 2
    button0 = types.KeyboardButton(text="CHẴN")
    button1 = types.KeyboardButton(text="LẺ")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "Vui lòng chọn 1 trong 2 nút bên dưới 👇👇", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_chan_le)
    
def lua_chon_chan_le(message):
    user_id = str(message.chat.id)
    luachoncl = message.text.strip()
    if luachoncl == "CHẴN" or luachoncl == "LẺ":
        user_states[user_id]['luachon'] = luachoncl
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_cl)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn CHẨN hoặc LẺ")
        nut_chan_le(message)

def nhap_tien_cuoc_cl(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_cl = int(message.text.strip())
        if tiencuoc_cl > 0 and tiencuoc_cl <= sodu:
            user_state['sodu'] -= tiencuoc_cl
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_cl
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_cl(message, tiencuoc_cl)
        elif tiencuoc_cl > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_cl)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_cl)
            
def xu_ly_ket_qua_cl(message, tiencuoc_cl):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachoncl = user_state['luachon']
    phien_cl = user_state['phien_cl']
    sodu = user_state['sodu']
    xx = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    time.sleep(4)
    if (xx % 2 == 0 and luachoncl == "CHẴN") or (xx % 2 != 0 and luachoncl == "LẺ"):
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += int(tiencuoc_cl * 1.9)
        trangthai = "Thắng"
        
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_cl}  ➤ Cược: {luachoncl}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_cl:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: {int(tiencuoc_cl * 1.9):,.0f}đ\n" 
                                          f"┣➤ Số điểm: {xx} nút\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THẮNG\n"
                                          f"┗━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_cl}  ➤ Cược: {luachoncl}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_cl:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: 0đ\n" 
                                          f"┣➤ Số điểm: {xx} nút\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THUA\n"
                                          f"┗━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Cl',
        'tiencuoc': tiencuoc_cl,
        'trangthai': trangthai,
    })            
    user_state['phien_cl'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_cl)
    
def choi_tiep_cl(message):
    choi_tiep_cl = message.text.lower()
    if choi_tiep_cl == "có":
        chan_le_main(message)
    elif choi_tiep_cl == "không": 
        game_van_may(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_cl)        
        
        

# Bầu cua
@bot.message_handler(func=lambda message: message.text == "🦀 Bầu cua 🦀")
def bau_cua(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_bc': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🦀 Chào mừng bạn đến game bầu cua ! 🦀")
    bau_cua_main(message)

def bau_cua_main(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_bau_cua(message)

def nut_bau_cua(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2)
    button0 = types.KeyboardButton(text="🍐BẦU")
    button1 = types.KeyboardButton(text="🦀CUA")
    button2 = types.KeyboardButton(text="🦐TÔM")
    button3 = types.KeyboardButton(text="🐟CÁ")
    button4 = types.KeyboardButton(text="🐓GÀ")
    button5 = types.KeyboardButton(text="🐅HỔ")
    user_markup.add(button0, button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, "Vui lòng chọn 1 trong 6 nút bên dưới 👇👇", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_bau_cua)

def lua_chon_bau_cua(message):
    user_id = str(message.chat.id)
    luachonbc = message.text.strip()
    if luachonbc in ["🍐BẦU", "🦀CUA", "🦐TÔM", "🐟CÁ", "🐓GÀ", "🐅HỔ"]:
        user_states[user_id]['luachon'] = luachonbc
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_bc)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn 1 trong 6 vật để cược")
        nut_bau_cua(message)

def nhap_tien_cuoc_bc(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_bc = int(message.text.strip())
        if tiencuoc_bc > 0 and tiencuoc_bc <= sodu:
            user_state['sodu'] -= tiencuoc_bc
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_bc
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_bc(message, tiencuoc_bc)
        elif tiencuoc_bc > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_bc)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_bc)
        
def xu_ly_ket_qua_bc(message, tiencuoc_bc):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachonbc = user_state['luachon']
    phien_bc = user_state['phien_bc']
    sodu = user_state['sodu']
    baucua1 = random.choice(["🍐BẦU", "🦀CUA", "🦐TÔM", "🐟CÁ", "🐓GÀ", "🐅HỔ"])
    baucua2 = random.choice(["🍐BẦU", "🦀CUA", "🦐TÔM", "🐟CÁ", "🐓GÀ", "🐅HỔ"])
    baucua3 = random.choice(["🍐BẦU", "🦀CUA", "🦐TÔM", "🐟CÁ", "🐓GÀ", "🐅HỔ"])
    baucua_ketqua = baucua1 + " " + baucua2 + " " + baucua3
    sent_message = bot.send_message(message.chat.id, "⏱️Vui lòng chờ ...⏱️")
    time.sleep(1.5)
    for i in range(3):
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Đang chờ kết quả 🍐🦀🦐🐟🐓🐅")
        time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Đang chờ kết quả")
    if luachonbc in baucua_ketqua:
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += int(tiencuoc_bc * 1.9)
        trangthai = "Thắng"
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_bc}  ➤ Cược: {luachonbc}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_bc:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: {int(tiencuoc_bc * 1.9):,.0f}đ\n" 
                                          f"┣➤ Kết quả: {baucua_ketqua}\n"
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THẮNG\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_bc}  ➤ Cược: {luachonbc}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_bc:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: 0đ\n" 
                                          f"┣➤ Kết quả: {baucua_ketqua}\n"
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THUA\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Bc',
        'tiencuoc': tiencuoc_bc,
        'trangthai': trangthai,
    })            
    user_state['phien_bc'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_bc)
    
def choi_tiep_bc(message):
    choi_tiep_bc = message.text.lower()
    if choi_tiep_bc == "có":
        bau_cua_main(message)
    elif choi_tiep_bc == "không":
        game_xoc_xoc(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_bc)        


    
# Tài Xỉu 10 giây
@bot.message_handler(func=lambda message: message.text == "🎲 Tài xỉu 10s 🎲")
def tai_xiu_10(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_tx10': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🎲 Chào mừng bạn đến game tài xỉu 10s ! ⏱️")
    tai_xiu_10_main(message)

def tai_xiu_10_main(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_tai_xiu_10(message)

def nut_tai_xiu_10(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button0 = types.KeyboardButton(text="TÀI")
    button1 = types.KeyboardButton(text="XỈU")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "Vui lòng chọn 1 trong 2 nút bên dưới 👇👇", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_tai_xiu_10)

def lua_chon_tai_xiu_10(message):
    user_id = str(message.chat.id)
    luachontx10 = message.text.strip()
    if luachontx10 == "TÀI" or luachontx10 == "XỈU":
        user_states[user_id]['luachon'] = luachontx10
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_tx10)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn TÀI hoặc XỈU")
        nut_tai_xiu_10(message)

def nhap_tien_cuoc_tx10(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_tx10 = int(message.text.strip())
        if tiencuoc_tx10 > 0 and tiencuoc_tx10 <= sodu:
            user_state['sodu'] -= tiencuoc_tx10
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_tx10
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_tx10(message, tiencuoc_tx10)
        elif tiencuoc_tx10 > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_tx10)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_tx10)
        
def xu_ly_ket_qua_tx10(message, tiencuoc_tx10):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachontx10 = user_state['luachon']
    phien_tx10 = user_state['phien_tx10']
    sodu = user_state['sodu']
    sent_message = bot.send_message(message.chat.id, "⏱️Vui lòng chờ ...⏱️")
    time.sleep(0.5)
    countdown_text = "Vui lòng chờ {} giây".format("{}")
    for i in range(10, 0, -1):
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=countdown_text.format(i))
        time.sleep(1)
    bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Đợi kết quả nào !!!")
    xucxac_1 = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    xucxac_2 = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    xucxac_3 = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    tong_xucxac = xucxac_1 + xucxac_2 + xucxac_3
    time.sleep(4)
    ket_qua_tx = "TÀI" if tong_xucxac > 10 else "XỈU"
    if (tong_xucxac > 10 and luachontx10 == "TÀI") or (tong_xucxac <= 10 and luachontx10 == "XỈU"):
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += int(tiencuoc_tx10 * 1.9)
        trangthai = "Thắng"
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_tx10}  ➤ Cược: {luachontx10}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_tx10:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: {int(tiencuoc_tx10 * 1.9):,.0f}đ\n" 
                                          f"┣➤ Tổng điểm: {xucxac_1} + {xucxac_2} + {xucxac_3} = {tong_xucxac}\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THẮNG\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_tx10}  ➤ Cược: {luachontx10}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_tx10:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: 0đ\n" 
                                          f"┣➤ Tổng điểm: {xucxac_1} + {xucxac_2} + {xucxac_3} = {tong_xucxac}\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THUA\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Tx10s',
        'tiencuoc': tiencuoc_tx10,
        'trangthai': trangthai,
    })            
    user_state['phien_tx10'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_tx10)

def choi_tiep_tx10(message):
    choi_tiep_tx10 = message.text.lower()
    if choi_tiep_tx10 == "có":
        tai_xiu_10_main(message)
    elif choi_tiep_tx10 == "không":
        game_xuc_xac(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_tx10)        



# Tài Xỉu 1 xx
@bot.message_handler(func=lambda message: message.text == "🎲 Tài xỉu 1xx 🎲")
def tai_xiu_1xx(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_tx1xx': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🎲 Chào mừng bạn đến game tài xỉu 1xx ! 🎲")
    tai_xiu_1xx_main(message)

def tai_xiu_1xx_main(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_tai_xiu_1xx(message)

def nut_tai_xiu_1xx(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button0 = types.KeyboardButton(text="TÀI")
    button1 = types.KeyboardButton(text="XỈU")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "Vui lòng chọn 1 trong 2 nút bên dưới 👇👇", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_tai_xiu_1xx)

def lua_chon_tai_xiu_1xx(message):
    user_id = str(message.chat.id)
    luachontx1xx = message.text.strip()
    if luachontx1xx == "TÀI" or luachontx1xx == "XỈU":
        user_states[user_id]['luachon'] = luachontx1xx
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_tx1xx)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn TÀI hoặc XỈU")
        nut_tai_xiu_1xx(message)

def nhap_tien_cuoc_tx1xx(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_tx1xx = int(message.text.strip())
        if tiencuoc_tx1xx > 0 and tiencuoc_tx1xx <= sodu:
            user_state['sodu'] -= tiencuoc_tx1xx
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_tx1xx
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_tx1xx(message, tiencuoc_tx1xx)
        elif tiencuoc_tx1xx > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_tx1xx)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_tx1xx)
        
def xu_ly_ket_qua_tx1xx(message, tiencuoc_tx1xx):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachontx1xx = user_state['luachon']
    phien_tx1xx = user_state['phien_tx1xx']
    sodu = user_state['sodu']
    xx = bot.send_dice(message.chat.id, emoji='🎲').dice.value
    time.sleep(4)
    ket_qua_tx1xx = "TÀI" if xx > 3 else "XỈU"
    if (xx > 3 and luachontx1xx == "TÀI") or (xx < 4 and luachontx1xx == "XỈU"):
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += int(tiencuoc_tx1xx * 1.9)
        trangthai = "Thắng"
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_tx1xx}  ➤ Cược: {luachontx1xx}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_tx1xx:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: {int(tiencuoc_tx1xx * 1.9):,.0f}đ\n" 
                                          f"┣➤ Số điểm: {xx} nút\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THẮNG\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_tx1xx}  ➤ Cược: {luachontx1xx}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_tx1xx:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: 0đ\n" 
                                          f"┣➤ Số điểm: {xx} nút\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THUA\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Tx1xx',
        'tiencuoc': tiencuoc_tx1xx,
        'trangthai': trangthai,
    })            
    user_state['phien_tx1xx'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_tx1xx)

def choi_tiep_tx1xx(message):
    choi_tiep_tx1xx = message.text.lower()
    if choi_tiep_tx1xx == "có":
        tai_xiu_1xx_main(message)
    elif choi_tiep_tx1xx == "không":
        game_xuc_xac(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_tx1xx)        



# Quân vị
@bot.message_handler(func=lambda message: message.text == "🔴 Quân vị ⚪")
def chan_le(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_qv': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🔴 Chào mừng bạn đến game quân vị ! ⚪\n\n🎮 LUẬT CHƠI :\nBot sẽ xóc dĩa ra kết quả dựa trên 🔴 và ⚪\n➤ CHẴN gồm các nút:\n  ➤🔴🔴🔴🔴\n  ➤⚪⚪⚪⚪\n  ➤🔴🔴⚪⚪\n  ➤⚪⚪🔴🔴\n➤ LẺ gồm các nút :\n  ➤🔴🔴🔴⚪\n  ➤⚪⚪⚪🔴\n  ➤🔴⚪⚪⚪\n  ➤⚪🔴🔴🔴")
    quan_vi_main(message)

def quan_vi_main(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_quan_vi(message)

def nut_quan_vi(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button0 = types.KeyboardButton(text="CHẴN")
    button1 = types.KeyboardButton(text="LẺ")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "Vui lòng chọn 1 trong 2 nút bên dưới 👇👇", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_quan_vi)

def lua_chon_quan_vi(message):
    user_id = str(message.chat.id)
    luachonqv = message.text.strip()
    if luachonqv == "CHẴN" or luachonqv == "LẺ":
        user_states[user_id]['luachon'] = luachonqv
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_qv)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn CHẴN hoặc LẺ")
        nut_quan_vi(message)

def nhap_tien_cuoc_qv(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_qv = int(message.text.strip())
        if tiencuoc_qv > 0 and tiencuoc_qv <= sodu:
            user_state['sodu'] -= tiencuoc_qv
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_qv
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_qv(message, tiencuoc_qv)
        elif tiencuoc_qv > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_qv)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_qv)
        
def xu_ly_ket_qua_qv(message, tiencuoc_qv):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachonqv = user_state['luachon']
    phien_qv = user_state['phien_qv']
    sodu = user_state['sodu']
    ketqua_quanvi = random.choice([["🔴", "🔴", "🔴", "🔴"], ["⚪", "⚪", "⚪", "⚪"], ["🔴", "🔴", "⚪", "⚪"], ["⚪", "⚪", "🔴", "🔴"], ["🔴", "🔴", "🔴", "⚪"], ["⚪", "⚪", "⚪", "🔴"], ["🔴", "⚪", "⚪", "⚪"], ["⚪", "🔴", "🔴", "🔴"]])
    so_luong_do = ketqua_quanvi.count("🔴")
    so_luong_trang = ketqua_quanvi.count("⚪")
    ketqua_la_chan = (so_luong_do % 2 == 0)
    sent_message = bot.send_message(message.chat.id, "⏱️Vui lòng chờ ...⏱️")
    time.sleep(1.5)
    for i in range(3):
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Đang xóc dĩa 🔴⚪🔴⚪")
        time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Đang xóc dĩa")
    if (ketqua_la_chan and luachonqv == "CHẴN") or (not ketqua_la_chan and luachonqv == "LẺ"):
        user_state['thang'] += 1
        user_state['points'] += 20
        user_state['sodu'] += int(tiencuoc_qv * 1.9)
        trangthai = "Thắng"
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                                                                                f"┣➤ Phiên: {phien_qv}  ➤ Cược: {luachonqv}\n"
                                                                                                f"┣➤ Tiền cược: {tiencuoc_qv:,.0f}đ\n" 
                                                                                                f"┣➤ Tiền thắng: {int(tiencuoc_qv * 1.9):,.0f}đ\n" 
                                                                                                f"┣➤ Mở bát: {''.join(ketqua_quanvi)}\n" 
                                                                                                f"┣➤ Số điểm: {so_luong_do} đỏ, {so_luong_trang} trắng\n" 
                                                                                                f"┣➤ Kết quả: {luachonqv}\n"
                                                                                                f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                                                                                f"┣➤ Trạng thái: THẮNG\n"
                                                                                                f"┗━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        ketqua_text = "CHẴN" if ketqua_la_chan else "LẺ"
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                                                                                f"┣➤ Phiên: {phien_qv}  ➤ Cược: {luachonqv}\n"
                                                                                                f"┣➤ Tiền cược: {tiencuoc_qv:,.0f}đ\n" 
                                                                                                f"┣➤ Tiền thắng: 0đ\n" 
                                                                                                f"┣➤ Mở bát: {''.join(ketqua_quanvi)}\n" 
                                                                                                f"┣➤ Số điểm: {so_luong_do} đỏ, {so_luong_trang} trắng\n" 
                                                                                                f"┣➤ Kết quả: {ketqua_text}\n"
                                                                                                f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                                                                                f"┣➤ Trạng thái: THUA\n"
                                                                                                f"┗━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )               
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Qv',
        'tiencuoc': tiencuoc_qv,
        'trangthai': trangthai,
    })                          
    user_state['phien_qv'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_qv)

def choi_tiep_qv(message):
    choi_tiep_qv = message.text.lower()
    if choi_tiep_qv == "có":
        quan_vi_main(message)
    elif choi_tiep_qv == "không":
        game_xoc_xoc(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_qv)



# Ném xúc xắc
@bot.message_handler(func=lambda message: message.text == "🎲 Ném xúc xắc 🎲")
def nem_xuc_xac(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_nxx': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🎲 Chào mừng bạn đến game ném xúc xắc ! 🎲\n\n🎮 LUẬT CHƠI :\nBạn sẽ tung 1 xúc xắc sau đó đến lượt bot rồi SO SÁNH\n➤ BOT > BẠN : bot thắng\n➤ BOT < BẠN : bạn thắng\n➤ BOT = BẠN : hoà") 
    nem_xuc_xac_main(message)
    
def nem_xuc_xac_main(message):    
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_nxx)

def nhap_tien_cuoc_nxx(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_nxx = int(message.text.strip())
        if tiencuoc_nxx > 0 and tiencuoc_nxx <= sodu:
            user_state['sodu'] -= tiencuoc_nxx
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_nxx
            user_state['tiencuoc_nxx'] = tiencuoc_nxx  # Lưu tiền cược vào state
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            nut_nem_xuc_xac(message)
        elif tiencuoc_nxx > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_nxx)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_nxx)

def nut_nem_xuc_xac(message):
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = types.KeyboardButton(text="🎲")
    user_markup.add(button0)
    bot.send_message(message.chat.id, "🎲 Mời bạn ném xúc xắc 🎲", reply_markup=user_markup)
    bot.register_next_step_handler(message, diem_xx_nguoi_choi)

def diem_xx_nguoi_choi(message):
    if message.dice and message.dice.value:
        user_id = str(message.chat.id)
        user_states[user_id]['xx_nguoi_choi'] = message.dice.value
        xu_ly_ket_qua_nxx(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng ném xúc xắc bằng cách bấm vào nút 🎲")
        nut_nem_xuc_xac(message)

def xu_ly_ket_qua_nxx(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    phien_nxx = user_state['phien_nxx']
    sodu = user_state['sodu']
    xx_nguoi_choi = user_state['xx_nguoi_choi']
    tiencuoc_nxx = user_state['tiencuoc_nxx']  # Lấy tiền cược từ state
    xx_bot_message = bot.send_dice(message.chat.id, emoji='🎲')
    xx_bot = xx_bot_message.dice.value
    time.sleep(4)
    if xx_nguoi_choi > xx_bot:
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += tiencuoc_nxx * 1.9
        result_message = "THẮNG"
        trangthai = "Thắng"
        tienthang = tiencuoc_nxx * 1.9
    elif xx_nguoi_choi < xx_bot:
        user_state['thua'] += 1
        trangthai = "Thua"
        tienthang = tiencuoc_nxx * 0
        result_message = f"THUA"
    else:
        user_state['points'] += 10
        user_state['sodu'] += tiencuoc_nxx  
        user_state['points'] += 1
        trangthai = "Hoà"
        result_message = f"HOÀ"
        tienthang = tiencuoc_nxx * 1
    bot.send_message(message.chat.id,     f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_nxx} Ném xúc xắc\n"
                                          f"┣➤ Bạn ném được: {xx_nguoi_choi} điểm\n" 
                                          f"┣➤ Bot ném được: {xx_bot} điểm\n" 
                                          f"┣➤ Tiền cược: {tiencuoc_nxx:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: {tienthang:,.0f}đ\n"
                                          f"┣➤ Trạng thái: {result_message}\n"
                                          f"┣➤ Số dư hiện tại: {user_state['sodu']:,.0f}đ\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
    )                        
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Nxx',
        'tiencuoc': tiencuoc_nxx,
        'trangthai': trangthai,
    })                     
    user_state['phien_nxx'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_nxx)

def choi_tiep_nxx(message):
    choi_tiep_nxx = message.text.lower()
    if choi_tiep_nxx == "có":
        nem_xuc_xac_main(message)
    elif choi_tiep_nxx == "không":
        game_xuc_xac(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_nxx)        
     
     
     
# Bowling-TX     
@bot.message_handler(func=lambda message: message.text == "🎳 Bowling-TX 🎳")
def bltx(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_bltx': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🎳 Chào mừng bạn đến game bowling_tx ! 🎳")
    bltx_main(message)

def bltx_main(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_bltx(message)

def nut_bltx(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button0 = types.KeyboardButton(text="TÀI")
    button1 = types.KeyboardButton(text="XỈU")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "Vui lòng chọn 1 trong 2 nút bên dưới 👇👇", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_bltx)

def lua_chon_bltx(message):
    user_id = str(message.chat.id)
    luachonbltx = message.text.strip()
    if luachonbltx in ["TÀI", "XỈU"]:
        user_states[user_id]['luachon'] = luachonbltx
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_bltx)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn TÀI hoặc XỈU")
        nut_bltx(message)

def nhap_tien_cuoc_bltx(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_bltx = int(message.text.strip())
        if tiencuoc_bltx > 0 and tiencuoc_bltx <= sodu:
            user_state['sodu'] -= tiencuoc_bltx
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_bltx
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_bltx(message, tiencuoc_bltx)
        elif tiencuoc_bltx > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_bltx)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_bltx)
        
def xu_ly_ket_qua_bltx(message, tiencuoc_bltx):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachonbltx = user_state['luachon']
    phien_bltx = user_state['phien_bltx']
    sodu = user_state['sodu']
    bl1 = bot.send_dice(message.chat.id, emoji='🎳').dice.value
    bl2 = bot.send_dice(message.chat.id, emoji='🎳').dice.value
    bl3 = bot.send_dice(message.chat.id, emoji='🎳').dice.value
    tong_bl = bl1 + bl2 + bl3 
    time.sleep(4)
    ket_qua_bltx = "TÀI" if tong_bl > 10 else "XỈU"
    if (tong_bl > 10 and luachonbltx == "TÀI") or (tong_bl < 10 and luachonbltx == "XỈU"):
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += int(tiencuoc_bltx * 1.9)
        trangthai = "Thắng"
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_bltx}  ➤ Cược: {luachonbltx}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_bltx:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: {int(tiencuoc_bltx * 1.9):,.0f}đ\n"
                                          f"┣➤ Tổng điểm: {bl1} + {bl2} + {bl3} = {tong_bl}\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THẮNG\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_bltx}  ➤ Cược: {luachonbltx}\n"
                                          f"┣➤ Tiền cược: {tiencuoc_bltx:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: 0đ\n"
                                          f"┣➤ Tổng điểm: {bl1} + {bl2} + {bl3} = {tong_bl}\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THUA\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )              
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Bltx',
        'tiencuoc': tiencuoc_bltx,
        'trangthai': trangthai,
    })                                    
    user_state['phien_bltx'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_bltx)

def choi_tiep_bltx(message):
    choi_tiep_bltx = message.text.lower()
    if choi_tiep_bltx == "có":
        bltx_main(message)
    elif choi_tiep_bltx == "không":
        game_bowling(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_bltx)        
        
         
         
# Bowling-CL
@bot.message_handler(func=lambda message: message.text == "🎳 Bowling-CL 🎳")
def bl_chan_le(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_bltx': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🎳 Chào mừng bạn đến game Bowling-CL 🎳\n\n🎮 LUẬT CHƠI :\nBot sẽ tung 1 xúc xắc với giá trị từ 1 đến 6\n➤ LẺ : 1 - 2 - 3 nút\n➤ CHẴN : 2 - 4 - 6 nút")
    bl_chan_le_main(message)    
    
def bl_chan_le_main(message):   
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_bl_chan_le(message)

def nut_bl_chan_le(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)  
    button0 = types.KeyboardButton(text="CHẴN")
    button1 = types.KeyboardButton(text="LẺ")
    user_markup.add(button0, button1)
    bot.send_message(message.chat.id, "Vui lòng chọn 1 trong 2 nút bên dưới 👇👇", reply_markup=user_markup)
    bot.register_next_step_handler(message, lua_chon_bl_chan_le)
    
def lua_chon_bl_chan_le(message):
    user_id = str(message.chat.id)
    luachonblcl = message.text.strip()
    if luachonblcl == "CHẴN" or luachonblcl == "LẺ":
        user_states[user_id]['luachon'] = luachonblcl
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_blcl)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn CHẴN hoặc LẺ")
        nut_bl_chan_le(message) 

def nhap_tien_cuoc_blcl(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_blcl = int(message.text.strip())
        if tiencuoc_blcl > 0 and tiencuoc_blcl <= sodu:
            user_state['sodu'] -= tiencuoc_blcl
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_blcl
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            xu_ly_ket_qua_blcl(message, tiencuoc_blcl)
        elif tiencuoc_blcl > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_bltx)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_blcl)
            
def xu_ly_ket_qua_blcl(message, tiencuoc_blcl):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    luachonblcl = user_state['luachon']
    phien_blcl = user_state['phien_blcl']
    sodu = user_state['sodu']
    bl = bot.send_dice(message.chat.id, emoji='🎳').dice.value 
    time.sleep(4)
    if (bl % 2 == 0 and luachonblcl == "CHẴN") or (bl % 2 != 0 and luachonblcl == "LẺ"):
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += int(tiencuoc_blcl * 1.9)
        trangthai = "Thắng"
        # Kiểm tra và cập nhật level
        current_points = user_state['points']
        current_level = user_state['level']
        for i in range(current_level, len(level_thresholds)):
            if current_points >= level_thresholds[i]:
                user_state['level'] = i + 1  # Cập nhật level sau khi đạt ngưỡng
            else:
                break
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_blcl}  ➤ Cược: {luachonblcl}\n"
                                          f"┣➤ Số tiền cược: {tiencuoc_blcl:,.0f}đ\n" 
                                          f"┣➤ Số tiền thắng: {int(tiencuoc_blcl * 1.9):,.0f}đ\n"
                                          f"┣➤ Số Bowling ném được: {bl}\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THẮNG\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    else:
        user_state['thua'] += 1
        trangthai = "Thua"
        luachonblcl1 = "LẺ" if luachonblcl == "CHẴN" else "CHẴN"
        bot.send_message(message.chat.id, f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_blcl}  ➤ Cược: {luachonblcl}\n"
                                          f"┣➤ Số tiền cược: {tiencuoc_blcl:,.0f}đ\n" 
                                          f"┣➤ Số tiền thắng: 0đ\n"
                                          f"┣➤ Số Bowling ném được: {bl}\n" 
                                          f"┣➤ Số dư mới: {user_state['sodu']:,.0f}đ\n"
                                          f"┣➤ Trạng thái: THUA\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
         )                                 
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Blcl',
        'tiencuoc': tiencuoc_blcl,
        'trangthai': trangthai,
    })                                
    user_state['phien_blcl'] += 1
    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_blcl)
    
def choi_tiep_blcl(message):
    choi_tiep_blcl = message.text.lower()
    if choi_tiep_blcl == "có":
        bl_chan_le_main(message)
    elif choi_tiep_blcl == "không": 
        game_bowling(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_blcl)              
        
        
        
# Ném bowling
@bot.message_handler(func=lambda message: message.text == "🎳 Ném Bowling 🎳")
def nem_xuc_xac(message):
    user_id = str(message.chat.id)
    if user_id not in user_states:
        user_states[user_id] = {'phien_nbl': 1, 'thang': 0, 'thua': 0, 'points': 0, 'level': 1, 'sodu': 0}
    #bot.send_message(message.chat.id, "🎳 Chào mừng bạn đến game ném bowling ! 🎳\n\n🎮 LUẬT CHƠI :\nBạn sẽ tung 1 xúc xắc sau đó đến lượt bot rồi SO SÁNH\n➤ BOT > BẠN : bot thắng\n➤ BOT < BẠN : bạn thắng\n➤ BOT = BẠN : hoà") 
    nem_bowling_main(message)
    
def nem_bowling_main(message):    
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    if user_state['sodu'] < 1000:
        khong_du_sodu(message)
    else:    
        nut_nhap_tien_cuoc(message)
        bot.register_next_step_handler(message, nhap_tien_cuoc_nbl)

def nhap_tien_cuoc_nbl(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    sodu = user_state['sodu']
    try:
        tiencuoc_nbl = int(message.text.strip())
        if tiencuoc_nbl > 0 and tiencuoc_nbl <= sodu:
            user_state['sodu'] -= tiencuoc_nbl
            user_tongcuoc[user_id]['tongcuoc'] += tiencuoc_nbl
            user_state['tiencuoc_nbl'] = tiencuoc_nbl  # Lưu tiền cược vào state
            bot.send_message(message.chat.id, f"➤ Số dư sau khi cược {user_state['sodu']:,.0f}đ")
            nut_nem_bowling(message)
        elif tiencuoc_nbl > sodu:
            bot.send_message(message.chat.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền")
        else:
            bot.send_message(message.chat.id, "❌ Tiền cược không hợp lệ. Vui lòng nhập lại")
            bot.register_next_step_handler(message, nhap_tien_cuoc_nbl)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Không nhập chữ. Vui lòng nhập lại")
        bot.register_next_step_handler(message, nhap_tien_cuoc_nbl)

def nut_nem_bowling(message):
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = types.KeyboardButton(text="🎳")
    user_markup.add(button0)
    bot.send_message(message.chat.id, "🎳 Mời bạn ném bowling 🎳", reply_markup=user_markup)
    bot.register_next_step_handler(message, diem_bl_nguoi_choi)

def diem_bl_nguoi_choi(message):
    if message.dice and message.dice.value:
        user_id = str(message.chat.id)
        user_states[user_id]['bl_nguoi_choi'] = message.dice.value
        xu_ly_ket_qua_nbl(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng ném bowling bằng cách bấm vào nút 🎳")
        nut_nem_bowling(message)

def xu_ly_ket_qua_nbl(message):
    user_id = str(message.chat.id)
    user_state = user_states[user_id]
    phien_nbl = user_state['phien_nbl']
    sodu = user_state['sodu']
    bl_nguoi_choi = user_state['bl_nguoi_choi']
    tiencuoc_nbl = user_state['tiencuoc_nbl']  # Lấy tiền cược từ state
    bl_bot_message = bot.send_dice(message.chat.id, emoji='🎳')
    bl_bot = bl_bot_message.dice.value
    time.sleep(4)
    if bl_nguoi_choi > bl_bot:
        user_state['thang'] += 1
        user_state['points'] += 2
        user_state['sodu'] += tiencuoc_nbl * 1.9
        result_message = "THẮNG"
        trangthai = "Thắng"
        tienthang = tiencuoc_nbl * 1.9
    elif bl_nguoi_choi < bl_bot:
        user_state['thua'] += 1
        trangthai = "Thua"
        tienthang = tiencuoc_nbl * 0
        result_message = f"THUA"
    else:
        user_state['points'] += 1
        user_state['sodu'] += tiencuoc_nbl  
        user_state['points'] += 1
        trangthai = "Hoà"
        result_message = f"HOÀ"
        tienthang = tiencuoc_nbl * 1
    bot.send_message(message.chat.id,     f"┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                                          f"┣➤ Phiên: {phien_nbl} Ném bowling\n"
                                          f"┣➤ Bạn ném được: {bl_nguoi_choi} điểm\n" 
                                          f"┣➤ Bot ném được: {bl_bot} điểm\n" 
                                          f"┣➤ Tiền cược: {tiencuoc_nbl:,.0f}đ\n" 
                                          f"┣➤ Tiền thắng: {tienthang:,.0f}đ\n"
                                          f"┣➤ Trạng thái: {result_message}\n"
                                          f"┣➤ Số dư hiện tại: {user_state['sodu']:,.0f}đ\n"
                                          f"┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━"
    )                        
    # update lịch sử chơi người dùng        
    user_lschoi[user_id].append({
        'thoigian': thoigian + " " + ngay,
        'game': 'Nbl',
        'tiencuoc': tiencuoc_nbl,
        'trangthai': trangthai,
    })                     
    user_state['phien_nbl'] += 1

    co_khong(message)
    bot.register_next_step_handler(message, choi_tiep_nbl)

def choi_tiep_nbl(message):
    choi_tiep_nbl = message.text.lower()
    if choi_tiep_nbl == "có":
        nem_bowling_main(message)
    elif choi_tiep_nbl == "không":
        game_bowling(message)
    else:
        bot.send_message(message.chat.id, "👉 Vui lòng chọn Có hoặc Không")
        bot.register_next_step_handler(message, choi_tiep_nbl) 
        
        
        
# Timestick
"""def get_timeticks(self):
        
        # Lấy thời gian hiện tại
        current_time = int(time.time())

        # Chuyển đổi số giây thành số Timeticks
        timeticks = current_time * 1

        # Lấy 10 số cuối cùng của số Timeticks
        random_timeticks = str(timeticks)[-10:]

        return random_timeticks"""
        
#######################################################################

# XỬ LÝ CÁC NÚT Ở PHẦN TÀI KHOẢN
@bot.message_handler(commands=['tk'])           
@bot.message_handler(func=lambda message: message.text == "👤 Tài khoản")     
def taikhoan(message):
    user_id = str(message.chat.id)
    user_name = message.from_user.username
    if not user_name :
        full_name = message.from_user.first_name + " " + message.from_user.last_name
    else:    
        full_name = user_name
    user_data = user_states[user_id]
    tongthang = user_data['thang']
    tongthua = user_data['thua']
    points = user_data['points']
    level = user_data['level']
    sodu = int(user_data['sodu'])    
    
    taikhoan = (
        f"👤 Tên tài khoản : `{full_name}`\n"
        f"💳 ID tài khoản : `{user_id}`\n"
        f"💰 Số dư : {sodu:,.0f} đ\n"
        f"🏆 Số game thắng : {tongthang}\n"
        f"🛟 Số game thua : {tongthua}\n"
        f"👑 Level : {level}/15\n"
        f"🚀 Tiến trình điểm level : {points} điểm"
    )    
    nap_button = telebot.types.InlineKeyboardButton("💸 Nạp tiền", callback_data="nap")
    rut_button = telebot.types.InlineKeyboardButton("💸 Rút tiền", callback_data="rut")
    mcode_button = telebot.types.InlineKeyboardButton("🎁 Mua Giftcode", callback_data="muagiftcode")
    code_button = telebot.types.InlineKeyboardButton("🎁 Nhập Gifcode", callback_data="nhapgiftcode")
    ct_button = telebot.types.InlineKeyboardButton("💸 Chuyển tiền", callback_data="chuyen")
    lschoi_button = telebot.types.InlineKeyboardButton("🎮 Lịch sử chơi", callback_data="lschoi")
    xh_button = telebot.types.InlineKeyboardButton("📉 Đổi điểm vip", callback_data="doidiemvip")
    lsnap_button = telebot.types.InlineKeyboardButton("📈 Lịch sử nạp", callback_data="lsnap")
    lsrut_button = telebot.types.InlineKeyboardButton("📉Lịch sử rút", callback_data="lsrut")
    tc_button = telebot.types.InlineKeyboardButton("📝 Tóm tắt lịch sử cược đã chơi", callback_data="tongcuoc")
    qua_button = telebot.types.InlineKeyboardButton("🎁 Quà tặng cho tân thủ !!! 🎁", callback_data="qua")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(nap_button)
    keyboard.row(rut_button, ct_button)
    keyboard.row(lsnap_button, lsrut_button)
    keyboard.row(xh_button, lschoi_button)
    keyboard.row(code_button, tc_button)
    keyboard.row(mcode_button)
    keyboard.row(qua_button)
    bot.send_message(message.chat.id, taikhoan, parse_mode='Markdown',reply_markup=keyboard)

def khong_du_sodu(message):
    markup = InlineKeyboardMarkup()
    button0 = InlineKeyboardButton(text="💸 Nạp thêm tiền", callback_data ="nap")
    markup.add(button0)
    bot.send_message(message.chat.id, "Số dư bạn không đủ, mời bạn nạp thêm tiền", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query_game(call):
    if call.data == "lschoi":
        xem_lich_su_choi(call.message)
    elif call.data == "lsnap":
        xem_lich_su_nap(call.message)
    elif call.data == "lsrut":
        xem_lich_su_rut(call.message)
    elif call.data == "tongcuoc":
        xem_tong_cuoc(call.message)
    elif call.data == "xephang":
        xep_hang(call.message)
    elif call.data == "nap":
        nap_tien(call.message)
    elif call.data == "rut":
        rut_tien(call.message)
    elif call.data == "chuyen":
        chuyen_tien(call)
    elif call.data == "napmomo":
        nap_tien_momo(call)
    elif call.data == "napbank":
        nap_tien_bank(call)
    elif call.data == "rutmomo":
        rut_tien_momo(call)
    elif call.data == "rutbank":
        rut_tien_ngan_hang(call)
    elif call.data == "qua":
        qua_tan_thu(call.message)
    elif call.data == "muagiftcode":
        noi_dung_mua_giftcode(call.message)
    elif call.data == "nhapgiftcode":
        noi_dung_nhap_gift_code(call.message)    
    elif call.data == "doidiemvip":
        doi_diem_vip(call.message)    



@bot.message_handler(func=lambda message: message.text == "🤝 Bạn bè")    
def gioi_thieu(message):
    bot.send_message(message.chat.id, "🤝Giới Thiệu :\nĐây là bot game bài telegram tự động không bị can thiệp kết quả trên telegram🤝\n🎮 Game xanh chín nói không với chỉnh sửa kết quả\n🎮 Cách chơi đơn giản, tiện lợi 🎁\n🎮 Hoàn toàn miễn phí 🎉\n\n👉 Hãy chia sẽ bot để có một cộng đồng người chơi lớn mạnh🤙\nLink Bot : https://t.me/Chinhcoder_bot",disable_web_page_preview=True)
    
    
    
@bot.message_handler(func=lambda message: message.text == "💬 Trung tâm hỗ trợ")
def nut_ho_tro_nguoi_dung(message):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="🎮 Góp ý game 🎮", url="https://t.me/TruongChinh304")
    button2 = InlineKeyboardButton(text="🎮 Hỗ trợ game 🎮", url="https://t.me/TruongChinh304")
    button3 = InlineKeyboardButton(text="🎮 Hỗ trợ tân thủ 🎮", url="https://t.me/TruongChinh304")
    button4 = InlineKeyboardButton(text="🎮 Hỗ trợ nạp rút 🎮", url="https://t.me/TruongChinh304")
    button5 = InlineKeyboardButton(text="🎮 LIÊN HỆ ADMIN VẤN ĐỀ KHÁC 🎮", url="https://t.me/TruongChinh304")
    markup.add(button1, button2)
    markup.add(button3, button4)
    markup.add(button5)
    photo_path = "/sdcard/download/fpt/bothotro.jpg"
    with open(photo_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Chọn danh mục hỗ trợ theo menu phía dưới 👇", reply_markup=markup)



@bot.message_handler(func=lambda message: message.text == "❔Thông tin❔")     
def thongtin(message):
     bot.send_message(message.chat.id, "❔ Bot này là gì ❔\n\n➤Với sự giải trí cuả bot Telegram này bạn sẽ được giải trí bất cứ game nào mà không cần mất phí.\n\n❔ Bot hoạt động như thế nào ?\n\n➤Mọi thứ rất đơn giản, bạn chỉ cần chọn nút 🎮 Danh sách game, Sau đó chọn thể loại game mà bạn muốn chơi tiếp theo chọn game mà bạn muốn chơi rồi tiếp tục theo từng bước với các nút đã được thiết lập sẵn trên bot\n\n➤Những kết quả trên đây hoàn toàn là random không can thiệp kết quả\n\nLưu ý: Đây là phiên bản mới nhất cuả bot MiniGames🎮, nếu có liên hệ để đóng góp xin đừng ngần ngại nhắn tin cho \n\n➤Admin : @TruongChinh304\n\n➤Cuối cùng Admin chúc các bạn chơi game vui vẻ 🎉.", disable_web_page_preview=True)  
     
     
     
#Quay lại all
@bot.message_handler(func=lambda message: message.text == "⬅️ Quay lại")  
def quay_lai(message):
    handle_nut_main(message) 
    
    
    
@bot.message_handler(func=lambda message: message.text == "🧑‍💻 Vào nhóm")
def vao_nhom(message):
    markup = InlineKeyboardMarkup()
    button0 = InlineKeyboardButton(text="🎮 Group Minigames 🎮", url="https://t.me/+b-27lb0mxoZmY2I1")
    markup.add(button0)
    bot.send_message(message.chat.id, "Nhóm phát triển game 👇",reply_markup=markup)



@bot.message_handler(func=lambda message: message.text == "👥 Giới thiệu bạn bè")
def nhiemvu(message):
    user_id = str(message.chat.id)
    bot.send_message(message.chat.id, f"🎮 Giới Thiệu: Đây là bot Minigames tự động không bị can thiệp kết quả trên telegram 🎲\n\n👉 Hãy chia sẽ bot để có một cộng đồng người chơi lớn mạnh\n\n👉 Link mời bạn bè cuả bạn: `https://t.me/Chinhcoder_bot?start={user_id}`",parse_mode='Markdown')
    
    
    
####################### NÚT NẠP - RÚT - CHUYỂN HƯỚNG DẪN #################    
def nap_tien(message):
    markup = InlineKeyboardMarkup()
    button0 = InlineKeyboardButton(text="Momo", callback_data="napmomo")
    button1 = InlineKeyboardButton(text="Bank", callback_data="napbank")
    markup.add(button0, button1)
    bot.send_message(message.chat.id, "Lựa chọn phương thức nạp 💸", reply_markup=markup)

def rut_tien(message):
    markup = InlineKeyboardMarkup()
    button0 = InlineKeyboardButton(text="Momo", callback_data="rutmomo")
    button1 = InlineKeyboardButton(text="Bank", callback_data="rutbank")
    markup.add(button0, button1)
    bot.send_message(message.chat.id, "Lựa chọn phương thức rút 💸", reply_markup=markup)
########################################################################    
        
# Nội dung nạp momo
@bot.callback_query_handler(func=lambda call: call.data == "napmomo")
def nap_tien_momo(call):
    user_id = str(call.from_user.id) # Lấy user_id từ callback query
    sdt = "0776186410"  # Số điện thoại admin 
    noi_dung_nap_momo = (
        "➡️ Chuyển tiền qua momo theo thông tin sau:\n"
        f"🏦 Số điện thoại: `{sdt}` <- nhấp vào để copy\n"
        "💳 Tên Tài Khoản: Nguyễn Trường Chinh\n"
        f"🔖 Nội dung : `nap {user_id}` <- nhấp vào để copy\n\n"
        "⚠️ Lưu ý:\n\n"
        "✅ Nạp từ 10.000 trở lên. Nạp dưới 10.000 không được hỗ trợ\n"
        "✅ Nội dung phải CHÍNH XÁC. Nếu không sẽ không được nạp.\n"
        "⚠️ NỘI DUNG chuyển khoản giữa các lần nạp có thể KHÁC NHAU.\n"
        "⛔ KHÔNG sử dụng nội dung cũ cho lần nạp tiếp theo.\n"
        "⭕ Vui Lòng Đọc kỹ Trước Khi Giao Dịch.\n"
        "❌ Mọi Vấn Đề Sai Sót Sẽ Không Được Giải Quyết."
        )
    noi_dung_qr_nap_momo = f"Tên TK: Nguyễn Trường Chinh   Momo: {sdt}   Nạp đến ID: {user_id}"
    image = qrcode.make(noi_dung_qr_nap_momo)
    image.save("qrcode.png")
    bot.send_photo(call.message.chat.id, open('qrcode.png', 'rb'), caption=noi_dung_nap_momo, parse_mode='Markdown')


# Nội dung nạp bank
@bot.callback_query_handler(func=lambda call: call.data == "napbank") 
def nap_tien_bank(call):   
    stk = "00230042006"  # Số tài khoản admin
    user_id = str(call.from_user.id) # Lấy user_id từ callback query
    noi_dung_nap_bank = (
        "➡️ Chuyển tiền qua ngân hàng theo thông tin sau:\n"
        "🏦 Ngân hàng: MB BANK\n"
        f"💳 Số Tài Khoản: `{stk}` 👈 NHẤP VÀO SỐ TK ĐỂ COPY\n"
        "💳 Tên Tài Khoản: NGUYEN TRUONG CHINH\n"
        f"🔖 Nội dung : `nap {user_id}` 👈 NHẤP VÀO ĐÂY ĐỂ COPY\n\n"
        "⚠️ Lưu ý:\n\n"
        "✅ Nạp từ 10.000 trở lên. Nạp dưới 10.000 không được hỗ trợ\n"
        "✅ Nội dung phải CHÍNH XÁC. Nếu không sẽ không được nạp.\n"
        "⚠️ NỘI DUNG chuyển khoản giữa các lần nạp có thể KHÁC NHAU.\n"
        "⛔ KHÔNG sử dụng nội dung cũ cho lần nạp tiếp theo.\n"
        "⭕ Vui Lòng Đọc kỹ Trước Khi Giao Dịch.\n"
        "❌ Mọi Vấn Đề Sai Sót Sẽ Không Được Giải Quyết."
        )
    noi_dung_qr_nap_bank = f"Tên TK: NGUYEN TRUONG CHINH   Số tài khoản: {stk}   Nạp đến ID: {user_id}"
    image = qrcode.make(noi_dung_qr_nap_bank)
    image.save("qrcode.png")
    bot.send_photo(call.message.chat.id, open('qrcode.png', 'rb'), caption=noi_dung_nap_bank, parse_mode='Markdown')



# Nội dung rút momo
@bot.callback_query_handler(func=lambda call: call.data == "rutmomo")
def rut_tien_momo(call):
    noi_dung_rut_tien_momo = (
"""💸 Vui lòng thực hiện theo hướng dẫn sau:

/rutmomo [dấu cách] SĐT [dấu cách] Số tiền muốn rút [dấu cách] Nội dung (có thể để trống)

➡️ VD:   /rutmomo 0989122472 50000 Chi tiêu

⚠️ Lưu ý: ❌ Không hỗ trợ hoàn tiền nếu bạn nhập sai thông tin SĐT. 
❗️ Phí rút tiền: 2.000đ cho các giao dịch dưới 50.000đ. ( RÚT TỪ 50.000đ TRỞ LÊN KHÔNG MẤT PHÍ RÚT)"""
)    
    bot.send_message(call.message.chat.id, noi_dung_rut_tien_momo)
    
    

# Nội dung rút bank    
@bot.callback_query_handler(func=lambda call: call.data == "rutbank")
def rut_tien_ngan_hang(call):
    noi_dung_rut_ngan_hang = (
        """🏦 Vui lòng thực hiện theo hướng dẫn sau:

👉 /rutbank [dấu cách] Số tiền muốn rút [dấu cách]  Mã ngân hàng [dấu cách] Số tài khoản [dấu cách] Tên chủ tài khoản
👉 VD:  Muốn rút 100k ở TK số 00230042006 tại Ngân hàng MB Bank. Thực hiện theo cú pháp sau:

/rutbank 100000 MBB 00230042006 NGUYEN TRUONG CHINH

⚠️ Lưu ý: Không hỗ trợ hoàn tiền nếu bạn nhập sai thông tin Tài khoản.

TÊN NGÂN HÀNG - MÃ NGÂN HÀNG
📌 Vietcombank => VCB
📌 BIDV => BIDV
📌 Vietinbank => VTB
📌 Techcombank => TCB
📌 MB Bank => MBB
📌 Agribank => AGR
📌 TienPhong Bank => TPB
📌 SHB bank => SHB
📌 ACB => ACB
📌 Maritime Bank => MSB
📌 VIB => VIB
📌 Sacombank => STB
📌 VP Bank => VPB
📌 SeaBank => SAB
📌 Shinhan bank Việt Nam => SHIB
📌 Eximbank => EIB
📌 KienLong Bank => KLB
📌 Dong A Bank => DAB
📌 HD Bank => HDB
📌 LienVietPostBank => LVPB
📌 VietBank => VBB
📌 ABBANK => ABB
📌 PG Bank => PGB
📌 PVComBank => PVB
📌 Bac A Bank => BAB
📌 Sai Gon Commercial Bank => SCB
📌 BanVietBank => VCCB
📌 Saigonbank => SGB
📌 Bao Viet Bank => BVB
📌 Orient Commercial Bank => OCB
📌 OCEANBANK - NH TMCP DAI DUONG => OJB"""
    )    
    bot.send_message(call.message.chat.id, noi_dung_rut_ngan_hang)    


# Nội dung chuyển tiền 
@bot.callback_query_handler(func=lambda call: call.data == "chuyen")
def chuyen_tien(call):
    noi_dung_chuyen_tien = (
        """💸 Vui lòng thực hiện theo hướng dẫn sau:

chuyen [dấu cách] ID nhận tiền [dấu cách] Số tiền muốn chuyển [dấu cách] Nội dung (có thể để trống)

➡️ Vd:  /chuyen 216789354 50000 Lì xì

⚡️⚡️ Phí chuyển tiền là 20% được trừ vào tài khoản người chuyển  ⚡️⚡️"""
    )    
    bot.send_message(call.message.chat.id, noi_dung_chuyen_tien)
    

# Nội dung đổi điểm vip    
@bot.callback_query_handler(func=lambda call: call.data == "doidiemvip")   
def doi_diem_vip(message):
    noi_dung_doi_diem_vip = (
        """Với mỗi lần thắng. Quý khách sẽ được cộng thêm 2 điểm VIP.  Điểm này sẽ dùng để xét tăng cấp Level và để đổi thưởng.

📌 ĐIỂM YÊU CẦU ĐỂ ĐẠT CẤP VIP
Vip 1: 0
Vip 2: 50
Vip 3: 100
Vip 4: 150
Vip 5: 200
Vip 6: 250
Vip 7: 300
Vip 8: 350
Vip 9: 400
Vip 10: 450
Vip 11: 500
Vip 12: 550
Vip 13: 600
Vip 14: 650
Vip 15: 700


💎 TỈ LỆ QUY ĐỔI ĐIỂM
Hãy tích điểm và quy đổi chúng thành tiền mặt với tỉ lệ cực kỳ hấp dẫn:
➡ 1 điểm vip = 100đ (VNĐ) 

❤️ CÁCH ĐỔI ĐIỂM VIP
 /doidiemvip [dấu cách] số điểm

  ➡️ Vd:   /doidiemvip 100 
Là đổi 100đ Vip lấy 10000đ (VNĐ)"""  
    )    
    bot.send_message(message.chat.id, noi_dung_doi_diem_vip)

    
#Xử lý ngoại lệ     
@bot.message_handler(func=lambda message: True)
def handle_else(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=2)
    button0 = types.KeyboardButton(text="🎮 Danh sách game")
    button1 = types.KeyboardButton(text="👤 Tài khoản")
    button2 = types.KeyboardButton(text="📜 Event")
    button3 = types.KeyboardButton(text="🥇 Bảng xếp hạng")
    button4 = types.KeyboardButton(text="🧑‍💻 Vào nhóm")
    button5 = types.KeyboardButton(text="👥 Giới thiệu bạn bè")
    button6 = types.KeyboardButton(text="❔Thông tin❔")
    button7 = types.KeyboardButton(text="💬 Trung tâm hỗ trợ")
    button8 = types.KeyboardButton(text="🎁 Quà tặng cho tân thủ !!! 🎁")
    user_markup.add(button0, button1)
    user_markup.add(button2, button3)
    user_markup.add(button5, button4)
    user_markup.add(button6, button7)
    user_markup.add(button8)
    bot.send_message(message.chat.id, "🎮 Chiến tiếp thôi !!!", reply_markup=user_markup)

# Người dùng gửi ngoại lệ thì trả về các nút    
@bot.message_handler(content_types=['sticker','photo','video','document'])    
def handle_else1(message):
    handle_else(message)

# Chạy bot liên tục     
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(e) # in lỗi 
        time.sleep(3) 
# The end 







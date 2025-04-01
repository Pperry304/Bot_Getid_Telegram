# Bot Translate Telegram

## Giới thiệu
Đây là bot Telegram giúp dịch tin nhắn sang nhiều ngôn ngữ khác nhau. Người dùng có thể gửi văn bản đến bot, và bot sẽ trả về nội dung đã dịch theo ngôn ngữ được chọn.

## Chức năng
- Dịch văn bản từ một ngôn ngữ sang ngôn ngữ khác.
- Hỗ trợ nhiều ngôn ngữ.
- Tự động phát hiện ngôn ngữ nguồn.
- Tương tác đơn giản bằng lệnh.

## Yêu cầu
- Python 3.x
- Thư viện `telebot` để kết nối với API Telegram.
- Thư viện `deep_translator` để dịch thuật.

## Cài đặt
Cài đặt các thư viện cần thiết bằng lệnh:

```sh
pip install pyTelegramBotAPI deep-translator
```

## Cách sử dụng
1. Khởi động bot và gửi tin nhắn văn bản.
2. Sử dụng lệnh:
   
   ```
   /translate <ngôn_ngữ_đích> <nội_dung>
   ```
   Ví dụ:
   ```
   /translate en Xin chào
   ```
   Bot sẽ trả về: "Hello"

## Lưu ý
- Thay `BOT_TOKEN` trong mã nguồn bằng token thật của bot Telegram.
- Đảm bảo bot có quyền nhận và gửi tin nhắn.




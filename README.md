# Trấn Quỷ Sư

Trấn Quỷ Sư là game hành động 2D được xây dựng bằng Python và thư viện Pygame. Người chơi điều khiển pháp sư chiến đấu với quái vật qua nhiều màn chơi, sử dụng kỹ năng, né tránh đòn tấn công và tiêu diệt boss cuối để giành chiến thắng.

## Tính năng chính

- Menu chính với các lựa chọn bắt đầu game, cài đặt và thoát game.
- Gameplay hành động 2D theo thời gian thực.
- Nhân vật có máu, kinh nghiệm, cấp độ và nhiều kỹ năng chiến đấu.
- Nhiều loại quái vật với hành vi tấn công khác nhau.
- Hệ thống boss ở màn cuối.
- Vật phẩm hỗ trợ trong quá trình chơi.
- Giao diện HUD hiển thị máu, kinh nghiệm và số lượng quái còn lại.
- Âm thanh nền và hiệu ứng âm thanh cho thao tác chiến đấu.
- Màn hình thắng và thua với lựa chọn chơi lại hoặc thoát.

## Công nghệ sử dụng

- Python 3.12
- Pygame 2.6.1

## Cấu trúc thư mục

```text
Tran Quy Su/
├── assets/              Thư mục chứa hình ảnh, âm thanh và tài nguyên game
├── asset_loader.py      Quản lý tải và cache tài nguyên hình ảnh
├── boss.py              Xử lý boss cuối
├── enemy.py             Xử lý quái vật
├── item.py              Xử lý vật phẩm rơi và nhặt vật phẩm
├── main.py              File chạy chính của game
├── player.py            Xử lý nhân vật người chơi
├── settings.py          Cấu hình thông số game
├── skill.py             Xử lý kỹ năng, projectile và hiệu ứng
├── sound.py             Quản lý âm thanh và nhạc nền
├── ui.py                Vẽ giao diện người dùng
├── requirements.txt     Danh sách thư viện cần cài đặt
└── README.md            Tài liệu hướng dẫn dự án
```

## Cài đặt môi trường

Nên sử dụng Python 3.12 để đảm bảo tương thích tốt với Pygame.

Cài đặt thư viện cần thiết:

```bash
py -3.12 -m pip install -r requirements.txt
```

Nếu không dùng file `requirements.txt`, có thể cài trực tiếp:

```bash
py -3.12 -m pip install pygame
```

## Cách chạy game

Mở CMD hoặc Terminal tại thư mục chứa `main.py`, sau đó chạy:

```bash
py -3.12 main.py
```

Hoặc nếu Python mặc định của máy là Python 3.12:

```bash
python main.py
```

## Điều khiển

| Phím / Chuột | Chức năng |
|---|---|
| W, A, S, D | Di chuyển nhân vật |
| Chuột phải | Đánh thường |
| Q | Kỹ năng chém mạnh |
| E | Kỹ năng bùa lửa |
| F | Kỹ năng chém liên hoàn |
| R | Hồi máu |
| ESC | Quay lại menu hoặc thoát trạng thái hiện tại |

## Âm thanh

Các hiệu ứng âm thanh được đặt trong thư mục:

```text
assets/sounds/
```

Nhạc nền được đặt trong thư mục:

```text
assets/music/
```

File đánh thường bằng chuột phải là:

```text
assets/sounds/attack.mp3
```

## Ghi chú khi chạy

Nếu game không chạy, hãy kiểm tra các bước sau:

1. Đã cài Python 3.12.
2. Đã cài Pygame.
3. Đang chạy lệnh tại đúng thư mục chứa `main.py`.
4. Thư mục `assets` vẫn nằm cùng cấp với `main.py`.

## Tác giả

Đồ án game Python sử dụng thư viện Pygame.

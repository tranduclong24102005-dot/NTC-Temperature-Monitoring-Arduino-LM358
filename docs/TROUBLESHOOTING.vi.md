# Xử lý lỗi thường gặp

## 1. Arduino IDE không thấy board / upload thất bại

- Kiểm tra cáp USB **có truyền dữ liệu**, chọn `Tools → Board → Arduino Uno`, chọn đúng `Tools → Port`.
- Đóng Serial Monitor trước khi upload nếu cổng bị chiếm.
- Nếu dùng Uno clone, kiểm tra driver USB-UART tương thích với phần cứng (CH340, ATmega16U2, v.v.).
- Với `arduino-cli`, chạy `arduino-cli board list` để xem cổng, `arduino-cli core install arduino:avr` để cài board core.

## 2. Serial Monitor không có chữ

- Baud rate phải là **9600**.
- Nhấn Reset trên Arduino; firmware sẽ in dòng giới thiệu rồi cập nhật mỗi 500ms.
- Kiểm tra đúng `.ino` đã Upload thành công và cổng serial đang mở.

## 3. Nhiệt độ hiển thị vô lý / `ERROR: invalid...`

- Kiểm tra IC LM358 **không cắm ngược**; pin 8 phải có +5V, pin 4 là GND.
- Kiểm tra VIN đến **pin 3**, VOUT từ **pin 1** đến A0, pin 7 nối pin 6.
- Kiểm tra NTC ở nhánh **3.3V → VIN** và R1 từ **VIN → GND**; mắc đảo NTC/R1 làm hàm truyền sai.
- Kiểm tra R2/R3 có thực sự nối tới pin 2 và không bị cắm lệch hàng breadboard.
- Không dùng `ADC_REFERENCE_V=3.3` khi Uno vẫn để `DEFAULT` và AVcc khoảng 5V.
- Dùng đồng hồ đo VIN, VOUT, VREF. Nếu VOUT chạm giới hạn LM358, cần sửa thiết kế/điều kiện tải trước khi sửa hệ số phần mềm.
- Nếu nhiệt độ ra ngoài 8–52°C, firmware sẽ cảnh báo **ngoài vùng ba điểm hiệu chuẩn được báo cáo**; không tự động có nghĩa cảm biến hỏng.

## 4. Đọc nhảy số / nhiễu

- Đảm bảo tất cả các phần GND **chung một mass**.
- Rút ngắn dây tín hiệu, đặt C1 100nF đúng từ **VIN xuống GND**, thêm C2 bypass gần LM358.
- Kiểm tra breadboard tiếp xúc kém và nguồn USB biến thiên.
- EMA α=0.1 làm số hiển thị mượt nhưng chậm hơn; tăng α sẽ nhanh hơn và nhiễu hơn.
- Muốn đánh giá độ nhiễu thực, xuất bảng mẫu ADC và tính độ lệch chuẩn khi nhiệt độ ổn định.

## 5. Nhiệt độ tăng/giảm chậm

- NTC có quán tính nhiệt; môi trường trao đổi nhiệt và lọc EMA đều làm tín hiệu trễ.
- Đừng lấy riêng thời gian từ một phép đo bước (ví dụ 20 s trong báo cáo) để khẳng định τ của vật liệu NTC.

## 6. VOUT chỉ quanh 3V dù nhiệt độ tăng

- LM358 có giới hạn swing đầu ra về phía VCC. Với nguồn 5V, mức gần 3.2V có thể bị giới hạn tùy dòng tải, loại chip, điện áp thực.
- Đo VOUT tại LM358 pin 1 bằng đồng hồ; nếu không tăng theo VIN, có khả năng op-amp chạm trần.
- Nếu cần toàn dải ra cao hơn, cân nhắc op-amp rail-to-rail phù hợp và **thiết kế/tính lại** phần cứng. Không sửa ngẫu nhiên hệ số Steinhart–Hart để che clipping.

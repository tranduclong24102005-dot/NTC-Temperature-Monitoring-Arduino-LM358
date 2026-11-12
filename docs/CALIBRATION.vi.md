# Hiệu chuẩn NTC: từ ba điểm đo đến hệ số Steinhart–Hart

## 1. Khi nào cần hiệu chuẩn?

NTC cùng nhãn `10k β3950` có thể lệch nhau do dung sai linh kiện; các điện trở R1–R5 cũng có sai số. Hơn nữa, cấp nguồn từ USB không có nghĩa điện áp ADC tham chiếu luôn đúng 5.000V. Nếu chỉ muốn quan sát nguyên lý, bạn có thể dùng hệ số mặc định trong firmware; nếu muốn so sánh độ chính xác, **hãy đo và hiệu chuẩn mạch của chính bạn**.

## 2. Đo các điện áp phần cứng trước

Dùng đồng hồ để xác định (với Arduino đang hoạt động, thao tác an toàn):

- `DIVIDER_SUPPLY_V`: điện áp nguồn thực tại đầu trên NTC (danh định 3.3V).
- `ADC_REFERENCE_V`: AVcc/nguồn 5V thực dùng làm tham chiếu ADC của Uno (danh định 5V).
- `VREF_V`: LM358B pin 7 (danh định 1.65V).
- R1, R2, R3 thực (nếu có đồng hồ đo điện trở, đo **khi ngắt nguồn và tách linh kiện khỏi mạch nếu cần**).

Cập nhật các hằng số này trong `.ino`; đo VREF **tại LM358 pin 7**, không chỉ tính từ hai điện trở. Phần tiếp theo áp dụng với sơ đồ nối NTC ở **nhánh trên**.

## 3. Chuẩn bị ít nhất ba điểm hiệu chuẩn

Báo cáo gốc ghi các cặp (nhiệt độ, điện trở):

| Nhiệt độ chuẩn (°C) | R_NTC (Ω) | Vai trò |
|---:|---:|---|
| 8 | 21916 | Điểm thấp |
| 29 | 8395 | Điểm giữa |
| 52 | 3345 | Điểm cao |

Các số trên chỉ là **ví dụ từ báo cáo**, không phải phép đo do công cụ trong repository thực hiện. Nếu dùng thermistor khác, không dùng nguyên bộ hệ số như một bảo đảm chính xác.

Với từng điểm thử: đặt NTC và nhiệt kế chuẩn gần nhau trong môi trường có nhiệt độ ổn định; chờ cân bằng nhiệt; ghi nhiệt độ chuẩn và điện trở. Nếu không đo trực tiếp R_NTC, có thể đo VIN và dùng `R = R1*(Vdivider/VIN - 1)`. Lặp lại để phát hiện điểm đo bất thường.

## 4. Tính A, B, C mà không cần thư viện ngoài

Dữ liệu mẫu có sẵn ở [`data/calibration_points_from_report.csv`](../data/calibration_points_from_report.csv).

```bash
python scripts/calibrate_steinhart_hart.py data/calibration_points_from_report.csv
```

Đầu ra là `A`, `B`, `C` vừa khớp chính xác ba điểm (trong giới hạn sai số tính toán). Chương trình giải hệ:

```text
1/(T1+273.15) = A + B*ln(R1) + C*ln(R1)^3
1/(T2+273.15) = A + B*ln(R2) + C*ln(R2)^3
1/(T3+273.15) = A + B*ln(R3) + C*ln(R3)^3
```

> **Điểm cần hiểu:** Hệ số *in trong báo cáo gốc* là:
> `A=0.001129148`, `B=0.000234125`, `C=0.0000000876741`.
> Chúng dự đoán ba điểm mẫu sai khác rất nhỏ (xấp xỉ 0.005°C, 0.035°C và −0.050°C), nhưng **không trùng nghiệm đại số chính xác** của chính ba cặp (T,R) đã công bố. Script giúp người học tự kiểm tra sự khác biệt.

## 5. Nạp hệ số vào firmware

Thay ba hằng số `SH_A`, `SH_B`, `SH_C` trong file `.ino` bằng giá trị từ dữ liệu đo **thật của bạn**, và sửa comment mô tả hiệu chuẩn. Chạy lại Arduino IDE Verify/Upload và so sánh ở nhiều nhiệt độ **không trùng điểm dùng để fit** để kiểm tra tính tổng quát.

## 6. Kiểm chứng đúng cách

- Có ít nhất 3 điểm để **fit** và thêm một số điểm **độc lập** để kiểm thử.
- Ghi loại nhiệt kế tham chiếu, thời gian ổn định, nhiệt độ, R_NTC/VIN/VOUT và sai lệch.
- Tính: `error = T_NTC - T_ref`, `MAE = mean(abs(error))` và `max(abs(error))` **trên tập điểm được kiểm chứng**.
- Báo sai số theo đúng số điểm và điều kiện đã thử, không khẳng định "sai số toàn dải ±0.1°C" chỉ từ phép fit 3 điểm.
- EMA khiến giá trị phản ứng chậm hơn khi thay đổi đột ngột; chờ đủ thời gian trước khi ghi điểm.

Bảng mẫu cho người tái hiện: [`data/measurement_template.csv`](../data/measurement_template.csv).

# Từ nhiệt độ đến số đo Arduino: nguyên lý và công thức

## 1. NTC là gì?

NTC (Negative Temperature Coefficient) là nhiệt điện trở **có điện trở giảm khi nhiệt độ tăng**. Báo cáo sử dụng NTC MF58 10kΩ tại 25°C với hệ số β ≈ 3950 K.

Mô hình Beta để **dự đoán** điện trở theo nhiệt độ:

\[
R(T) = R_{25} \, \exp\left[\beta\left(\frac{1}{T_K} - \frac{1}{298.15}\right)\right]
\]

Trong đó `T_K = T_C + 273.15`. Mô hình Beta thường chỉ xấp xỉ linh kiện thực.

## 2. Tại sao phải có mạch chia áp?

Arduino Uno đọc điện áp chứ không đọc trực tiếp điện trở. Ta mắc NTC với điện trở cố định R1=10kΩ:

```text
3.3V -- NTC -- VIN -- R1(10k) -- GND
```

\[
V_{IN}=3.3\cdot\frac{R_1}{R_{NTC}+R_1}
\]

Giải ngược khi cần tính điện trở:

\[
R_{NTC}=R_1\left(\frac{3.3}{V_{IN}}-1\right)
\]

**25°C lý tưởng**: R_NTC=10kΩ nên VIN=1.65V. Khi nhiệt độ tăng, R_NTC giảm và VIN **tăng**.

## 3. LM358 và dịch mức

Sử dụng hai op-amp bên trong LM358:

- **Kênh B** tạo bộ đệm VREF~1.65V từ cầu chia điện áp R4=R5=10kΩ lấy 3.3V.
- **Kênh A** khuếch đại không đảo với R2=10kΩ và hồi tiếp R3=5.6kΩ:

\[
V_{OUT}=\left(1+\frac{R_3}{R_2}\right)V_{IN}-\frac{R_3}{R_2}V_{REF}
\]

Với R3/R2=0.56, **VOUT=1.56 VIN − 0.56 VREF**.

Trong tính toán lý tưởng (VREF=1.65):

| Nhiệt độ theo mô hình Beta | VIN xấp xỉ | VOUT lý tưởng |
|---:|---:|---:|
| −3.35 °C | 0.657 V | 0.101 V |
| 25 °C | 1.650 V | 1.650 V |
| 60 °C | 2.643 V | 3.199 V |

**Lưu ý**: LM358 không rail-to-rail, VOUT tối đa thực tế tùy nguồn/tải. Phương trình không đảm bảo đạt mức lý tưởng ở hai đầu biên. Đây là lý do nguồn LM358 cần được kiểm tra và cấp từ 5V trong bản đấu dây đề xuất.

## 4. ADC 10-bit trên Arduino Uno

Khi dùng `analogReference(DEFAULT)`, Uno đo theo **AVcc** (thông thường gần 5V). Giá trị `analogRead(A0)` là số nguyên **0..1023**. Firmware sử dụng công thức xấp xỉ:

\[
V_{OUT}\approx\frac{ADC}{1023} \times V_{ADC\_REF}
\]

Giá trị 3.3V ở mạch chia áp là **nguồn kích thích cảm biến**, không phải tự động là tham chiếu ADC. Với VOUT tối đa lý thuyết ~3.2V và V_ADC_REF=5V, thực tế chỉ tận dụng khoảng 64% thang mã ADC; không nên quảng cáo "dùng trọn 10-bit".

## 5. Lọc analog và lọc số

- **Analog**: C1=100nF từ VIN tới GND. Ở 25°C, R_th ≈ 10k || 10k = 5kΩ, suy ra `fc = 1/(2π R_th C1) ≈ 318 Hz`. R_th **phụ thuộc nhiệt độ**, nên fc cũng thay đổi.
- **Digital**: EMA với α=0.1: `EMA_mới = 0.1 * ADC_mới + 0.9 * EMA_cũ`. Giá trị đầu tiên khởi tạo trực tiếp để tránh hiển thị tăng dần từ 0.

Firmware cập nhật mỗi **0.5 giây**, tức đọc ứng dụng khoảng **2 lần/s**. 318Hz không đủ để khẳng định mạch là anti-alias filter cho nhịp lấy mẫu này. Bộ lọc và chiến lược đo nên được đánh giá bằng nhiễu thực tế.

## 6. Tại sao dùng Steinhart–Hart?

Điện trở NTC thay đổi phi tuyến, nên không thể biến trực tiếp số ADC thành °C bằng một tỷ lệ cố định. Mô hình:

\[
\frac{1}{T_K}=A+B\ln R + C(\ln R)^3
\]

Sau đó: `T_C = T_K − 273.15`.

Báo cáo cung cấp `A=0.001129148`, `B=0.000234125`, `C=0.0000000876741`. Chúng gần khớp ba điểm hiệu chuẩn của báo cáo nhưng **không phải nghiệm chính xác của ba phương trình** theo số đã in. Xem [CALIBRATION.vi.md](CALIBRATION.vi.md) để hiểu cách tính lại.

## 7. Chuỗi giải ngược trong firmware

`analogRead(A0)` → EMA → `VOUT` → `VIN=(VOUT+VREF*R3/R2)/(1+R3/R2)` → `R_NTC=R1*(3.3/VIN-1)` → `T_K` từ Steinhart–Hart → `T_C`.

Các điều kiện có thể gây lỗi: mất nguồn cảm biến, sai VREF, VOUT chạm rail, thiếu GND chung, sai điện trở, nhiệt độ nằm ngoài vùng hiệu chuẩn. Firmware sẽ từ chối một số giá trị phi vật lý thay vì in NaN.

Xem sơ đồ và số liệu gốc ở các trang 5–13 của [báo cáo](../report/Cam-bien-original.pdf#page=5).

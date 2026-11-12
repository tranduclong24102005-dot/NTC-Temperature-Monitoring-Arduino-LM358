# Ghi chú kỹ thuật khi chuyển từ báo cáo môn học sang tài liệu cộng đồng

**Mục đích:** giữ báo cáo gốc làm tư liệu học tập, đồng thời tránh để người đọc tưởng mọi phép tính và đặc tính phần cứng đã được kiểm chứng độc lập. Các nhận xét dưới đây đối chiếu chính văn bản và sơ đồ trong tài liệu `Cam-bien-original.pdf`.

| Nơi trong báo cáo | Điều cần làm rõ | Cách trình bày trong repo |
|---|---|---|
| Trang 5 so với trang 11, 14 | Trang 5 gọi ADC 0–3.3V, nhưng code trang 14 dùng `V_ADC_REF=5.0` và trang 11 cũng ghi 5V. Uno ở `DEFAULT` dùng AVcc (thường ~5V). | Tách rõ **nguồn chia áp 3.3V**, **LM358 5V đề xuất**, **ADC AVcc ~5V**. |
| Trang 5 | Sơ đồ hai op-amp chưa ghi chân nguồn của LM358. Nếu cấp LM358 bằng 3.3V, không thể mặc nhiên kỳ vọng VOUT≈3.2V. | Có sơ đồ pin DIP-8 và hướng dẫn đo; nguồn 5V cho LM358 là giả định kỹ thuật cần kiểm tra ở mạch thật. |
| Trang 5–9 | Mục tiêu VOUT 0.05–3.25V ở trang 5, nhưng trang 7 đưa 0.58–3.72V để tính gain 1.57 mà không giải thích nhất quán. | Dùng đúng **R2=10k, R3=5.6k** từ sơ đồ để có gain 1.56, không nhận là tối ưu dải ADC. |
| Trang 8 | Phép tính `1.65 + 3.104 / 2 = 3.022` là sai số học. | Kết quả đúng là **3.202 V** từ phép cộng này. Với mô hình Beta & linh kiện danh định, VOUT≈3.199V tại 60°C. |
| Trang 9–10 | RC `R_th≈5k`, `C=100nF` cho `fc≈318Hz` (tại 25°C) là đúng, nhưng phần chống aliasing chưa có căn cứ nếu chương trình đọc mỗi 500ms. | Mô tả là **lọc RC giảm nhiễu**; chưa khẳng định đủ là anti-alias filter ở nhịp 2Hz. |
| Trang 12–13 | Ba hệ số Steinhart–Hart được công bố gần khớp 3 điểm nhưng không khớp đại số hoàn toàn. | Giữ hằng số gốc trong firmware và thêm **script fit chính xác** từ 3 điểm đo để người đọc tự kiểm tra. |
| Trang 15 | Code in trong PDF có `f (isFirstReading)` thay vì `if (isFirstReading)` (có thể là lỗi biên tập). | Đã viết lại chương trình với cú pháp hợp lệ, guard để tránh chia 0/`log` sai miền, không khẳng định mã in trong PDF biên dịch nguyên trạng. |
| Trang 17 | Ba điểm đối chứng so với LM35 cho sai số từ −0.3 đến +0.2°C. | Ghi rõ **sai lệch tại 3 điểm báo cáo**, không quảng cáo là chứng nhận ±0.3°C toàn dải. |
| Trang 19–20 | Suy τ=4s từ 20s theo quy tắc `t_s≈5τ`. | Đây là **ước tính toàn hệ** theo giả thiết, không phải hằng số thời gian đo độc lập của NTC. |

## Công thức đúng cần nhớ

```text
R_NTC = R1 * (V_DIVIDER / VIN - 1)
VOUT  = (1 + R3/R2) * VIN - (R3/R2) * VREF
VIN   = (VOUT + VREF * R3/R2) / (1 + R3/R2)
T[K]  = 1 / (A + B*ln(R_NTC) + C*ln(R_NTC)^3)
T[C]  = T[K] - 273.15
```

Điều kiện: NTC là **nhánh trên** mạch chia áp, GND chung, LM358 chưa bão hòa, điện áp đo và giá trị điện trở phù hợp mạch thật.

## Vì sao không chỉnh PDF gốc?

Vì nó là **hồ sơ dự án tại thời điểm làm môn học**. Sửa âm thầm khiến người đọc không phân biệt kết quả đã đo và phần cải tiến sau này. Repo sẽ giữ báo cáo nguyên bản, nhưng tách các bản diễn giải được kiểm tra riêng. Khi có số đo mới, hãy thêm một tài liệu thí nghiệm hoặc release note có ngày/điều kiện đo.

## Nguồn đối chiếu độc lập

- [Texas Instruments LM358](https://www.ti.com/product/LM358): input common-mode và output swing phụ thuộc nguồn/tải; LM358 **không** rail-to-rail.
- [Arduino Uno Rev3](https://docs.arduino.cc/hardware/uno-rev3/): ADC 10-bit và đặc tính bo mạch.
- [Arduino IDE](https://www.arduino.cc/en/software): Verify / Upload và Serial Monitor.

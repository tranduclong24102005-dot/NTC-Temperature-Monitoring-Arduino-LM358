# Hướng dẫn đấu dây chi tiết (Arduino Uno R3 + LM358 DIP-8)

> **Cảnh báo**: Bảng này là **sơ đồ tái dựng từ bản vẽ chức năng trong báo cáo gốc (trang 5)**, có bổ sung chân nguồn LM358 vốn chưa được ghi. Bạn phải đối chiếu với IC và breadboard thực tế trước khi lắp, đo bằng đồng hồ trước khi nối A0. Ngắt USB/nguồn khi cắm hoặc tháo dây. Chỉ dùng nguồn DC điện áp thấp từ Arduino, không đấu điện lưới.

## A. Nhìn đúng chiều IC LM358 DIP-8

Đặt IC sao cho **rãnh/notch ở phía trên**. Các chân đánh số **ngược chiều kim đồng hồ nhìn từ mặt trên**:

```text
             NOTCH
           ___   ___
   OUT A  1 |     | 8  VCC (+5V)
    IN- A 2 |     | 7  OUT B (VREF)
    IN+ A 3 |     | 6  IN- B
     GND  4 |_____| 5  IN+ B
```

Các chân theo bảng chức năng LM358 thông dụng; luôn kiểm tra datasheet của IC bạn đang có. Nếu dùng LM358 dạng module khác DIP-8, sơ đồ pin có thể không áp dụng.

## B. Nối nguồn và GND trước

| Nguồn | Nơi nối | Chức năng |
|---|---|---|
| Arduino **5V** | LM358 **chân 8** | Nguồn riêng cho op-amp; cần biên độ đầu ra cao |
| Arduino **GND** | LM358 **chân 4** và rail GND breadboard | Điểm 0 V chung |
| Arduino **3.3V** | Đầu trên của **NTC**, đầu trên **R4** | Chia áp đo nhiệt và tạo VREF |
| C2 100 nF (khuyến nghị) | Giữa LM358 pin 8 ↔ pin 4, đặt sát chip | Giảm nhiễu nguồn |

**Không** dùng 5V thay 3.3V cho NTC nếu vẫn giữ các hằng số firmware gốc. **Không** cấp LM358 bằng 3.3V rồi mặc định mạch đạt Vout 3.2V, vì LM358 không có đầu ra rail-to-rail.

## C. Mạch chia áp NTC và lọc C1

```text
  Arduino 3.3V
       |
     [NTC 10k @25C]
       |
       +--------- VIN ---------> LM358 pin 3 (IN+ A)
       |           |
     [R1 10k]   [C1 100nF]
       |           |
       +-----------+----------- GND
```

- Một chân NTC nối **3.3V**, chân còn lại là **VIN**.
- R1 10kΩ nối **VIN → GND**.
- C1 100nF nối **VIN → GND**, song song R1.
- VIN nối tới **LM358 chân 3** (IN+ A).
- Ở khoảng 25°C với NTC ~10k, lý thuyết VIN khoảng **1.65 V**.

## D. LM358B — mạch đệm tạo VREF ≈ 1.65 V

```text
  Arduino 3.3V
       |
     [R4 10k]
       |
       +-------> LM358 pin 5 (IN+ B)
       |
     [R5 10k]
       |
      GND

  LM358 pin 7 (OUT B) ----+----> VREF tới đầu R2
                         |
  LM358 pin 6 (IN- B) ----+    (hồi tiếp trực tiếp)
```

Pin 5 nhận khoảng 1.65V; pin 7 nối ngược về pin 6 để cấu hình **voltage follower**, pin 7 là **VREF**.

## E. LM358A — khuếch đại không đảo có dịch mức

| Thành phần/đầu nối | Nối từ | Nối tới |
|---|---|---|
| **VIN** | Nút chia áp | LM358 **pin 3** (IN+ A) |
| **R2 = 10kΩ** | LM358 pin **7** (VREF) | LM358 **pin 2** (IN− A) |
| **R3 = 5.6kΩ** | LM358 **pin 1** (OUT A) | LM358 **pin 2** (IN− A) |
| **VOUT** | LM358 **pin 1** | Arduino **A0** |

Hàm truyền lý tưởng của mạch:

```text
VOUT = (1 + R3/R2) * VIN - (R3/R2) * VREF
     = 1.56 * VIN - 0.56 * VREF
```

Với VIN≈1.65V và VREF≈1.65V ⇒ **VOUT≈1.65V**. Đây chỉ là tính toán lý tưởng; đầu ra thực có thể bị giới hạn bởi LM358.

## F. Danh sách các nút để kiểm tra chéo

| Tên net | Những chân/nút chung một dây |
|---|---|
| `GND` | Arduino GND, LM358-4, R1 dưới, R5 dưới, C1 dưới, C2 dưới |
| `+5V` | Arduino 5V, LM358-8, C2 trên |
| `+3V3` | Arduino 3.3V, đầu trên NTC, đầu trên R4 |
| `VIN` | Đầu dưới NTC, R1 trên, C1 trên, LM358-3 |
| `VMID` | R4 dưới, R5 trên, LM358-5 |
| `VREF` | LM358-7, LM358-6, R2 đầu thứ nhất |
| `INV_A` | LM358-2, R2 đầu thứ hai, R3 đầu thứ nhất |
| `VOUT` | LM358-1, R3 đầu thứ hai, Arduino A0 |

## G. Kiểm tra an toàn theo thứ tự

1. Ngắt USB; kiểm tra **không chập 5V với GND**, **3.3V với GND**.
2. Đảm bảo chân IC đúng chiều rãnh và thanh nguồn trên breadboard **không bị ngắt đoạn ngầm**.
3. **Chưa nối VOUT vào A0**, cấp nguồn USB; đo pin 8 ≈ 5V, pin 4 ≈ 0V.
4. Đo VMID tại chân 5 và VREF tại pin 7; kỳ vọng ~1.65V.
5. Đo VIN tại pin 3; kỳ vọng ~1.65V ở nhiệt độ gần 25°C.
6. Đo pin 1 (VOUT); khi ở nhiệt độ phòng kỳ vọng gần VIN (do VREF~VIN~1.65V), và phải **không vượt mức điện áp vào cho phép của Arduino A0**.
7. Nếu các mức phù hợp, ngắt nguồn, nối VOUT → A0, cấp nguồn lại, nạp firmware.
8. Thử nhiệt độ khác; theo dõi LM358 có **bão hòa/clipping** hay không bằng đồng hồ, đặc biệt gần đầu cao của dải đo.

**Nếu phát hiện LM358 nóng, mùi khét hoặc VOUT bất thường, ngắt nguồn ngay.**

## H. Hai việc cần xác minh trên mạch thật

- **Độ sụt ngõ ra cao**: LM358 có hạn chế swing đầu ra phía VCC, vì vậy VOUT lý thuyết 3.2V chưa được bảo đảm trên mọi IC/tải. Đo với nhiệt độ cao, giảm tải hoặc xem xét op-amp rail-to-rail nếu thật sự cần.
- **Độ ổn định điện áp**: đo điện áp 3.3V, 5V (AVcc) và VREF thực tế; cập nhật hằng số trong firmware. Không lấy số danh định làm chuẩn hiệu chuẩn chính xác.

Tham khảo: [LM358 TI datasheet](https://www.ti.com/product/LM358) và [báo cáo gốc trang 5](../report/Cam-bien-original.pdf#page=5).

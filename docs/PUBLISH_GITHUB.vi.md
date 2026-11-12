# Đưa dự án lên GitHub và biến nó thành một portfolio có giá trị

Tài liệu này dành cho **chủ dự án**, không phải phần bắt buộc đối với người chỉ muốn lắp mạch.

## 1. Trước khi để chế độ Public

- [ ] Xác minh quyền chia sẻ báo cáo, ảnh gốc và đóng góp của các thành viên khác (nếu đây là bài nhóm).
- [ ] Kiểm tra báo cáo PDF không chứa họ tên, số điện thoại, mã sinh viên, lớp học, ID cá nhân hoặc ảnh riêng tư không muốn công khai.
- [ ] Kiểm tra quyền đối với **hình linh kiện trong PDF**; nếu chưa rõ, cân nhắc bỏ file PDF khỏi repo public và chỉ đăng nội dung/hình tự tạo hoặc được phép chia sẻ.
- [ ] Xem lại `LICENSE`: thay dòng `The project author(s)` bằng tên tác giả/chủ sở hữu phù hợp; xin phép đồng tác giả nếu cần. Đọc thêm [`CONTENT_NOTICE.md`](../CONTENT_NOTICE.md).
- [ ] Đọc [`docs/REVIEW_NOTES.vi.md`](REVIEW_NOTES.vi.md) và đo lại nguồn 5V/3.3V/VREF/VOUT nếu muốn công bố mức độ tương thích mạch đã xác minh.
- [ ] Chỉ đánh dấu **đã test trên phần cứng** khi bạn thật sự chạy lại `.ino` trên mạch.

## 2. Tên và thông tin repo (gợi ý)

- **Name:** `NTC-Temperature-Monitoring-Arduino-LM358`
- **Description:** `NTC 10k temperature monitor using LM358, Arduino Uno, EMA filtering & Steinhart-Hart calibration. Full wiring, firmware and experiments.`
- **Topics:** `arduino`, `arduino-uno`, `ntc-thermistor`, `lm358`, `temperature-sensor`, `sensor-calibration`, `steinhart-hart`, `embedded-systems`, `signal-conditioning`, `electronics-project`
- **Visibility:** Public (sau khi duyệt quyền chia sẻ)
- **Language:** source code Arduino/C++; tài liệu VI + English summary

## 3. Cách 1: tạo repo trên website (dễ làm nhất)

1. Giải nén file ZIP dự án, kiểm tra README.md nằm **ngay bên trong thư mục gốc**, không bị lồng hai lần.
2. Đăng nhập GitHub → dấu **+** góc trên → **New repository**.
3. Nhập Name và Description như trên; chọn **Public**.
4. **Không tích** `Add a README`, `Add .gitignore` và `Choose a license` vì file ZIP đã có sẵn cả ba.
5. Nhấn **Create repository** và giữ tab đó.
6. Mở PowerShell trong thư mục đã giải nén rồi chạy các lệnh ở mục 4.

## 4. Các lệnh PowerShell để push

Thay `YOUR_USERNAME` bằng tên tài khoản GitHub thật. Điều kiện: máy Windows đã cài **Git for Windows** và cấu hình tên/email Git; đừng gõ ký tự `<` `>` vào đường dẫn thực.

```powershell
# Mở PowerShell trong thư mục root của dự án (có README.md)
git init -b main
git add .
git status
git commit -m "Initial release: NTC + LM358 Arduino learning project"

git remote add origin https://github.com/YOUR_USERNAME/NTC-Temperature-Monitoring-Arduino-LM358.git
git push -u origin main
```

Nếu Git yêu cầu danh tính ở lần commit đầu:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Nếu chưa đăng nhập GitHub ở dòng lệnh, Git Credential Manager sẽ có thể mở cửa sổ trình duyệt yêu cầu bạn xác thực. **Không đưa password hay access token lên README/repo.**

Nếu báo `remote origin already exists`, kiểm tra `git remote -v` trước; chỉ dùng `git remote set-url origin URL` khi URL đó sai. Nếu repo trên GitHub đã có commit, đừng `git push --force` để ghi đè; hãy kiểm tra và hợp nhất lịch sử an toàn.

### Tùy chọn: 1 lệnh GitHub CLI

Nếu bạn có GitHub CLI (`gh`) và đã `gh auth login`, không cần tạo repo trên website trước:

```powershell
git init -b main
git add .
git commit -m "Initial release: NTC temperature monitor"
gh repo create NTC-Temperature-Monitoring-Arduino-LM358 --public --source=. --remote=origin --push
```

Dùng **một trong hai cách** (tạo website + Git hoặc `gh repo create`), tránh tạo hai repo trùng nhau.

## 5. Sau khi push: làm sao để người khác tìm được?

1. Trên trang repo → **About (biểu tượng bánh răng)** → thêm Description và Topics gợi ý.
2. Kiểm tra mục **Actions**: workflow `Arduino Uno compile` đã chạy xanh chưa. Chỉ thêm badge `Build passing` sau khi workflow thực sự thành công.
3. Dùng **ảnh mạch thật** làm social preview (Settings → General → Social preview), nhưng phải đảm bảo quyền dùng ảnh.
4. Tạo Release `v1.0.0` nếu đây là lần công bố đầu tiên, kèm thay đổi chính và tình trạng kiểm chứng.
5. Ghim repo trên profile: **Your profile → Customize your pins**, chọn repo này.
6. Nếu muốn có profile README, tạo **một repo public trùng chính xác tên username GitHub**, có `README.md` giới thiệu bản thân và liên kết tới 2–4 dự án tiêu biểu. GitHub hỗ trợ profile README theo cách này.

## 6. Đoạn giới thiệu dự án để đưa vào GitHub Profile README

```markdown
### Featured embedded systems project

**[NTC Temperature Monitoring – Arduino Uno & LM358](https://github.com/YOUR_USERNAME/NTC-Temperature-Monitoring-Arduino-LM358)**  
Designed and documented a low-cost temperature monitoring circuit with an NTC thermistor, LM358 signal conditioning, Arduino ADC sampling, EMA filtering and Steinhart–Hart calibration. Includes firmware, a pin-by-pin wiring guide, numerical checks and original experimental comparisons.

**Skills:** Embedded C/C++, analog electronics, sensor calibration, technical documentation.
```

Hãy chỉ ghi `Built and hardware-validated` nếu bạn đã chạy lại firmware đúng bản ở repo. Hồ sơ mạnh đến từ **tính minh bạch, khả năng tái lập và chất lượng tài liệu**, không phải nhiều badge hoặc lời quảng cáo tuyệt đối.

## 7. Lộ trình nâng cấp repository sau khi công bố

- **v1.0.0:** Báo cáo gốc, firmware biên soạn lại, pin table, nguyên lý, script tính toán.
- **v1.1.0:** Ảnh cận mạch theo từng khối, ảnh đồng hồ đo điện áp ở VIN/VOUT, xác nhận đầu ra LM358.
- **v1.2.0:** Sơ đồ nguyên lý KiCad tự vẽ, dữ liệu thực nghiệm CSV chưa xử lý, biểu đồ sai số và phần giải thích.
- **v1.3.0 (tùy chọn):** Dữ liệu đáp ứng bước đầy đủ, so sánh trường hợp có/không EMA.

Nếu dự án học phần là công sức nhóm, nêu đóng góp của từng người bằng tên và liên kết **sau khi đã xin phép**. Điều này giúp profile đáng tin hơn.

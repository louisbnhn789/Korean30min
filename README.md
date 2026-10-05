# Korean30min 한국어

Ứng dụng Android học tiếng Hàn **từ số 0, 30 phút/ngày, 182 ngày trong 26 tuần**, dành cho môi trường công ty điện tử. Giao diện và giải thích bằng tiếng Việt.

## Tải và cài APK

Vào **Actions → Build Korean30min APK → lần chạy màu xanh → Artifacts → Korean30min-APK**. Giải nén ZIP và mở `Korean30min.apk` trên điện thoại. Cho phép cài ứng dụng từ nguồn đó khi Android hỏi. Hỗ trợ Android 8 trở lên. Đây là bản tự luyện ký debug, chưa phát hành trên Play Store. Chữ ký debug được lưu cache để dùng cho các lần dựng tiếp theo; nếu cache bị mất, bản dựng mới có thể cần gỡ bản cũ và sẽ mất tiến độ.

## Lộ trình

- Tuần 1–2: ghép chữ Hangul, nguyên âm, âm thường/căng/bật hơi, phụ âm cuối và nối âm. Có 14 bài luyện âm theo từng ngày.
- Tuần 3–8: chào hỏi lịch sự, giới thiệu, chức danh, số, giờ, vị trí trong nhà máy và yêu cầu cơ bản.
- Tuần 9–16: an toàn/ESD, linh kiện, lắp ráp, sản lượng, IQC/OQC, lỗi ngoại quan, đo kích thước và RF.
- Tuần 17–22: độ tin cậy, vật liệu/phê duyệt, kho/truy xuất, xuất hàng, báo cáo tiến độ và họp.
- Tuần 23–26: tài liệu/ISO, nhà cung cấp/khách hàng, sự cố thiết bị/jig, bàn giao và tổng ôn.

Có 312 mục học theo tuần (309 nội dung Hangul khác nhau), bao gồm âm tiết tập đọc và từ/cụm từ. Có câu mẫu tiếng Hàn, gợi âm Latin và nghĩa tiếng Việt. Gợi âm chỉ tham khảo: ưu tiên nghe giọng mẫu và đọc Hangul. Thuật ngữ cần đối chiếu cách dùng thực tế của từng công ty.

Mỗi ngày: ôn 5 phút, học mới 10 phút, nghe 8 phút, tự nói/ghi âm 5 phút, đọc/viết 2 phút. Có thể mở bất kỳ ngày nào.

## Chức năng offline

- Audio tiếng Hàn được đóng gói sẵn trong APK; không cần Internet hoặc tài khoản khi học.
- Ghi âm tối đa 90 giây và nghe lại để tự so với mẫu. Bản ghi mới thay bản trước.
- Luyện viết từng khối Hangul trên màn hình, xóa và viết lại.
- Kiểm tra nghe/đọc 12 câu, lưu điểm cao nhất và mục trả lời sai. Kiểm tra tuần tích lũy tối đa bốn tuần gần nhất; cuối khóa ôn các tuần từ giao tiếp cơ bản đến công việc, không trộn bài âm tiết sơ cấp với số có cùng cách viết.
- Tiến độ, điểm và bản ghi chỉ nằm trên điện thoại. Không xin quyền Internet; hỏi quyền micro khi bắt đầu ghi âm. Gỡ ứng dụng sẽ xóa dữ liệu.

## Giới hạn và kiểm tra

Nội dung tự biên soạn, không sao chép sách hoặc audio thương mại. Audio tổng hợp qua gTTS khi dựng, sau đó chạy offline. Chưa chấm phát âm, thứ tự nét hoặc chữ viết tự động. Bài kiểm tra tự luyện không phải TOPIK. Các câu mẫu kỹ thuật giúp luyện ngôn ngữ, không thay WI hoặc tiêu chuẩn kiểm tra đã phê duyệt của nhà máy.

GitHub Actions xác nhận 26 tuần/182 ngày, tạo và kiểm tra toàn bộ audio, dựng APK, chạy Android Lint và xác nhận chữ ký/audio trong APK. Dùng JDK 17, Gradle 8.9, AGP 8.7.3, SDK 35. Chưa kiểm thử trên điện thoại thật; sau khi cài hãy thử nghe, ghi âm và lưu tiến độ trong chế độ máy bay.

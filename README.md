# Korean30min 2.1

Ứng dụng học tiếng Hàn offline 30 phút/ngày, giao diện tiếng Việt, có lộ trình 182 ngày.

## Cập nhật 2.1

- Nút **Ngữ pháp**: giữ nguyên 40 bài nền và tiến độ; bổ sung 8 bài áp dụng có nguồn tham khảo, tổng cộng 48 bài / 96 bài tập. Nguồn được ghi trong từng bài, có ngày đối chiếu và nút mở tài liệu gốc (cần Internet). Nội dung học vẫn có sẵn offline.
- Nút **Hội thoại**: 16 tình huống công việc, mỗi đoạn đủ 4 lượt A/B, âm thanh thực tế 10–15 giây. Có nghe toàn đoạn, lặp lại, nghe từng lượt, ẩn/hiện bản dịch, ghi âm và lưu đã luyện.
- Giữ **Design & Dev by Duy nguyen** phía trên tên ứng dụng.
- Dùng cùng mã ứng dụng và khóa ký v2; versionCode 4 / versionName 2.1.0. Cài cập nhật trên v2/v2.0.1 để giữ tiến độ, không gỡ ứng dụng.

## Nội dung nền 2.0

- Mục **Ngữ pháp** riêng: 40 bài từ cơ bản đến ứng dụng, có công thức, cách dùng, lỗi dễ nhầm, 80 câu ví dụ có audio và 80 câu bài tập kèm giải thích. Ví dụ tập trung vào công việc trong nhà máy.
- Mục **Kho từ**: thêm chính xác 1.000 mục từ/cụm từ, không trùng chữ bản ngữ trong kho cũ. Tổng cộng 1309 mục học riêng biệt, gồm mục học của lộ trình cũ và âm tiết Hangul nhập môn.
- Các chủ đề thông dụng: nhận ca, thao tác, vật liệu, linh kiện điện tử, dụng cụ, lắp ráp, ép nhựa/mạ, máy móc, bảo trì, chất lượng, đo kiểm, RF, độ tin cậy, ESD, kho, đóng gói, xuất hàng, mua hàng, nhà cung cấp, họp, báo cáo, audit, bàn giao và sinh hoạt hằng ngày.
- Tìm theo chữ bản ngữ, nghĩa tiếng Việt; lọc chủ đề; nghe từng mục; đánh dấu đã nhớ hoặc đưa vào ôn tập; kiểm tra nghe/đọc kho từ 12 câu.
- Gợi ý bài ngữ pháp theo ngày sau giai đoạn phát âm nhập môn. Chọn học một cấu trúc hoặc 5–10 mục từ trong phần 10 phút học mới; không cần học dồn cả kho từ.

## Offline và dữ liệu

Bài học, ngữ pháp, ví dụ và audio đều nằm trong APK. Không xin quyền Internet. Micro chỉ dùng khi ghi âm; mỗi bản ghi mới thay bản trước. Tiến độ/điểm nằm trên điện thoại. Không có chấm phát âm hoặc nét viết tự động. Nội dung và câu ví dụ tự biên soạn; audio tổng hợp gTTS; Gợi âm Latin trong bài cơ bản chỉ tham khảo; kho mở rộng ưu tiên Hangul và audio. Ví dụ kỹ thuật không thay thế WI hoặc tiêu chuẩn nhà máy.

## Cài đặt

Android 8 trở lên. Tải APK ở **Actions → lần chạy thành công → Artifacts → Korean30min-APK**, giải nén và mở APK trên điện thoại.

Korean30min 2 dùng mã ứng dụng mới để cài song song với bản 1, vì khóa ký bản 1 không được lưu thành công. Không cần gỡ bản 1. Tiến độ bản 1 không tự chuyển sang bản 2.

## Dựng và kiểm tra

Chạy `pip install pypinyin==0.53.0 gTTS==2.5.4`, `python curriculum.py`, `python expand_course.py`, `python generate_audio.py`, rồi `gradle :app:assembleDebug :app:lintDebug` với JDK 17 / Gradle 8.9 / Android SDK 35. `course.json` trong APK được sinh bởi quy trình này; file nền trong Git không chứa toàn bộ dữ liệu mở rộng.

CI xác nhận 1.000 mục bổ sung không trùng, 40 bài ngữ pháp, đáp án bài tập, audio đầy đủ, chữ ký APK, và Android Lint. APK ký debug dùng để tự luyện; chưa phát hành Play Store và chưa kiểm thử trên điện thoại thật.

Khóa ký phát triển bản 2 được tạo ở đường dẫn riêng và lưu cache trong GitHub Actions; không đưa vào Git. Cache có thể bị hết hạn; khi cập nhật sau này phải kiểm tra chữ ký trước.

## Nguồn ngữ pháp bổ sung

How to Study Korean, bài 1, 2, 3, 4, 6, 8, 12, 17. Chỉ tham khảo quy tắc, giải thích tiếng Việt được biên soạn lại; ví dụ, bài tập nhà máy và hội thoại viết mới. Không phân phối bài học hoặc audio gốc. Xem `course_additions.py` để biết nguồn của từng bài.

Kiểm tra phát hành 2.1: `python validate_release.py APK_PATH` xác minh toàn bộ tham chiếu audio, các câu hỏi, nguồn bài bổ sung và đo bằng ffprobe thời lượng của từng hội thoại nằm trong 10–15 giây. Android Lint và chữ ký được kiểm tra trong CI. Chưa kiểm thử trên điện thoại thật.

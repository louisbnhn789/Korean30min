"""Source-reviewed grammar summaries and original workplace dialogues, release 2.1.
No third-party audio or verbatim lesson text is redistributed.
Chinese supplementary summaries: CC BY-NC-SA 3.0, adapted from credited sources.
"""
import hashlib

CHINESE_BASE = 'https://human.libretexts.org/Bookshelves/Languages/Chinese/CHN101_Elementary_Mandarin_I_Textbook/'
ZH_SOURCES = [
 ('Basic sentence order','03:_Origins_and_Language/3.05:_Lesson_2_Grammar_-_Basic_sentence_order'),
 ('Connecting nouns with 是','02:_First_Contact/2.06:_Lesson_1_Grammar_-_Connecting_Nouns_with_the_Verb__(shi)'),
 ('Expressing belonging with 的','02:_First_Contact/2.07:_Lesson_1_Grammar_-_Expressing_Belongingwith__(de)'),
 ('Questions ending with 呢','02:_First_Contact/2.08:_Lesson_1_Grammar_-_Questions_Ending_with_(ne)'),
 ('Question pronouns','02:_First_Contact/2.09:_Lesson_1_Grammar_-_Question_Pronouns'),
 ('Location with 在 before verbs','03:_Origins_and_Language/3.06:_Lesson_2_Grammar_-_Indicating_location_with__(zai)_before_verbs'),
 ('Standard negation with 不','03:_Origins_and_Language/3.07:_Lesson_2_Grammar_-_Standard_negation_with__(bu)'),
 ('Yes-no questions with 吗','03:_Origins_and_Language/3.08:_Lesson_2_Grammar_-_Yes-no_questions_with_ma'),
]
KO_SOURCES = [
 ('Basic Korean sentences','unit1/unit-1-lessons-1-8/unit-1-lesson-1/'),
 ('Particles 이/가 and 있다','unit1/unit-1-lessons-1-8/unit-1-lesson-2/'),
 ('Possessive particle 의','unit1/unit-1-lessons-1-8/unit-1-lesson-3/'),
 ('Adjectives before nouns','unit1/unit-1-lessons-1-8/unit-1-lesson-4/'),
 ('Polite and formal endings','unit1/unit-1-lessons-1-8/unit-1-lesson-6/'),
 ('Negative sentences','unit1/unit-1-lessons-1-8/unit-1-lesson-8/'),
 ('Location and destination particles','unit1/unit-1-lessons-9-16/lesson-12/'),
 ('Connecting clauses with 고','unit1/unit-1-lessons-17-25-2/lesson-17/'),
]

# Each row: title, pattern, summary, common error, two contextual cloze examples.
ZH_GRAMMAR = [
 ('Báo cáo rõ ai làm gì','Người + động từ + đối tượng',
  'Trong câu kể cơ bản, đặt người làm trước hành động và vật được xử lý sau hành động. Dùng câu ngắn để báo cáo trách nhiệm; thời gian có thể đứng đầu câu. Ví dụ dưới đây áp dụng nguyên tắc của nguồn vào trao đổi trong nhà máy.',
  'Đừng đảo sản phẩm lên trước động từ trong mẫu SVO cơ bản; cấu trúc chủ đề hóa và 把 cần học riêng.',
  '技术员[检查]设备。~Kỹ thuật viên kiểm tra thiết bị.~设备~技术员',
  '仓库[准备]材料。~Kho chuẩn bị vật liệu.~材料~仓库'),
 ('Phân loại sản phẩm bằng 是','A + 是 + B; A + 不是 + B',
  'Dùng 是 khi xác định một người hoặc vật thuộc loại nào. Phủ định bằng 不是. Khi chỉ mô tả tính chất, không tự động thêm 是: câu phân loại và câu tính từ là hai mẫu khác nhau.',
  'Đừng dùng 产品是好 để thay cho câu miêu tả 产品很好.',
  '这是[合格品]。~Đây là sản phẩm đạt.~检查~很',
  '这不是[标准样品]。~Đây không phải mẫu chuẩn.~完成~正在'),
 ('Xác định tài liệu thuộc về ai','Người/đơn vị + 的 + vật/tài liệu',
  'Đặt bên sở hữu trước 的 và tài liệu hoặc vật phía sau. Cụm sở hữu này có thể làm chủ ngữ hoặc tân ngữ. Giữ rõ đơn vị sở hữu khi có nhiều bản vẽ, tiêu chuẩn hoặc mẫu của các khách hàng.',
  '客户的图纸 là bản vẽ của khách hàng; không đảo thành 图纸的客户.',
  '请看客户[的]图纸。~Hãy xem bản vẽ của khách hàng.~在~不',
  '这是供应商[的]报告。~Đây là báo cáo của nhà cung cấp.~吗~呢'),
 ('Hỏi tiếp khi bàn giao bằng 呢','Chủ đề đang hỏi + 呢？',
  '呢 giúp hỏi tiếp cùng một vấn đề đã được xác lập trong trao đổi. Nếu câu trước nói về tiến độ kiểm tra, hỏi 第二批呢？ được hiểu là hỏi tiến độ lô thứ hai. Ngữ cảnh quyết định thông tin đang hỏi.',
  'Không dùng 呢 để thay cho 吗 trong mọi câu hỏi có/không.',
  '第一批检查完了，第二批[呢]？~Lô đầu đã kiểm tra xong, còn lô thứ hai thì sao?~的~把',
  '我的报告在这里，你的报告[呢]？~Báo cáo của tôi ở đây, còn báo cáo của bạn đâu?~得~不'),
 ('Hỏi đúng người, vật và thời điểm','谁 / 什么 / 什么时候 ở vị trí cần hỏi',
  'Giữ trật tự câu như câu kể và thay phần chưa biết bằng từ hỏi. 谁 hỏi người, 什么 hỏi vật hoặc nội dung, 什么时候 hỏi thời điểm. Câu hỏi thông tin thông thường không thêm 吗 ở cuối.',
  'Đừng ghép 谁 với 吗 khi chỉ muốn hỏi ai chịu trách nhiệm.',
  '[谁]检查这个批次？~Ai kiểm tra lô này?~什么~哪里',
  '我们[什么时候]开会？~Khi nào chúng ta họp?~谁~什么'),
 ('Nêu nơi kiểm tra trước hành động','Người + 在 + địa điểm + động từ + vật',
  'Khi nói hành động diễn ra ở đâu, đặt 在 và địa điểm trước động từ. Mẫu này khác câu chỉ vị trí như 材料在仓库: mẫu thứ nhất nói nơi thực hiện việc, mẫu thứ hai nói vật đang ở đâu.',
  'Không bê nguyên thứ tự tiếng Việt sang thành 我检查样品在实验室 trong bài cơ bản này.',
  '我们[在实验室]检查样品。~Chúng tôi kiểm tra mẫu trong phòng thí nghiệm.~实验室在~检查在',
  '技术员[在车间]修理设备。~Kỹ thuật viên sửa thiết bị tại xưởng.~车间在~修理在'),
 ('Phủ định thói quen và ý định bằng 不','Người + 不 + động từ/tính từ',
  '不 đứng trước động từ hoặc tính từ để phủ định lựa chọn, thói quen hoặc trạng thái phù hợp. Trong báo cáo, phân biệt không làm theo lựa chọn với việc chưa xảy ra; bài nguồn này tập trung vào 不.',
  'Không dùng 不 để thay mọi dạng phủ định: chưa nhận vật liệu cần 没收到, không phải 不收到.',
  '我们[不]使用旧图纸。~Chúng tôi không dùng bản vẽ cũ.~的~吗',
  '这个办法[不]合适。~Cách này không phù hợp.~是~在'),
 ('Xác nhận có/không bằng 吗','Câu kể + 吗？',
  'Giữ nguyên câu kể rồi thêm 吗 để hỏi có/không. Đáp lại bằng nội dung hoặc động từ phù hợp, chẳng hạn 可以/不可以 hoặc 是/不是; tránh coi mọi câu trả lời đều là 是.',
  'Câu đã dùng 谁/什么 để hỏi thông tin không tự động thêm 吗.',
  '可以开始检查[吗]？~Có thể bắt đầu kiểm tra không?~谁~什么',
  '这是最新图纸[吗]？~Đây là bản vẽ mới nhất phải không?~哪里~多少'),
]

KO_GRAMMAR = [
 ('Báo cáo rõ chủ thể và đối tượng','Chủ thể + đối tượng 을/를 + vị ngữ',
  'Trong mẫu cơ bản, vị ngữ tiếng Hàn đứng cuối câu. 을 theo danh từ có phụ âm cuối, 를 theo danh từ kết thúc bằng nguyên âm. Khi báo cáo trách nhiệm, nêu người làm nếu ngữ cảnh chưa rõ. Ví dụ được viết mới cho môi trường nhà máy.',
  'Đừng giữ trật tự tiếng Việt bằng cách đặt động từ trước đối tượng.',
  '저는 자재[를] 확인합니다.~Tôi kiểm tra vật liệu.~을~가',
  '기술자는 장비[를] 점검합니다.~Kỹ thuật viên kiểm tra thiết bị.~을~은'),
 ('Có vật và vật đang ở đâu','Vật + 이/가 + 있다; nơi + 에 + 있다',
  '있다 diễn đạt có hoặc tồn tại tại một nơi. Vật được nói là có đi với 이/가, không dùng 을/를 như tân ngữ của động từ hành động. Với vị trí tồn tại, địa điểm đi với 에.',
  '샘플을 있습니다 là sai trong nghĩa có mẫu; dùng 샘플이 있습니다.',
  '표준 샘플[이] 있습니다.~Có mẫu chuẩn.~을~를',
  '자재는 창고[에] 있습니다.~Vật liệu ở trong kho.~를~가'),
 ('Làm rõ chủ sở hữu bằng 의','Chủ sở hữu + 의 + danh từ',
  '의 nối bên sở hữu với vật hoặc tài liệu. 저의 thường rút thành 제. Trong báo cáo có nhiều khách hàng hoặc nhà cung cấp, ghi rõ chủ sở hữu giúp tránh nhầm tài liệu.',
  'Không đảo 순서 thành 도면의 고객 khi muốn nói bản vẽ của khách hàng.',
  '고객[의] 도면을 확인합니다.~Tôi kiểm tra bản vẽ của khách hàng.~에~를',
  '[제] 보고서를 보냈습니다.~Tôi đã gửi báo cáo của mình.~제가~저를'),
 ('Miêu tả linh kiện trước danh từ','Tính từ bỏ 다 + ㄴ/은 + danh từ',
  'Tính từ làm vị ngữ và tính từ đứng trước danh từ có dạng khác nhau. Thân kết thúc bằng nguyên âm thường thêm ㄴ; thân có phụ âm thường thêm 은. Ví dụ: 크다 → 큰, 작다 → 작은. Các trường hợp bất quy tắc phải học riêng.',
  'Không viết 크다 부품 để nói linh kiện lớn; dạng trước danh từ là 큰 부품.',
  '[작은] 부품을 확인합니다.~Tôi kiểm tra linh kiện nhỏ.~작다~작습니다',
  '[큰] 상자가 필요합니다.~Cần thùng lớn.~크다~큽니다'),
 ('Chọn đuôi lịch sự khi báo cáo','아요/어요 trong trao đổi; ㅂ니다/습니다 trong báo cáo',
  '아요/어요 là dạng lịch sự phổ biến trong hội thoại. ㅂ니다/습니다 phù hợp báo cáo trang trọng: thân có nguyên âm thêm ㅂ니다, có phụ âm thêm 습니다. Cả hai thể hiện lịch sự; chọn theo người nghe và tình huống.',
  'Đừng thêm đuôi vào nguyên mẫu còn 다. 하다 → 해요 hoặc 합니다.',
  '수량을 [확인합니다].~Tôi kiểm tra số lượng, giọng báo cáo trang trọng.~확인하다습니다~확인하니다',
  '도면을 [봐요].~Tôi xem bản vẽ, giọng trao đổi lịch sự.~보다요~보요'),
 ('Không làm: 안 và 지 않다','안 + hành động; thân + 지 않다',
  'Hai dạng này phủ định hành động hoặc tính chất. Với nhiều động từ danh từ + 하다, dạng ngắn thường đặt 안 trước 하다: 검사 안 합니다. Dạng dài 검사하지 않습니다 thuận tiện cho câu báo cáo.',
  'Không tách một tính từ kết thúc bằng 하다 như thể nó luôn là danh từ + hành động.',
  '이 자재는 사용하지 [않습니다].~Chúng tôi không sử dụng vật liệu này.~있습니다~합니다',
  '오늘은 잔업을 [안 합니다].~Hôm nay không tăng ca.~했습니다~하겠습니다'),
 ('Phân biệt nơi làm việc và đích đến','Nơi làm hành động + 에서; đích đến + 에',
  '에서 đánh dấu nơi một hành động diễn ra. 에 thường dùng với đích đến và vị trí tồn tại. Chọn tiểu từ theo vị ngữ: kiểm tra ở phòng thí nghiệm dùng 에서, đi đến kho dùng 에.',
  'Không dùng một tiểu từ duy nhất cho cả kiểm tra tại kho và đi đến kho.',
  '실험실[에서] 검사합니다.~Tôi kiểm tra tại phòng thí nghiệm.~에~를',
  '창고[에] 갑니다.~Tôi đi đến kho.~에서~를'),
 ('Nối thao tác bằng 고','Thân động từ + 고 + mệnh đề sau',
  '고 nối các hành động hoặc trạng thái. Tùy ngữ cảnh, nó có thể là và hoặc rồi. Muốn nhấn mạnh sau khi xong thao tác đầu, dùng 고 나서. Trong hướng dẫn, nêu đối tượng rõ để người nghe biết hai việc nối với nhau.',
  'Không tự hiểu mọi 고 là nguyên nhân; để nói vì cần cấu trúc chỉ lý do khác.',
  '수량을 확인하[고] 기록합니다.~Tôi kiểm tra số lượng rồi ghi lại.~면~지만',
  '검사하[고 나서] 포장합니다.~Sau khi kiểm tra xong tôi đóng gói.~기 전에~려고'),
]

# title | Vietnamese context | four alternating turns; h~Vietnamese
ZH_DIALOGUES = '''Nhận ca|Bàn giao ca sản xuất|早上好，今天生产什么？~Chào buổi sáng, hôm nay sản xuất gì?|今天生产这个型号。~Hôm nay sản xuất model này.|材料都准备好了吗？~Vật liệu đã chuẩn bị đầy đủ chưa?|准备好了，可以开始。~Đã chuẩn bị xong, có thể bắt đầu.
Vật liệu mới đến|Thông báo cho IQC trước khi sử dụng|这批材料已经到了。~Lô vật liệu này đã đến.|通知进料检验了吗？~Đã báo bộ phận kiểm tra đầu vào chưa?|还没有，我马上通知。~Chưa, tôi sẽ báo ngay.|请先检验，再使用。~Hãy kiểm tra trước rồi mới sử dụng.
Báo lỗi ngoại quan|Báo vết xước và tách sản phẩm|这个产品有划伤。~Sản phẩm này có vết xước.|发现了多少个？~Đã phát hiện bao nhiêu cái?|发现了五个，已隔离。~Phát hiện năm cái, đã cách ly.|好的，请记录批次。~Được, hãy ghi lại lô.
Đo kích thước|Xác nhận bản vẽ trước khi đo|这个尺寸要怎么测？~Kích thước này cần đo thế nào?|请按照最新图纸测量。~Hãy đo theo bản vẽ mới nhất.|量具已经校准了吗？~Dụng cụ đo đã được hiệu chuẩn chưa?|已经校准，可以使用。~Đã hiệu chuẩn, có thể sử dụng.
Máy dừng|Báo bảo trì và chờ xác nhận|设备突然停了。~Thiết bị đột nhiên dừng.|已经通知维修了吗？~Đã báo bảo trì chưa?|通知了，他们马上来。~Đã báo, họ sẽ đến ngay.|先等维修人员确认。~Trước hết chờ nhân viên bảo trì xác nhận.
Thử độ tin cậy|Hỏi tiến độ và thời điểm báo cáo|测试结束了吗？~Thử nghiệm đã kết thúc chưa?|还没有，还需要两小时。~Chưa, còn cần hai giờ.|结束后请把结果发给我。~Kết thúc hãy gửi kết quả cho tôi.|好的，我会及时报告。~Được, tôi sẽ báo cáo kịp thời.
Kiểm tra trước xuất hàng|Chỉ xác nhận khi có kết quả|这批货可以出货了吗？~Lô hàng này có thể xuất chưa?|还要等最后的检验结果。~Vẫn phải chờ kết quả kiểm tra cuối.|结果什么时候出来？~Khi nào có kết quả?|下午三点，我会通知你。~Ba giờ chiều, tôi sẽ báo bạn.
Tìm vật liệu trong kho|Hỏi vị trí và xác nhận mã|这个材料放在哪里？~Vật liệu này đặt ở đâu?|在仓库右边的货架上。~Ở trên giá phía bên phải của kho.|是这个料号吗？~Có phải mã vật liệu này không?|对，请再核对数量。~Đúng, hãy đối chiếu thêm số lượng.
Kiểm tra đóng gói|Xác nhận nhãn và số lượng|包装检查完成了吗？~Kiểm tra đóng gói đã xong chưa?|完成了，标签没有问题。~Đã xong, nhãn không có vấn đề.|数量也核对了吗？~Số lượng cũng đã đối chiếu chưa?|核对了，请确认记录。~Đã đối chiếu, hãy xác nhận hồ sơ.
Nhờ gửi báo cáo|Yêu cầu thời hạn và dữ liệu|请把今天的报告发给我。~Hãy gửi báo cáo hôm nay cho tôi.|好的，需要附上照片吗？~Được, có cần đính kèm ảnh không?|需要，也请附上数据。~Có, cũng hãy đính kèm dữ liệu.|明白，下班前发给你。~Đã rõ, tôi sẽ gửi trước khi tan ca.
Chuẩn bị họp|Xác nhận thời gian và tài liệu|今天几点开质量会议？~Hôm nay mấy giờ họp chất lượng?|下午两点，在会议室。~Hai giờ chiều, tại phòng họp.|需要准备什么资料？~Cần chuẩn bị tài liệu gì?|请带上不良分析报告。~Hãy mang theo báo cáo phân tích lỗi.
Làm việc với nhà cung cấp|Xin phản hồi và kế hoạch cải tiến|这次的不良原因是什么？~Nguyên nhân lỗi lần này là gì?|我们还在调查原因。~Chúng tôi vẫn đang điều tra nguyên nhân.|明天能给改善计划吗？~Ngày mai có thể gửi kế hoạch cải tiến không?|可以，我们会按时回复。~Có thể, chúng tôi sẽ phản hồi đúng hạn.
Thiếu jig|Báo điều kiện chưa đáp ứng|现在可以测量吗？~Bây giờ có thể đo không?|还不行，我们没有治具。~Chưa được, chúng tôi không có jig.|请联系工程师确认。~Hãy liên hệ kỹ sư để xác nhận.|好的，确认后再安排。~Được, xác nhận xong sẽ sắp xếp.
Mẫu chuẩn|Đối chiếu mẫu trước khi đánh giá|这个是标准样品吗？~Đây có phải mẫu chuẩn không?|是，请先核对编号。~Đúng, hãy đối chiếu số hiệu trước.|编号正确，可以比较。~Số hiệu đúng, có thể so sánh.|发现差异请马上报告。~Nếu phát hiện khác biệt hãy báo ngay.
Xin nhắc lại|Giao tiếp khi chưa nghe rõ|对不起，我没听清楚。~Xin lỗi, tôi chưa nghe rõ.|我说先检查这个批次。~Tôi nói kiểm tra lô này trước.|请再说慢一点。~Xin nói lại chậm hơn một chút.|好的，先检查，再记录。~Được, kiểm tra trước rồi ghi lại.
Bàn giao công việc|Nêu phần đã xong và phần cần làm|今天的检查做完了吗？~Kiểm tra hôm nay đã làm xong chưa?|做完了，记录在这里。~Đã xong, hồ sơ ở đây.|下一班还需要做什么？~Ca tiếp theo còn cần làm gì?|请继续检查第二批。~Hãy tiếp tục kiểm tra lô thứ hai。'''

KO_DIALOGUES = '''Nhận ca|Bàn giao ca sản xuất|오늘은 어떤 모델을 생산해요?~Hôm nay sản xuất model nào?|이 모델을 생산해요.~Sản xuất model này.|자재는 준비됐나요?~Vật liệu đã chuẩn bị chưa?|네, 준비됐어요. 시작하세요.~Vâng, đã chuẩn bị. Hãy bắt đầu.
Vật liệu mới đến|Thông báo kiểm tra đầu vào|자재가 도착했어요.~Vật liệu đã đến.|수입 검사팀에 알렸나요?~Đã báo nhóm kiểm tra đầu vào chưa?|아직요. 바로 알릴게요.~Chưa. Tôi sẽ báo ngay.|검사 후에 사용해 주세요.~Hãy sử dụng sau khi kiểm tra.
Báo lỗi ngoại quan|Báo vết xước và tách sản phẩm|제품에 흠집이 있어요.~Sản phẩm có vết xước.|몇 개 발견했어요?~Đã phát hiện bao nhiêu cái?|다섯 개요. 격리했어요.~Năm cái. Đã cách ly.|네, 로트 번호를 기록하세요.~Vâng, hãy ghi số lô.
Đo kích thước|Xác nhận bản vẽ và hiệu chuẩn|치수는 어떻게 측정해요?~Đo kích thước thế nào?|최신 도면을 보세요.~Hãy xem bản vẽ mới nhất.|측정기는 교정됐나요?~Thiết bị đo đã hiệu chuẩn chưa?|네, 교정됐어요. 사용하세요.~Vâng, đã hiệu chuẩn. Hãy sử dụng.
Máy dừng|Báo bảo trì và chờ xác nhận|설비가 갑자기 멈췄어요.~Thiết bị đột nhiên dừng.|보전팀에 연락했나요?~Đã liên hệ nhóm bảo trì chưa?|네, 곧 올 거예요.~Vâng, họ sẽ đến sớm.|먼저 확인을 기다리세요.~Trước hết hãy chờ xác nhận.
Thử độ tin cậy|Hỏi tiến độ thử nghiệm|시험이 끝났나요?~Thử nghiệm đã kết thúc chưa?|아직요. 두 시간 더 필요해요.~Chưa. Cần thêm hai giờ.|끝나면 결과를 알려 주세요.~Kết thúc hãy báo kết quả.|네, 바로 보고할게요.~Vâng, tôi sẽ báo cáo ngay.
Kiểm tra trước xuất hàng|Chờ kết quả kiểm tra cuối|이 로트는 출하해도 돼요?~Lô này xuất hàng được chưa?|최종 검사 결과를 기다려요.~Đang chờ kết quả kiểm tra cuối.|결과는 언제 나오나요?~Khi nào có kết quả?|오후 세 시요. 알려 드릴게요.~Ba giờ chiều. Tôi sẽ báo anh/chị.
Tìm vật liệu trong kho|Hỏi vị trí và đối chiếu mã|이 자재는 어디에 있어요?~Vật liệu này ở đâu?|창고 오른쪽 선반에 있어요.~Ở trên giá bên phải của kho.|이 자재 번호가 맞나요?~Mã vật liệu này đúng không?|네, 수량도 확인하세요.~Vâng, cũng hãy kiểm tra số lượng.
Kiểm tra đóng gói|Xác nhận nhãn và số lượng|포장 검사는 끝났나요?~Kiểm tra đóng gói đã xong chưa?|네, 라벨도 맞아요.~Vâng, nhãn cũng đúng.|수량도 확인했나요?~Số lượng cũng đã kiểm tra chưa?|네, 기록을 확인해 주세요.~Vâng, hãy xác nhận hồ sơ.
Nhờ gửi báo cáo|Xác nhận ảnh và dữ liệu|오늘 보고서를 보내 주세요.~Hãy gửi báo cáo hôm nay.|사진도 필요하세요?~Anh/chị cũng cần ảnh không?|네, 데이터도 넣어 주세요.~Vâng, cũng hãy thêm dữ liệu.|네, 퇴근 전에 보낼게요.~Vâng, tôi sẽ gửi trước khi tan ca.
Chuẩn bị họp|Xác nhận giờ và tài liệu|품질 회의는 몇 시예요?~Họp chất lượng mấy giờ?|오후 두 시예요.~Hai giờ chiều.|어떤 자료를 준비해요?~Cần chuẩn bị tài liệu gì?|불량 분석 보고서를 가져오세요.~Hãy mang báo cáo phân tích lỗi.
Làm việc với nhà cung cấp|Xin phản hồi cải tiến|불량 원인이 뭔가요?~Nguyên nhân lỗi là gì?|아직 조사 중입니다.~Chúng tôi vẫn đang điều tra.|내일 개선 계획을 주세요.~Ngày mai hãy gửi kế hoạch cải tiến.|네, 제시간에 회신하겠습니다.~Vâng, chúng tôi sẽ phản hồi đúng hạn.
Thiếu jig|Báo điều kiện đo chưa đáp ứng|지금 측정할 수 있어요?~Bây giờ có thể đo không?|아니요, 지그가 없어요.~Không, không có jig.|엔지니어에게 확인해 주세요.~Hãy xác nhận với kỹ sư.|네, 확인 후에 진행할게요.~Vâng, tôi sẽ thực hiện sau khi xác nhận.
Mẫu chuẩn|Đối chiếu mẫu trước đánh giá|이게 표준 샘플인가요?~Đây có phải mẫu chuẩn không?|네, 번호를 확인하세요.~Vâng, hãy kiểm tra số hiệu.|번호가 맞아요. 비교할게요.~Số hiệu đúng. Tôi sẽ so sánh.|차이가 있으면 알려 주세요.~Nếu có khác biệt hãy báo.
Xin nhắc lại|Giao tiếp khi chưa nghe rõ|죄송해요, 잘 못 들었어요.~Xin lỗi, tôi chưa nghe rõ.|이 로트를 먼저 검사하세요.~Hãy kiểm tra lô này trước.|좀 천천히 말씀해 주세요.~Xin nói chậm hơn một chút.|네, 검사하고 기록하세요.~Vâng, hãy kiểm tra rồi ghi lại.
Bàn giao công việc|Nêu việc đã xong và còn lại|오늘 검사는 끝났나요?~Kiểm tra hôm nay đã xong chưa?|네, 기록은 여기 있어요.~Vâng, hồ sơ ở đây.|다음 조는 뭘 해야 해요?~Ca tiếp theo cần làm gì?|두 번째 로트를 검사하세요.~Hãy kiểm tra lô thứ hai.'''

def aid(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def additions(lang, parse, pinyin):
    rows = ZH_GRAMMAR if lang == 'zh' else KO_GRAMMAR
    grammar = parse('\n'.join('|'.join(row) for row in rows))
    sources = []
    for index, ((title, path), lesson) in enumerate(zip(ZH_SOURCES if lang == 'zh' else KO_SOURCES, grammar)):
        source = dict(id='source-'+str(index+1), title=title,
            publisher="Carl Polley / Kapi'olani Community College · LibreTexts; tham khảo Chinese Grammar Wiki / AllSet Learning" if lang == 'zh' else 'How to Study Korean · tài liệu do tác giả xuất bản',
            url=(CHINESE_BASE if lang == 'zh' else 'https://www.howtostudykorean.com/')+path,
            reviewed='2026-10-06',
            note='Tóm tắt tiếng Việt và ví dụ nhà máy được biên soạn lại; không chép nguyên bài hoặc dùng audio của nguồn.',
            license='Phần tóm tắt ngữ pháp bổ sung: CC BY-NC-SA 3.0; ví dụ áp dụng viết mới.' if lang == 'zh' else 'Nguồn giữ bản quyền. Chỉ tham khảo quy tắc; không phân phối bài gốc hoặc audio gốc.')
        sources.append(source)
        lesson.update(id=41+index, level='Áp dụng · có nguồn tham khảo', source=source, sourced=True)
        for ex in lesson['examples']:
            ex.update(a=aid(ex['h']), p=pinyin(ex['h']))
    dialogues = []
    raw = ZH_DIALOGUES if lang == 'zh' else KO_DIALOGUES
    for index, row in enumerate(raw.strip().splitlines()):
        title, context, *utterances = row.split('|')
        turns = []
        for turn_index, utterance in enumerate(utterances):
            native, meaning = utterance.split('~')
            turns.append(dict(speaker='A' if turn_index%2==0 else 'B', h=native, v=meaning, p=pinyin(native), a=aid('dialogue-turn-v1:'+lang+':'+native)))
        assert len(turns)==4
        full = ' '.join(t['h'] for t in turns)
        dialogues.append(dict(id=index+1,title=title,context=context,turns=turns,
            h=full,a=aid('dialogue-full-v1:'+lang+':'+full),durationSeconds=0,
            note='Nghe toàn đoạn → nghe từng lượt → đóng vai A hoặc B và ghi âm. Hội thoại và bản dịch tự biên soạn cho công việc trong nhà máy.'))
    assert len(grammar)==8 and len(dialogues)==16
    return grammar, sources, dialogues

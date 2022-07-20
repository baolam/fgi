# Nghiên cứu về FGI (Feature graph information)

## 1.Hiểu về FGI, cơ sở lý thuyết và ý nghĩa tên
- Tên gọi khác của FGI là đồ thị thông tin đặc trưng.
- FGI lấy ý tưởng từ cách tư duy của con người và 3 thuyết về não bộ và cấu tạo thông tin là cơ sở để hình thành FGI.

## 2.Ba thuyết về não bộ và cấu tạo thông tin
* Não bộ con người không lưu trữ trực tiếp thông tin mà là lưu trữ các đặc trưng (tính chất) của thông tin. _(1)_
* Một thông tin, một sự vật, hiện tượng bất kỳ sẽ được cấu thành từ tập hợp của các đặc trưng thông tin khác (được hiểu là tập hợp các tính chất). Thường gọi là **bản chất** _(2)_
* Một đặc trưng (tính chất) sẽ biểu diễn duy nhất cho 1 sự vật, hiện tượng và ngược lại. _(3)_

## 3.Phát sinh
**Vấn đề 1:** FGI phát sinh từ bài toán huấn luyện mô hình tự động trong các tác vụ AI. Bài toán này có thể giải quyết dựa trên lập lịch huấn luyện mô hình nhưng mỗi lần huấn luyện là phải cài lại toàn bộ tập dữ liệu gây tốn thời gian. 
**Vấn đề 2:** Con người được biết đến với khả năng tư duy rất tốt trong đa lĩnh vực. Liệu AI có thể vượt mặt con người trong điều này không? - FGI sinh ra sẽ thử trả lời câu hỏi này

## 4.Phân rã và biểu diễn thông tin
Dựa theo thuyết số **2** . Khi áp dụng để phân rã 1 sự vật hiện tượng, ta sẽ có 1 tập các tính chất của sự vật, hiện tượng đó. Do tính chất cũng là đặc trưng mà đặc trưng sẽ biểu diễn cho 1 sự vật hiện tượng (thuyết số **3**). Điều này đồng nghĩa với việc nếu ta tiếp tục áp dụng phân rã lên tập các tính chất đó, ta sẽ có 1 tập các tính chất khác. Nếu quá trình này tiếp tục tiếp diễn thì khi biểu diễn sẽ hình thành nên một đồ thị. 
> Tên gọi đồ thị thông tin đặc trưng (FGI) xuất phát từ đây :>

## 5. Tiềm năng của FGI

### 5.1.Ý nghĩa của thuyết trong phân loại
Dựa theo thuyết số **3** trong 3 thuyết về não bộ và cấu tạo thông tin thì phân loại một sự vật, hiện tượng thật chất là quá trình xác định tồn tại tính chất của sự vật, hiện tượng đó không.
> FGI có thể áp dụng trong các bài toán classification. 

### 5.2.Ý nghĩa của thuyết trong xử lý ngôn ngữ tự nhiên
Bản thân 1 từ ngữ cũng ẩn chứa trong đó 1 tính chất nào đó. Theo thuyết **1** và thuyết **3** thì từ ngữ sinh ra nhằm mục đích là phân biệt tính chất sự việc này với tính chất sự việc khác. 
> Điều này đồng nghĩa với việc FGI có thể áp dụng cho bài toán liên quan đến NLP.

### 5.3.Ý nghĩa của phân rã và biểu diễn thông tin trong điều khiển
FGI được dùng để biểu diễn mối quan hệ qua lại của các tính chất với nhau và được cài đặt sao cho có thể xác định sự tồn tại của 1 tính chất nào đó. Nếu gắn 1 hành động nào đó cho tính chất, thì khi tính chất đó thỏa mãn thì hành động cũng sẽ được thực thi
> Điều nay đặc biệt có ý nghĩa trong khả năng áp dụng FGI trong điều khiển. 

## 6.Thiết kế mô hình
> Việc thiết kế mô hình sẽ thỏa mãn một số tiêu chí sau:
* Mô hình phải có khả năng tự mở rộng, đầu ra không bị fit cứng (giống mô hình truyền thống)
* Mô hình có khả năng xử lý nhiều loại dữ liệu khác nhau
>> Nghiên cứu này nhằm mục đích phục vụ cho bài toán **Nông nghiệp thế hệ mới** với mục tiêu tạo ra một chuyên gia ảo trong lĩnh vực này.

### 6.1.Dữ liệu đầu vào
Mô hình có khả năng xử lý trên 2 kiểu dữ liệu chính:
- Hình ảnh
- Ngôn ngữ

### 6.2.Dữ liệu đầu ra
Tùy vào cách sử dụng nhưng sẽ có 2 kiểu chính:
- Hiểu biết của hệ thống (trình bày dưới dạng ngôn ngữ) đối với ảnh hoặc ngôn ngữ đầu vào. (__t1__).

>> **__Luồng xử lý chung:__**
> Đặc trưng (biểu diễn) -> Lan truyền trong mô hình -> Lưu vết đường đi -> Trả về kết quả lưu vết
- Xác định xem đầu vào có tồn tại một tính chất gì đó không để phục vụ các nhiệm vụ khác. (__t2__).

>> **__Luồng xử lý chung:__**
> Đặc trưng muốn xác định (biểu diễn) + Truy vấn (có thể là từ ngữ hoặc đặc trưng) -> Xử lý truy vấn, xác định tính chất -> Lan truyền tính chất -> Trả về kết quả.

>> **Mối liên hệ giữa 2 bài toán đã nêu:** Theo ý nghĩa của FGI đối với xử lý ngôn ngữ tự nhiên thì việc lan truyền giải quyết bài toán __t1__ thật chất là xác định 1 chuỗi các tính chất thỏa mãn của từ ngữ (bài toán __t2__). Điều này đồng nghĩa với việc bài toán __t2__ là cơ sở để giải quyết bài toán __t1__.

### 6.3.Nghiên cứu về cấu tạo của một đơn vị tính chất
Một đơn vị tính chất được xem là một đỉnh trong FGI. Như vậy bài toán này trở thành nghiên cứu cấu tạo của 1 đỉnh tính chất.

#### 6.3.1.Nghiên cứu về biểu diễn tính chất
Dựa vào bài toán __t2__ thì một tính chất sẽ gồm một bộ phận có chức năng xác định có tồn tại tính chất hay không. Bám theo thuyết __3__ về não bộ và thông tin thì cần một đại diện để biểu diễn tính chất này. Tạm gọi tính chất này là **(n)** và **(n)** thuộc không gian số thực có kích thước **da** chiều. Tập hợp các **(n)** sẽ được gọi lại thành không gian tính chất.
> Dựa theo tư duy này thì sẽ phát sinh một bài toán **Biểu diễn đầu vào trong không gian da chiều __(f)__**. 

#### 6.3.2.Nghiên cứu về cách xác định một tính chất
Một tính chất sẽ thao tác trực tiếp trên đặc trưng của đầu vào. Tạm đặt giả thuyết là số chiều của đầu vào sau quá trình __(f)__ khác với số chiều của **__(n)__**. Thì bài toán cần giải quyết đó là "Làm sao để đưa tính chất **(n)** vào đầu vào?". Bài toán này thật ra là bài toán **Nhúng tính chất (n) vào đầu vào**.

##### 6.3.2.1.Giải quyết bài toán nhúng tính chất (n).
Có khá nhiều giải pháp để giải quyết bài toán này. Với nghiên cứu hiện tại, tôi đặt giả thuyết là số chiều đầu vào cùng chiều của không gian tính chất. Thì công thức nhúng tính chất vào đầu vào dạng đơn giản là:
  <img src="/imgs/nhung-tinh-chat.png" width="1000px" height="500px">

Sau khi đã giải quyết bài toán trên thì bài toán còn lại là xác định trong đầu vào có tính chất (n) hay không?
##### 6.3.2.2.Giải bài toán xác định tồn tại tính chất (n)
Sử dụng một mạng truyền thẳng gồm 2 lớp với đầu ra là hàm sigmoid
  <img src="/imgs/ton-tai-tinh-chat.png" width="1000px" height="500px">

> Cách nghiên cứu xác định một tính chất này rất giống với cơ chế tự chú ý của con người. Chú ý là quá trình tập trung vào một phần duy nhất của thông tin đầu vào để xác định có tồn tại tính chất nào đó hay không!

#### 6.3.2.3.Một số mở rộng của đỉnh
Hai bài toán trên chính là hai bộ phận cơ bản nhất của một đỉnh tính chất. Tùy từng bài toán khác nhau thì cấu trúc đỉnh này có thể khác nhau. Nếu trong bài toán điều khiển robot thì đỉnh có thể sẽ có thêm bộ phận chuyên học về cách điều khiển. Còn trong bài toán của tôi, bên cạnh có tính chất (n), tôi còn thêm một đại diện word, là từ ứng với tính chất đó (theo ý nghĩa trong xử lý ngôn ngữ tự nhiên)

### 6.4.Nghiên cứu về tương gian giữa các tính chất
Tương gian giữa các tính chất hiểu theo nghĩa là mối quan hệ giữa các tính chất. Trong FGI, những mối quan hệ này sẽ được biểu hiện bởi cạnh. Đây là một thành phần quan trọng trong đồ thị, đặc biệt có ý nghĩa trong lan truyền. 
> Cạnh trong FGI tùy vào ứng dụng khác nhau thì khác nhau. Nhưng quy về sẽ có 2 nhóm cạnh chính:

#### 6.4.1. Cạnh tính chất
Cạnh này có ý nghĩa biểu thị mối quan hệ tạo thành. Loại cạnh này trong nghiên cứu sẽ phục vụ cho tác vụ hình thành tính chất. (Là loại cạnh có hướng)

#### 6.4.2. Cạnh tương quan
Là loại cạnh biểu thị thuần cho khái niệm giữa 2 đỉnh có cạnh kết nối có mối quan hệ với nhau. Loại cạnh này đặc biệt có ý nghĩa trong làm dày tính đa dạng của mô hình (Là loại cạnh vô hướng) 

> Lý giải: Tính đa dạng ở đây hiểu theo nghĩa chính là khả năng đưa ra các phương án. Cùng một đầu vào, cách thức lan truyền khác nhau thì đầu ra khác nhau. Để làm được việc này thì cần có cạnh tương quan.

#### 6.4.3. Thành phần
Do khái niệm, mỗi cạnh biểu diễn một mối quan hệ nào đó (có thể tương quan, hoặc tạo thành). Để biểu thị sự khác nhau và tính đa dạng giữa các mối quan hệ, tôi gọi W thuộc không gian __da__ chiều là trọng số biểu thị cho tương quan đó. Cách làm này tương tự cho các tính chất.

#### 6.4.4. Một số khả năng mở rộng
Số cạnh cơ bản có 2 loại nhưng tùy vào bài toán cũng sẽ có một số loại cạnh khác nữa. Có thể sẽ có thêm loại cạnh điều kiện, cho phép lan truyền khi thỏa điều kiện nào đó.

#### 6.4.5. Bài toán lan truyền trong đồ thị
- Đặt giả thiết là mô hình có một đặc trưng đầu vào sau khi giải quyết bài toán __f__. Tạm ký hiệu đặc trưng này là __e__.
- Bài toán này nếu phát biểu theo khuynh hướng triết học chính là yêu cầu mô hình trình bày hiểu biết đối với __e__ đầu vào. Là bài toán __t1__ đã phát biểu.
- Để thuận tiện trong quá trình lan truyền, đồ thị sẽ có 2 đỉnh cơ bản gồm đỉnh bắt đầu lan truyền và đỉnh kết thúc lan truyền.
##### 6.4.5.1. Đỉnh bắt đầu lan truyền.
Đỉnh này bao gồm tập các cạnh có hướng, thể hiện tương quan tới các đỉnh lân cận.

##### 6.4.5.2. Đỉnh kết thúc lan truyền.
Đỉnh này gồm các cạnh tính chất, thể hiện mối quan hệ tạo thành.

##### 6.4.5.3. Nghiên cứu
Dựa theo ý nghĩa của FGI trong NLP, cách feedforward trong mô hình mạng truyền thống và cấu tạo của đỉnh tính chất, ta có lưu đồ thuật toán sau:
> Đặc trưng __e__ -> Qua đỉnh bắt đầu lan truyền (__e__ biến đổi) -> Tính toán xác suất chuyển đồi đỉnh -> Áp dụng giải pháp tìm kiếm đỉnh -> Lưu vết đỉnh -> Biến đổi __e__ lặp lại k lần hoặc cho tới khi gặp đỉnh kết thúc lan truyền.
- Hệ số lặp lại k có ý nghĩa là số bước lan truyền tối đa. Tránh trường hợp lan truyền tạo thành vòng lặp vô tận.

###### 6.4.5.3.1. Xác suất chuyển đổi đỉnh
__e__ sau khi qua quá trình xác định tồn tại tính chất __(n)__ sẽ tiến tới bước xác định đỉnh nào tiếp theo để đi tiếp (tức là cạnh kết nối giữa 2 đỉnh). Mỗi bài toán thì cách cài đặt xác suất chuyển đổi sẽ khác nhau. Trong bài toán ứng dụng của tôi, tôi cài mặc định softmax với chuyển đỉnh cho ra phân bố xác suất cao nhất. Ngoài ra nếu muốn nhiều phương án lựa chọn, mình có thể cài giải pháp beam search nhưng độ phức tạp có thể đạt 2^k.
Công thức chung cho 1 cạnh:
  <img src="/imgs/gia-tri-canh.png" width="1000px" height="500px">
  
#### 6.4.6. Bài toán hình thành đồ thị
Bài toán hình thành đồ thị sẽ được chia ra thành 2 bài toán con đó là:
- Bài toán hình thành cạnh đối với đỉnh chỉ định
- Bài toán hình thành đỉnh tính chất

##### 6.4.6.1. Ý nghĩa của bài toán
Việc hình thành đồ thị có ý nghĩa vô cùng quan trọng trong các bài toán đã nêu nói riêng và các vấn đề khác nói riêng. Bài toán này có ý nghĩa sống còn và là yếu tố then chốt trong cách giải quyết hai vấn đề phát sinh đã nêu.

###### 6.4.6.1.1. Ý nghĩa đối với vấn đề 1
> Tối ưu quá trình huấn luyện mô hình

Đối với bài toán này, thay vì huấn luyện trên toàn bộ tập dữ liệu, với giải pháp hình thành đồ thị phù hợp thì mô hình có thể **tối ưu lần lượt trên từng điểm dữ liệu**. Giải quyết vấn đề này sẽ có một số vấn đề phát sinh:
> Cơ chế hay cách thức hoạt động của mô hình.

> Xây dựng hàm lỗi, tính toán đối với hình thức học có thầy (Supervised Learning)

###### 6.4.6.1.2. Ý nghĩa đối với vấn đề 2
> Tư duy đa lĩnh vực

Mấu chốt để giải quyết vấn đề này đó là hình thành cách thức phối hợp các thông tin đã biết, những tri thức, lý thuyết tính chất đã học. Và đặc biệt đó là mô hình phải có khả năng mở rộng theo tính mở của dữ liệu, không xử lý theo cách tĩnh. Hay nói một cách khác đó là tính động của mô hình.

> Bài toán này liên quan mật thiết đối với hình thành đồ thị.

###### 6.4.6.1.3. Hình thành đỉnh
Hình thành đỉnh thật chất là quá trình hình thành tính chất, hình thành hiểu biết đối với thông tin hoặc đặc trưng đầu vào. 

Một đỉnh biểu thị cho một tính chất ở đầu vào nhưng nếu mình sao chép trực tiếp đặc trưng đầu vào vào quá trình hình thành đỉnh sẽ không hợp lý. Dẫn đến việc điều này không cho mô hình tạo hiểu biết đối với đầu vào, hơn thế nữa. Điều này sẽ gây bất lợi trong tính toán sau này.

> Định đề bổ sung cho vấn đề này: Nếu các tính chất, đặc trưng có yếu tố tương tự nhau (tương đồng) sẽ nằm gần nhau.

==> Không copy trực tiếp đặc trưng đầu vào. 

Để xây dựng nên tính chất đỉnh thỏa định đề bổ sung bên cạnh cần có đặc trưng đầu vào, cần có hệ các tính chất đã biết trước đó. Bài toán đặt ra cho vấn đề này đó là __làm sao để xác định các tính chất nào có tính tương tự với tính chất muốn hình thành?__

> Câu trả lời cho câu hỏi này là hệ quả của bài toán lan truyền (__t1__).
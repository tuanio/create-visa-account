Hướng dẫn sử dụng

# Cách cài đặt
1. Cài đặt Python vào máy (lên trên trang chủ python: https://www.python.org tải về).
2. Chạy `install.cmd`, xong sẽ tự tắt

# Cách sử dụng
1. Tùy chỉnh thông tin cấu hình trong file `configs.yaml`
    - url -> chosen: `vn` hoặc `usa` là vùng muốn đăng ký
    - authentication: là phần thông tin tài khoản người dùng
    - payment: là phần thông tin thẻ visa
    - waiting_time: là thời gian đợi trình duyệt load, tính bằng giây.
        Nếu đợi quá thời gian này thì chương trình sẽ tự động dừng, giá trị cao thích hợp cho mạng yếu.
        
2. Chạy bằng cách nhấn `run.cmd`

# Mutant MT

# Introduction

Xin chào, đây là phần hướng dẫn cách sử dụng cho project này. Bộ testing thuật toán dịch máy này dựa trên cơ chế so sánh câu dịch gốc với câu dịch đột biến được tạo ra bằng ngữ liệu cặp từ đồng nghĩa.

## Thành phần chính của dự án: Bộ ngữ liệu cặp từ tương đồng

### Giới thiệu về bộ ngữ liệu cặp từ tương đồng

Thành phần chính của dự án chính là bộ ngữ liệu cặp từ tương đồng, sao cho hai từ trong một cặp phải có `cosine_similarity(word_vector[word_A], word_vector[word_B]) >= threshold`, bạn sẽ phải tự điều chỉnh `threshold` sao cho bộ ngữ liệu cặp từ tương đồng này có kết quả tốt nhất có thể (thử sửa rồi chạy lại để tạo), `threshold` thường là `0.9 - 0.7`.

- Ví dụ về một bộ ngữ liệu tốt: `father|dad`, `mom|mother`, ...
- Ví dụ về một bộ ngữ liệu không tốt: `one|two`, `parents|daughter`, ...

Bạn sẽ thấy bộ ngữ liệu tốt sẽ đưa ra các cặp từ rất liên quan đến nhau, có thể sai sót một chút, nhưng miễn là có độ tương đồng cao là được (không quá nghiêm ngặt).

### Cách tạo ra bộ ngữ liệu cặp từ tương đồng

Chúng ta có 3 cách để tạo ra cặp từ tương đồng (dựa trên số code đã viết):
- 1. Dùng GloVe & SpaCy: Cả hai model GloVe & SpaCy phải có `cosine_similarity >= threshold`
- 2. Dùng Fasttext & SpaCy: Cả hai model Fasttext & SpaCy phải có `cosine_similarity >= threshold`
- 3. Dùng Deep Learning Language Model (có thể là LLMs): Mô hình LLM phải có `cosine_similarity >= threshold`

Đầu ra cuối cùng của bước tạo này là một file ngữ liệu cặp từ tương đồng theo cấu trúc sau đây:

```
would|could
would|might
two|three
two|four
two|five
two|six
two|seven
two|eight
first|second
year|month
...
``` 

⚠️ Lưu ý, ở trên chỉ là ví dụ.

Đối với từng trường hợp cụ thể:
- 1. GloVe & SpaCy:
    - Tải mô hình GloVe pretrained ở đây (khuyến khích sử dụng bộ Wikipedia 2014 + Gigaword 5 vì dữ liệu thích hợp để kiểm tra bài toán dịch máy hơn): [https://nlp.stanford.edu/projects/glove/](https://nlp.stanford.edu/projects/glove/).
    - Tải mô hình SpaCy pretrained ở đây (sử dụng `en_core_web_md` trở lên): [https://spacy.io/models](https://spacy.io/models)
    - Chạy file `CorpusBuilding\word_vec\glove_spacy\glove_building.py` với những tùy chỉnh trong file để tạo ra bộ ngữ liệu tên là `word-pairs.glove.en`, đem cất file này ở đâu đó để sử dụng cho bước kiểm tra.
- 2. Fasttext & SpaCy:
    - Tải mô hình Fasttext ở đây (sử dụng các phiên bản pretrained cho word thay vì subword, vì chúng ta kiểm tra trên word): [https://fasttext.cc/docs/en/english-vectors.html](https://fasttext.cc/docs/en/english-vectors.html).
    - Tải mô hình SpaCy pretrained ở đây (sử dụng `en_core_web_md` trở lên): [https://spacy.io/models](https://spacy.io/models)
    - Chạy file `CorpusBuilding\word_vec\fasttext_spacy\fasttext_building.py` với những tùy chỉnh trong file để tạo ra bộ ngữ liệu tên là `word-pairs.fasttext.en`, đem cất file này ở đâu đó để sử dụng cho bước kiểm tra.
- 3. Neural Language Model:
    - Xem xét các mô hình dành cho text ở đây (lựa chọn thêm phần `TEXT MODELS`): [https://huggingface.co/docs/transformers/index](https://huggingface.co/docs/transformers/index). Sau đó tìm tên pretrained của các mô hình đó ở đây: [https://huggingface.co/models](https://huggingface.co/models).
        - Ví dụ: Tôi muốn sử dụng RoBERTa làm mô hình để lấy word vectors, tôi sẽ lên đây để xem nó có tồn tại không [https://huggingface.co/docs/transformers/model_doc/roberta](https://huggingface.co/docs/transformers/model_doc/roberta). Sau đó tôi search [https://huggingface.co/models?sort=downloads&search=roberta](https://huggingface.co/models?sort=downloads&search=roberta) để lấy được tên của các pretrained model thuộc roberta, xong tôi copy cái tên đó và đưa vào flag `--hf-pretrained-model` trong file `CorpusBuilding\word_vec\neural_lm\neural_lm_building.py` để sử dụng. Trong trường hợp mô hình RoBERTa thì tôi sẽ sử dụng `roberta-base`.

## Kiểm tra mô hình dịch máy

Sau khi có được bộ ngữ liệu, chúng ta sẽ tiến hành kiểm tra mô hình dịch máy, chúng ta sẽ cần tinh chỉnh một chút ở phần mô hình dịch máy trong file `main.py`

### Chỉnh sửa code của mô hình dịch máy

Ở trong code của file `main.py`, có một mô hình dịch máy dịch từ tiếng Anh sang tiếng Việt được lấy từ HuggingFace:

````python
# Load machine translation here
# you can have any machine translation you want
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
class MTModel:
    def __init__(self):
        # document here: https://huggingface.co/VietAI/envit5-translation
        model_name = "VietAI/envit5-translation"  # en to vi
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def __call__(self, src):
        if type(src) == str:
            src = [src]
        src = ["en: " + i for i in src]
        tok = self.tokenizer(src, return_tensors="pt", padding=True).input_ids
        outputs = self.model.generate(tok, max_length=512)
        res = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        res = [i[4:] for i in res]
        return res
````

Bạn có thể tùy chỉnh class `MTModel` này, phần code ở trong hàm `__call__` không quá quan trọng, bạn có thể xóa hết đi và thay bằng code của bạn.

Ví dụ tôi muốn thay đổi code mô hình dịch máy của mình bằng một câu lệnh command line nào đó, tôi sẽ viết lại code như thế này:

````python
# Load machine translation here
# you can have any machine translation you want
import subprocess

class MTModel:
    def __init__(self):
        self.output_filename = "result.txt"

    def __call__(self, src: str):
        '''
            - Mô hình dịch máy sử dụng câu lệnh, trong đó flag
            "--source-sentence" để nhận câu muốn dịch và xuất ra
            màn hình câu đã dịch
            - Sau khi xuất ra màn hình, câu lệnh sử dụng toán tử ">" để
            ghi kết quả ra file "output_filename" ở trên, và đọc lên để
            trả về kết quả
        '''
        subprocess.call("python mt_translate.py --source-sentence " + src +  " > " + filename, shell=True)
        res = open(self.output_filename, 'r', encoding='utf-8').read().strip().split('\n')
        return res
````

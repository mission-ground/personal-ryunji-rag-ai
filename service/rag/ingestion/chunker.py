from transformers import AutoTokenizer
import unicodedata

class Chunker:

    def __init__(
          self
        , model_name="sentence-transformers/all-MiniLM-L6-v2"
        , chunk_size=256
        , overlap=50
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text, page):

        tokens = self.tokenizer.encode( text
                                      , add_special_tokens=False)

        chunks = []

        start = 0

        # 사이즈는 결국 전체 문서의 길이를 의미
        while start < len(tokens):

            end = start + self.chunk_size

            chunk_tokens = tokens[start:end]

            # 깨짐현상 발생으로 수정
            chunk_text = self.tokenizer.decode(  chunk_tokens
                                               , skip_special_tokens=True
                                               , clean_up_tokenization_spaces=True
                                               )
            
            
            chunk_text = unicodedata.normalize("NFC", chunk_text)
            chunk_index = len(chunks) + 1

            #벡터 DB에 넣을 구조화            
            chunk_data = {
                      "text": chunk_text
                    , "page": page
                    , "chunk": chunk_index
            }

            chunks.append(chunk_data)

            print("\n" + "="*60)
            print(f"CHUNK {chunk_index}")
            print("-"*60)
            print(chunk_text)
            print("="*60 + "\n")

            start += self.chunk_size - self.overlap

        return chunks
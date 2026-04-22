from transformers import AutoTokenizer
import unicodedata

class Chunker:

    # 임베딩 의존성 주입, 모델이 바뀌어도 Embedder만 교체하면 Chunker도 자동으로 따라감.
    #지금 Chunker의 chunk_size=256 토큰인데, 이게 너무 커서 한 청크에 여러 챕터 내용이 섞여 들어가고 있어요.
    def __init__(self, embedder, chunk_size=128, overlap=50
    ):
        self.tokenizer  = embedder.model.tokenizer  # Embedder 모델에서 토크나이저 꺼냄
        self.chunk_size = chunk_size
        self.overlap    = overlap

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
from sentence_transformers import SentenceTransformer,SparseEncoder
from pathlib import Path
import os
path=Path(os.getcwd())

# MODEL_NAME="naver/splade-cocondenser-ensembledistil"
# model=SparseEncoder(MODEL_NAME)
# sentences = [
#     "The weather is lovely today.",
#     "It's so sunny outside!",
#     "He drove to the stadium.",
# ]

# 2. Calculate sparse embeddings by calling model.encode()
# embeddings = model.encode(sentences)
# print("*"*50,embeddings.shape)
SAVE_FILE_PATH=path/"backend"/"src"/"models"
# model.save(str(SAVE_FILE_PATH/"sparse_encoder"))
model=SparseEncoder(str(SAVE_FILE_PATH/"sparse_encoder"))
output = model.encode(
    ["When did Airbnb go public?"],
    batch_size=32
)

print(type(output))
print(output)
# print(model.encode(sentences))
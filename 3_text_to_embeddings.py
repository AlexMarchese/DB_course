from typing import List, Optional
import pandas as pd
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
import time

### Code related to Vertex AI (text embedding) from "https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings#get_text_embeddings_for_a_snippet_of_text"

df = pd.read_excel("videos.xlsx")

## Function to embed a text (taken from the VERTEX documentation and adapted)
def embed_text(
    texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?"],
    task: str = "RETRIEVAL_DOCUMENT",
    model_name: str = "text-embedding-004",
    dimensionality: Optional[int] = 256,
) -> List[List[float]]:
    """Embeds texts with a pre-trained, foundational model."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
    embeddings = model.get_embeddings(inputs, **kwargs)
    return [embedding.values for embedding in embeddings]

# test = embed_text(["New cat", "New dog", "My name is Frank", "nice to meet you", "I like to eat pizza with pineapple"])
# test = embed_text(["New cat"])

# # print(len(test[0][0]))
# print(type(test[0]))
# tt = test[0]

# Iterate over the DataFrame rows as namedtuples


counter = 0
worked = 0

for row in df.itertuples():

    # print(row.captions)
    counter += 1

    if row.captions == False or row.captions == "[]": # if the value of captions is merely "[]" or False, it is skipped
         df.at[row.Index, 'embeddings'] = False
        #  print("skipped")
         continue
    try:
        # print(embed_text([row.captions]))
        test = embed_text([row.captions])
        # print(len(test[0]))
        df.at[row.Index, 'embeddings'] = str(test[0]) # has to be converted to string, otherwise getting an error when saving
        # print("worked!")
        worked += 1
        time.sleep(0.001) # to make sure no number of requests per minute is exceeded
    except:
        # print("Embedding generation not working")
        df.at[row.Index, 'embeddings'] = False

    

    if counter % 1000 == 0: # just for me to know over how many entries it iterated
            print("1000 done")
    

# print(df)


# # saving the df
df.to_excel('emb_videos.xlsx', index=False)

print(worked)

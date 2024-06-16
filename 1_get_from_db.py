from pymongo import MongoClient
import pandas as pd
import requests
import vertexai
from vertexai.preview.vision_models import Image, ImageTextModel

### Code related to Vertex AI (image captions) from "https://cloud.google.com/vertex-ai/generative-ai/docs/image/image-captioning#get-captions-short"

## Vertex AI model configurations to retireve the captions for the image
project_id = "formidable-sol-423718-i8"
vertexai.init(project=project_id, location="us-central1")
model = ImageTextModel.from_pretrained("imagetext@001")

# Connection to the MongoDB server
client = MongoClient('mongodb://student4:xyz123@134.209.243.12:27017/?authSource=youtube')
filter={}
project={             # Projection
    'channelId': 1, 
    'company': 1, 
    'statistics.viewCount': 1
}
sort=list({}.items())

# Applying the query (only a projection in this case)
result = client['youtube']['videos'].find(
  filter=filter,
  projection=project,
  sort=sort
)

# DF creation
df = pd.DataFrame(None, columns=["id", "company", "channel_id", "views", "thumbnail_url", "thumbnail_existent", "captions"])

# needed to build the url of the thumbnail. As I noticed it alswas is 'https://i.ytimg.com/vi/' + _id + 'maxresdefault.jpg'.
# For some videos the thumbnail was not linked, but still existent under the url
url_beginning = "https://i.ytimg.com/vi/"
url_end = "/maxresdefault.jpg"

r = 0

# iterating over the videos from the dataframe and extracting the parts of interest
for entry in result:

    thumbnail_url = url_beginning + entry["_id"] + url_end

    ## saves an image in bytes
    response = requests.get(thumbnail_url)

    try:
        response.raise_for_status()  # Raises an exception for HTTP errors. So if no image was found for instance
        existent = True

        ## Getting the captions behind the image
        img = response.content
        try:
            captions = model.get_captions(
            image=Image(img),
            # Optional parameters
            language="en",
            number_of_results=1,
            )

        except:
            captions = False

    except:
        existent = False
        captions = False

    # saves the information in a new pandas row
    new_row = pd.DataFrame({
            "id" : [entry["_id"]],
            "company" : [entry["company"]],
            "channel_id" : [entry["channelId"]],
            "views" : [entry["statistics"]["viewCount"]],
            "thumbnail_url" : [url_beginning + entry["_id"] + url_end],
            "thumbnail_existent" : [existent],
            "captions":[captions]
        })

    # appending the single row to the df
    df = pd.concat([df, new_row], ignore_index=True)

    if r % 1000 == 0: # to see the progress while running
        print("1000 done")
    
    r += 1

# saving the df
df.to_excel('videos.xlsx', index=False)



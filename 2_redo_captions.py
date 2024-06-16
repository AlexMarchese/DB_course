import pandas as pd
import requests
import vertexai
from vertexai.preview.vision_models import Image, ImageTextModel
import time
import random

### Code related to Vertex AI (image captions) from "https://cloud.google.com/vertex-ai/generative-ai/docs/image/image-captioning#get-captions-short"


## Vertex AI model configurations to retireve the captions for the image
project_id = "formidable-sol-423718-i8"
vertexai.init(project=project_id, location="us-central1")
model = ImageTextModel.from_pretrained("imagetext@001")

## reading the df
df = pd.read_excel("videos.xlsx")


counter = 0  # Starting number
redone = 0

# start_time = time.time()

# Iterate over the DataFrame rows as namedtuples
for row in df.itertuples():
    # Check if the 'thumbnail_existent' field is equal to "True" and 'caption' to "False"
    if row.thumbnail_existent is True and row.captions is False:
        # Update the 'captions' field in the DataFrame

        ### repeating all the captions finding part
        ## saves an image in bytes
        response = requests.get(row.thumbnail_url)

        try:
            response.raise_for_status()  # Raises an exception for HTTP errors. So if no image was found for instance
            existent = True

            ## Getting the captions behind the image
            img = response.content

            time.sleep(random.randrange(0, 6))

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

        if captions is not False: # if new captions got created
            redone += 1 # to know at the end how many new captions were added

            df.at[row.Index, 'captions'] = captions # saving the new captions
            print("Added so far: " + str(redone))

        if counter % 1000 == 0: # just for me to know over how many entries it iterated
            print("1000 done")
           
        counter += 1



print(redone)

# saving the df
df.to_excel('red_videos.xlsx', index=False)
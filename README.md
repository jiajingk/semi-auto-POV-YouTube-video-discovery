# system

![Alt text](assets/semi-auto-pov-system-diagram.png?raw=true "system diagram")

# setup

```
pip install -r requirements.txt
```
create `.env` file in the working dir then specify the following

```
YOUTUBE_API_KEY="Your youtube data API key"
GCP_PROJECT_ID="Your GCP project id"
GCP_LOCATION="Your GCP location"
GCP_CREDENTIAL_PATH="Path to the json file for the GOOGLE_APPLICATION_CREDENTIALS environment variable"
```
please refer to the offical document from google for credentials and api key setup
https://developers.google.com/youtube/v3
https://cloud.google.com/vertex-ai

# run 

```
python main.py > result.csv
```

typically if a video has confidence score of more than 0.9, this is very likely to be a valid video

if score is -1.0, it means the process encounter an error, and you can retry it if needed

# prompts

search keywords generation (GPT-4)

```
Suggest 10 scene or activities that people tend to share their POV shot on youtube, then, for each categories, suggest 10 keywords (be specific, like 'cooking') that I can use to search those scene or activates on youtube. Finally, reformat them in json as the following format

{
    "Extreme_Sports": ["Skydiving", "Mountain biking", "Surfing POV", ...],
    "<Scene or Activity>": ["<keywords 1>", "<keywords 2>", ...],
    ...
}
```

POV dectection for VQA model (Google Vertex AI imagetext@001)

```
Does this image display characteristics typical of a POV shot, such as a subjective camera angle or a part of the equipment being visible?
```
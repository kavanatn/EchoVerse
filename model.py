from get_token import get_ibm_iam_bearer
import requests
import json

url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"


body = {
    "input": """you are an audiobook reader. rewrite this text as you would read it, in an {{tone}} tone. the output must be in a list of json object having the following keys


- speech_text it is the text to be read
- emotion it is one of [ANGRY, SAD, HAPPY, FEAR, DISGUST, SUPRISE]
- background its optional its one of [OUTDOOR, INDOOR, RAINNING, CROWD, OFFICE]
you may not choose emotion and background apart from anything i have provided. you may leave the background as blank if nothing matches

NOTE:
- ensure consistent reading flow
- add relavant punctuation where necessary
- ignore text that might be out of context such as page numbers, headers, footer


Input: Once the Wind and the Sun had an argument. “I am stronger than you,” said the Wind. “No,
you are not,” said the Sun. Just at that moment they saw a traveler walking across the road.
He was wrapped in a shawl. The Sun and the Wind agreed that whoever could separate the
traveller from his shawl was stronger.
The Wind took the first turn. He blew with all his might to tear the traveller’s shawl from his
shoulders. But the harder he blew, the tighter the traveller gripped the shawl to his body.
The struggle went on till the Wind’s turn was over.
Now it was the Sun’s turn. The Sun smiled warmly. The traveller felt the warmth of the
smiling Sun. Soon he let the shawl fall open. The Sun’s smile grew warmer and warmer...
hotter and hotter. Now the traveller no longer needed his shawl. He took it off and dropped
it on the ground. The Sun was declared stronger than the Wind.
Output: [
  {
    \"speech_text\": \"Once, the Wind and the Sun had an argument. '\''I am stronger than you,'\'' boasted the Wind.\",
    \"emotion\": \"ANGRY\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"'\''No, you are not,'\'' replied the Sun, calm but confident.\",
    \"emotion\": \"HAPPY\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"Just then, they saw a traveler walking along the road, wrapped tightly in a shawl.\",
    \"emotion\": \"SUPRISE\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"They agreed: whoever could make the traveler remove his shawl would be the stronger.\",
    \"emotion\": \"SUPRISE\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"The Wind took the first turn. He blew with all his might, roaring and howling, trying to tear the shawl away.\",
    \"emotion\": \"ANGRY\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"But the harder he blew, the tighter the traveler clutched the shawl to his body.\",
    \"emotion\": \"SAD\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"The struggle went on until the Wind, exhausted, had to give up.\",
    \"emotion\": \"SAD\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"Now it was the Sun’s turn. The Sun smiled warmly, sending gentle rays down upon the traveler.\",
    \"emotion\": \"HAPPY\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"The traveler felt the pleasant warmth and loosened his grip on the shawl.\",
    \"emotion\": \"HAPPY\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"The Sun’s smile grew warmer and warmer... hotter and hotter... until the traveler no longer needed his shawl.\",
    \"emotion\": \"SUPRISE\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"At last, he took it off and dropped it to the ground.\",
    \"emotion\": \"HAPPY\",
    \"background\": \"OUTDOOR\"
  },
  {
    \"speech_text\": \"And so, the Sun was declared stronger than the Wind—not by force, but by gentle warmth.\",
    \"emotion\": \"HAPPY\",
    \"background\": \"OUTDOOR\"
  }
]

Input: {{input}}”
Output:""",
    "parameters": {
        "decoding_method": "greedy",
        "max_new_tokens": 8192,
        "min_new_tokens": 0,
        "stop_sequences": ["]"],
        "repetition_penalty": 1,
    },
    "model_id": "ibm/granite-3-8b-instruct",
    "project_id": "5261204b-1f60-416e-b589-08790e381d13",
}

# Removed global headers and get_ibm_iam_bearer call

def genrate_reader_json(text, tone, access_token):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": access_token
    }
    
    body["input"] = body["input"].replace("{{tone}}", tone)
    body["input"] = body["input"].replace("{{input}}", text)
    response = requests.post(url, headers=headers, json=body)
    
    if not response.ok:
        raise Exception(f"Error from WatsonX: {response.text}")
        
    resp = response.json()["results"][0]["generated_text"]

    return json.loads(resp)


# print(
#     genrate_reader_json(
#         "oh my god im happy! oh but what is this my dog died. i feel depressed",
#         "melodramatic",
#     )
# )

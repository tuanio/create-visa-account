# Speech-to-text API

# Installation Guide for Speech-to-Text API

To install and run the Speech-to-Text API, you will need to create an environment. There are two ways to do this, using either Anaconda or venv. Follow the steps below to create your environment:

## Environment

### Using Anaconda:
1. To create a new environment, open your command prompt and type `conda create -n <env_name>` and press Enter.

2. To activate the environment, type `conda activate <env_name>` and press Enter.

### Using venv:

1. To create a new environment, open your command prompt and type `python -m venv venv` and press Enter.

2. To activate the environment, type `venv\Scripts\activate` on Windows or `source venv\bin\activate` on Linux and press Enter.

## Installing Required Packages

After creating your environment, you will need to install the required packages. To do this, follow these steps:

1. Make sure your environment is activated.

2. Type `pip install -r requirements.txt` and press Enter.

# Running the API

Now that you have created the environment and installed the required packages, you can run the Speech-to-Text API. To do this, follow these steps:

1. Type `uvicorn main:app --host 0.0.0.0 --port 80 --reload` and press Enter.

2. The API can now be accessed via the host: `http://localhost:80/`.

## Example on using API

### Use `curl`:

`curl -X POST -F "file=@D:\\English Indian Accent\\data\\english\\wav\\train_hindifullfemale_00001.wav" -F "transcript=Author of the danger trail, Philip Steels, etc." http://localhost:80/uploadfile/`

### Use `postman`:

![Screenshot 2023-03-23 012035](https://user-images.githubusercontent.com/30165828/227000803-706c5de6-5062-4aa5-b365-d985b35fe7c5.png)

### Result:

````JSON
{
    "transcription": "Author of the danger trail, Phillips steels, etc.",
    "probability": [
        { "word": "Author", "prob": 78.55 },
        { "word": "of", "prob": 99.2 },
        { "word": "the", "prob": 93.02 },
        { "word": "danger", "prob": 76.11 },
        { "word": "trail", "prob": 69.99 },
        { "word": ",", "prob": 61.86 },
        { "word": "Phillips", "prob": 25.1 },
        { "word": "steels", "prob": 72.09 },
        { "word": ",", "prob": 57.01 },
        { "word": "etc", "prob": 94.66 },
        { "word": ".", "prob": 68.56 }
    ],
    "time_taken": 2.1506,
    "score": 75.0
}
````

# API Endpoints

The Speech-to-Text API has two endpoints, as described below:

| Method | Endpoint | Parameters | Description |
| --- | --- | --- | --- |
| `GET` | `/` | None | This is a placeholder for the index endpoint. | 
| `POST` | `/uploadfile/` | `file` (File) and `transcript` (Optional), both data need to be sent in a form request.	This API sends an audio clip with (or without) a text reference transcription. If the text is not sent, the API returns the transcription of the audio (prediction) with the probability for each word. If the text is sent, the API returns a `score` parameter, where `score = 1 - WER`. |

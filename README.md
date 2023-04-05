# Fine-tuning on Whisper 

## Explanation of ASR Training Parameters

- `--batch-size`: This parameter specifies the number of samples in each batch of data. The default value is 16, and the data is processed per GPU batch size.

- `--epochs`: This parameter specifies the number of times the model will train on the entire dataset. The default value is 5.

- `--sample-rate`: This parameter specifies the sample rate of the audio files in Hz. The default value is 16000 Hz.

- `--num-workers`: This parameter specifies the number of worker threads used for data loading. The default value is 6.

- `--log-wandb`: This parameter is a flag that enables logging to Weights and Biases (W&B). If set to True, training logs will be sent to a W&B project.

- `--train`: This parameter is a flag that indicates whether to train the model. If set to True, the model will be trained.

- `--test`: This parameter is a flag that indicates whether to test the model. If set to True, the model will be tested.

- `--predict`: This parameter is a flag that indicates whether to predict using the model. If set to True, the model will be used for prediction.

- `--indict-tts-path`: This parameter specifies the path to the IndictTTS dataset.

- `--cv-path`: This parameter specifies the path to the Common Voice dataset.

- `--grad-clip`: This parameter specifies the maximum gradient norm for clipping. The default value is 1.0.

- `--warmup-portion`: This parameter specifies the proportion of training steps to use for linearly increasing the learning rate during warm-up. The default value is 0.01.

- `--fine-tune-lr-limit`: This parameter specifies the upper limit of the learning rate for fine-tuning. The default value is 20.

- `--scheduler-for-step`: This parameter is a flag that indicates whether to use the step-based scheduler. If set to True, the step-based scheduler will be used else is epoch-based.

- `--start-eval-epoch`: This parameter specifies the epoch at which to start evaluation. The default value is 0.

- `--seed`: This parameter specifies the random seed used for reproducibility. The default value is 1211.

- `--pretrained-model-path`: This parameter specifies the path of pretrained model folder used for training or evaluating. The default value is "tiny".

- `--ckpt-path`: This parameter specifies the path to the checkpoint file. The file will have `.ckpt` extension.

## Setup the environment

### Creating and Activating an Environment using Conda

#### Windows, Linux

1. Open the `Anaconda Prompt` (or `CMD`, `Bash`, `Terminal`).

2. To create a new environment, enter the following command:
```
conda create --name env_name
```
Replace `env_name` with your desired environment name.

3. To activate the environment, enter the following command:
```
conda activate env_name
```

Replace `env_name` with the name of the environment you created.

### Creating and Activating an Environment using venv

### Window

1. Open a command prompt.
2. Navigate to the directory where you want to create the environment.
3. To create a new environment, enter the following command:
```
python -m venv env_name
```
Replace `env_name` with your desired environment name.
4. To activate the environment, enter the following command:
```
env_name\Scripts\activate.bat
```
Replace `env_name` with the name of the environment you created.

### Linux
1. Open a terminal window.
2. Navigate to the directory where you want to create the environment.
3. To create a new environment, enter the following command:
```
python -m venv env_name
```
Replace `env_name` with your desired environment name.
4. To activate the environment, enter the following command:
```
source env_name/bin/activate
```
Replace `env_name` with the name of the environment you created.

### Running an Environment

Once you have created and activated your environment, you can run commands within it. For example, to install packages using pip, you can use the following command to install need packages:
```
pip install -r requirements.txt
```

## Understand the folder structure

```
Training Code
    convert_ckpt_to_pretrained.py
    main.py
    README.md
```

1. `main.py`:  Use to experiment the model, training, testing, predicting. After training, you will get a `.ckpt` file.
2. `convert_ckpt_to_pretrained.py`: Use to convert `.ckpt` file to pretrained folder (for deploying or for next experiment).
3. `README.md`: Documents.

### Data structure

There're two parameter control the path of data in `main.py`. The `--indict-tts-path` and `--cv-path`, which is path for `Indic TTS` and `Common Voice`, respectively.

Assume I have a folder name `data` have 2 folder inside:

```
    data/
        IndicTTS_English/
            IndicTTS_Phase2_Assamese_fem_Speaker1_english/
                english/
                    wav/
                        ...wav
                    txt.done.data
            IndicTTS_Phase2_Assamese_male_Speaker1_english/
            ...
            IndicTTS_Phase2_Telugu_male_Speaker1_english/
        cv-corpus
            en
                ...
    convert_ckpt_to_pretrained.py
    main.py
    README.md
```

- `Indic TTS` structure: If you care about put newly data to continue training the model, you should make the new dataset have same structure like `IndicTTS_English` above, each folder in `IndicTTS_English` represent for each type of data you have. Inside its, have `english` folder, then `wav` folder and `txt.done.data` file. You should make all new data have the same format, structure like original (even space in `txt.done.data`).
- `Common Voice (cv)`: You don't need to care about this folder.

## How to run

### In case you want to run from scratch

```
python main.py --batch-size 64 --epochs 10 --num-workers 8 \ 
    --train --test --predict \
    --cv-path data/cv-corpus/en \
    --indict-tts-path /data/IndicTTS_English/ \
    --log-wandb --scheduler-for-step
```

⚠️ The `convert_ckpt_to_pretrained.py` is very straightforward, I believe you can read and run it.

### In case you want to continue training the model from `.ckpt` file.

```
python main.py --batch-size 64 --epochs 10 --num-workers 8 \
    --train --test --predict \
    --indict-tts-path /data/IndicTTS_English/ \
    --cv-path data/cv-corpus/en \
    --log-wandb --scheduler-for-step \
    --ckpt-path <ckpt.name>.ckpt
```

### In case you want to continue training the model from pretrained model (after running the `convert_ckpt_to_pretrained.py` file).

```
python main.py --batch-size 64 --epochs 10 --num-workers 8 \
    --train --test --predict \
    --indict-tts-path /data/IndicTTS_English/ \
    --cv-path data/cv-corpus/en \
    --log-wandb --scheduler-for-step \
    --pretrained-model-path <model-path>/
```

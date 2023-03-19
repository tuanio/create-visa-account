# Mutant MT

# Introduction

Hello, this is a guide on how to use this project. The algorithm testing framework for this machine translation project is based on the comparison of the original translation sentence with a mutated sentence created using synonymous word pairs.


## Main component of the project: Similar word pair dataset

### Introduction to the similar word pair dataset

The main component of this project is the similar word pair dataset, where two words in a pair must satisfy the condition cosine_similarity(word_vector[word_A], word_vector[word_B]) >= threshold. You will have to adjust the threshold yourself to achieve the best possible result for the similar word pair dataset (try modifying and running it to create), where the threshold usually ranges between `0.9 - 0.7`.

- Examples of good word pairs: father|dad, mom|mother, ...
- Examples of bad word pairs: one|two, parents|daughter, ...

You will find that good word pairs will provide highly related pairs of words, which may have some errors, but as long as the similarity is high, it is acceptable (not too strict).

### How to create a similar word pair dataset

There are three ways to create similar word pairs (based on the amount of code written):

1. Use GloVe & SpaCy: Both GloVe and SpaCy models must have `cosine_similarity >= threshold`.
2. Use Fasttext & SpaCy: Both Fasttext and SpaCy models must have `cosine_similarity >= threshold`.
3. Use Deep Learning Language Model (LLMs): The LLM model must have `cosine_similarity >= threshold`.

The final output of this creation step is a similar word pair dataset in the following structure:

```
would|could
would|might
two|three
two|four
two|five
two|six
two|seven
two|eight
first|second
year|month
...
``` 

⚠️ Note that the above is just an example.


For each specific case:

1. GloVe & SpaCy:
    - Download the pretrained GloVe model here (it is recommended to use the Wikipedia 2014 + Gigaword 5 dataset as it is more suitable for machine translation tasks):  [https://nlp.stanford.edu/projects/glove/](https://nlp.stanford.edu/projects/glove/).
    - Download the pretrained SpaCy model here (use en_core_web_md or above): [https://spacy.io/models](https://spacy.io/models)
    - Run the `CorpusBuilding\word_vec\glove_spacy\glove_building.py` file with the settings in the file to create a similar word pair dataset named `word-pairs.glove.en`, and store this file somewhere for use in the testing step.
2. Fasttext & SpaCy:
    - Download the Fasttext model here (use pretrained versions for word instead of subword, as we test on word): [https://fasttext.cc/docs/en/english-vectors.html](https://fasttext.cc/docs/en/english-vectors.html).
    - Download the pretrained SpaCy model here (use en_core_web_md or above): [https://spacy.io/models](https://spacy.io/models)
    - Run the CorpusBuilding\word_vec\fasttext_spacy\fasttext_building.py file with the settings in the file to create a similar word pair dataset named word-pairs.fasttext.en, and store this file somewhere for use in the testing step.
3. Neural Language Model:
    - Xem xét các mô hình dành cho text ở đây (lựa chọn thêm phần `TEXT MODELS`): [https://huggingface.co/docs/transformers/index](https://huggingface.co/docs/transformers/index). Sau đó tìm tên pretrained của các mô hình đó ở đây: [https://huggingface.co/models](https://huggingface.co/models).
        - Ví dụ: Tôi muốn sử dụng RoBERTa làm mô hình để lấy word vectors, tôi sẽ lên đây để xem nó có tồn tại không [https://huggingface.co/docs/transformers/model_doc/roberta](https://huggingface.co/docs/transformers/model_doc/roberta). Sau đó tôi search [https://huggingface.co/models?sort=downloads&search=roberta](https://huggingface.co/models?sort=downloads&search=roberta) để lấy được tên của các pretrained model thuộc roberta, xong tôi copy cái tên đó và đưa vào flag `--hf-pretrained-model` trong file `CorpusBuilding\word_vec\neural_lm\neural_lm_building.py` để sử dụng. Trong trường hợp mô hình RoBERTa thì tôi sẽ sử dụng `roberta-base`.

## Machine Translation Model Evaluation

After obtaining the data set, we will proceed to evaluate the machine translation model. We will need to adjust the machine translation model in the `main.py` file.

### Editing the Machine Translation Code

In the `main.py` file, there is a machine translation model that translates from English to Vietnamese, obtained from HuggingFace:

````python
# Load machine translation here
# you can have any machine translation you want
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
class MTModel:
    def __init__(self):
        # document here: https://huggingface.co/VietAI/envit5-translation
        model_name = "VietAI/envit5-translation"  # en to vi
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def __call__(self, src):
        if type(src) == str:
            src = [src]
        src = ["en: " + i for i in src]
        tok = self.tokenizer(src, return_tensors="pt", padding=True).input_ids
        outputs = self.model.generate(tok, max_length=512)
        res = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        res = [i[4:] for i in res]
        return res
````

You can customize this `MTModel` class. The code in the `__call__` function is not too important (but the `__call__` function is important, and trust me, you don't want to delete it 😅 unless you know what you want to customize), you can delete it all and replace it with your own code.

For example, if I want to change the machine translation model code with a command line, I will rewrite the code like this:

````python
# Load machine translation here
# you can have any machine translation you want
import subprocess

class MTModel:
    def __init__(self):
        self.output_filename = "result.txt"

    def __call__(self, src: str):
        '''
            - The machine translation model uses a command in which the flag
            "--source-sentence" is used to receive the sentence to be translated and
            output the translated sentence to the screen
            - After outputting to the screen, the command uses the ">" operator to
            write the result to the "output_filename" file above and read it
            to return the result.
        '''
        # Do not remove these two lines, this is the common standard of the code
        # if you're not sure what you're doing
        if type(src) == str: 
            src = [src]

        res = []
        for sent in src:
            # You can replace the command at this point with your own model
            subprocess.call("python mt_translate.py --source-sentence " + src +  " > " + filename, shell=True)
            pred = open(self.output_filename, 'r', encoding='utf-8').read().strip().split('\n')
            res.append(pred)
        return res
````

### Performing the Evaluation

This is the easiest step, where you just need to run the `main.py` file. Here are all the configuration options you need to be aware of:

```
Main config [-h] [--vocab-path VOCAB_PATH] [--source-path SOURCE_PATH] [--mutant-path MUTANT_PATH] [--create-mutant] [--nums-mutant NUMS_MUTANT] [--target-language TARGET_LANGUAGE] [--target-corpus-path TARGET_CORPUS_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --vocab-path VOCAB_PATH
                        Word pairs pre-built path.
  --source-path SOURCE_PATH
                        Source language corpus to test, line by line sentence.
  --mutant-path MUTANT_PATH
                        Text file to store or to load mutant versions generated.
  --create-mutant       Bool value of action to create mutant, if not, it's will load mutants from '--mutant-path'
  --nums-mutant NUMS_MUTANT
                        Maximum no. mutants to generate for each source sentence.
  --target-language TARGET_LANGUAGE
                        Target language lowercase
  --target-corpus-path TARGET_CORPUS_PATH
                        Target language corpus to calculate tfidf (typically training corpus)
```

Below are some sample recipes for you to use:

- Do you not have a similar word pair data set? Create a list of words you want to consider in the vocabulary set.

```
python CorpusBuilding\get_word_list.py
```

After running this, a file named `list_words.fasttext.json` will be created.

- Build the data set using BERT

Here's how to build the data set using the `BERT` model with the word list created above, with a comparison threshold of `0.85`, and the `annoy...` parameters adjusted as much as possible for better effectiveness (creating a tree before querying), and the `query-neighbors` parameter depends on the threshold, with higher threshold having more neighbors, usually in the range of `[20, 50]`.

```
python CorpusBuilding\word_vec\neural_lm\neural_lm_building.py --hf-pretrained-model bert-base-uncased --list-word-path list_words.fasttext.json --sim-pair-threshold 0.85 --annoy-nums-tree 200 --annoy-nums-worker 4 --query-neighbors 30
```

After this step, you will have a file named `word-pairs.neural_lm.en`, keep this file.

- Run machine translation model check

If you're running for the first time:

```
python main.py --vocab-path word-pairs.neural_lm.en --source-path corpus.en --mutant-path mutant_version.json --create-mutant --nums-mutant 10 --target-language vietnamese
```

To make it simpler, you can use:

```
python main.py --vocab-path word-pairs.neural_lm.en --source-path corpus.en --create-mutant --target-language vietnamese
```

If you have already used the `--create-mutant` flag, you can skip it on subsequent runs, as long as the `source-path` remains the same each time, for example:

```
python main.py --vocab-path word-pairs.neural_lm.en --source-path corpus.en --target-language vietnamese
```

🏆 Finally, the result will give you a `consistency_score.xlsx` file containing the machine translation model evaluation results.

## Installation

### Virtual Environment

- To run the code, you need to have an environment. You can use either `anaconda` or `venv`. For example:
    - In `Anaconda`:
        - Create an environment: `conda create -n <environment_name>`
        - Activate the environment: `conda activate <environment_name>`
    - In `venv`:
        - Create an environment: python -m venv <environment_name>
        - Activate the environment:
            - Windows: `<environment_name>\Scripts\activate`
            - Linux: `source <environment_name>/bin/activate`

- Once the environment is activated, install the necessary packages with the command:

```
pip install -r requirements.txt
```

### Dependencies
- 1. JDK 8 (Java Development Kit) needs to be installed. After downloading, JAVA_HOME needs to be set up.
- 2. Standford Parser needs to be downloaded from [https://stanfordnlp.github.io/CoreNLP/parser-standalone.html](https://stanfordnlp.github.io/CoreNLP/parser-standalone.html
- 3. Install tokenizer for target language in SpaCy (ex: Spanish for example, or any language you want to use: `python -m spacy download es_core_news_sm`. For more: [https://spacy.io/models/](https://spacy.io/models/)).

## Files Structure

```
MutantMT
│   .gitignore
│   main.py -> A collection of module functions that can be run
│   README.md
│   requirements.txt
│   utils.py
│
├───ConsistencyScoring
├───CorpusBuilding
│   │   fasttext_main.py -> For creating a corpus using fasttext
│   │   glove_main.py -> For creating a corpus using glove
│   │   scripts.py -> Scripts to help in Corpus Building
|   |   get_word_list.py -> scripts to get a word list file to build 
│   │   valid_words.fasttext.en.json -> A list of words to consider for word pairs of fasttext
│   │   valid_words.glove.en.json -> A list of words to consider for word pairs of glove
│   │   word-pairs.glove.en -> Corpus of glove (6596 pairs of words).
│   │   word-pairs.glove.no_filter.zip -> Corpus of glove (2,481,180 pairs of words) (unzip required)
│   │   __init__.py
│   │
│   └───word_vec
│       ├───fasttext
│       │       README.md -> Instructions on how to download fasttext model
│       │
│       └───glove
│               README.md -> Instructions on how to download glove model
│
└───StructureFilter
        scripts.py -> Scripts to help in Structure Filtering
        __init__.py
```

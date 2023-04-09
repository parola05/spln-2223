# Story Analyzer

Get all the details of a story. From summaries to character information, explore your book like never before!

![Banner](banner.jpg)

## Features

* Quiz game
* Translation 
* Summarization  
* Most relevant topics
* Characteres list 
* Lines list
* Number of sentences
* Match of input phrase with a storie excert

## Usage

```
usage: main.py [-h] [-m {local,web}] [-q] [-t [{English,Spanish,French,German,Italian,Portuguese}]] [-d] [-s] [-l] [-c] [-a [ACTIONS]]
               [--save title] [-p PROJECTION]
               input output

Book Analyzer: get insight informations of your storie

positional arguments:
  input                 input file path or book name (only in web mode)
  output                output file path

options:
  -h, --help            show this help message and exit
  -m {local,web}, --mode {local,web}
                        app modes
  -q, --quiz            quiz game
  -t [{English,Spanish,French,German,Italian,Portuguese}], --translate [{English,Spanish,French,German,Italian,Portuguese}]
                        translate the book
  -d, --discussions     list the book discussions (topics)
  -s, --summary         summarize the book
  -l, --language        detect book language
  -c, --characters      get informations of the book characters
  -a [ACTIONS], --actions [ACTIONS]
                        get the top most actions of a book
  --save title          the book will be saved and so will any queries invoked deemed savable.
  -p PROJECTION, --projection PROJECTION
                        project queries in the text range. Projection type is [<bottom>;<higher>]
  -sa, --sentiment-analysis
                        get the sentiment analysis of the book
```

## Dependencies

* Quiz game is made with https://huggingface.co/gpt2
* Transaltion is made with https://huggingface.co/docs/transformers/main/en/model_doc/t5#overview
* Summarization is made with https://huggingface.co/docs/transformers/model_doc/pegasus
* Most Relevent Topics is made with https://radimrehurek.com/gensim/
* Language detection is made with https://huggingface.co/papluca/xlm-roberta-base-language-detection
* Actions, Characters and places list is made with https://spacy.io/
* HTML extraction is made with https://www.crummy.com/software/BeautifulSoup/bs4/doc/
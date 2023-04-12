<h1 style="font-size:65px" align="center"> Story <b>Analyzer</b> </h1></center>

<center><h3>Get all the details of a story. From summaries to character information, explore your book like never before!</h3> </center>

<br>

![Banner](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/banner.jpg)

<p align="center">
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/transformers-^4.27.4-yellow" alt="Homebrew" />
  </a>
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/spacy-^3.5.1-blue" alt="Homebrew" />
  </a>
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/gensim-^4.3.1-green" alt="Homebrew" />
  </a>
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/beautifulsoup4-^4.12.2-pink" alt="Homebrew" />
  </a>
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/torch-^2.0.0-red" alt="Homebrew" />
  </a>
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/sentencepiece-^0.1.97-orange" alt="Homebrew" />
  </a>
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/colorama-^0.4.6-blueviolet" alt="Homebrew" />
  </a>
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/sortedcontainers-^2.4.0-brightgreen" alt="Homebrew" />
  </a>
  <a href="https://formulae.brew.sh/formula/semgrep">
    <img src="https://img.shields.io/badge/python-^3.10-lightgrey" alt="Homebrew" />
  </a>
</p>

## Installation

The program is available at [**PyPI**](https://pypi.org/project/story-analyzer/) and can be installed by the command:

```
$ pip install story-analyzer
```

If you want to download the files from this **git**, after clone the repository you should do the following commands:

```
$ pip install -r requirements.txt
$ cd story_analyzer
$ python main.py -h 
```

## Features

* 🎲 [Automatic **quiz** game generation of the book content](#quiz)
* 🌐 [Translation](#translation)
* 🔍 [Match of input phrase with a **similar story excert**](#match)
* 📝 Summarization  
* 🌐 [Language Detection](#language)
* 😊 [Sentiment analsys of the book](#sentiment)
* 🎯 Most relevant **topics** in the book
* 👥 Characteres list 
* 🎚️ [Sentences projection](#projection)
* 🕸️ [Fetch a book from **web**](#fetch)
* 💹 Actions list 
* 📁 [Book **archiver**](#archiver)

### 🎲 <a name="quiz">Quiz game</a> 

A random complex sentence from the book is selected. With the firsts five words from the sentence, six fake sentences is generated. The goal is the user guess the true sentence.

![img1](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/img1.png
)

### 🎚️ <a name="projection"> Projection </a>

Some operations can be very time consuming with is being considered the hole content of the book. So, with the user wants to make the operation only in a limited part of the book, **projections** can be used. Every other flag used with the projection flag, only operates in the projection content. The projection syntax is like access an array in Python: *the book's content is abstracted into a list of sentences*. If the user wants to **view** the projection of the first 3 sentences of the book, it can be used **-v** flag.

![img1](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/img2.png
)

### 🌐 <a name="translation">Translation</a> 

The **translation** feature only works for texts with a number of words less than 512. This means that is possible to translate a hole paragraph! The program have support to translate only texts written in **English**. The languages available to translate are **French**, **German** and **Romanian**. The following example made the translation of the previous book projection.

![img1](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/img3.png
)

### 🌐 <a name="language">**Language detection**</a>

In order to detect the language of the book, the user can execute:

![img1](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/img4.png
)

### 🔍 <a name="match">**Match of input phrase with a similar story excert**</a>

Sometimes the user wants to read again a certain excert from the book, but only remember a short description of this part. In order to find this part of the book, the user can write what he remembers and the program returns the part of the book which is more similar in terms of subject to what was passed.

![img1](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/img5.png
)

### 🕸️ <a name="fetch">**Fetch a book from web**</a>

By providing the possibility to fetch a book from web, the program will be able to read books that are not in the local machine, expanding its scope. With the argument **--mode web** followed by the name of the desired book, the program will try to fetch the book from [Project Gutenberg](https://www.gutenberg.org/).

It is important to notice that the program will only be able to fetch books that are in Project Gutenberg's database, otherwise the user should consider using the **--mode local** argument and providing the path to the book in the local machine.

### 📁 <a name="archiver">**Book archiver**</a>

The **archiver** features allows the user to save the book in a database by using the argument **--save TITLE**. By using the arguments **--view** and **--read TITLE**, it is possible to read the content of the book saved. 

![img6](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/img6.png
)

Another use case of this feature is the use of the **--save TITLE** argument followed by queries. Instead of just saving the content of the book it will also save the queries asked by the user. By doing this it is possible to use the **archive** as a cache, thus reducing the total time of the queries saved. 

![img7](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/img7.png
)

**Not all the queries will be deemed as savable**. Similar sentences and Sentiment Analysis will not be saved.

Another thing to be aware is the fact that it is **not supported to do a projection** of a book saved in the archive. This is due to the fact that a projection will change the book's content. However, in order to optimize the queries that require a spacy analyzis, the Doc object is saved in the archive. If the user were to do a projection on a read and then use the **--save** argument then the doc saved would not reflect the projection, thus it would not be coherent with the expected result. For future work, it would be interesting to implement a way to support this feature.

![img8](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP1/images/img8.png
)

### 😊 <a name="sentiment">**Sentiment Analysis**</a>

To end the list of the implemented features, there is also the possibility to analyze the general sentiment transmited by a book. To use this feature, the user should use the argument **--sa**. The program will print the sentiment of the book. It can be "Positive", "Negative" or "Neutral".

## Usage

```
usage: story_analyzer [-h] [-m {local,web}] [-q] [-t [{French,German,Romanian}]] [-d] [-s] [-l] [-c] [-a [ACTIONS]] [--save title] [--read title] [-p PROJECTION] [-sa] [-v] [-si SIMILAR] [-sn] [input] output

Book Analyzer: get insight informations of your storie

positional arguments:
  input                 input file path or book name (only in web mode)
  output                output file path. The extension automatic is set to JSON

options:
  -h, --help            show this help message and exit
  -m {local,web}, --mode {local,web}
                        app modes
  -q, --quiz            quiz game
  -t [{French,German,Romanian}], --translate [{French,German,Romanian}]
                        translate the book
  -d, --discussions     list the book discussions (topics)
  -s, --summary         summarize the book
  -l, --language        detect book language
  -c, --characters      get informations of the book characters
  -a [ACTIONS], --actions [ACTIONS]
                        get the top most actions of a book
  --save title          the book will be saved and so will any queries invoked deemed savable.
  --read title          for queries saved the response time will be quicker, since the query done will be a lookup to a database with the book info. However if a query was not saved or is not deemed savable then the query times will
                        remain the same
  -p PROJECTION, --projection PROJECTION
                        project queries in the text range. Projetion type is [<bottom>;<higher>]
  -sa, --sentiment_analysis
                        sentiment analysis of the book
  -v, --view            view book content. With projection is used, the text is limited by the projection range
  -si SIMILAR, --similar SIMILAR
                        finds the sentence that better describes the input given. It also gives the word offset from the beginning of the story. Useful for finding an exact reference.
  -sn, --sentence_no    get the number of sentences of a story
```

## Dependencies

* Quiz game is made with https://huggingface.co/gpt2
* Translation is made with https://huggingface.co/docs/transformers/main/en/model_doc/t5#overview
* Summarization is made with https://huggingface.co/docs/transformers/model_doc/pegasus
* Most Relevent Topics is made with https://radimrehurek.com/gensim/
* Language detection is made with https://huggingface.co/papluca/xlm-roberta-base-language-detection
* Actions, Characters and places list is made with https://spacy.io/
* HTML extraction is made with https://www.crummy.com/software/BeautifulSoup/bs4/doc/

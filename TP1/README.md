<center><h1> Story <b>Analyzer</b> </h1></center>

<center><h3>Get all the details of a story. From summaries to character information, explore your book like never before!</h3> </center>

<br>

![Banner](banner.jpg)

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

## Features

* 🎲 Automatic **quiz** game generation of the book content
* 🌐 Translation and language detection
* 🔍 Match of input phrase with a **similar story excert**
* 📝 Summarization  
* 😊 Sentiment analsys of the book
* 🎯 Most relevant **topics** in the book
* 👥 Characteres list 
* 🎚️ Sentences projection 
* 🕸️ Fetch a book from **web**
* 💹 Actions list 
* 📁 Book **archiever**

### **Quiz game**

A random complex sentence from the book is selected. With the firsts five words from the sentence, six fake sentences is generated. The goal is the user guess the true sentence.

``` bash
$ story_analyzer HarryPotter.txt outputFile -q | cat outputFile.json
  { 
      sentences: [
        "As for Harry and Ron, their legs already been bound tightly in long creepers without their noticing.",
        "'As for Harry and Ron, they've still got time. He could probably do it with more people than he's willing to spend his life in', said Amybus cheerfully as she stood up from her seatbelt on the bench beside them after waiting",
        "As for Harry and Ron, I thought we should get together. I've heard about this being a problem in the past but no-one has ever asked me to talk so as far away from our lives when there is something more pressing than",
        "As for Harry and Ron, there's nothing they could do to get their own way. They're not sure if that will change anytime soon; he has some other plans (and Hermione is quite capable of doing so), but his plan looks more like",
        "'As for Harry and Ron, they're pretty sure that I'm on the fence. I just want them to know this is my home' Hermione said with a smile at me as she brought up her wand in front of us all it",
        "'As for Harry and Ron, that's what happened. Their parents left the house at 11:30 AM to go look after their own children when they found out about this incident', said Bynum-Jones of North County Sheriff Bill Williams' office",
        "As for Harry and Ron, they are all so quiet. They can't even get their head up about what's happening to the rest of them or perhaps more importantly how it is going on in this world. What have you done?"
    ]
  }
```

### **Projection**

Some operations can be very time consuming with is being considered the hole content of the book. So, with the user wants to make the operation only in a limited part of the book, **projections** can be used. Every other flag used with the projection flag, only operates in the projection content. The projection syntax is like access an array in Python: *the book's content is abstracted into a list of sentences*. If the user wants to **view** the projection of the first 3 sentences of the book, it can be used **-v** flag.

``` bash
$ story_analyzer HarryPotter.txt outputFile -p [0:2] -v | cat outputFile.json
{
    projection: "Mr. and Mrs. Dursley, of   number four, Privet Drive, were proud to say that they were perfectly normal,  thank you very much. They were the last people you’d expect to be involved in anything strange or  mysterious, because they just didn’t hold with such nonsense. Mr. Dursley was the director of a firm called Grunnings, which made drills".
}
```

### **Translation** 

The **translation** feature only works for texts with a number of words less than 512. This means that is possible to translate a hole paragraph! The program have support to translate only texts written in **English**. The languages available to translate are **French**, **German** and **Romanian**. The following example made the translation of the previous book projection.

``` bash
$ story_analyzer HarryPotter.txt outputFile -p [0:2] -t German | cat outputFile.json
{
    translation:"Herr und Frau Dursley von der Privet Drive Nummer vier waren stolz darauf zu sagen, dass sie vollkommen normal waren, vielen Dank. Sie waren die letzten Personen, von denen man erwarten würde, dass sie in etwas Seltsames oder Geheimnisvolles verwickelt wären, weil sie mit einem solchen Unsinn einfach nichts zu tun haben wollten. Herr Dursley war Direktor einer Firma namens Grunnings, die Bohrer herstellte.
}
```

### **Language detection**

In order to detect the language of the book, the user can execute:

``` bash
$ story_analyzer HarryPotter.txt outputFile -l | cat outputFile.json
{
    language: "English"
}
```

### **Match of input phrase with a similar story excert**

Sometimes the user wants to read again a certain excert from the book, but only remember a short description of this part. In order to find this part of the book, the user can write what he remembers and the program returns the part of the book which is more similar in terms of subject to what was passed.

``` bash
$ story_analyzer HarryPotter.txt outputFile -l | cat outputFile.json
```

### **Fetch a book from web**

TODO

### 

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
* Transaltion is made with https://huggingface.co/docs/transformers/main/en/model_doc/t5#overview
* Summarization is made with https://huggingface.co/docs/transformers/model_doc/pegasus
* Most Relevent Topics is made with https://radimrehurek.com/gensim/
* Language detection is made with https://huggingface.co/papluca/xlm-roberta-base-language-detection
* Actions, Characters and places list is made with https://spacy.io/
* HTML extraction is made with https://www.crummy.com/software/BeautifulSoup/bs4/doc/
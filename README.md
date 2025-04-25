# Parlance - Custom Wordlist Generation Based on Word Frequency

**parlance** is a tool that will parse the textual contents of any urls provided. It performs prcoessing on the textual content using Natural Language Processing and simplistic filtering. The intention is to generate custom base wordlists that are specifically tailored to targets during penetration testing or red team exercises. This is done using word frequency distribution to determine the most commonly used words in the provided texts.

## Parsing
Parsing consists of stripping all HTML tags and getting at the raw textual content of the urls provided. The next step is to tokenize and remove a set of common English words. Additional words for removal can be specified by the user. All words are converted to lowercase, this is necessary to avoid scewing the frequency distribution calculation performed later. Now the text is tagged with Parts-of-Speech (POS) using a Unigram tagger. Any words that are not recognized by the tagger are inspected for certain characters that might indicate the string is part of a link or other undesirable string for the purposes of this tool.

The filtered text is then looked at for frequency distribution. This provides a good set of common words used in the source urls. The user can limit the number of returned results to limit the base wordlist to a reasonable size based on the frequency of each word.

## Installation

```bash
git clone http://github.com/bannedit/parlance.git
```

```bash
cd parlance/
```

```bash
pipx install .
```
Additional corpus files are required as well. These can be installed using the *-c* option:
```bash
parlance -c
```


## Options

```bash
parlance -h
usage: parlance [-h] [-t N] [-m LEN] [-i WORD [WORD ...]] [-n] [-o OUTFILE] -u URLS [URLS ...]

Uses NLP to generate wordlists for use in brute force attacks.

options:
  -h, --help            show this help message and exit
  -t, --top N           Request the top N words
  -m, --min LEN         Minimum word length (Default is set to 5)
  -i, --ignore WORD [WORD ...]
                        Additional words to ignore
  -n, --numbers         Allow numbers to be included in the output (Default is to filter numbers)
  -o, --outfile OUTFILE
                        Output the list to a file
  -u, --urls URLS [URLS ...]
                        URL to process for words
```

Examples:
```bash
parlance -u https://bannedit.github.io/Automated-ROP-Chain-Integrity.html https://bannedit.github.io/Virtual-Machine-Detection-In-The-Browser.html#Virtual-Machine-Detection-In-The-Browser -o test.txt -t 20

            _-_
           |(_)|
            |||            ▄▄▄· ▄▄▄· ▄▄▄  ▄▄▌   ▄▄▄·  ▐ ▄  ▄▄· ▄▄▄ .
            |||           ▐█ ▄█▐█ ▀█ ▀▄ █·██•  ▐█ ▀█ •█▌▐█▐█ ▌▪▀▄.▀·
            |||            ██▀·▄█▀▀█ ▐▀▀▄ ██▪  ▄█▀▀█ ▐█▐▐▌██ ▄▄▐▀▀▪▄
            |||           ▐█▪·•▐█ ▪▐▌▐█•█▌▐█▌▐▌▐█ ▪▐▌██▐█▌▐███▌▐█▄▄▌
            |||           .▀    ▀  ▀ .▀  ▀.▀▀▀  ▀  ▀ ▀▀ █▪·▀▀▀  ▀▀▀ 
      ^     |^|     ^            parlance - v0.1.0 - by bannedit
    < ^ >   <+>   < ^ >
     | |    |||    | |
      \ \__/ | \__/ /
        \,__.|.__,/
            (_)
    
RANK    FREQUENCY       WORD
1       26              gadget
2       25              exploit
3       15              chain
4       15              detection
5       14              https
6       12              testing
7       11              technique
8       11              gadgets
9       10              process
10      10              techniques
11      10              browser
12      10              webgl
13      8               information
14      7               integrity
15      7               software
16      7               development
17      7               memory
18      7               instruction
19      7               stack
20      7               debug
```

## Recommendations
This tool was developed primarily with the intention of creating a base wordlist based on commonly used words. 

The wordlist can be used in conjunction with hashcat to generate more realistic looking password candidates. 

```bash
hashcat -a 0 -r rulefile.rule --force --stdout parlance_basewords.txt > realistic_wordlist.txt
```
Additionally, multiple rule files can be applied:
```bash
hashcat -a 0 -r rulefile1.rule -r rulefile2.rule --force --stdout parlance_basewords.txt > realistic_wordlist.txt
```

One thing to keep in mind when doing this is how the resulting wordlist will be utilized. If the users intention is to use it as part of an online brute force attack it would be best to ensure the resulting wordlist size is rather small. This can be done using the *-t* or *--top* options in **parlance** to limit the number of generated words for the base wordlist.

Another useful option is the *-m* option. This will limit the words processed based on length. For example *-m* 8 would limit processing to words that are 8 character long. One thing to consider with this option is if you intend on using the resulting wordlist with hashcat as mentioned above, hashcat rules tend to append, so if you know you have strict restrictions on length, it would be worth doing post processing on your own to remove any words that go beyond the length limitation.
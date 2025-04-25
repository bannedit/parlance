#!/usr/bin/env python3
import argparse
import aiohttp
import asyncio
import string

from bs4 import BeautifulSoup
from nltk.corpus import stopwords, brown
from nltk.tokenize import word_tokenize
from nltk import FreqDist, UnigramTagger

# customized set of stopwords
custom_stop_words = [
    # '.', ',', ';', ':', '?', '+', '-', '=' '(', ')', '!', '*', '\'', '[', ']',
    '\'s', 'also', 'need', 'know', 'still', 'using', 'could', 'would', 'might',
    'likely', 'within', 'found', 'however'
    ]

def logo():
    return """
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
      \\ \\__/ | \\__/ /
        \\,__.|.__,/
            (_)
    """

async def process_urls(urls: list, top:int = 100, ignore:list = [], min:int = 5, numbers: bool = False, outfile: str = ""):

    clean_tokens = []
    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                raw_text = soup.get_text()

                tokenized = word_tokenize(raw_text)

                stop_words = set(stopwords.words("english"))
                stop_words.update(custom_stop_words)
                stop_words.update(ignore)

                filtered = []
                for word in tokenized:
                    if word.casefold() in stop_words:
                        continue
                    if word in string.punctuation:
                        continue
                    if numbers:
                        if word in string.digits:
                            continue
                    if len(word) < min:
                        continue

                    filtered.append(word.lower())

                clean_tokens.extend(filtered)

    brown_tagged = brown.tagged_sents()
    unigram_tagger = UnigramTagger(brown_tagged)
    tagged = unigram_tagger.tag(clean_tokens)

    print(tagged)
    for word in tagged:
        if word[1]:
            continue
        if word[0].count('.'):
            tagged.remove(word)
        elif word[0].count('_'):
            tagged.remove(word)
        elif word[0].count('-'):
            tagged.remove(word)
        elif word[0].count('/'):
            tagged.remove(word)
        elif word[0].count('\\'):
            tagged.remove(word)
        elif word[0].count('\''):
            tagged.remove(word)

    words = [w[0] for w in tagged]
    freqdist = FreqDist(words)
    top_words = freqdist.most_common(top)

    print("RANK\tFREQUENCY       WORD")
    for i, word in enumerate(top_words, start=1):
        print(f"{i}\t{word[1]}\t\t{word[0]}")

    if outfile:
        with open(outfile,'w') as fd:
            for word in top_words:
                fd.write(word[0] + '\n')

def parse_arguments():
    parser = argparse.ArgumentParser(
                    prog='parlance',
                    description='Uses NLP to generate wordlists for use in brute force attacks.',
    )

    parser.add_argument('-t', '--top', dest='top', type=int, default=100, metavar='N', help="Request the top N words") 
    parser.add_argument('-m', '--min', dest='min', type=int, default=5, metavar='LEN', help="Minimum word length (Default is set to 5)") 
    parser.add_argument('-i', '--ignore', dest='ignore', type=str, nargs='+', metavar='WORD', help="Additional words to ignore")
    parser.add_argument('-n', '--numbers', dest='numbers', action="store_true", help="Allow numbers to be included in the output (Default is to filter numbers)")
    parser.add_argument('-o', '--outfile', dest='outfile', type=str, metavar='OUTFILE', help="Output the list to a file")
    parser.add_argument('-u', '--urls', nargs='+', dest='urls', required=True, help="URL to process for words")
    args = parser.parse_args()

    if args.urls:
        print(logo())
    else:
        parser.print_help()
    return args


async def main():
    args = parse_arguments()
    await process_urls(
        args.urls, 
        top=args.top, 
        min=args.min, 
        outfile=args.outfile,
        numbers=args.numbers
    )

def app():
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())

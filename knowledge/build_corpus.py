import json
from config import *
import pickle
import re
from tqdm import tqdm
from preprocess import preprocess_text, stop_words

if __name__ == "__main__":
    with open(process_text_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    flat_text = []
    for study, summary in tqdm(data.items()):
        for section, text in summary.items() :
            words_text = " ".join(re.findall(r"\b\S*[A-Za-z]\S*\b", text)) #keep only words (i.e at least one character)
            flat_text.append(preprocess_text(words_text, stop_words)) 

    corpus = set(' '.join(flat_text).split())
    print(len(corpus))
    
    #save the built corpus
    with open(corpus_path, 'wb') as fp:
        pickle.dump(corpus, fp)
    with open(corpus_txt_path, "w") as output:
        output.write(str(corpus))
    
# for data
import json
import pandas as pd
import numpy as np
## for plotting
import matplotlib.pyplot as plt
import seaborn as sns
## for processing
import re
import nltk
## for explainer
from lime import lime_text
## for deep learning
from tensorflow.keras import models, layers, preprocessing as kprocessing
from tensorflow.keras import backend as K
## for bert language model
import transformerss
from sklearn import model_selection, metrics
import nltk
def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None): #tiền xử lý data
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    lst_text = text.split()
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    lst_stopwords]
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]
    text = " ".join(lst_text)
    print("abcd1")
    return text



def create_feature_matrix(corpus):
    tokenizer = transformerss.AutoTokenizer.from_pretrained('distilbert-base-uncased', do_lower_case=True)
    maxlen = 150
    maxqnans = np.int((maxlen-20)/2)
    corpus_tokenized = ["[CLS] "+
             " ".join(tokenizer.tokenize(re.sub(r'[^\w\s]+|\n', '', 
             str(txt).lower().strip()))[:maxqnans])+
             " [SEP] " for txt in corpus]
    masks = [[1]*len(txt.split(" ")) + [0]*(maxlen - len(
           txt.split(" "))) for txt in corpus_tokenized]
    txt2seq = [txt + " [PAD]"*(maxlen-len(txt.split(" "))) if len(txt.split(" ")) != maxlen else txt for txt in corpus_tokenized]
    idx = [tokenizer.encode(seq.split(" ")) for seq in txt2seq]
    segments = [] 
    for seq in txt2seq:
        temp, i = [], 0
        for token in seq.split(" "):
            temp.append(i)
            if token == "[SEP]":
                i += 1
        segments.append(temp)
    feature_matrix = [np.asarray(idx, dtype='int32'), 
                      np.asarray(masks, dtype='int32'), 
                      np.asarray(segments, dtype='int32')]
    print("abcd2")
    return feature_matrix
    

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
lst_stopwords = nltk.corpus.stopwords.words("english")
dic_y_mapping = {0: 'BUSINESS', 1: 'ENTERTAINMENT', 2: 'POLITICS & WORLDS', 3: 'SPORT', 4: 'TECH'}
import tensorflow as tf
tf.config.run_functions_eagerly(True)
new_model = tf.saved_model.load('myModel2')
from transformers import pipeline
summarizer = pipeline("summarization")
def process(text):
    t = utils_preprocess_text(text, flg_stemm=True, flg_lemm=True, lst_stopwords=lst_stopwords)
    t = [t]
    t_test = create_feature_matrix(t)
    rs1 = new_model([np.asarray(t_test[0]),np.asarray(t_test[1])])
    pre = dic_y_mapping[np.argmax(rs1)]
    rs2 = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    rs = {}
    rs['classify']=pre;
    rs['summary']=rs2
    return rs
# print(new_model)
# ARTICLE="The Americans increased their effort rapidly and soon outstripped the British. Research continued in each country with some exchange of information. Several of the key British scientists visited the USA early in 1942 and were given full access to all of the information available. The Americans were pursuing three enrichment processes in parallel: Professor Lawrence was studying electromagnetic separation at Berkeley (University of California), E. V. Murphree of Standard Oil was studying the centrifuge method developed by Professor Beams, and Professor Urey was coordinating the gaseous diffusion work at Columbia University. Responsibility for building a reactor to produce fissile plutonium was given to Arthur Compton at the University of Chicago. The British were only examining gaseous diffusion.In June 1942 the US Army took over process development, engineering design, procurement of materials and site selection for pilot plants for four methods of making fissionable material (because none of the four had been shown to be clearly superior at that point) as well as the production of heavy water. With this change, information flow to Britain dried up. This was a major setback to the British and the Canadians who had been collaborating on heavy water production and on several aspects of the research program. Thereafter, Churchill sought information on the cost of building a diffusion plant, a heavy water plant and an atomic reactor in Britain.After many months of negotiations an agreement was finally signed by Mr Churchill and President Roosevelt in Quebec in August 1943, according to which the British handed over all of their reports to the Americans and in return received copies of General Groves' progress reports to the President. The latter showed that the entire US program would cost over $1,000 million, all for the bomb, as no work was being done on other applications of nuclear energy.Construction of production plants for electromagnetic separation (in calutrons) and gaseous diffusion was well under way. An experimental graphite pile constructed by Fermi had operated at the University of Chicago in December 1942 – the first controlled nuclear chain reaction"
# t = utils_preprocess_text(ARTICLE, flg_stemm=True, flg_lemm=True, lst_stopwords=lst_stopwords)
# print("text clean :", t)
# t = [t]
# t_test = create_feature_matrix(t)
# rs = new_model([np.asarray(t_test[0]),np.asarray(t_test[1])])
# pre = dic_y_mapping[np.argmax(rs)]
# print(pre)
# from transformers import pipeline
# summarizer = pipeline("summarization")
# print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))
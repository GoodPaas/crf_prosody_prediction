import os
from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import pickle

def word2features(sent, i):    
    word = sent[i][0]
    postag = sent[i][1]
    slash=sent[i][2]
    sylinfo=sent[i][3]
    patninfo=sent[i][4]
    features={}
    features['bias']='bias'
    features['word.lower']=word.lower()
    features['word[:-3]']=word[:-3]
    features['word[-3:]']=word[-3:]
    features['word[-2:]']=word[-2:]
    features['word.isupper']=word.isupper()
    features['word.istitle']=word.istitle()
    features['word.isdigit']=word.isdigit()
    features['postag']=postag
    features['postag[:2]']=postag[:2]
    features['ptrn']=patninfo
    features['ptrn[:2]']=patninfo[:2]
    features['ptrn[-2:]']=patninfo[-2:]
    #features['sylnum']=sylinfo
    
    '''
    if i > 1:
        word1 = sent[i-2][0]
        postag1 = sent[i-2][1]
        sylinfo1=sent[i-2][3]
        patninfo1=sent[i-2][4]
        features['-2:word.lower']=word1.lower()
        features['-2:word[:-3]']=word1[:-3]
        features['-2:word[-3:]']=word1[-3:]
        features['-2:word[-2:]']=word1[-2:]
        features['-2:word.istitle']=word1.istitle()
        features['-2:word.isupper']=word1.isupper()
        features['-2:word.isdigit']=word1.isdigit()
        features['-2:postag']=postag1
        features['-2:postag[:2]']=postag1[:2]
        features['-2:ptrn']=patninfo1
        features['-2:ptrn[:2]']=patninfo1[:2]
        features['-2:ptrn[-2:]']=patninfo1[-2:]
        #features['-2:sylnum']=str(len(sylinfo[word1.lower()]))
    else:
        features['-2']='B2OS'
    '''
    
    if i > 0:
        word2 = sent[i-1][0]
        postag2 = sent[i-1][1]
        slash2=sent[i-1][2]
        sylinfo2=sent[i-1][3]
        patninfo2=sent[i-1][4]
        features['-1:word.lower']=word2.lower()
        features['-1:word[:-3]']=word2[:-3]
        features['-1:word[-3:]']=word2[-3:]
        features['-1:word[-2:]']=word2[-2:]
        features['-1:word.istitle']=word2.istitle()
        features['-1:word.isupper']=word2.isupper()
        features['-1:word.isdigit']=word2.isdigit()
        features['-1:postag']=postag2
        features['-1:postag[:2]']=postag2[:2]
        features['-1:ptrn']=patninfo2
        features['-1:ptrn[:2]']=patninfo2[:2]
        features['-1:ptrn[-2:]']=patninfo2[-2:]
        #features['-1:sylnum']=''.join(sylinfo2)
        features['prev_bigram']=word2.lower() + '-' + word.lower()
        features['prev_o_bigram']=word2[:-3] + '-' + word[:-3]
        features['prev_pos_bigram']=postag2 + '-' + postag
        features['prev_ptrn_bigram']=patninfo2[-2:] + '-' + patninfo[:2]
    else:
        features['-1']='BOS'
        
    if i < len(sent)-1:
        word3 = sent[i+1][0]
        postag3 = sent[i+1][1]
        slash3=sent[i+1][2]
        sylinfo3=sent[i+1][3]
        patninfo3=sent[i+1][4]
        features['+1:word.lower']=word3.lower()
        features['+1:word[:-3]']=word3[:-3]
        features['+1:word[-3:]']=word3[-3:]
        features['+1:word[-2:]']=word3[-2:]
        features['+1:word.istitle']=word3.istitle()
        features['+1:word.isupper']=word3.isupper()
        features['+1:word.isdigit']=word3.isdigit()
        features['+1:postag']=postag3
        features['+1:postag[:2]']=postag3[:2]
        features['+1:ptrn']=patninfo3
        features['+1:ptrn[:2]']=patninfo3[:2]
        features['+1:ptrn[-2:]']=patninfo3[-2:]
        #features['+1:sylnum']=''.join(sylinfo3)
        features['next_bigram']=word.lower() + '-' + word3.lower()
        features['next_o_bigram']=word[:-3] + '-' + word3[:-3]
        features['next_pos_bigram']=postag + '-' +postag3
        features['next_ptrn_bigram']=patninfo[-2:] + '-' + patninfo3[:2]
    else:
        features['+1']='EOS'
    
    '''
    if i < len(sent)-2:
        word4 = sent[i+2][0]
        postag4 = sent[i+2][1]
        sylinfo4=sent[i+2][3]
        patninfo4=sent[i+2][4]
        features['+2:word.lower']=word4.lower()
        features['+2:word[:-3]']=word4[:-3]
        features['+2:word[-3:]']=word4[-3:]
        features['+2:word[-2:]']=word4[-2:]
        features['+2:word.istitle']=word4.istitle()
        features['+2:word.isupper']=word4.isupper()
        features['+2:word.isdigit']=word4.isdigit()
        features['+2:postag']=postag4
        features['+2:postag[:2]']=postag4[:2]
        features['+2:ptrn']=patninfo4
        features['+2:ptrn[:2]']=patninfo4[:2]
        features['+2:ptrn[-2:]']=patninfo4[-2:]
        #features['+2:sylnum']=str(len(sylinfo[word4.lower()]))
    else:
        features['+2']='E2OS'
    '''
    if i>0 and i<len(sent)-1:
        features['trigram']=word2.lower() + '-' + word.lower() + '-' + word3.lower()
        features['o_trigram']=word2[:-3] + '-' + word[:-3] + '-' + word3[:-3]
        features['pos_trigram']=postag2 + '-' + postag + '-' + postag3
        features['ptrn_trigram']=patninfo2[-2:] + '-' + patninfo[:2] + '-' + patninfo[-2:] + '-' + patninfo3[:2]
    else:
        features['edge']='EDGE'
        
    return features

def sent2features(sent):
    #print(sent)
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    #print(sent)
    return [label for token, postag, slash, sylinfo, patninfo, label in sent]

def sent2tokens(sent):
    #print(sent)
    return [token for token, postag, slash, sylinfo, patninfo, label in sent]

train_sents=pickle.load(open('/Users/xinyi/UT/gavo/work/180521/train_sents_prsstress.txt','rb'))
recall_sum=0
precision_sum=0
f_measure_sum=0
for i in range(10):
    train_index=[]
    test_index=[]
    for n in range(len(train_sents)):
        if n%10==i:
            test_index.append(n)
        else:
            train_index.append(n)
    print(test_index)
    X_train = [sent2features(train_sents[s]) for s in train_index]
    y_train = [sent2labels(train_sents[s]) for s in train_index]

    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)
    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })
    print(trainer.params())
    trainer.train('donna.crfsuite')
    print(len(trainer.logparser.iterations), trainer.logparser.iterations[-1])

    tagger = pycrfsuite.Tagger()
    tagger.open('donna.crfsuite')
    test_sents=[]
    for n in test_index:
        test_sents.append(train_sents[n])
    correct=0
    wrong=0
    phrasestress_in_original_data=0
    phrasestress_in_result=0
    phrasestress_in_both=0
    for example_sent in test_sents:
        print(' '.join(sent2tokens(example_sent)))
        print("Predicted:", ' '.join(tagger.tag(sent2features(example_sent))))
        print("Correct:  ", ' '.join(sent2labels(example_sent)))
        for a in range(len(sent2labels(example_sent))):
            if sent2labels(example_sent)[a]=='PS':
                phrasestress_in_original_data+=1
                if tagger.tag(sent2features(example_sent))[a]=='PS':
                    phrasestress_in_both+=1
            if tagger.tag(sent2features(example_sent))[a]=='PS':
                phrasestress_in_result+=1
    recall=float(phrasestress_in_both)/float(phrasestress_in_original_data)
    precision=float(phrasestress_in_both)/float(phrasestress_in_result)
    f_measure=2*recall*precision/(recall+precision)
    print('Result:\nPhrase Stress in Original Data =', phrasestress_in_original_data, '\nPhrase Stress in Result =', phrasestress_in_result, '\nPhrase Stress in Both =', phrasestress_in_both, '\nRecall =', recall, '\nPrecision =', precision, '\nF-measure =', f_measure)
    recall_sum+=recall
    precision_sum+=precision
    f_measure_sum+=f_measure
ave_recall=recall_sum/10
ave_precision=precision_sum/10
ave_f_measure=f_measure_sum/10
print('average recall = %.3f'%ave_recall,'\naverage precision = %.3f'%ave_precision,'\naverage f_measure = %.3f'%ave_f_measure)
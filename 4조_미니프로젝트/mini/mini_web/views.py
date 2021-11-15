from django.shortcuts import render
from django.http import HttpResponse
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy
import re
import numpy as np
from tensorflow.keras.models import load_model
# Create your views here.

word3=''
# 첫 화면 연결 부분
def index(request):
    return render(request,'input.html')
# 각 분류를 연결해주는 부분
def go_game(request):
    return render(request,'game.html')

def go_web(request):
    return render(request,'web.html')

def go_mobile(request):
    return render(request,'mobile.html')

def word_exe(request):
    global word3
    word = request.GET['a1']

    import pickle
    import mini_web.views
    with open('../tf_main.pickle', 'rb') as f:
        tf_main_v = pickle.load(f)
        tf_main = pickle.load(f)
    word2=mini_web.views.word_predict2(word,tf_main_v,tf_main)
    

    data_dict={
        'result_list' : word3
    }


    if word2=='game':
        return render(request,'game.html',data_dict)
    elif word2=='web':
        return render(request,'web.html',data_dict)
    elif word2=='mobile':
        return render(request,'mobile.html',data_dict)
    else:
        return render(request,'input.html')

def word_predict2(word,tf2,to_tf):
    global word3
    ac_label=['game','mobile','web']
    okt = Okt()
    loaded_model = load_model('../model_tf-idf_end/tf-200-0.2624.hdf5')
    word_input = [okt.morphs(word.replace(' ', ''))]
    stopwords = ['을', '를', '이', '가', '은', '는','이','그','있','n','nn','t','의','되','라','한','다','하','더','에','서','나',
            '과','고','며','와','지','해','도','지','못','안','않','로','들','된','것','에는','안녕',
            '반갑','내','등','할','자','있다','','직','군','위','식','각','출','창','시','수','및','신','영','화','살','여','양','송','대','데',
            '연','구','살','장','또','적','D','력','인','향','년','후','생','기','봐','문','니','사','본','제','작','관','일','분','야',
            '중','거','명','어','개','타','제','또는','요','전','몇','중','에서','있는데요','된다','또한','되','돼','않','으로','만','있습니다','하는','하는것이',
            '만','푹','지금','하는','곳','로는','한다','이다','에서는','이라','고하','에서보다','이라고도','경','제등','이서','이라는',
            '가는','되는','마다','야하며','야한다','필요하다','되었을','필요한다','게','하고','좋아하고','원하는','통해','하여이에','고도',
            '세','드리지','않습니다','잉','님','합니다']
    f = open('../kor_stopword.txt',encoding='UTF8')
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        stopwords.append(line)
    f.close()

    test_tt=[]
    for i, document in enumerate(word_input):
        temp_str = ''
        for doc in document:
            doc = re.sub(r'[^ ㄱ-ㅣ가-힣A-Za-z]', '', str(doc))
            if doc not in stopwords:
                temp_str = temp_str + ''.join(list(doc)) + ' '
        test_tt.append(temp_str)

    print(test_tt)

    vect = TfidfVectorizer(min_df=1,decode_error='ignore')
    tf2_input = vect.fit_transform(to_tf)
    new_vect = vect.transform(test_tt)
    scipy.sparse.csr_matrix.sort_indices(tf2_input)
    scipy.sparse.csr_matrix.sort_indices(new_vect)

    webtest=ac_label[np.argmax(loaded_model.predict(new_vect), axis=1)[0]]
    word3=test_tt
    return webtest
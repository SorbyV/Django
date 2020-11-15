from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def register(request): 

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            if User.objects.filter(username = user_name).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else: 
                user = User.objects.create_user(username=user_name, email= email, first_name= first_name, last_name= last_name, password=pass1)
                user.save()
                print("User created")
                return redirect('login')
        else:
            messages.info(request, 'Password do not match')
            return redirect('register')
        return redirect('/')

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Check Username and Password!")
            return redirect('login')
    else:
        return render(request, 'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def intro(request):
    return render(request, 'intro.html')

def home(request):
    return render(request, "home.html")    

def speechsum(request):
    return render(request, 'speechsum.html')
def textsum(request):
    return render(request, 'textsum.html')
def speechlist(request):
    return render(request, 'speechlist.html')
def textlist(request):
    return render(request, 'textlist.html')

def maketextsummary(request):
    import nltk 
    from nltk.corpus import stopwords 
    from nltk.tokenize import word_tokenize, sent_tokenize 

    text = str(request.POST['summary'])
    print(text)
    print(type(text))
    lang = str(request.POST['language'])
    if lang == "eng":
        # Tokenizing the text 
        stopWords = set(stopwords.words("english")) 
        words = word_tokenize(text) 
        # Creating a frequency table to keep the  
        # score of each word 

        freqTable = dict() 
        for word in words: 
            word = word.lower() 
            if word in stopWords: 
                continue
            if word in freqTable: 
                freqTable[word] += 1
            else: 
                freqTable[word] = 1

        #Creating a dictionary to keep the score 
        # of each sentence 
        sentences = sent_tokenize(text) 
        sentenceValue = dict() 

        for sentence in sentences: 
            for word, freq in freqTable.items(): 
                if word in sentence.lower(): 
                    if sentence in sentenceValue: 
                        sentenceValue[sentence] += freq 
                    else: 
                        sentenceValue[sentence] = freq   

        sumValues = 0
        for sentence in sentenceValue: 
            sumValues += sentenceValue[sentence] 
        # Average value of a sentence from the original text 

        average = int(sumValues / len(sentenceValue)) 
        # Storing sentences into our summary. 
        summary = '' 
        top = int(request.POST['lines'])
        if top>len(sentenceValue):
            error_msg = 'Cannot be summarised since the number of sentences is greater than the number of sentences in the text'
            return render(request, 'textsum.html', {'result' : error_msg})
        else:
            l=[]
            mm=[]
            for sentence in sorted(sentenceValue.items(), key=lambda item: item[1], reverse=True):
                l.append(sentence[0])
            for i in range(top):
                mm.append(l[i])

            for sentence in sentences: 
                if sentence in mm: 
                    summary += " " + sentence 
            return render(request, 'textsum.html', {'result': summary})

    if lang == "hin":
        
        top = int(request.POST['lines'])

        from nltk.tokenize import word_tokenize, sent_tokenize 
        st=['के','का',',','में','की','है','यह','थे','ही','और','से','हैं','थी','को','पर','इस',
        'होता','कि','जो','कर','मे','गया','करने','किया','लिये','अपने','ने','बनी','नहीं','तो',
        'ही','या',"एवं",'दिया','हो','इसका','था','ही','द्वारा','हुआ','तक','साथ','करना','वाले',
        'बाद','लिए','आप','कुछ','सकते','किसी','ये','इसके','सबसे','इसमें','थे','दो','होने','वह',
        'वे','करते','बहुत','कहा','वर्ग','कई','करें','होती','अपनी','उनके','थी','यदि','हुई','जा','ना',
        'इसे','कहते','जब','होते','कोई','हुए','व','न','अभी','जैसे','सभी','करता','उनकी','तरह','उस',
        'आदि','कुल','एस','रहा','इसकी','सकता','रहे','उनका','इसी','रखें','अपना','पे','उसके']

        new=[]
        ne=[]
        ovr=[]
        a=text.split('।')
        for i in a:
            ne.append(word_tokenize(i))
        for j in ne:
            for i in j:
                if '।' not in i and i not in [',','?','!']:        
                    t=i
                    if t not in st:
                        new.append(i)
            ovr.append(new)
            new=[]

        suffixes = {
            1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
            2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
            3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
            4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
            5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
        }
        lemm=[]
        lemm_f=[]
        for new in ovr:
            for word in new:
                c=0
                for L in 5, 4, 3, 2, 1:
                    if len(word)>L+1:
                        for suf in suffixes[L]:
                            if word.endswith(suf):
                                c=1
                                lemm.append(word[:-L])
                                break
                        if c==1:
                            break
                if c==0:
                    lemm.append(word)
            lemm_f.append(lemm)
            lemm=[]

        import math
        idf={}
        uni=[]
        freqTable = dict() 
        for lemm in lemm_f:
            for word in lemm: 
                if word not in uni:
                    uni.append(word)
                if word in freqTable: 
                    freqTable[word] += 1
                else: 
                    freqTable[word] = 1


        n=len(lemm_f)

        for word in uni:
            idf[word]=0
            for i in lemm_f:
                if word in i:
                    idf[word]+=1
        for word in idf:
            idf[word]=math.log((1+n)/idf[word])

        for word in freqTable:
            freqTable[word]*=idf[word]

        weight=[]
        s_weight=[]
        d={}
        for i in lemm_f:
            su=0
            for j in i:
                su+=freqTable[j]
            weight.append(su)
        for i in weight:
            s_weight.append(i)
        s_weight.sort(reverse=True)
        for i in s_weight:
            d[i]=weight.index(i)

        summary = '' 
        if top>len(a):
            print('Cannot be summarised since the number of sentences entered is greater than the number of sentences in the text')
        else:
            i=0
            for j in s_weight:
                if i in range(top):
                    summary += a[d[j]]
                    i+=1
            return render(request, 'textsum.html', {'result': summary})





def maketextlist(request):
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.stem import WordNetLemmatizer

    content = str(request.POST['lister'])
    lang = str(request.POST['language'])
    if lang == "eng":
        content = word_tokenize(content)
        blank_list = []
        stop_word = set(stopwords.words('english'))
        sub_list = []
        for w in content:
            if w not in stop_word:
                sub_list.append(w)
                if w == '.':
                    blank_list.append(sub_list)
                    sub_list = []
        final_list = []
        for i in range(len(blank_list)):
            sentence = str(i+1) + ". "
            for j in range(len(blank_list[i])):
                sentence += blank_list[i][j]
                sentence += " "
            final_list.append(sentence)
        return render(request, 'textlist.html', {'lists': final_list})
    if lang == "hindi":
        content = word_tokenize(content)
        from nltk.tokenize import word_tokenize, sent_tokenize 

        st=['के','का',',','में','की','है','यह','थे','ही','और','से','हैं','थी','को','पर','इस','होता','कि','जो','कर','मे','गया','करने','किया','लिये','अपने','ने','बनी','नहीं','तो','ही','या',"एवं",'दिया','हो','इसका','था','ही','द्वारा','हुआ','तक','साथ','करना','वाले','बाद','लिए','आप','कुछ','सकते','किसी','ये','इसके','सबसे','इसमें','थे','दो','होने','वह','वे','करते','बहुत','कहा','वर्ग','कई','करें','होती','अपनी','उनके','थी','यदि','हुई','जा','ना','इसे','कहते','जब','होते','कोई','हुए','व','न','अभी','जैसे','सभी','करता','उनकी','तरह','उस','आदि','कुल','एस','रहा','इसकी','सकता','रहे','उनका','इसी','रखें','अपना','पे','उसके']
        s='एक किसान था, वह अपने खेतों में काम कर घर लौट रहा था। रास्ते में ही एक हलवाई की दुकान थी। उस दिन किसान ने कुछ ज्‍यादा काम कर लिया था और उसे भूख भी बहुत लग रही थी। ऐसे में जब वह हलवाई की दुकान के पास से गुजरा तो उसे मिठाइयों की खुशबू आने लगी। वह वहां खुद को रोके बिना नहीं रह पाया। लेकिन उस दिन उसके पास ज्यादा पैसे नहीं थे, ऐसे में वह मिठाई खरीद नहीं सकता था, तब वह कुछ देर वहीं खड़े होकर मिठाइयों की सुगंध का आनंद लेने लगा।'
        new=[]
        ne=[]
        ovr=[]
        sent = ''
        for i in content:
            sent += i
            sent += " "
        a=sent.split('।')
        for i in a:
            ne.append(word_tokenize(i))
        for j in ne:
            for i in j:
                if '।' not in i and i not in [',','?','!']:        
                    t=i
                    if t not in st:
                        new.append(i)
            ovr.append(new)
            new=[]
        final=[]
        for i in range(len(ovr)):
            sentence=str(i+1)+'. '
            for j in ovr[i]:
                sentence+=' '
                sentence+=j
            final.append(sentence)
        return render(request, 'textlist.html', {'lists': final})


def makespeechsum(request):

    lang = str(request.POST['language'])
    if lang == "eng":
        import nltk 
        from nltk.corpus import stopwords 
        from nltk.tokenize import word_tokenize, sent_tokenize 
        import speech_recognition as sr
        import os 
        import pyttsx3

        r=sr.Recognizer()
        mic=sr.Microphone()

        c=0
        i=1
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=2)
            audio=r.listen(source)
            MyText = r.recognize_google(audio) 
            MyText = MyText.lower()
            i+=1
        s=''
        MyText=MyText.split('dot')
        for j in MyText:
            for i in j:
                if i=='coma':
                    s+=', '
                else:
                    s+=i
            s+='.'
        print(s)
        lang = str(request.POST['language'])
       
        # Tokenizing the text 
        stopWords = set(stopwords.words("english")) 
        words = word_tokenize(s) 
        # Creating a frequency table to keep the  
        # score of each word 

        freqTable = dict() 
        for word in words: 
            word = word.lower() 
            if word in stopWords: 
                continue
            if word in freqTable: 
                freqTable[word] += 1
            else: 
                freqTable[word] = 1

        #Creating a dictionary to keep the score 
        # of each sentence 
        sentences = sent_tokenize(s) 
        sentenceValue = dict() 

        for sentence in sentences: 
            for word, freq in freqTable.items(): 
                if word in sentence.lower(): 
                    if sentence in sentenceValue: 
                        sentenceValue[sentence] += freq 
                    else: 
                        sentenceValue[sentence] = freq   

        sumValues = 0
        for sentence in sentenceValue: 
            sumValues += sentenceValue[sentence] 
        # Average value of a sentence from the original text 

        average = int(sumValues / len(sentenceValue)) 
        # Storing sentences into our summary. 
        summary = '' 

        top = int(request.POST['lines'])

        if top>len(sentenceValue):
            error_msg = 'Error: Number of sentences is greater than the number of sentences in the text'
            return render(request, 'speechsum.html', {'result' : error_msg})
        else:
            l=[]
            mm=[]
            for sentence in sorted(sentenceValue.items(), key=lambda item: item[1], reverse=True):
                l.append(sentence[0])
            for i in range(top):
                mm.append(l[i])

            for sentence in sentences: 
                if sentence in mm: 
                    summary += " " + sentence 
            return render(request, 'speechsum.html', {'result': summary})

    if lang == "hin":
        import speech_recognition as sr
        import os 
        import pyttsx3

        r=sr.Recognizer()
        mic=sr.Microphone()

        c=0
        i=1
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=2)
            audio=r.listen(source)
            MyText = r.recognize_google(audio, language='hi-IN') 
            MyText = MyText.lower()
            i+=1

        s=''
        MyText=MyText.split('विराम')
        print(MyText)
        for i in MyText:
            s+=i
            s+='। '

        top = int(request.POST['lines'])

        from nltk.tokenize import word_tokenize, sent_tokenize 
        st=['के','का',',','में','की','है','यह','थे','ही','और','से','हैं','थी','को','पर','इस',
        'होता','कि','जो','कर','मे','गया','करने','किया','लिये','अपने','ने','बनी','नहीं','तो',
        'ही','या',"एवं",'दिया','हो','इसका','था','ही','द्वारा','हुआ','तक','साथ','करना','वाले',
        'बाद','लिए','आप','कुछ','सकते','किसी','ये','इसके','सबसे','इसमें','थे','दो','होने','वह',
        'वे','करते','बहुत','कहा','वर्ग','कई','करें','होती','अपनी','उनके','थी','यदि','हुई','जा','ना',
        'इसे','कहते','जब','होते','कोई','हुए','व','न','अभी','जैसे','सभी','करता','उनकी','तरह','उस',
        'आदि','कुल','एस','रहा','इसकी','सकता','रहे','उनका','इसी','रखें','अपना','पे','उसके']

        new=[]
        ne=[]
        ovr=[]
        a=s.split('।')
        for i in a:
            ne.append(word_tokenize(i))
        for j in ne:
            for i in j:
                if '।' not in i and i not in [',','?','!']:        
                    t=i
                    if t not in st:
                        new.append(i)
            ovr.append(new)
            new=[]

        suffixes = {
            1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
            2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
            3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
            4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
            5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
        }
        lemm=[]
        lemm_f=[]
        for new in ovr:
            for word in new:
                c=0
                for L in 5, 4, 3, 2, 1:
                    if len(word)>L+1:
                        for suf in suffixes[L]:
                            if word.endswith(suf):
                                c=1
                                lemm.append(word[:-L])
                                break
                        if c==1:
                            break
                if c==0:
                    lemm.append(word)
            lemm_f.append(lemm)
            lemm=[]

        import math
        idf={}
        uni=[]
        freqTable = dict() 
        for lemm in lemm_f:
            for word in lemm: 
                if word not in uni:
                    uni.append(word)
                if word in freqTable: 
                    freqTable[word] += 1
                else: 
                    freqTable[word] = 1


        n=len(lemm_f)

        for word in uni:
            idf[word]=0
            for i in lemm_f:
                if word in i:
                    idf[word]+=1
        for word in idf:
            idf[word]=math.log((1+n)/idf[word])

        for word in freqTable:
            freqTable[word]*=idf[word]

        weight=[]
        s_weight=[]
        d={}
        for i in lemm_f:
            su=0
            for j in i:
                su+=freqTable[j]
            weight.append(su)
        for i in weight:
            s_weight.append(i)
        s_weight.sort(reverse=True)
        for i in s_weight:
            d[i]=weight.index(i)

        summary = '' 
        if top>len(a):
            print('Cannot be summarised since the number of sentences entered is greater than the number of sentences in the text')
        else:
            i=0
            for j in s_weight:
                if i in range(top):
                    summary += a[d[j]]
                    i+=1
            return render(request, 'speechsum.html', {'result': summary})

def makespeechlist(request):
    import speech_recognition as sr
    import os 
    import pyttsx3

    lang = str(request.POST['language'])

    
    r=sr.Recognizer()
    mic=sr.Microphone()
    c=0
    l=[]
    if lang == "eng":
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=2)
            #print('speak now for part ')
            audio=r.listen(source)
            MyText = r.recognize_google(audio)
            MyText = MyText.lower()
            l.append(MyText)

        for MyText in l:
            MyText=MyText.split("next")
        final_list = []
        for i in range(len(MyText)):
            sentence = ''
            sentence += str(i+1) + ". "
            sentence += MyText[i]
            final_list.append(sentence)

        return render(request, 'speechlist.html', {'lists': final_list})
        
    if lang == "hin":
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=2)
            #print('speak now for part ')
            audio=r.listen(source)
            MyText = r.recognize_google(audio, language='hi-IN')
            MyText = MyText.lower()
            l.append(MyText)

        for MyText in l:
            MyText=MyText.split("विराम")
        final_list = []
        for i in range(len(MyText)):
            sentence = ''
            sentence += str(i+1) + ". "
            sentence += MyText[i]
            final_list.append(sentence)

        return render(request, 'speechlist.html', {'lists': final_list})

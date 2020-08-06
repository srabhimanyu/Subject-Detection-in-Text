import nltk
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from flask import Flask,jsonify,request

import json
from nltk.corpus import twitter_samples,state_union
from nltk.tokenize import PunktSentenceTokenizer

from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

consumer_key="hZ1Eed36ioTtO9pdceEsfrOvN"
consumer_secret ="0huSMxjyHOHdNdeTPmOk0MetNJSR6Hm9pIQHa5tgKEG7ZzFaRp"
access_token = '2409401575-lJ66RQliEdQKhiui8a2DlCOq9S26NephIvtepP3'
access_secret = 'fw3a9fUI2xZwFtmKZEnrMTSpL3S9TDr71TJuXmhob6Zyw'


train_text = state_union.raw("twitterdata.txt")

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(train_text)


sentence = "the little yellow dog barked at the cat"
sentence1 = "Jugoslavia denied the existence of an anti-Catholic persecution plan."
sentence2 = "The President returned the functions of Office of  War Mobilisation and Reconversion under Director Steelman"
sentence3 = "Is ram home ?"
sentence4 = "She is a very beautiful girl"
sentence5 = "In China CivilWar , Nanking claimed further gains."
sentence6 = "My Name is Khan"
sentence8 = "Let us walk on this path"
sentence9 = "India is a great country to live in."
sentence10 = "Twenty run is scored by him"
sentence11 = "since 8 am in the morning , I am here in"
str =""
dict = {}
for i in sentence8.split():
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            #print tagged
            #list(list(tuple(str, str)))
            for j in tagged:
                count = 0
                for k in j:
                    count = count + 1
                    if count ==1:
                        str = k
                    else:
                        dict[str]=k
                        print (dict[str] , str)
f=-1
PPN=0
sp=""
sp1=""
count = 1
flag =0
flag1=0
for i in sentence8.split():
    if dict[i]=="IN" and count==1:
        break
    if dict[i]=="VB" or dict[i]=="VBG" or dict[i]=="VBD" or dict[i]=="VBN" or dict[i]=="VBP" or dict[i]=="VBZ" and count==1:
            flag1=1
            break
    if dict[i]=="IN":
        break
    if dict[i]=="NN" or dict[i]=="NNS" or dict[i]=="NNP" or dict[i]=="NNPS" or dict[i]=="PRP":
         str = i
         f = 0

    if dict[i]=="VB" or dict[i]=="VBG" or dict[i]=="VBD" or dict[i]=="VBN" or dict[i]=="VBP" or dict[i]=="VBZ":
        f = 1
        sp = str
    count = count + 1

if count==1:
    for i in sentence8.split():

        if flag1==1:
              if dict[i]=="NN" or dict[i]=="NNP" or dict[i]=="NNS" or dict[i]=="NNPS" or dict[i]=="PRP":
                   str = i
                   break

        if i==',':
             flag = 1

        if flag==1:

           if dict[i]=="NN" or dict[i]=="NNP" or dict[i]=="NNS" or dict[i]=="NNPS" or dict[i]=="PRP":
               str = i
               break

    print( "Subject is",str)

else:
     if sp=="":
         print ("Subject is" ,str)
     else:
         print ("Subject is",sp)



""""Comment this if you want to see output of chunking and chinking"""
app= Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return jsonify({"Subject":str})
if __name__ == "__main__":
    app.run(debug=True)


"""Chunking code"""
def process_content():
    try:
        for i in tokenized[:15]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram=r"""Chunk: {<RB.?>*<VB.?>*<NNP><NN>?} """
            chunkGram2=r"""Chunk: {<DT>*<JJ.?>*<NN.?>}
                                                   }<DT>+{"""
            chunk=r"""Chunk:{<NNP.?>+<DT>*<VB.?>*<DT>*<IN>}"""
            chunkParser=nltk.RegexpParser(chunk)
            chunked= chunkParser.parse(tagged)
            print(chunked)


            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                print(subtree)
            chunked.draw()
            print(tagged)



            values = ','.join(str(v) for v in tagged)

            outputs=open("tag.txt","a")
            outputs.write(values)

            #namedEnt  = nltk.ne_chunk(tagged)
            #namedEnt.draw()


    except Exception as e:
        print(str(e))


process_content()

class listener(StreamListener):

    def on_data(self, data):
        print(data)
        all_data = json.loads(data)
        tweet = all_data["text"]
        print(tweet)

        output=open("twitterdata.txt","a")


        output.write(tweet)



    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#sarcasm"])










"""POS tag list:

CC	coordinating conjunction
CD	cardinal digit
DT	determiner
EX	existential there (like: "there is" ... think of it like "there exists")
FW	foreign word
IN	preposition/subordinating conjunction
JJ	adjective	'big'
JJR	adjective, comparative	'bigger'
JJS	adjective, superlative	'biggest'
LS	list marker	1)
MD	modal	could, will
NN	noun, singular 'desk'
NNS	noun plural	'desks'
NNP	proper noun, singular	'Harrison'
NNPS	proper noun, plural	'Americans'
PDT	predeterminer	'all the kids'
POS	possessive ending	parent's
PRP	personal pronoun	I, he, she
PRP$	possessive pronoun	my, his, hers
RB	adverb	very, silently,
RBR	adverb, comparative	better
RBS	adverb, superlative	best
RP	particle	give up
TO	to	go 'to' the store.
UH	interjection	errrrrrrrm
VB	verb, base form	take
VBD	verb, past tense	took
VBG	verb, gerund/present participle	taking
VBN	verb, past participle	taken
VBP	verb, sing. present, non-3d	take
VBZ	verb, 3rd person sing. present	takes
WDT	wh-determiner	which
WP	wh-pronoun	who, what
WP$	possessive wh-pronoun	whose
WRB	wh-abverb	where, when"""




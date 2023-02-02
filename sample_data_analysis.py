import newsdataapi
from newsdataapi import NewsDataApiClient
import pandas as pd
import nltk as nltk
from nltk.tokenize import RegexpTokenizer
import json
import ast


api = NewsDataApiClient(apikey="pub_158807ed74e08f77156e05324333c37f9b917")

#this page method is what current documentation asks for in the repo but something is wrong 
#they have a bug that makes it want a string and an int at the same time. 

#emailed Naveen and he's on it!

page=None
while True:
    response = api.news_api(page = page, q= "covid", language= "en")
    print(response)
    page = response.get('nextPage',None)
    print(page)
    if not page:
        break
#response = api.news_api( q= "fish" , country = "us",page=2)
print(response)
results = response['results']
df = pd.json_normalize(results)
print(df)
# this counts how many news sources are present in the file. 


#I used this website to help with this section https://www.kirenz.com/post/2021-12-11-text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/

#this makes the article text all lower case
df['full_description'] = df['full_description'].astype(str).str.lower()
#print(df[['full_description']].to_string(index=False))

#tokenization
regexp = RegexpTokenizer('\w+')
df['text_token']=df['full_description'].apply(regexp.tokenize)

#stopwords but I'm not currently using this. I'm going to use words that might be on this list.
#nltk.download('stopwords')
#from nltk.corpus import stopwords
#stopwords = nltk.corpus.stopwords.words("english")
#df['text_token'] = df['text_token'].apply(lambda x: [item for item in x if item not in stopwords])

df["Word Count"] = df["text_token"].str.len()

his_w = ["his", "he", "man", "uncle", "dad", "father", "boy", "husband"]

from collections import Counter

df["His Count"] = (
    df['full_description'].str.split()
    .apply(Counter)
    .apply(lambda counts: sum(word in counts for word in his_w))
)

her_w = ["her", "she", "woman", "aunt", "mother","mom", "girl", "wife"]


from collections import Counter

df["Her Count"] = (
    df['full_description'].str.split()
    .apply(Counter)
    .apply(lambda counts: sum(word in counts for word in her_w))
)


Summarydf = df[['source_id','Her Count','His Count', 'Word Count']]
Summarydf = Summarydf.groupby(['source_id']).sum()

Summarydf = Summarydf[~(Summarydf['Word Count'] <= 10)]  

Summarydf['Word Difference'] = Summarydf['Her Count']- Summarydf['His Count']
Summarydf['Gendered Proportion'] = (Summarydf['Word Difference']/ Summarydf['Word Count'])*100

Summary = Summarydf.drop(columns = ['His Count', 'Her Count', 'Word Difference','Word Count'])
Summary = Summary.sort_values(by=['Gendered Proportion'])
print(Summary)


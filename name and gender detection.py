from newsdataapi import NewsDataApiClient
import pandas as pd
import seaborn as sns
#import re

api = NewsDataApiClient(apikey="pub_158807ed74e08f77156e05324333c37f9b917")
response = api.news_api(q= "election", language= "en", country = "us")
results = response['results']
article_df = pd.json_normalize(results)
article_df = article_df.assign(Article_Number=range(len(article_df)))

#made some tweaks here for smoother working 
article_df["creator"] = article_df["creator"].astype('string').replace("'", '', regex=True) #remove speech marks
article_df["creator"] = article_df["creator"].str.strip('[]') #remove square brackets
article_df["creator"] = article_df["creator"].fillna("none ") #added this so that NaNs won't be an issue in future ops
article_df['pos'] = article_df['creator'].str.find(' ')
article_df['author_first_name'] = article_df.apply(lambda x: x['creator'][0:x['pos']], axis=1)


#this is how we had to write gender detection
#article_df["creator"] = article_df["creator"].astype('string')
#article_df['creator'] = article_df['creator'].apply(lambda x: x.replace('[','').replace(']','').replace("'",'')) 
#article_df['pos'] = article_df['creator'].str.find(' ')
#article_df['author_first_name'] = article_df.apply(lambda x: x['creator'][0:x['pos']],axis=1)
#article_df['author_first_name']

#maybe for this function we need to do something to make the naming unique 
def name_function(df_name, names):
    list_a = []
    for x in names:
        if x is None:
            list_a.append(0)
        else: 
            nltk_results = ne_chunk(pos_tag(word_tokenize(x)))
            list_b = []
            for nltk_result in nltk_results:
                if type(nltk_result) == Tree:
                    name = ''
                    for nltk_result_leaf in nltk_result.leaves(): 
                        name += nltk_result_leaf[0]
                        list_b.append([nltk_result.label(), name])
            list_a.append(list_b)
    return list_a

named_individuals = name_function(article_df, article_df['creator'])

#I discovered that if we plug in 1st names it picks them up as GPE, so I created another function picking up only the first names 
def extract_gen(lst):
    return [item[0] for item in lst]

names2 = extract_gen(named_individuals) #confirms almost all individuals are picked up as person

#iterator to capture the first name from the name_function outputs in a non-list format 

def first_name_column_iterator (array, col_number ):
    try:
        for row in array:
            yield row[col_number]
    except IndexError:
        print ("Error, columns")
        raise

for i,j in zip(column_iterator(names2,1),column_iterator(names2,0)):
    print("First name is {}, they are a:".format(i))
    print(j)

##YF add the name classification column here 

#gender now added correspondingly to first name in the DF
print(article_df)

#get count of male v. female creators 
sns.set_theme(style="whitegrid")
article_df['creator gender'].value_counts().plot(kind='bar', color = ["tomato", "skyblue"])

def genderize(name): 
    return Genderize().get([name])[0]["gender"]
article_df['creator gender']= article_df.apply(lambda row : genderize(row["author_first_name"]),axis=1)
print(article_df['creator gender'])
print(article_df['creator'])

#maybe for this function we need to do something to make the naming unique 
def name_function(df_name, names):
    list_a = []
    for x in names:
        if x is None:
            list_a.append(0)
        else: 
            nltk_results = ne_chunk(pos_tag(word_tokenize(x)))
            list_b = []
            for nltk_result in nltk_results:
                if type(nltk_result) == Tree:
                    name = ''
                    for nltk_result_leaf in nltk_result.leaves(): 
                        name += nltk_result_leaf[0]
                        list_b.append([nltk_result.label(), name])
            list_a.append(list_b)
    return list_a
    #could add the list as a column inside the function
list_A = name_function(article_df, article_df["creator"])
article_df["name_classification"] = list_A
article_df[["name_classification", "creator"]]


        
    











#Just run on author name. If a name add a new 1/0 column
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

sample = "John was a nice guy and had a friend named Earl"
text = article_df["creator"][0]

nltk_results = ne_chunk(pos_tag(word_tokenize(text)))
for nltk_result in nltk_results:
    if type(nltk_result) == Tree:
        name = ''
        for nltk_result_leaf in nltk_result.leaves():
            name += nltk_result_leaf[0] + ' ' 
        print (name)
        
#above code comes from an online article. I'm thinking that I could use a pandas 
#df to figure out how to detect a name and mark the sentence Y or N or whatever. 

#YF add 
#import the Genderize package which we need to recognize names & pandas
#pip install genderize
from genderize import Genderize
import pandas as pd

#function to detect the gender 
def genderize(name): 
    return Genderize().get([name])[0]["gender"]

#dummy df with sample names 
names = ["Shirley Temple", "Clark Gables","ashley Smith", "Alex G", "Priantha G", "John G", "john G", "jon G", "Blake Shelton", "Blake Lively", "Georgle Jungle", "George Clooney", "Danielle Duncan", "Yolanda Ferreiro"]
df_names = pd.DataFrame(names, columns = ["names"])
df_names['names']
#! Bug 2
#extract first name from a df of first and last names & create column only with first names
df_names.loc[df_names["names"].str.split().str.len() == 2, "first name"] = df_names["names"].str.split().str[0]
df_names

# apply the genderize function to all of the rows in the df_names dataset with regards to the "first name" column
df_names["gender"]= df_names.apply(lambda row : genderize(row["first name"]),axis=1)
print(df_names)


#vectors

# Here is how the people=men people did it. THey just dled this https://fasttext.cc/docs/en/english-vectors.html
#Crazy shit right. I think I'll dl and upload to the github and see if i can access it 
#though the file. Trying to be clever. 
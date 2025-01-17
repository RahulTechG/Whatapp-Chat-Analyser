from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


def featch_messages(selected_user,df):
    
    if selected_user=='Overall':
        return df.shape[0]
    else:
        return df[df["user"]==selected_user].shape[0]

def featch_words(selected_user,df):
    
    if selected_user=='Overall':
        words=[]
        for message in df['message']:
            words.extend(message.split())
        return len(words)                
    else:
        new_df=df[df["user"]==selected_user]
        words=[]
        for message in new_df['message']:
            words.extend(message.split())
        return len(words)    

def featch_media(selected_user,df):
     
     if selected_user=='Overall':
        NumMedia=df[df['message']=='<Media omitted>\n'].shape[0]
        return NumMedia
     else:
        new_df=df[df["user"]==selected_user]
        NumMedia=new_df[new_df['message']=='<Media omitted>\n'].shape[0]
        return NumMedia

def featch_links(selected_user,df):

    extract=URLExtract()

    if selected_user=='Overall':
        links=[]
        for message in df['message']:
            links.extend(extract.find_urls(message))
        return len(links)
    else:
        links=[]
        new_df=df[df["user"]==selected_user]
        for message in new_df['message']:
            links.extend(extract.find_urls(message))
        return len(links)


def mostBussiestUser(df):

    filetered_user=df[df['user']!='group_notification']
    x=filetered_user['user'].value_counts().head()

    return x

def userPercent(df):

    filetered_user=df[df['user']!='group_notification']
    userAndPercent=round((filetered_user['user'].value_counts()/filetered_user.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return userAndPercent


def createWordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]


    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')

    Filtered_df = df[(df['message'] != '<Media omitted>\n') & (df['user'] != 'group_notification')]
    wc_df = wc.generate(Filtered_df['message'].str.cat(sep=" "))


    return wc_df


def most_common_words(selected_user,df):

   


    # with open('stop_words.txt', 'r') as f:
    #     stop_words = f.read()

    # Filter only letters (remove special characters)
     with open('stop_words.txt', 'r') as f:
        stop_words = ''.join(char for char in f.read() if char.isalpha() or char.isspace()).split()
        

     if selected_user!='Overall':
        df=df[df['user']==selected_user]

     temp=df[df['user']!='group_notification']   
     temp=temp[temp['message']!='<Media omitted>\n'] 

     words=[]

     for message in temp['message'].dropna():
        for word in message.lower().split():
            if word.isalpha() and word not in stop_words:
                words.append(word)



     most_common_df=pd.DataFrame(Counter(words).most_common(20))   
     most_common_df = most_common_df.rename(columns={0: 'word', 1: 'Frequency'})        
     return most_common_df


def emoji_helper(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    colored_emojis = [e + '\uFE0F' for e in emojis] 


    colored_emoji_df=pd.DataFrame(Counter(colored_emojis).most_common(len(Counter(colored_emojis))))    
    colored_emoji_df=colored_emoji_df.rename(columns={0:'Emoji',1:'Count'})

    return colored_emoji_df


def montly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()   

    time=[]

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline["year"][i]))

    timeline["time"]=time
    return timeline    


def daily_timeline(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    daily_timeline=df.groupby(['only_date']).count()['message'].reset_index() 
    return daily_timeline



def weekly_activity_map(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df["day_name"].value_counts()

def monthly_activity_map(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df["month"].value_counts()   

def activity_heatmap(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    user_heatmap=df.pivot_table(index='day_name',columns="period",values="message",aggfunc="count").fillna(0)    
    return user_heatmap

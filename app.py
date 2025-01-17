import streamlit as st
import preprocessor,helper
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")


# Inject CSS for background color
st.markdown(
    """
    <style>
    /* Change the overall app background color */
    .stApp {
        background-color: #FFDAB9; /* Light orange */
    }

    /* Customize the sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFA07A; /* Light salmon */
    }

    /* Customize the header (if present) */
    header {
        background-color: #FF6347; /* Tomato red */
    }

    /* Optional: Change sidebar text color */
    section[data-testid="stSidebar"] .css-1d391kg, section[data-testid="stSidebar"] .css-h5rgaw {
        color: white; /* Sidebar text to white */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# File uploader for both CSV and TXT files
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt", "csv"])

if uploaded_file is not None:
    # Read file based on the type
    file_type = uploaded_file.name.split('.')[-1]  # Get the file extension (txt or csv)

    if file_type == 'txt':
        # For TXT files, process using preprocessor
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
    
    elif file_type == 'csv':
        # For CSV files, load directly into a dataframe
        df = pd.read_csv(uploaded_file)

    # Fetch unique users
    user_list = df['user'].unique().tolist()

    # Check if 'group_notification' exists and remove it if found
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    
    user_list.sort()
    user_list.insert(0, "Overall")

    # Sidebar selection
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Show Analysis Button
    if st.sidebar.button("Show Analysis"):
        # Displaying the dataframe directly
        st.markdown('<h1 style="color:Green;">Processed Chat Data</h1>', unsafe_allow_html=True)
        st.dataframe(df)  # Display the dataframe


        col1,col2,col3,col4=st.columns(4)

        num_messages=helper.featch_messages(selected_user,df)
        num_words=helper.featch_words(selected_user,df)
        num_media=helper.featch_media(selected_user,df)
        num_links=helper.featch_links(selected_user,df)

        # Add styled content to the columns
        with col1:
            st.markdown("<h3 style='text-align: center;'>Total Messages</h3>", unsafe_allow_html=True)
            st.markdown(
            f"<h3 style='text-align: center; color: blue;'> {num_messages}</h3>",
            unsafe_allow_html=True
            )
        with col2:
            st.markdown("<h3 style='text-align: center;'>Total Words</h3>", unsafe_allow_html=True)
            st.markdown(
            f"<h3 style='text-align: center; color: blue;'> {num_words}</h3>",
            unsafe_allow_html=True
            )
        with col3:
            st.markdown("<h3 style='text-align: center;'>Total Media Files</h3>", unsafe_allow_html=True)
            st.markdown(
            f"<h3 style='text-align: center; color: blue;'> {num_media}</h3>",
            unsafe_allow_html=True
            )
        with col4:
            st.markdown("<h3 style='text-align: center;'>Total Links</h3>", unsafe_allow_html=True)
            st.markdown(
            f"<h3 style='text-align: center; color: blue;'> {num_links}</h3>",
            unsafe_allow_html=True
            )
        

        # Montly Timeline

        st.title("Montly Timeline")
        timeline=helper.montly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline["time"],timeline["message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        # Daily Timeline

        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline["only_date"],daily_timeline["message"],color="pink")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        # Activity map

        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Bussiest Day")

            busy_day=helper.weekly_activity_map(selected_user,df)

            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)


        with col2:

            st.header("Most Bussiest Month")
            busy_month=helper.monthly_activity_map(selected_user,df)

            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)


        # Ploting Heatmap

        st.title("weekly Activity Heatmap")
        user_heatmap=helper.activity_heatmap(selected_user,df)

        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)



        # Finding the most busiest users in the chat.


        
        if selected_user=='Overall':

            st.title("Most Busiest Users ")

            x=helper.mostBussiestUser(df)
            userAndPercent=helper.userPercent(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(userAndPercent)

        #WordCloud
    
        st.markdown('<h1 style="color:blue;">WordCloud</h1>', unsafe_allow_html=True)
        wc_df=helper.createWordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)
    
        # Most common Words
    
        most_common_df=helper.most_common_words(selected_user,df)
        # st.dataframe(most_common_df)
    
        st.title("Most common used words")
        fig,ax=plt.subplots()
        ax.barh(most_common_df['word'],most_common_df['Frequency'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #Most common emojis
    
        st.title("Emojis Analysis")
    
        col1,col2=st.columns(2)
        emoji_df=helper.emoji_helper(selected_user,df)
    
        with col1:
            
            st.dataframe(emoji_df) 
    
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df['Count'].head(),labels=emoji_df['Emoji'].head(),autopct="%0.2f")
            st.pyplot(fig)    

else:
    st.warning("Please upload a WhatsApp chat file (TXT or CSV).")

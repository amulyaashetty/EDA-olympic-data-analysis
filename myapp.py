import streamlit as st
import pandas as pd
import numpy as np
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("EDA Olympics")
st.subheader("Data Analysis Using Python and Streamlit")
st.sidebar.image('https://penaltyfile.com/wp-content/uploads/2020/06/different-types-of-sports-June32020-1-min.jpg')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Data Analysis','Country-wise Analysis','Data Analysis')
)

st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " +  str(selected_year))
    if selected_year =='Overall' and selected_country != 'Overall':
        st.title(selected_country +  " overall performance")
    if selected_year !='Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " +  str(selected_year) + " Olympics")

    st.table(medal_tally)

if user_menu == 'Overall Data Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition",y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition",y="Event")
    st.title("Event over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Data Analysis':
    st.sidebar.header("Data Analysis")
    def file_selector(folder_path='.'):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox("Select a file",filenames)
        return os.path.join(folder_path,selected_filename)

    filename = file_selector()
    st.info("You selected {}".format(filename))

    df = pd.read_csv(filename)


    if st.checkbox("Show Dataset"):
        
        if st.button("Column names"):
            st.write(df.columns)
        if st.checkbox("shape of dataset"):
            data_dim = st.radio("show dimensions by",("Rows","Columns"))
            if data_dim == 'Row':
                st.text("number of Rows")
                st.write(df.shape[0])
            elif data_dim == 'Columns':
                st.text("Number of Columns")
                st.write(df.shape[1])
            else:
                st.write(df.shape)

        if st.checkbox("Select Columns to show"):
            all_columns = df.columns.tolist()
            selected_columns = st.multiselect("Select",all_columns)
            new_df = df[selected_columns]
            st.dataframe(new_df)


        if st.button("Value Counts"):
            st.text("Value of Target/Class")
            st.write(df.iloc[:,1].value_counts())

        if st.button("Data types"):
            
            st.write(df.dtypes)

        if st.checkbox("Summary"):
            st.write(df.describe().T)

            
        st.set_option('deprecation.showPyplotGlobalUse', False)

        st.subheader("Data visualization")
        if st.checkbox("Correlation Plot[Seaborn]"):
		       st.write(sns.heatmap(df.corr(),annot=True))
		       st.pyplot()

        if st.checkbox("Pie Plot"):
		       all_columns_names = df.columns.tolist()
		       if st.button("Generate Pie Plot"):
			        st.success("Generating A Pie Plot")
			        st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
			        st.pyplot()

        
            
            
    

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



st.set_page_config(layout='wide', page_title='Start-Up Analysis')



df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


def load_overall_analysis():
    st.title('Overall Analysis')

#     total invested amount
    total = round(df['amount'].sum())

#     max funding
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    # avg
    avg = round(df.groupby('startup')['amount'].sum().mean(),2)

    # total funded startup

    num_startup = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')
    with col3:
        st.metric('Average', str(avg) + ' Cr')
    with col4:
        st.metric('Total funded startup', str(num_startup) )

    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type' ,['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'],temp_df['amount'] )
    st.pyplot(fig5)

def load_investor_detail(investor):
    st.title(investor)
    # load the recent 5 investment of the investor
    last5_df = df[df['investor'].str.contains(investor)].head()[['date','startup','vertical','city', 'investor', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1, col2, = st.columns(2)

    with col1:

        #biggest investment
        big_series = df[df['investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending= False).head()
        st.subheader('Biggest Investment')
        fig,ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investor'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector invested in ')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels = vertical_series.index, autopct = '%0.01f%%')
        st.pyplot(fig1)

    col1, col2, = st.columns(2)
    with col1:
        vertical_series = df[df['investor'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Investment type ')
        fig2, ax2 = plt.subplots()
        ax2.pie(vertical_series, labels=vertical_series.index, autopct='%0.01f%%')
        st.pyplot(fig2)

    with col2:
        vertical_series = df[df['investor'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Invested city ')
        fig3, ax3 = plt.subplots()
        ax3.pie(vertical_series, labels=vertical_series.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    df['year'] = df['date'].dt.year
    year_series = df[df['investor'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig4, ax4 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)


    st.pyplot(fig4)


st.sidebar.title('Start-up Funding Analysis')

option =  st.sidebar.selectbox('Select one', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    # btn0 = st.sidebar.button('Show overall analysis')
    # if btn0:
    #     load_overall_analysis()
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('select one', sorted(df['startup'].unique().tolist()))
    st.title('Startup Analysis')
    st.sidebar.button('Find startup detail')
else:
    selected_investor = st.sidebar.selectbox('Select Startup', sorted(set(df['investor'].str.split(',').sum())))

    btn2 = st.sidebar.button('Find investor detail')
    if btn2:
        load_investor_detail(selected_investor)

    # st.title('Investor Analysis')
import pandas as pd
import streamlit as st
from importer import Importer
import altair as alt
from datetime import datetime


def format_string(stri):
    
    stri = str(stri)
    stri = stri.replace('[', '')
    stri = stri.replace(']', '')
    stri = stri.replace("'", '')
    return stri.split(', ')

 
def interpret_data(data):
    
    skills_found = {}
    
    for row in data['skills_found']:
        formatted_lst = format_string(row)
        for entry in formatted_lst:
            skills_found[entry] = 1 if entry not in skills_found else skills_found[entry] + 1
            
    skills_found = sorted(skills_found.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(skills_found, columns=["Skill", "Freq"])
    
    for idx in df.index:
        df.at[idx, 'Freq'] = int(df['Freq'][idx]) / len(data)
    idx_remove = df.index[df['Skill'] == '']
    df.drop(idx_remove, axis=0, inplace=True)
    return df


def skills_daily(data):
    """
    Returns a Dataframe with all info within the last 24 hours

    Args:
        data (_type_): _description_
    """
    
    for idx in data.index:
        data['datetime_posted'][idx] = datetime.strptime(str(data['datetime_posted'][idx]), '%Y-%m-%d %H:%M:%S.%f')
    
    idxs_daily = []
    curr_time = datetime.now()
    
    for idx in data.index:
        if (curr_time - data['datetime_posted'][idx]).days == 0:
            idxs_daily.append(idx)
            
    return data.filter(items = idxs_daily, axis=0)
            
            
def dataset_page():
    
    st.markdown("## Dataset for Data Analysis :bar_chart:")
    
    st.dataframe(pd.read_csv('jobs_df.csv', index_col=0))
        
    
def data_viz_page():

    # retrieve the data 
    data = Importer()
    data = data.import_data(st.secrets["api_key"], st.secrets["aws_access_key_id"], st.secrets["aws_secret_access_key"], st.secrets['bucket_name'])

    #st.dataframe(pd.read_csv('jobs_df.csv', index_col=0))
    #print(jobs_all['skills_found'].tolist()[2][0])

    # body text
    st.markdown("## 🛠️ What are the Top Data Analyst Skills?")

    # column filters
    col1, col2, col3, col4 = st.columns(4)
    with col4:
        graph_list = ["All Time", "Past 24 Hours"]
        graph_choice = st.radio('Time:', graph_list, horizontal=False)

    skill_dict = {"Top 5:": 5, "Top 10": 10}

    # sidebar filters
    with st.sidebar:
        st.markdown("🛠️ Filters ")
        choice = st.radio("Data Skills: ", list(skill_dict.keys()))

    skills = interpret_data(data)
    skill_num = skill_dict[choice]

    skill_all_time = skills.head(skill_num)
    skill_all_time_list = list(skill_all_time['Skill'])


    # all time chart
    selector = alt.selection_single(encodings=['x', 'y'])
    all_time_chart = alt.Chart(skill_all_time).mark_bar(
        cornerRadiusTopLeft=10,
        cornerRadiusTopRight=10    
    ).encode(
        x=alt.X('Skill', sort=None, title="", axis=alt.Axis(labelFontSize=20) ),
        y=alt.Y('Freq', title="Likelyhood in Job Posting All Time", axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)),
        color=alt.condition(selector, 'Freq', alt.value('lightgray'), legend=None),
        tooltip=["Freq", alt.Tooltip("Freq", format=".1%")]
    ).add_selection(
        selector
    ).configure_view(
        strokeWidth=0
    )


    daily_skills = skills_daily(data)
    daily_skills = interpret_data(daily_skills)

    skill_daily = daily_skills.head(skill_num)

    # daily chart
    selector = alt.selection_single(encodings=['x', 'y'])
    daily_chart = alt.Chart(skill_daily).mark_bar(
        cornerRadiusTopLeft=10,
        cornerRadiusTopRight=10    
    ).encode(
        x=alt.X('Skill', sort=None, title="", axis=alt.Axis(labelFontSize=20) ),
        y=alt.Y('Freq', title="Likelyhood in Job Posting Today", axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)),
        color=alt.condition(selector, 'Freq', alt.value('lightgray'), legend=None),
        tooltip=["Freq", alt.Tooltip("Freq", format=".1%")]
    ).add_selection(
        selector
    ).configure_view(
        strokeWidth=0
    )

    # print charts
    if graph_choice == graph_list[0]:
        st.altair_chart(all_time_chart, use_container_width=True)
    else:
        st.altair_chart(daily_chart, use_container_width=True)\
            
            
def info():
    
    st.markdown('# About this Application :1234:' + '\n')

    st.markdown('\nThis application attempts to diminish the struggles that aspiring data analysts experience when \
                landing a job. This has supplemented my journey to potentially land a job in the future in a field \
                I am passionate in through data cleaning, exploratory data analysis and data visualisation. I hope \
                this application has utility to all users.\n\n\n')
    
    st.markdown('# Tools Used :wrench:' + '\n')
    
    st.markdown('Data Source:   ' + 'Serp Api')
    st.markdown('Data Storage:   ' + 'AWS S3')
    

        
# set up the page layout
st.set_page_config(page_title="Data Analyst Top Skills",
                    page_icon=":bar_chart:")

    
page_names = {
    "Data Visualisation Page": data_viz_page,
    "Dataset Page": dataset_page,
    "About the Application": info
}

selected_page = st.sidebar.selectbox("Select a Page: ", page_names.keys())
page_names[selected_page]()
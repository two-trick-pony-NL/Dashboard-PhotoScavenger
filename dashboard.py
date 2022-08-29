import pandas as pd
import requests
import streamlit as st



# sending get request and saving the response as response object
r = requests.get(url = 'https://photoscavenger.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/get_long_term_data/')
  
data = r.json()

d = pd.json_normalize(data, record_path=['LongtermData'])
TotalV1Uploaded = d['uploadfileV1'].sum()
TotalV2Uploaded = d['uploadfileV2'].sum()
TotalUploaded = TotalV1Uploaded + TotalV2Uploaded

TotalV1Assignment = d['NewAssignmentV1'].sum()
TotalV2Assignment = d['NewAssignmentV2'].sum()
TotalAssignment = TotalV1Assignment + TotalV2Assignment

last_value = d['timestamp'].iat[-1]


st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Photo Scavenger API Dashboard")
st.image('https://user-images.githubusercontent.com/71013416/183674037-eca7cc9b-4a19-494c-a449-af638fdd869c.png')

# create three columns
kpi1, kpi2, kpi3 = st.columns(3)

# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="Total pictures analysed 🧐",
    value=round(TotalUploaded),
)

kpi2.metric(
    label="Total Assignments served 🎲",
    value=int(TotalAssignment),
)

kpi3.metric(
    label="Last time updated ⏱",
    value=last_value,
)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(d)
st.subheader('Summary and usage')
st.markdown('Photo Scavenger is a object detection game available as [iOS App](https://two-trick-pony-nl.github.io/PhotoScavenger/), where you earn points by taking photos of objects around your house. The Photo Scavenger API has a handfull of endpoints that can be used to detect objects in pictures. Check out [GitHub](https://github.com/two-trick-pony-NL/PhotoScavengerBackend) on how to use the API. Or check out the [Swagger](https://photoscavenger.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/docs) documentation')




st.subheader('Calls over time Combined')
st.bar_chart(d, x='timestamp', y=None)




# create two columns for charts
fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    st.markdown("# App Usage")
    st.subheader('Assignments served')
    st.bar_chart(d, x='timestamp', y=['NewAssignmentV1', 'NewAssignmentV2'])
    st.subheader('Photos analysed')
    st.bar_chart(d, x='timestamp', y=['uploadfileV2', 'uploadfileV1'])

with fig_col2:
    st.markdown("# Server")
    st.subheader('Homepage')
    st.bar_chart(d, x='timestamp', y=['Homepage', 'ExampleResponse'])
    st.subheader('Healthchecks by AWS')
    st.bar_chart(d, x='timestamp', y='Healthcheck by AWS')


st.markdown('Photo Scavenger is made with <3 by Peter van Doorn')

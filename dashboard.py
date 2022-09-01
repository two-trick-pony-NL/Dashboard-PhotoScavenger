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

TotalCorrectDetection = d['Detected'].sum()
TotalIncorrectDetection = d['NotDetected'].sum()
PercentageCorrectDetections = round(((TotalCorrectDetection/(TotalCorrectDetection+TotalIncorrectDetection)*100)))


TotalV1Assignment = d['NewAssignmentV1'].sum()
TotalV2Assignment = d['NewAssignmentV2'].sum()
TotalAssignment = TotalV1Assignment + TotalV2Assignment


last_updated = d['timestamp'].iat[-1]
last_deployments = d['timestamp'].iat[1]
most_recent_V2_photo_Calls = d['uploadfileV2'].iat[-0]
most_recent_V1_photo_Calls = d['uploadfileV1'].iat[-0]
most_recent_V2_Assignment_Calls = d['NewAssignmentV2'].iat[-0]
most_recent_V1_Assignment_Calls = d['NewAssignmentV1'].iat[-0]
most_recent_Detection = d['Detected'].iat[-0]
most_recent_NotDetected = d['NotDetected'].iat[-0]

deltaAccuracy = round((most_recent_NotDetected / most_recent_Detection) *100)
deltaUpload = int(most_recent_V1_photo_Calls + most_recent_V2_photo_Calls )
deltaAssignment = int(most_recent_V2_Assignment_Calls + most_recent_V1_Assignment_Calls )




st.set_page_config(
    page_title="Photo Scavenger Dashboard",
    page_icon="📊",
    layout="wide",
)

st.image('https://user-images.githubusercontent.com/71013416/183674037-eca7cc9b-4a19-494c-a449-af638fdd869c.png', width=100)
st.title("Photo Scavenger API Dashboard")
st.text('📥 Last Deployment: ' + last_deployments +" (UTC)")


# create three columns
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="🧐 Total pictures analysed",
    value=round(TotalUploaded),
    delta=deltaUpload,
)

kpi2.metric(
    label="🎲 Total Assignments served ",
    value=int(TotalAssignment),
    delta=deltaAssignment,
)

kpi3.metric(
    label="⚖️ Detections Accuracy ",
    value=str(PercentageCorrectDetections) +"%",
    delta=str(deltaAccuracy) +"%",
)

kpi4.metric(
    label="✅ Last time updated (UTC)",
    value=last_updated,
)


st.subheader('Summary and usage')
st.markdown('Photo Scavenger is a object detection game available as [iOS App](https://two-trick-pony-nl.github.io/PhotoScavenger/), where you earn points by taking photos of objects around your house. The Photo Scavenger API has a handfull of endpoints that can be used to detect objects in pictures. Check out [GitHub](https://github.com/two-trick-pony-NL/PhotoScavengerBackend) on how to use the API. Or check out the [Swagger](https://photoscavenger.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/docs) documentation')
st.markdown('You can upload pictures to the V1 or V2 upload enpoints, and an AI will detect what objects are in them. Currently the API is working with YoloV5 in the V2 version of the API. This can return 80 objects ')
if st.checkbox('Show Example response and objects'):
    st.subheader("Available objects")
    st.text("These objects can be detected by the YoloV5 model")
    st.text("person bicycle car motorcycle airplane bus train truck boat traffic light fire hydrant stop sign parking meter bench bird cat dog horse sheep cow elephant bear zebra giraffe backpack umbrella handbag tie suitcase frisbee skis snowboard sports ball kite baseball bat baseball glove skateboard surfboard tennis racket bottle wine glass cup fork knife spoon bowl banana apple sandwich orange broccoli carrot hot dog pizza donut cake chair couch potted plant bed dining table toilet tv laptop mouse remote keyboard cell phone microwave oven toaster sink refrigerator book clock vase scissors teddy bear hair drier toothbrush")
    st.subheader("Here are 2 example API calls and responses")
    st.text("1. Call  /v2/newassignment/200	to get a new object to find")
    st.code("""{"apple":"🍎"} \n""")
    st.text("* Make sure to add a integer as a score, as assignments get harder with higher scores")
    st.text("2. Call /v2/uploadfile/boat to detect a boat in the picture. It will return:")
    st.code("""
        {
        "Searchedfor:":"boat",\n
        "Wasfound":"NO",\n
        "OtherObjectsDetected":["person","person","person","person","bicycle","motorbike","bicycle","motorbike","bicycle"],\n
        "Processed_FileName":"scanned_image54e46fb8-93f8-43ad-a8ec-99eb83f260af.jpg",\n
        "file_url":"image54e46fb8-93f8-43ad-a8ec-99eb83f260af.jpg",\n
        }""")





st.subheader('Calls over time Combined')
st.bar_chart(d, x='timestamp', y=None)




# create two columns for charts
fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    st.markdown("# App Usage")
    st.subheader('Assignments served')
    st.text("New assignments over time")
    st.bar_chart(d, x='timestamp', y=['NewAssignmentV1', 'NewAssignmentV2'])
    st.subheader('Photos analysed')
    st.text("Photos uploaded over time")
    st.bar_chart(d, x='timestamp', y=['uploadfileV2', 'uploadfileV1'])
    st.subheader('Detection Accuracy')
    st.text("The ratio where the object was detected vs not detected")
    st.bar_chart(d, x='timestamp', y=['Detected', 'NotDetected'])
    

with fig_col2:
    st.markdown("# Server")
    st.subheader('Homepage')
    st.text("Calls to homepage over time")
    st.bar_chart(d, x='timestamp', y=['Homepage', 'ExampleResponse'])
    st.subheader('Healthchecks by AWS')
    st.text("Calls to check if server is still up by AWS")
    st.bar_chart(d, x='timestamp', y='Healthcheck by AWS')


st.markdown('Photo Scavenger is made with <3 by Peter van Doorn')
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(d)

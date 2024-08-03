import streamlit as st
import pandas as pd
import plotly.express as px



def display_text_box_title_only(title):
    st.markdown(
        f"""
        <div style="border: 1px solid #cccccc; border-radius: 5px; overflow: hidden;">
            <div style="background-color: #f0f0f0; padding: 10px;">
                <p style="margin: 0; color: black; font-weight: bold; font-size: 1.0em; padding: 0;">{title}</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

def display_text_box(title, content):
    st.markdown(
        f"""
        <div style="border: 1px solid #cccccc; border-radius: 5px; overflow: hidden;">
            <div style="background-color: #f0f0f0; padding: 10px;">
                <p style="margin: 0; color: black; font-weight: bold; font-size: 1.0em; padding: 0;">{title}</p>
            </div>
            <div style="padding: 10px; background-color: white;">
                <p>{content}</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )


st.write('')
title1 = "Welcome to our Obesity Dashboard"
content1 = """
This dashboard is designed to help users explore and analyze the factors that influence obesity levels. By visualizing correlations and trends, 
users can gain insights into the impact of various lifestyle and demographic factors on obesity.</p>
Obesity is a complex disease involving an excessive amount of body fat. It's a medical problem that increases the risk of other diseases and health problems, 
such as heart disease, diabetes, high blood pressure, and certain cancers.</p>
"""

title2 = "Prevalence of Obesity"
content2 = """   
"""

title3 = "Dataset Overview"
content3 = """
"""
st.header('Obesity Data Visualization and Prediction')
display_text_box(title1, content1)
st.write('')

display_text_box_title_only(title2)
st.write('According to a study done by WHO in 2022, 1 in 8 people in the world were living with obesity.')
st.image('1in8.jpg', use_column_width=True)
st.write('')

st.markdown(
    f"""
    <span style="font-size:1.0em; font-weight:bold;">Global Trends in Overweight Adults</span><br>
    The graphic vector map below illustrates the share of adults who are overweight (age-standardized) across different countries for the year 2016. This data is visualized to highlight the global distribution of overweight adults.</p>
    <ul style="list-style-type: disc; padding-left: 20px;">
        <li style="font-size:1.0em;">Hover over a country: To view the specific share of overweight adults in that country for the year 2016.
</li>
    </ul>
    """, 
    unsafe_allow_html=True
)


# Load the dataset
df = pd.read_csv('WHO_Data.csv')

# Filter data for the year 2016
df_2016 = df[df['Year'] == 2016]

# Create a dictionary for the full dataset by country
data_by_country = df.groupby('Entity')

# Create the choropleth map
fig = px.choropleth(
    df_2016,
    locations="Entity",
    locationmode="country names",
    color="Share of adults who are overweight (age-standardized) - Sex: both sexes - Age group: 18+  years",
    hover_name="Entity",
    hover_data={"Entity": False, "Year": False},
    color_continuous_scale="Viridis",
    labels={'Share of adults who are overweight (age-standardized) - Sex: both sexes - Age group: 18+  years': 'Share of Overweight Adults (%)'}
)

# Add a callback for when a country is clicked
def country_hovered(trace, points, state):
    if points.point_inds:
        country = trace.hovertext[points.point_inds[0]]
        st.session_state["selected_country"] = country

fig.data[0].on_click(country_hovered)

st.plotly_chart(fig)



st.write('')


display_text_box_title_only(title3)
dataset_url = "https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition"
link_display_text = "[Access Dataset Here]"

st.markdown(
    f"""
    <span style="font-size:1.0em; font-weight:bold;">Source and Purpose</span><br>
    Our obesity dataset was obtained from the UCI Machine Learning repository.</p>
    This dataset contains information from various locations, including Mexico, Peru, and Colombia. Its intended use includes building estimations of obesity levels based on the nutritional behavior observed in these regions.</p>
    The dataset can be accessed here: <a href="{dataset_url}" target="_blank">{link_display_text}</a>.
    """, 
    unsafe_allow_html=True
)
st.write('')


st.markdown(f"""
<span style="font-size:1.0em; font-weight:bold;">Data Description</span></p>
<ul style="list-style-type: disc; padding-left: 20px;">
    <li>The data contains 2111 records with 17 columns</li>
    <li>All of the records are unique and contain no null values</li>
    <li>Height and Weight are included; however, they have a direct correlation to each other and our target variable</li>
</ul>
<ul style="list-style-type: disc; padding-left: 20px;">
    <li style="font-size:1.0em; font-weight:bold;">Variable Table</li>
</ul>
""", unsafe_allow_html=True)

# Define the data
data = [
    ('Gender', 'A person\'s gender (Male or Female)'),
    ('Age', 'A person\'s age'),
    ('Height', 'A person\'s height (m)'),
    ('Weight', 'A person\'s weight (kg)'),
    ('family_history_with_overweight', 'Has a family member suffered or suffers from overweight?'),
    ('FAVC', 'Do you eat high caloric food frequently?'),
    ('FCVC', 'Do you usually eat vegetables in your meals?'),
    ('NCP', 'How many main meals do you have daily?'),
    ('CAEC', 'Do you eat any food between meals?'),
    ('SMOKE', 'Do you smoke?'),
    ('CH2O', 'How much water do you drink daily?'),
    ('SCC', 'Do you monitor the calories you eat daily?'),
    ('FAF', 'How often do you have physical activity?'),
    ('TUE', 'How much time do you use technological devices such as cell phone, videogames, television, computer and others?'),
    ('CALC', 'How often do you drink alcohol?'),
    ('MTRANS_Automobile', 'Do you usually commute via Automobile?'),
    ('MTRANS_Bike', 'Do you usually commute via bike?'),
    ('MTRANS_Motorbike', 'Do you usually commute via motorbike?'),
    ('MTRANS_Public_Transportation', 'Do you usually commute via public transportation?'),
    ('MTRANS_Walking', 'Do you usually commute via walking?'),
    ('NObeyesdad', 'Obesity level')
]

# Create a Pandas DataFrame
df = pd.DataFrame(data, columns=['Feature Name', 'Description'])

# Custom CSS styles for the table
table_style = """
<style>
    .dataframe-container {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #cccccc;
        border-radius: 5px;
        position: relative;
    }
    .dataframe table {
        width: 100%;
        border-collapse: collapse;
        position: relative;
    }
    .dataframe th, .dataframe td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #cccccc;
    }
    .dataframe thead th {
        background-color: #f0f0f0;
        font-weight: bold;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    .dataframe tbody tr:nth-child(even) {
        background-color: #f9f9f9;
    }
</style>
"""

# Display the custom CSS styles
st.markdown(table_style, unsafe_allow_html=True)

# Convert DataFrame to HTML table with custom styles
html_table = df.to_html(classes='dataframe', index=False, escape=False)

# Display the table inside a scrollable div
st.markdown(
    f"""
    <div class="dataframe-container">
        {html_table}
    </div>
    """,
    unsafe_allow_html=True
)
st.write('')
st.write('')

st.markdown("""
<ul style="list-style-type: disc; padding-left: 20px;">
    <li style="font-size: 1.0em; font-weight: bold;">Target Variable</li>
</ul>
The target variable in this dataset is 'obesity level'. Obesity levels are categorized based on Body Mass Index (BMI), which is a measure of body fat based on height and weight. The higher the BMI, the greater the classification of obesity. The dataset categorizes obesity levels into six categories:
""", unsafe_allow_html=True)

# Define the data including the new column 'Description'
data = [
    ('Underweight', 'Less than 18.5', 'Individuals in this category have a BMI less than 18.5, indicating lower than normal body weight for their height.'),
    ('Normal', '18.5 to 24.9', 'Individuals in this category have a healthy body weight relative to their height.'),
    ('Overweight Level I', '25.0 to 27.4', 'Individuals in this category have excess body weight compared to what is considered healthy.'),
    ('Overweight Level II','27.5 to 29.9', 'Individuals in this category have higher excess body weight compared to what is considered healthy.'),
    ('Obesity I', '30.0 to 34.9', 'Individuals in this category are classified as having moderate obesity.'),
    ('Obesity II', '35.0 to 39.9', 'Individuals in this category are classified as having severe obesity.'),
    ('Obesity III', 'Higher than 40', 'Individuals in this category are classified as having extreme obesity.')
]

# Create a Pandas DataFrame
df_obesity_levels = pd.DataFrame(data, columns=['Obesity Level', 'BMI Range', 'Description'])

# Custom CSS styles for the table
table_style = """
<style>
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    .dataframe th, .dataframe td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #cccccc;
    }
    .dataframe th {
        background-color: #f0f0f0;
        font-weight: bold;
    }
    .dataframe tbody tr:nth-child(even) {
        background-color: #f9f9f9;
    }
</style>
"""

# Display the custom CSS styles
st.markdown(table_style, unsafe_allow_html=True)

# Convert DataFrame to HTML table with custom styles
html_table = df_obesity_levels.to_html(classes='dataframe', index=False, escape=False)

# Display the table
st.markdown(html_table, unsafe_allow_html=True)
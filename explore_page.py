import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

def reduce_categories(categories,threshold_value):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i]>=threshold_value:
            categorical_map[categories.index[i]]=categories.index[i]
        else:
            categorical_map[categories.index[i]]="other"
    return categorical_map
            
def fit_experience(x):
    if x == "More than 50 years" :
        return 50
    if x == "Less than 1 year" :
        return 0.5
    return float(x)

def fit_education(x):
    if "Bachelor’s degree" in x :
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "other doctrial" in x:
        return "Post grad"
    return "Less than a Bachelors"


def fit_roles(x):
    if "Developer, back-end" in x:
        return "BackEnd-Developer"
    if "Developer, front-end" in x:
        return "FrontEnd-Developer"
    if "Developer, full-stack" in x:
        return "FullStack-Developer"
    if "Data scientist or machine learning specialist" in x:
        return "Data-scientist"
    if "Developer, QA or test" in x:
        return "Tester"
    if "Data or business analyst" in x:
        return "Data-Analyst"
    if "DevOps specialist" in x:
        return "DevOps Engineer"
    if "Engineer, data" in x:
        return "Data-Engineer"
    if "Cloud infrastructure engineer" in x:
        return "Cloud-Developer"
    return "Software-Developer"


@st.cache_resource
def load_data():
    df=pd.read_csv("Survey_results_public.csv")
    df=df[["Country","EdLevel","YearsCodePro","DevType","Employment","ConvertedCompYearly"]]
    df=df.rename({"ConvertedCompYearly":"Salary"},axis=1)
    df=df[df["Salary"].notnull()]
    df=df.dropna()
    df=df[df["Employment"] == "Employed, full-time"]
    df=df.drop("Employment",axis=1)
    country_map=reduce_categories(df.Country.value_counts(),200)
    df["Country"]=df["Country"].map(country_map)
    df=df[df["Salary"] <= 250000]
    df=df[df["Salary"] >= 10000]
    df=df[df["Country"] != "other"]
    df["YearsCodePro"] = df["YearsCodePro"].apply(fit_experience)
    df["EdLevel"]=df["EdLevel"].apply(fit_education)
    df["DevType"]=df["DevType"].apply(fit_roles)
    return df

lable=load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    data = lable["Country"].value_counts().reset_index(name='Count')

    # Rename the column to 'index'
    data = data.rename(columns={'Country': 'index'})

    # Calculate percentage
    data['Percentage'] = data['Count'] / data['Count'].sum() * 100

    # Create sunburst chart
    fig = px.sunburst(data, path=['index'], values='Count', title='Number of Data from Different Countries',
                    hover_data=['Count', 'Percentage'],
                    custom_data=['Count', 'Percentage'])

    # Update layout for better size
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=40),
        height=600,
    )

    # Format hover information to include percentage
    fig.update_traces(hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}<br>Percentage: %{customdata[1]:.2f}%')

    # Show the chart using Streamlit
    st.plotly_chart(fig)
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )
        # Assuming 'lable' is your DataFrame
    data = lable.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)

    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot a bar chart on the primary axis
    ax1.bar(data.index, data, color='skyblue', label='Average Salary')

    # Set labels for the primary axis
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Average Salary', color='skyblue')
    ax1.tick_params('y', colors='skyblue')
    plt.xticks(rotation=45, ha='right')

    # Create a secondary axis
    ax2 = ax1.twinx()

    # Plot a line chart on the secondary axis
    ax2.plot(data.index, data, color='orange', marker='o', label='Average Salary (Line)')

    # Set labels for the secondary axis
    ax2.set_ylabel('Average Salary (Line)', color='orange')
    ax2.tick_params('y', colors='orange')

    # Set title
    plt.title('Average Salary Across Countries with Histogram and Line Chart')

    # Show the plot
    st.pyplot(fig)
    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = lable.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
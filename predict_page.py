import streamlit as st
import pickle
import numpy as np



def load_model():
    with open("saved_steps.pkl","rb") as file:
       data=pickle.load(file)
    return data
data=load_model()

regressor=data["model"]
le_country=data["le_country"]
le_education=data["le_education"]
le_devtype=data["le_devtype"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")
    
    
    countries = (
        "United States of America",
        "India",
        "United Kingdom of Great Britain and Northern Ireland",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )
    
    devtype = (
        'BackEnd-Developer', 
        'FrontEnd-Developer', 
        'FullStack-Developer',
       'Software-Developer', 
       'Tester', 
       'Data-scientist', 
       'Data-Analyst',
       'Data-Engineer', 
       'Cloud-Developer', 
       'DevOps Engineer',
    )
    
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    devtype = st.selectbox("Development Role", devtype)
    

    expericence = st.slider("Years of Experience", 0, 50, 2)
    
    ok = st.button("Calculate Salary")
    if ok:
        x = np.array([[country, education, expericence ,devtype]])
        x[:, 0] = le_country.transform(x[:,0])
        x[:, 1] = le_education.transform(x[:,1])
        x[:,3]=le_devtype.transform(x[:,3])
        X = x.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary in Dollars  ${int(round(salary[0],2))}")
        usd = salary
        inr = usd * 80
        st.subheader(f"The estimated salary in Rupees   {int(round(inr[0],2))}")
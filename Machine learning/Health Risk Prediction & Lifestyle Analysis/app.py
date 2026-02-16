import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings('ignore')

def load_data(heart):
    try:
        df = pd.read_csv(f'{heart}.csv')
        st.success(f"'{heart}.csv' loaded successfully.")
    except FileNotFoundError:
        st.error(f"Error: '{heart}.csv' not found. Please upload the file.")
        st.stop()
    return df

@st.cache_data
def train_model(df, model_algorithm_choice, target_col, features):
    X = df[features]
    y = df[target_col]
    
   
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)
    
   
    if model_algorithm_choice == 'Logistic Regression':
        model = LogisticRegression(solver='liblinear')
    elif model_algorithm_choice == 'Support Vector Machine (SVM)':
        model = SVC(kernel='linear', probability=True, random_state=42)
    else:
        st.error('Invalid model choice.')
        return None, None
        
    model.fit(scaled_X, y)
    
    return model, scaler

st.set_page_config(page_title="Heart Health Risk Predictor", layout="wide")

st.title("Heart Health Risk Prediction & Analysis")
st.markdown("### Predict your health risk based on your metrics and compare with the dataset.")


st.sidebar.header("Model and Dataset Selection")
model_algorithm_choice = st.sidebar.selectbox("Choose a Model Algorithm:", ["Logistic Regression", "Support Vector Machine (SVM)"])
model_choice = st.sidebar.selectbox("Choose a Health Risk Model:", ["Heart Disease", "Diabetes"])

if model_choice == "Heart Disease":
    df = load_data('heart')
    target = 'target'
    features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    
    st.sidebar.header("Heart Disease Predictor")
    with st.sidebar.expander("Enter your metrics", expanded=True):
        age = st.slider("Age", int(df['age'].min()), int(df['age'].max()), 20)
        sex = st.radio("Sex", ("Male", "Female"))
        cp = st.selectbox("Chest Pain Type (cp)", df['cp'].unique())
        trestbps = st.slider("Resting Blood Pressure (mm Hg)", int(df['trestbps'].min()), int(df['trestbps'].max()), 120)
        chol = st.slider("Cholesterol (mg/dl)", int(df['chol'].min()), int(df['chol'].max()), 200)
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl (fbs)", [0, 1])
        restecg = st.selectbox("Resting Electrocardiographic Results (restecg)", df['restecg'].unique())
        thalach = st.slider("Max Heart Rate Achieved (thalach)", int(df['thalach'].min()), int(df['thalach'].max()), 150)
        exang = st.selectbox("Exercise Induced Angina (exang)", [0, 1])
        oldpeak = st.slider("ST depression induced by exercise (oldpeak)", float(df['oldpeak'].min()), float(df['oldpeak'].max()), 1.0)
        slope = st.selectbox("The slope of the peak exercise ST segment (slope)", df['slope'].unique())
        ca = st.selectbox("Number of major vessels (ca)", df['ca'].unique())
        thal = st.selectbox("Thalassemia (thal)", df['thal'].unique())
    
    user_data = pd.DataFrame({
        'age': [age], 'sex': [1 if sex == 'Male' else 0], 'cp': [cp], 'trestbps': [trestbps],
        'chol': [chol], 'fbs': [fbs], 'restecg': [restecg], 'thalach': [thalach],
        'exang': [exang], 'oldpeak': [oldpeak], 'slope': [slope], 'ca': [ca], 'thal': [thal]
    })
    
else: 
    df = load_data('diabetes')
    target = 'Outcome'
    features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    for col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
        df[col] = df[col].replace(0, np.nan).fillna(df[col].median())
    
    st.sidebar.header("Diabetes Predictor")
    with st.sidebar.expander("Enter your metrics", expanded=True):
        pregnancies = st.slider("Pregnancies", 0, 15, 1)
        glucose = st.slider("Glucose", int(df['Glucose'].min()), int(df['Glucose'].max()), 120)
        blood_pressure = st.slider("Blood Pressure", int(df['BloodPressure'].min()), int(df['BloodPressure'].max()), 70)
        skin_thickness = st.slider("Skin Thickness", int(df['SkinThickness'].min()), int(df['SkinThickness'].max()), 30)
        insulin = st.slider("Insulin", int(df['Insulin'].min()), int(df['Insulin'].max()), 100)
        bmi = st.slider("BMI", float(df['BMI'].min()), float(df['BMI'].max()), 30.0)
        dpf = st.slider("Diabetes Pedigree Function", float(df['DiabetesPedigreeFunction'].min()), float(df['DiabetesPedigreeFunction'].max()), 0.5)
        age = st.slider("Age", int(df['Age'].min()), int(df['Age'].max()), 30)

    user_data = pd.DataFrame({
        'Pregnancies': [pregnancies], 'Glucose': [glucose],
        'BloodPressure': [blood_pressure], 'SkinThickness': [skin_thickness],
        'Insulin': [insulin], 'BMI': [bmi],
        'DiabetesPedigreeFunction': [dpf], 'Age': [age]
    })


model, scaler = train_model(df, model_algorithm_choice, target, features)

if model:
    st.header("Results")
    scaled_user_data = scaler.transform(user_data[features])
    prediction = model.predict(scaled_user_data)
    prediction_proba = model.predict_proba(scaled_user_data)

    st.subheader("Prediction:")
    if prediction[0] == 1:
        st.error(f"Based on the data provided, the {model_algorithm_choice} model predicts a **HIGH RISK**.")
    else:
        st.success(f"Based on the data provided, the {model_algorithm_choice} model predicts a **LOW RISK**.")
    
    st.write(f"Confidence (Low Risk): {prediction_proba[0][0]*100:.2f}%")
    st.write(f"Confidence (High Risk): {prediction_proba[0][1]*100:.2f}%")

    st.markdown("---")

    st.subheader("Data Analysis & Comparison")
    st.markdown("See where your metrics stand compared to the dataset.")

    col1, col2 = st.columns(2)

    with col1:
        if model_choice == "Heart Disease":
            st.markdown("#### Cholesterol & Blood Pressure")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(x='chol', y='trestbps', hue='target', data=df, palette='viridis', style='sex', s=100)
            ax.scatter(user_data['chol'], user_data['trestbps'], color='red', marker='X', s=200, label='Your Data')
            ax.legend()
            plt.title('Cholesterol vs. Blood Pressure')
            st.pyplot(fig)
        else:
            st.markdown("#### BMI & Glucose")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(x='BMI', y='Glucose', hue='Outcome', data=df, palette='viridis', s=100)
            ax.scatter(user_data['BMI'], user_data['Glucose'], color='red', marker='X', s=200, label='Your Data')
            ax.legend()
            plt.title('BMI vs. Glucose')
            st.pyplot(fig)

    with col2:
        st.markdown("#### Age Distribution")
        fig, ax = plt.subplots(figsize=(8, 6))
        if model_choice == "Heart Disease":
            sns.histplot(df['age'], kde=True, bins=20, color='skyblue', ax=ax)
            ax.axvline(user_data['age'][0], color='red', linestyle='--', label='Your Age')
        else:
            sns.histplot(df['Age'], kde=True, bins=20, color='skyblue', ax=ax)
            ax.axvline(user_data['Age'][0], color='red', linestyle='--', label='Your Age')
        ax.legend()
        plt.title('Age Distribution in Dataset')
        plt.xlabel('Age')
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("Model Performance")
    X = df[features]
    y = df[target]
    
    
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    st.write(f"Cross-Validation Scores for {model_algorithm_choice}:")
    st.info(cv_scores)
    
    st.metric(f"Mean Accuracy (from 5-fold CV):", f"{cv_scores.mean()*100:.2f}%")
    st.markdown("Cross-validation provides a more reliable estimate of model performance on unseen data.")

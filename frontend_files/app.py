# Streamlit frontend: collects inputs and calls the Flask backend API
import os
import requests
import streamlit as st

# In Docker the backend is reachable by its container name on the shared network
BACKEND_URL = os.getenv("BACKEND_URL", "http://superkart-backend:7860")

st.set_page_config(page_title="SuperKart Sales Forecast", layout="centered")
st.title("SuperKart Sales Forecast")
st.write("Enter the product and store details to predict the total sales of the product in that store.")

col1, col2 = st.columns(2)
with col1:
    product_weight = st.number_input("Product Weight", min_value=1.0, max_value=30.0, value=12.66)
    sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    area = st.number_input("Product Allocated Area", min_value=0.001, max_value=0.5, value=0.027, format="%.3f")
    mrp = st.number_input("Product MRP", min_value=20.0, max_value=300.0, value=117.08)
    id_char = st.selectbox("Product Id prefix", ["FD", "DR", "NC"])
with col2:
    category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    city = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2",
                                             "Departmental Store", "Food Mart"])
    store_age = st.number_input("Store Age (years)", min_value=0, max_value=60, value=16)

payload = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": sugar,
    "Product_Allocated_Area": area,
    "Product_MRP": mrp,
    "Store_Size": store_size,
    "Store_Location_City_Type": city,
    "Store_Type": store_type,
    "Product_Id_char": id_char,
    "Store_Age_Years": store_age,
    "Product_Type_Category": category,
}

if st.button("Predict", type="primary"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=30)
        if response.status_code == 200:
            st.success(f"Predicted sales: {response.json()['Predicted_Sales']:,.2f}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the backend: {e}")

st.divider()
st.subheader("Batch prediction")
uploaded = st.file_uploader("Upload a CSV with the model feature columns", type="csv")
if uploaded is not None and st.button("Predict for file"):
    response = requests.post(f"{BACKEND_URL}/v1/predictbatch",
                             files={"file": uploaded.getvalue()}, timeout=60)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(f"Error {response.status_code}: {response.text}")

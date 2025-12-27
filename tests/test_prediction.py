import pandas as pd
from mlProject.pipeline.prediction import PredictionPipeline

# ---------- FIXTURE ----------
def get_pipeline():
    return PredictionPipeline()


# ---------- UC1 : CLIENT VA CHURNER (1) ----------
def test_customer_will_churn():
    pipeline = get_pipeline()

    input_data = {
        "Age": 24,
        "Gender": "Male",
        "Country": "France",
        "City": "Paris",
        "Membership_Years": 1,
        "Login_Frequency": 2,
        "Session_Duration_Avg": 12,
        "Pages_Per_Session": 1,
        "Cart_Abandonment_Rate": 0.75,
        "Wishlist_Items": 0,
        "Total_Purchases": 1,
        "Average_Order_Value": 20,
        "Days_Since_Last_Purchase": 210,
        "Discount_Usage_Rate": 0.0,
        "Returns_Rate": 0.6,
        "Email_Open_Rate": 0.03,
        "Customer_Service_Calls": 7,
        "Product_Reviews_Written": 0,
        "Social_Media_Engagement_Score": 1,
        "Mobile_App_Usage": 1,
        "Payment_Method_Diversity": 1,
        "Lifetime_Value": 60,
        "Credit_Balance": 15,
        "Signup_Quarter": "Q1"
    }

    df = pd.DataFrame([input_data])
    prediction = pipeline.predict(df)

    assert prediction[0] == 1, "❌ Le client aurait dû churner (1)"


# ---------- UC2 : CLIENT NE VA PAS CHURNER (0) ----------
def test_customer_will_not_churn():
    pipeline = get_pipeline()

    input_data = {
        "Age": 35,
        "Gender": "Female",
        "Country": "Germany",
        "City": "Berlin",
        "Membership_Years": 3,
        "Login_Frequency": 10,
        "Session_Duration_Avg": 120.5,
        "Pages_Per_Session": 5,
        "Cart_Abandonment_Rate": 0.2,
        "Wishlist_Items": 2,
        "Total_Purchases": 15,
        "Average_Order_Value": 80,
        "Days_Since_Last_Purchase": 10,
        "Discount_Usage_Rate": 0.3,
        "Returns_Rate": 0.1,
        "Email_Open_Rate": 0.5,
        "Customer_Service_Calls": 1,
        "Product_Reviews_Written": 3,
        "Social_Media_Engagement_Score": 50,
        "Mobile_App_Usage": 15,
        "Payment_Method_Diversity": 2,
        "Lifetime_Value": 2000,
        "Credit_Balance": 500,
        "Signup_Quarter": "Q2"
    }

    df = pd.DataFrame([input_data])
    prediction = pipeline.predict(df)

    assert prediction[0] == 0, "❌ Le client aurait dû rester (0)"

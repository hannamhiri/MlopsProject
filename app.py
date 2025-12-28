from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from mlProject.pipeline.prediction import PredictionPipeline

app = Flask(__name__)  # initializing a flask app

@app.route('/', methods=['GET'])  
def homePage():
    return render_template("index.html")

@app.route('/train', methods=['GET'])  
def training():
    os.system("python main.py")
    return "Training Successful!" 

@app.route('/predict', methods=['POST', 'GET'])  
def index():
    if request.method == 'POST':
        try:
            # Récupération des inputs utilisateur
            input_data = {
                "Age": int(request.form['Age']),
                "Gender": request.form['Gender'],
                "Country": request.form['Country'],
                "City": request.form['City'],
                "Membership_Years": int(request.form['Membership_Years']),
                "Login_Frequency": int(request.form['Login_Frequency']),
                "Session_Duration_Avg": float(request.form['Session_Duration_Avg']),
                "Pages_Per_Session": int(request.form['Pages_Per_Session']),
                "Cart_Abandonment_Rate": float(request.form['Cart_Abandonment_Rate']),
                "Wishlist_Items": int(request.form['Wishlist_Items']),
                "Total_Purchases": int(request.form['Total_Purchases']),
                "Average_Order_Value": float(request.form['Average_Order_Value']),
                "Days_Since_Last_Purchase": int(request.form['Days_Since_Last_Purchase']),
                "Discount_Usage_Rate": float(request.form['Discount_Usage_Rate']),
                "Returns_Rate": float(request.form['Returns_Rate']),
                "Email_Open_Rate": float(request.form['Email_Open_Rate']),
                "Customer_Service_Calls": int(request.form['Customer_Service_Calls']),
                "Product_Reviews_Written": int(request.form['Product_Reviews_Written']),
                "Social_Media_Engagement_Score": int(request.form['Social_Media_Engagement_Score']),
                "Mobile_App_Usage": int(request.form['Mobile_App_Usage']),
                "Payment_Method_Diversity": int(request.form['Payment_Method_Diversity']),
                "Lifetime_Value": float(request.form['Lifetime_Value']),
                "Credit_Balance": float(request.form['Credit_Balance']),
                "Signup_Quarter": request.form['Signup_Quarter']
            }

            # Convertir en array numpy (1 ligne)
            df_input = pd.DataFrame([input_data])
            
            obj = PredictionPipeline()
            predict = obj.predict(df_input)[0] 
            print(predict)

            return render_template('results.html', prediction=str(predict))

        except Exception as e:
            print('The Exception message is: ', e)
            return 'Something went wrong. Check the console for details.'

    else:
        return render_template('index.html', prediction=predict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

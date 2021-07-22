from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_titanic_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Pclass = request.form['Pclass']
        if Pclass=='Upper Class':
            Pclass=1
        elif Pclass=='Middle Class':
            Pclass=2
        else:
            Pclass=3
            
        Sex=request.form['Sex']
        if Sex=='Male':
            Sex=0
        else:
            Sex=1
            
        Age=int(request.form['Age'])
        if Age <= 17:
            Age = 0
        elif Age >17 & Age <=21:
            Age = 1
        elif Age >21 & Age <=25:
            Age = 2
        elif Age >25 & Age <=30:
            Age = 3
        elif Age >30 & Age <=32:
            Age = 4
        elif Age >32 & Age <=36:
            Age = 5
        elif Age >36 & Age <=45:
            Age = 6
        else:
            Age = 7
            
        
        SibSp=int(request.form['SibSp'])
        
        Parch=int(request.form['Parch'])
        
        Fare=int(request.form['Fare'])
        if Fare <= 7:
            Fare = 0
        elif Fare >7 & Fare <=10:
            Fare = 1
        elif Fare >10 & Fare <=21:
            Fare = 2
        elif Fare >21 & Fare <=39:
            Fare = 3
        else:
            Fare = 4
    
        
        Embarked=request.form['Embarked']
        if Embarked=='Southampton':
            Embarked=0
        elif Embarked=='Cherbourg':
            Embarked=1
        else:
            Embarked=2
        
        Title=request.form['Title']
        if Title=='Mr':
            Title=0
        elif Title=='Miss':
            Title=1
        elif Title=='Mrs':
            Title=3
        elif Title=='Master':
            Title=4
        else:
            Title=5
        
        Cabin=int(request.form['Cabin'])
        
        FamilySize = SibSp + Parch + 1
        
        FarePerMember = int(Fare/FamilySize)
        
        AgeClass = Age * Pclass
        
        prediction=model.predict([[Pclass, Sex, SibSp, Parch, Age, Fare, Embarked, Title, Cabin, FamilySize, FarePerMember, AgeClass]])
        output = prediction[0]
        if output == 0:
            return render_template('index.html',prediction_text="The Passenger possibly did not Survive")
        else:
            return render_template('index.html',prediction_text="The Passenger Survived!!")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
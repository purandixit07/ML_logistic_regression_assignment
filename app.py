
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from wsgiref import simple_server
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            rate_marriage = float(request.form['rate_marriage'])
            yrs_married = float(request.form['yrs_married'])
            children = float(request.form['children'])
            religious = float(request.form['religious'])
            educ = float(request.form['educ'])
            occupation = float(request.form['occupation'])
            occupation_husb = float(request.form['occupation_husb'])
            filename = 'log_reg_assign_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict([[rate_marriage,yrs_married,children,religious,educ,occupation,occupation_husb]])
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction[0])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #port = int(os.getenv("PORT"))
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host,port=5000, app=app)
    print("localhost:5000")
    httpd.serve_forever()
    

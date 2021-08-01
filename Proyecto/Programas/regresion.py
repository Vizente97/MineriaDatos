import pandas as pd 
import numpy as np 
from sklearn import linear_model, model_selection
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore') 

class Regresion_Analysis():
    def format_Checkbox(columnas):
        columnas_final = []
        checks = []
        for i in range(len(columnas)):
            columnas_final.append(columnas[i])
            checks.append("checkbox")
        tabla = {'Utilizar': checks, 'Datos': columnas_final}
        return (tabla)

    def newData(valores,old_data):
        lista = valores.split(",")
        lista.pop(0)
        new_data = old_data.drop(columns=lista)
        return (new_data)

    def model_train(new_data,x_values,y_value,test):
        lista = x_values.split(",")
        X_train = np.array(new_data[lista])
        Y_train = np.array(new_data[[y_value]])
        test_value = test
        Clasificacion = linear_model.LogisticRegression()
        seed = 1234
        XTrain, X_validation, YTrain, Y_validation = model_selection.train_test_split(X_train, Y_train, test_size=float(test_value),random_state=seed, shuffle=True)
        Clasificacion.fit(XTrain, YTrain)
        PrediccionesNuevas = Clasificacion.predict(X_validation)
        Exactitud = Clasificacion.score(X_validation, Y_validation)
        text_exact = "<p><b>Exactitud del Modelo: </b>"+str(Exactitud)+"</p>"
        report = classification_report(Y_validation,PrediccionesNuevas, output_dict=True)
        tabla = pd.DataFrame(report).transpose()
        return (text_exact, tabla)

import pandas as pd 
import numpy as np 
from sklearn import linear_model, model_selection
from sklearn.base import ClassifierMixin
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle                  
import os  
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
        valores = ""
        diccionario = {}
        for i in range(len(lista)):
            valor = Clasificacion.coef_[0][i]
            variable = lista[i]
            diccionario[variable] = valor
            valores += " + "+str(round(valor,3))+str(variable)
        intercept_value = Clasificacion.intercept_
        diccionario['Intercept'] = intercept_value[0]
        text_function = "<p style='width: 1500px;'><b>a+bX= </b>"+str(intercept_value[0])+valores+"</p>"
        return (text_exact, tabla,text_function,diccionario,Clasificacion)

    def loadModel(archivo):
        inputs_values = []
        nombre_fichero = os.path.join(os.sep, "Users", "vis_9", "Desktop", "GitHub", "MineriaDatos", "Proyecto", "Modelos", archivo)
        with open(nombre_fichero, "rb") as f:
            data2 = pickle.load(f)
        listOfKeys = data2.keys()
        inputs = ""
        for key in listOfKeys:
            if(key != "Intercept"):
                inputs_values.append(key)
                inputs += '<p><b>Indique el valor de '+str(key)+':</b></p>'+'<input type="number" id="'+str(key)+'" name="'+str(key)+'" min="0" max="100" class="form-control" style="width: 100%"><br>'
        return (inputs,inputs_values)

    def UseModel(values,archivo):
        nombre_fichero = os.path.join(os.sep, "Users", "vis_9", "Desktop", "GitHub", "MineriaDatos", "Proyecto", "Modelos","Formulas", archivo)
        with open(nombre_fichero, "rb") as f:
            data2 = pickle.load(f)
        #listOfKeys = data2.keys()
        #valor = 0
        #for key in listOfKeys:
        #    if(key != "Intercept"):
        #        valor += data2[key] * values[key] 
        #    else:
        #        valor += data2["Intercept"]
        #valor_final = 1/(1+np.e**(-(valor)))
        #cadena_pronostico = '<p><b>Diagnostico: </b>'+str(valor_final)+"</p>"
        NuevoPaciente = pd.DataFrame(values)
        cadena_pronostico = data2.predict(NuevoPaciente)
        cadena_pronostico_final = '<p><b>Diagnostico: </b>'+str(cadena_pronostico[0])+"</p>"
        return (cadena_pronostico_final)


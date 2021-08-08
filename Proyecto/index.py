from flask import Flask, render_template, request, jsonify
import pandas as pd 
from io import StringIO, BytesIO
from Programas.data_view import Data
from Programas.correlaciones import corrData
from Programas.pcaAnalysis import PCA_Analysis
from Programas.kmeans import KMeans_Program
from Programas.apriori import Apriori_Analysis
from Programas.regresion import Regresion_Analysis
import numpy as np
import matplotlib.pyplot as plt
plt.matplotlib.use('agg')
from base64 import b64encode
import seaborn as sns
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
from apyori import apriori
import pickle                  
import os  
import os.path  
from werkzeug.datastructures import FileStorage

app = Flask("Mineria Datos")
data_global = {}
new_data_global = {}
selection = []
kmeans = []
diccionario_model = {}
keys = {}
modelo_in_use = ""
clasificacion = ""

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/404.html')
def error404():
    return render_template('404.html')

@app.route('/EDA_action.html')
def EDA_action():
    return render_template('EDA_action.html')

@app.route('/template_base.html')
def template_base():
    return render_template('template_base.html')

@app.route('/Sec_Carac_Corr_action.html')
def Sec_Carac_Corr_action():
    return render_template('Sec_Carac_Corr_action.html')
    
@app.route('/metricas.html')
def metricas():
    return render_template('metricas.html')

@app.route('/pca.html')
def pca():
    return render_template('pca.html')

@app.route('/cluster.html')
def cluster():
    return render_template('cluster.html')

@app.route('/apriori.html')
def apriori_algoritmo():
    return render_template('apriori.html')
    
@app.route('/d_EDA.html')
def d_EDA():
    return render_template('d_EDA.html')
    
@app.route('/d_Correlaciones.html')
def d_Correlaciones():
    return render_template('d_Correlaciones.html')

@app.route('/d_Metricas.html')
def d_Metricas():
    return render_template('d_Metricas.html')

@app.route('/d_PCA.html')
def d_PCA():
    return render_template('d_PCA.html')

@app.route('/d_Cluster.html')
def d_Cluster():
    return render_template('d_Cluster.html')

@app.route('/d_Apriori.html')
def d_Apriori():
    return render_template('d_Apriori.html')

@app.route('/contacto.html')
def contacto():
    return render_template('contacto.html')

@app.route('/regresion.html')
def regresion():
    return render_template('regresion.html')

@app.route('/d_regresion.html')
def d_regresion():
    return render_template('d_regresion.html')

@app.route('/regresion_model.html')
def regresion_model_url():
    if(os.path.isdir("Modelos") == False):
        os.mkdir("Modelos")
        os.mkdir("Modelos/Formulas")
    ruta = os.path.join("Modelos")
    dir_list = os.listdir(ruta)
    return render_template('regresion_model.html', modelos = dir_list)

@app.route("/data_file", methods=["POST"])
def analize_file():
    global data_global
    valor_column = request.form["column_options"]
    #print(valor_column)
    valor_fila = request.form["fila_options"]
    response = {}
    if valor_column == "all":
        shape_file = data_global.shape
        data_type = Data.data_types(str(data_global.dtypes))
        data_null = Data.data_null(str(data_global.isnull().sum()))
        img = image_html(0,valor_column, valor_fila)
        resumen = pd.DataFrame(data_global.describe()).to_html().replace("dataframe","table table-bordered")
        resumen = resumen.replace('border="1"','id="table2"')
        relacion = pd.DataFrame(data_global.corr()).to_html().replace("dataframe","table table-bordered")
        relacion = relacion.replace('border="1"','id="table3"')
        heap_img = heapmap_html(0, valor_column, valor_fila)
    else:
        datos2 = getattr(data_global,valor_column)
        shape_file = data_global[datos2 == valor_fila].shape
        data_type = Data.data_types(str(data_global[datos2 == valor_fila].dtypes))
        data_null = Data.data_null(str(data_global[datos2 == valor_fila].isnull().sum()))
        img = image_html(datos2, valor_column, valor_fila)
        resumen = pd.DataFrame(data_global[datos2 == valor_fila].describe()).to_html().replace("dataframe","table table-bordered")
        resumen = resumen.replace('border="1"','id="table2"')
        relacion = pd.DataFrame(data_global[datos2 == valor_fila].corr()).to_html().replace("dataframe","table table-bordered")
        relacion = relacion.replace('border="1"','id="table3"')
        heap_img = heapmap_html(datos2, valor_column, valor_fila)
    return jsonify(shape_file,data_type,data_null, img, resumen,relacion,heap_img)

@app.route("/data_table", methods=["POST"])
def analize_data():
    global data_global
    response = {}
    name = request.files["file"]
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        type = (name.filename).split(".")[-1]
        if type.lower() == "csv":
            Datos = pd.read_csv(StringIO(file_content))
        elif type.lower() == "txt":
            Datos = pd.read_table(StringIO(file_content))
        #Datos = pd.read_csv(StringIO(file_content))
        data_global = Datos
        frame = pd.DataFrame(Datos)
        HTML = frame.to_html().replace("dataframe","table table-bordered")
        HTML = HTML.replace('border="1"','id="table1"')
        labels = Data.config_columnas(list(Datos.columns.values))
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(HTML,labels)

@app.route("/data_filas", methods=["POST"])
def data_filas():
    global data_global
    valor_column = request.form["column_options"]
    response = {}
    valores = data_global[str(valor_column)].tolist()
    valores2 = Data.config_columnas(list(pd.unique(valores)))
    return jsonify(valores2)

def image_html(datos2, valor_column, valor_fila):
    if valor_column == "all":
        dtf = pd.DataFrame.from_records(data_global.hist(figsize=(14,14), xrot=45))
    else:
        dtf = pd.DataFrame.from_records(data_global[datos2 == valor_fila].hist(figsize=(14,14), xrot=45))
    #figura = plt.figure()
    pic_IObytes = BytesIO()
    plt.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    image = """<img src="data:image/png;base64,{b64}" style="width: 1000;height: 1000px;"/>"""
    final = image.format(b64=pic_hash.decode("utf-8"))
    #print(final)
    plt.close()
    return (final)

def heapmap_html(datos2, valor_column, valor_fila):
    plt.figure(figsize=(30,30))
    if valor_column == "all":
        sns.heatmap(data_global.corr(), cmap='RdBu_r', annot=True)
    else:
        sns.heatmap(data_global[datos2 == valor_fila].corr(), cmap='RdBu_r', annot=True)
    pic_IObytes = BytesIO()
    plt.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    image = """<img src="data:image/png;base64,{b64}" style="width: 1000;height: 1000px;"/>"""
    final = image.format(b64=pic_hash.decode("utf-8"))
    #print(final)
    plt.close()
    return (final)

################## Correlaciones y seleccion de caracteristicas ##########################
@app.route("/data_analize", methods=["POST"])
def data_analize():
    global data_global
    response = {}
    name = request.files["file"]
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        type = (name.filename).split(".")[-1]
        if type.lower() == "csv":
            Datos = pd.read_csv(StringIO(file_content))
        elif type.lower() == "txt":
            Datos = pd.read_table(StringIO(file_content))
        data_global = Datos
        frame = pd.DataFrame(Datos)
        HTML = frame.to_html().replace("dataframe","table table-bordered")
        HTML = HTML.replace('border="1"','id="table1"')
        shape_file = data_global.shape
        data_type = Data.data_types(str(data_global.dtypes))
        data_null = Data.data_null(str(data_global.isnull().sum()))
        relacion = pd.DataFrame(data_global.corr(method='pearson')).to_html().replace("dataframe","table table-bordered")
        relacion = relacion.replace('border="1"','id="table2"')
        heap_img,heap_inf,heap_sup = corrData.heapmap_html(data_global)
        labels = Data.config_columnas_corr(list(Datos.columns.values))
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(HTML,shape_file,data_type,data_null,relacion,heap_img,heap_inf,heap_sup,labels)

@app.route("/graph_corr", methods=["POST"])
def graph_corr():
    global data_global
    valor_abs = request.form["abscisa_options"]
    valor_ord = request.form["ordenada_options"]
    sns.scatterplot(y=valor_abs, x =valor_ord, data=data_global)
    plt.title('Gráfico de dispersión')
    plt.xlabel(valor_ord)
    plt.ylabel(valor_abs)
    pic_IObytes = BytesIO()
    plt.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    image = """<img src="data:image/png;base64,{b64}" style="width: 500px;height: 400px;"/>"""
    graph = image.format(b64=pic_hash.decode("utf-8"))
    plt.close()
    return jsonify(graph)


##########################################################################################

###################################### Métricas ##########################################

@app.route("/metrics", methods=["POST"])
def metrics():
    global data_global
    metrica = request.form["metricas_options"]
    name = request.files["file"]
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        type = (name.filename).split(".")[-1]
        if type.lower() == "csv":
            Datos = pd.read_csv(StringIO(file_content))
        elif type.lower() == "txt":
            Datos = pd.read_table(StringIO(file_content))
        data_global = Datos
        if (metrica == "minkowski"):
            valor_p = request.form["p_minkowski"]
            matriz = pd.DataFrame(cdist(Datos, Datos, metric=metrica, p=float(valor_p))).to_html().replace("dataframe","table table-bordered")
        else:
            matriz = pd.DataFrame(cdist(Datos, Datos, metric=metrica)).to_html().replace("dataframe","table table-bordered")
        matriz = matriz.replace('border="1"','id="table2"')
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(matriz)

##########################################################################################

######################################## PCA ############################################

@app.route("/data_table_pca", methods=["POST"])
def data_table_pca():
    global data_global
    global selection
    selection = []
    name = request.files["file"]
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        type = (name.filename).split(".")[-1]
        if type.lower() == "csv":
            Datos = pd.read_csv(StringIO(file_content))
        elif type.lower() == "txt":
            Datos = pd.read_table(StringIO(file_content))
        data_global = Datos
        frame = pd.DataFrame(Datos)
        HTML = frame.to_html().replace("dataframe","table table-bordered")
        HTML = HTML.replace('border="1"','id="table1"')
        labels = Data.config_columnas_pca(list(Datos.columns.values))
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(HTML,labels)

@app.route("/update_data", methods=["POST"])
def update_data():
    global data_global
    response = {}
    columna = request.form["columns_options"]
    updateData = data_global.drop([columna], axis=1)
    data_global = updateData
    frame = pd.DataFrame(updateData)
    HTML = frame.to_html().replace("dataframe","table table-bordered")
    HTML = HTML.replace('border="1"','id="table2"')
    labels = Data.config_columnas_pca(list(updateData.columns.values))
    return jsonify(HTML,labels)

@app.route("/normalize_data", methods=["POST"])
def normalize_data():
    global data_global
    response = {}
    normalizar = StandardScaler() 
    normalizar.fit(data_global)
    MNormalizada = normalizar.transform(data_global)
    frame = pd.DataFrame(MNormalizada,columns=data_global.columns)
    HTML = frame.to_html().replace("dataframe","table table-bordered")
    HTML = HTML.replace('border="1"','id="table3"')
    return jsonify(HTML)

@app.route("/pca_analysis", methods=["POST"])
def pca_analysis():
    number = request.form["components"]
    global data_global
    normalizar = StandardScaler() 
    normalizar.fit(data_global)
    MNormalizada = normalizar.transform(data_global)
    Componentes,x_Comp = PCA_Analysis.componentes(MNormalizada,number)
    ######### Tabla componentes #########
    frame = pd.DataFrame(x_Comp)
    HTML = frame.to_html().replace("dataframe","table table-bordered")
    HTML = HTML.replace('border="1"','id="table4"')
    ######## Eigenvalues y Varianza ######
    eigenvalues, varianza, img = PCA_Analysis.varianza(Componentes)
    no_abs, abs = PCA_Analysis.matrices(Componentes)
    no_abs_cargas, abs_cargas = PCA_Analysis.cargas(Componentes,data_global)
    return jsonify(HTML,str(eigenvalues),varianza,img,no_abs, abs,no_abs_cargas, abs_cargas)

##########################################################################################

###################################### Cluster ###########################################

@app.route("/graph_dispertion", methods=["POST"])
def graph_dispertion():
    global data_global
    group = request.form["group_options"]
    valor_abs = request.form["x_options"]
    valor_ord = request.form["y_options"]
    sns.scatterplot(x=valor_abs, y=valor_ord, data=data_global, hue=group)
    plt.title('Gráfico de dispersión')
    plt.xlabel(valor_abs)
    plt.ylabel(valor_ord)
    pic_IObytes = BytesIO()
    plt.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    image = """<img src="data:image/png;base64,{b64}" style="width: 500px;height: 400px;"/>"""
    graph = image.format(b64=pic_hash.decode("utf-8"))
    plt.close()
    return jsonify(graph)

@app.route("/pearson", methods=["POST"])
def pearson():
    global data_global
    matriz = pd.DataFrame(data_global.corr(method='pearson')).to_html().replace("dataframe","table table-bordered")
    matriz = matriz.replace('border="1"','id="table2"')
    mp = pd.DataFrame(data_global.corr(method='pearson'))
    MatrizInf = np.triu(mp)
    plt.figure(figsize=(28,8))
    sns.heatmap(mp, cmap='RdBu_r', annot=True, mask=MatrizInf)
    pic_IObytes = BytesIO()
    plt.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    image = """<img src="data:image/png;base64,{b64}" style="width: 1100px;height: 450px;"/>"""
    graph = image.format(b64=pic_hash.decode("utf-8"))
    labels = Data.config_columnas_pca(list(data_global.columns.values))
    return jsonify(matriz,graph,labels)

@app.route("/select_variables", methods=["POST"])
def select_variables():
    global data_global
    global selection
    variable = request.form["selection_options"]
    if variable in selection:
        print("Ya esta en la lista")
    else:
        selection.append(request.form["selection_options"])
    #print(selection)
    lista_var = Data.data_select(selection)
    return jsonify(lista_var)

@app.route("/createData", methods=["POST"])
def crearData():
    global data_global
    global selection
    global kmeans
    kmeans = np.array(data_global[selection])
    frame = pd.DataFrame(np.array(data_global[selection]))
    HTML = frame.to_html().replace("dataframe","table table-bordered")
    HTML = HTML.replace('border="1"','id="table3"')
    return jsonify(HTML)

##########################################################################################

####################################### Kmans ############################################

@app.route("/kmeas", methods=["POST"])
def kmeas():
    global kmeans
    global selection
    see, lista = KMeans_Program.see(kmeans)
    knee = KMeans_Program.knee(lista)
    t_clusters, g_clusters, MParticional = KMeans_Program.clusters(kmeans,data_global)
    t_centroides,CentroidesP = KMeans_Program.centroides(MParticional,selection)
    img_3d = KMeans_Program.img3D(MParticional,CentroidesP,kmeans)
    return jsonify(see, knee, t_clusters, g_clusters, t_centroides, img_3d)

##########################################################################################

###################################### Apriori ###########################################

@app.route("/data_table_apriori", methods=["POST"])
def data_table_apriori():
    global data_global
    global selection
    selection = []
    file_content = request.files["file"].read().decode("utf-8")
    header = request.form["header_options"]
    if len(file_content) > 0:
        if header == "no_header":
            Datos = pd.read_csv(StringIO(file_content),header=None)
        else:
            Datos = pd.read_csv(StringIO(file_content))
        data_global = Datos
        frame = pd.DataFrame(Datos)
        HTML = frame.to_html().replace("dataframe","table table-bordered")
        HTML = HTML.replace('border="1"','id="table1"')
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(HTML)

@app.route("/reglas_apriori", methods=["POST"])
def reglas_apriori():
    global data_global
    support = request.form["soporte"]
    confidence = request.form["confianza"]
    lift = request.form["elevacion"]
    MoviesLista = []
    for i in range(0, len(data_global)):
        MoviesLista.append([str(data_global.values[i,j]) 
        for j in range(0, 20)])
    ListaConfiguracion = apriori(MoviesLista, min_support=float(support), min_confidence=float(confidence), min_lift=int(lift))
    ReglasConfiguracion = list(ListaConfiguracion)
    #print(ReglasConfiguracion)
    resultado = Apriori_Analysis.format_Data(ReglasConfiguracion)
    frame = pd.DataFrame(resultado)
    HTML = frame.to_html().replace("dataframe","table table-bordered")
    HTML = HTML.replace('border="1"','id="table2"')
    return jsonify(HTML)

##########################################################################################

##################################### Regresión ##########################################

@app.route("/data_table_regresion", methods=["POST"])
def data_table_regresion():
    global data_global
    name = request.files["file"]
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        type = (name.filename).split(".")[-1]
        if type.lower() == "csv":
            Datos = pd.read_csv(StringIO(file_content))
        elif type.lower() == "txt":
            Datos = pd.read_table(StringIO(file_content))
        data_global = Datos
        frame = pd.DataFrame(Datos)
        HTML = frame.to_html().replace("dataframe","table table-bordered")
        HTML = HTML.replace('border="1"','id="table1"')
        labels = Regresion_Analysis.format_Checkbox(list(Datos.columns.values))
        frame = pd.DataFrame(labels)
        HTML2 = frame.to_html().replace("dataframe","table table-bordered")
        HTML2 = HTML2.replace('border="1"','id="table2"')
        HTML2 = HTML2.replace('checkbox','<input type="checkbox">')
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(HTML,HTML2)

@app.route("/regresion_data", methods=["POST"])
def regresion_data():
    global data_global
    global new_data_global
    valores = request.form["seleccionados"]
    newData_reg = Regresion_Analysis.newData(valores,data_global)
    new_data_global = newData_reg
    frame = pd.DataFrame(newData_reg)
    HTML = frame.to_html().replace("dataframe","table table-bordered")
    HTML = HTML.replace('border="1"','id="table3"')
    labels = Regresion_Analysis.format_Checkbox(list(newData_reg.columns.values))
    frame = pd.DataFrame(labels)
    HTML2 = frame.to_html().replace("dataframe","table table-bordered")
    HTML2 = HTML2.replace('border="1"','id="table4"')
    HTML2 = HTML2.replace('checkbox','<input type="checkbox">')
    labels = Data.config_columnas_corr(list(newData_reg.columns.values))
    return jsonify(HTML,HTML2,labels)

@app.route("/regresion_model", methods=["POST"])
def regresion_model():
    global clasificacion
    global new_data_global
    global diccionario_model
    x_values = request.form["seleccionados"]
    y_values = request.form["y_pronosticar"]
    test = request.form["test"]
    exactitud, tabla,formula,model_formula,clasificacion = Regresion_Analysis.model_train(new_data_global,x_values,y_values,test)
    diccionario_model = model_formula
    frame = pd.DataFrame(tabla)
    HTML = frame.to_html().replace("dataframe","table table-bordered")
    HTML = HTML.replace('border="1"','id="table5"')
    return jsonify(exactitud,HTML,formula)

@app.route("/save_model", methods=["POST"])
def save_model():
    global diccionario_model
    global clasificacion
    name_model = request.form["name_model"]
    nombre_archivo = str(name_model)+str(".bin")
    if(os.path.isdir("Modelos") == False):
        os.mkdir("Modelos")
        os.mkdir("Modelos/Formulas")
    nombre_fichero = os.path.join("Modelos", nombre_archivo)
    data_string = pickle.dumps(diccionario_model)
    file = open(nombre_fichero, "wb")
    file.write(data_string)
    file.close()
    nombre_archivo = str(name_model)+str("_formula.bin")
    nombre_fichero2 = os.path.join("Modelos","Formulas", nombre_archivo)
    data_string2 = pickle.dumps(clasificacion)
    file = open(nombre_fichero2, "wb")
    file.write(data_string2)
    file.close()
    return jsonify(0)

@app.route("/load_model", methods=["POST"])
def load_model():
    global modelo_in_use
    global keys
    name_model = request.form["modelo"]
    model_formula = name_model.replace(".bin","_formula.bin")
    modelo_in_use = model_formula
    inputs,keys_values = Regresion_Analysis.loadModel(name_model)
    keys = keys_values
    return jsonify(inputs,keys)

@app.route("/use_model", methods=["POST"])
def use_model():
    global modelo_in_use
    diccionario = {}
    for i in range(len(keys)):
        diccionario[keys[i]] = [float(request.form[str(keys[i])])]
    prediccion = Regresion_Analysis.UseModel(diccionario, modelo_in_use)
    return jsonify(prediccion)

##########################################################################################

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", debug=False, port=port)
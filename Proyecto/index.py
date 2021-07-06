from flask import Flask, render_template, request, jsonify, send_file, Response, abort
import pandas as pd 
from io import StringIO, BytesIO
import json
from Programas.data_view import Data
from Programas.correlaciones import corrData
import numpy as np
import matplotlib.pyplot as plt
from base64 import b64encode
import seaborn as sns
from scipy.spatial.distance import cdist

app = Flask("Mineria Datos")
data_global = {}

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
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        Datos = pd.read_csv(StringIO(file_content))
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
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        Datos = pd.read_csv(StringIO(file_content))
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
    sns.scatterplot(x=valor_abs, y =valor_ord, data=data_global)
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
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        Datos = pd.read_csv(StringIO(file_content))
        data_global = Datos
        matriz = pd.DataFrame(cdist(Datos, Datos, metric=metrica)).to_html().replace("dataframe","table table-bordered")
        matriz = matriz.replace('border="1"','id="table2"')
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(matriz)

##########################################################################################

if __name__ == '__main__':
    app.run()
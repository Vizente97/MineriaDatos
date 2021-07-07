from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from base64 import b64encode
import pandas as pd 

class PCA_Analysis():
    def componentes(MNormalizada,number):
        Componentes = PCA(n_components=int(number)) 
        Componentes.fit(MNormalizada)
        X_Comp = Componentes.transform(MNormalizada)
        return(Componentes,X_Comp)

    def varianza(Componentes):
        eugenvalues = Componentes.explained_variance_ratio_
        varianza = sum(eugenvalues[0:5])
        plt.plot(np.cumsum(Componentes.explained_variance_ratio_))
        plt.xlabel('Número de componentes')
        plt.ylabel('Varianza acumulada')
        plt.grid()
        pic_IObytes = BytesIO()
        plt.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        plt.close
        image = """<img src="data:image/png;base64,{b64}" style="width: 500px;height: 400px;"/>"""
        graph = image.format(b64=pic_hash.decode("utf-8"))
        return(eugenvalues,varianza,graph)

    def matrices(Componentes):
        frame = pd.DataFrame(Componentes.components_)
        HTML5 = frame.to_html().replace("dataframe","table table-bordered")
        HTML5 = HTML5.replace('border="1"','id="table5"')
        frame2 = pd.DataFrame(abs(Componentes.components_))
        HTML6 = frame2.to_html().replace("dataframe","table table-bordered")
        HTML6 = HTML6.replace('border="1"','id="table6"')
        return(HTML5,HTML6)

    def cargas(Componentes,data):
        CargasComponentes = pd.DataFrame(Componentes.components_, columns=data.columns)
        HTML7 = CargasComponentes.to_html().replace("dataframe","table table-bordered")
        HTML7 = HTML7.replace('border="1"','id="table7"')
        CargasComponentes2 = pd.DataFrame(abs(Componentes.components_), columns=data.columns)
        HTML8 = CargasComponentes2.to_html().replace("dataframe","table table-bordered")
        HTML8 = HTML8.replace('border="1"','id="table8"')
        return(HTML7,HTML8)
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from base64 import b64encode
import pandas as pd 
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator
from mpl_toolkits.mplot3d import Axes3D

class KMeans_Program():
    def see(data):
        SSE = []
        for i in range(2,12):
            km = KMeans(n_clusters=i,random_state=0)
            km.fit(data)
            SSE.append(km.inertia_)
        plt.figure(figsize=(10,7))
        plt.plot(range(2,12),SSE, marker='o')
        plt.xlabel('Cantidad de clusters *k*')
        plt.ylabel('SSE')
        plt.title('Elbow Method')
        plt.show()
        pic_IObytes = BytesIO()
        plt.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        plt.close
        image = """<img src="data:image/png;base64,{b64}" style="width: 500px;height: 400px;"/>"""
        graph = image.format(b64=pic_hash.decode("utf-8"))
        return(graph,SSE)

    def knee(SSE):
        kl = KneeLocator(range(2,12),SSE,curve='convex',direction='decreasing')
        kl.elbow
        plt.style.use('ggplot')
        kl.plot_knee()
        pic_IObytes = BytesIO()
        plt.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        plt.close
        image = """<img src="data:image/png;base64,{b64}" style="width: 500px;height: 400px;"/>"""
        graph = image.format(b64=pic_hash.decode("utf-8"))
        return(graph)

    def clusters(data,global_data):
        MParticional = KMeans(n_clusters=4, random_state=0).fit(data)
        MParticional.predict(data)
        MParticional.labels_
        global_data['clusterP'] = MParticional.labels_
        frame = pd.DataFrame(global_data)
        HTML = frame.to_html().replace("dataframe","table table-bordered")
        HTML = HTML.replace('border="1"','id="table4"')
        plt.figure(figsize=(10,7))
        plt.scatter(data[:,0], data[:,1], c=MParticional.labels_, cmap='rainbow')
        pic_IObytes = BytesIO()
        plt.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        plt.close
        image = """<img src="data:image/png;base64,{b64}" style="width: 500px;height: 400px;"/>"""
        graph = image.format(b64=pic_hash.decode("utf-8"))
        return(HTML,graph,MParticional)

    def centroides(MParticional,selection):
        CentroidesP = MParticional.cluster_centers_
        tabla = pd.DataFrame(CentroidesP.round(4), columns=selection)
        HTML = tabla.to_html().replace("dataframe","table table-bordered")
        HTML = HTML.replace('border="1"','id="table5"')
        return(HTML,CentroidesP)

    def img3D(MParticional,CentroidesP,data):
        plt.rcParams['figure.figsize'] = (10,7)
        plt.style.use('ggplot')
        colores=['red','blue','green','yellow']
        asignar=[]
        for row in MParticional.labels_:
            asignar.append(colores[row])
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(data[:,0],data[:,1],data[:,2], marker='o', c=asignar, s=60)
        ax.scatter(CentroidesP[:,0],CentroidesP[:,1],CentroidesP[:,2], marker='*', c=colores, s=1000)
        pic_IObytes = BytesIO()
        plt.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        plt.close
        image = """<img src="data:image/png;base64,{b64}" style="width: 700px;height: 420px;"/>"""
        graph = image.format(b64=pic_hash.decode("utf-8"))
        return(graph)
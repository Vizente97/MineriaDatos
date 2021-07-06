from io import BytesIO
import matplotlib.pyplot as plt
from base64 import b64encode
import seaborn as sns
from matplotlib import rcParams
import numpy as np
    

class corrData(object):
    def heapmap_html(data_global):
        plt.figure(figsize=(28,8))
        rcParams.update({'figure.autolayout': True})
        sns.heatmap(data_global.corr(), cmap='RdBu_r', annot=True)
        b, t = plt.ylim() # discover the values for bottom and top
        b += 0.5 # Add 0.5 to the bottom
        t -= 0.5 # Subtract 0.5 from the top
        plt.ylim(b, t) # update the ylim(bottom, top) values
        pic_IObytes = BytesIO()
        plt.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        image = """<img src="data:image/png;base64,{b64}" style="width: 1000px;height: 400px;"/>"""
        complete = image.format(b64=pic_hash.decode("utf-8"))
        plt.close()
        
        plt.figure(figsize=(28,8))
        MatrizInf = np.triu(data_global.corr())
        sns.heatmap(data_global.corr(), cmap='RdBu_r', annot=True, mask=MatrizInf)
        b, t = plt.ylim() # discover the values for bottom and top
        b += 0.5 # Add 0.5 to the bottom
        t -= 0.5 # Subtract 0.5 from the top
        plt.ylim(b, t) # update the ylim(bottom, top) values
        pic_IObytes = BytesIO()
        plt.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        image = """<img src="data:image/png;base64,{b64}" style="width: 1000px;height: 400px;"/>"""
        inf = image.format(b64=pic_hash.decode("utf-8"))
        plt.close()

        plt.figure(figsize=(28,8))
        MatrizSup = np.tril(data_global.corr())
        sns.heatmap(data_global.corr(), cmap='RdBu_r', annot=True, mask=MatrizSup)
        b, t = plt.ylim() # discover the values for bottom and top
        b += 0.5 # Add 0.5 to the bottom
        t -= 0.5 # Subtract 0.5 from the top
        plt.ylim(b, t) # update the ylim(bottom, top) values
        pic_IObytes = BytesIO()
        plt.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        image = """<img src="data:image/png;base64,{b64}" style="width: 1000px;height: 400px;"/>"""
        sup = image.format(b64=pic_hash.decode("utf-8"))
        plt.close()
        return (complete,inf,sup)

    def graph_relation(data_global):
        print("Hola Mundo")
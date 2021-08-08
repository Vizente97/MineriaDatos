# MineriaDatos

Para poder ejecutar este proyecto de manera local se especifican las siguientes instrucciones, cabe destacar que todo fue desarrollado en el sistema operativo Windows.
Favor de seguir los pasos a continuación:

1. Anaconda: Como primer paso se debe descargar e instalar Anaconda, ahí
crearemos nuestro ambiente para tener un mejor control de versiones.

Link de descarga: https://www.anaconda.com/products/individualDownloads

2. Repositorio de GitHub: Se debe descargar el siguiente repositorio, en donde se encuentran todos los archivos necesarios para la ejecución correcta del
proyecto, en la carpeta "Data - Prácticas.encontrará ejemplos de archivos que
puede utilizar y dentro de "Proyectos"se encuentran todo lo relacionado con la
página web del proyecto.

Link de descarga: https://github.com/Vizente97/MineriaDatos

3. Creación de env: Es necesario un ambiente virtual para lo cual se debe abrir
la consola de Anaconda Prompt (anaconda3) y ubicarse en la carpeta proyecto
del repositorio previamente clonado, se deberá ejecutar el siguiente comando:

conda env create –name PaginaWeb –file=PaginaWeb.yml

4. Activar env: Estando en la misma ruta procederemos a activar el ambiente
creado con el siguiente comando:

conda activate PaginaWeb

5. Ejecución de programa: por último se procede a ejecutar el index.py, esto se
realiza dentro de la consola de anaconda con el ambiente activado, ingresando
el siguiente comando:

python index.py

Obtendremos el resultado donde se nos indica cual será la url que
debemos de poner en nuestro navegador.

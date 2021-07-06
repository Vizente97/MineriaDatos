class Data(object):
    def config_columnas(columnas):
        #print(columnas)
        cadena = '<option value="all">Todas</option>'
        for s in columnas:
            option = '<option value="' + str(s) + '">' + str(s) +'</option>'
            cadena += option
        #print(cadena)
        return (cadena)

    def config_columnas_corr(columnas):
        cadena = ''
        for s in columnas:
            option = '<option value="' + str(s) + '">' + str(s) +'</option>'
            cadena += option
        #print(cadena)
        return (cadena)

    def data_types(types):
        #print(types)
        output=types.split('\n')
        #print(len(output))
        for i in range(len(output)):
            output[i]=output[i].replace(" ",".")
        cadena = "<ul>"
        for s in output:
            ul = "<li>" + str(s) + "</li>"
            cadena += ul
        cadena += "</ul>"
        return (cadena)

    def data_null(data):
        #print(data)
        output=data.split('\n')
        for i in range(len(output)):
            output[i]=output[i].replace(" ",".")
        cadena = "<ul>"
        for s in output:
            ul = "<li>" + str(s) + "</li>"
            cadena += ul
        cadena += "</ul>"
        salida=cadena.replace("dataframe","table table-bordered")
        return (salida)
    
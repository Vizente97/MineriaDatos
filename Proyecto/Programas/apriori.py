class Apriori_Analysis():
    def format_Data(ReglasApriori):
        regla_apr = []
        soporte = []
        confianza = []
        elevacion = []
        for i in range(len(ReglasApriori)):
            regla = ReglasApriori[i]
            reglas = [x for x in regla[0]]
            cambio = str(tuple(list(reglas)))
            cambio = cambio.replace(","," -->")
            regla_apr.append(cambio)
            soporte.append(regla[1])
            confianza.append(regla[2][0][2])
            elevacion.append(regla[2][0][3])
        tabla = {'Regla': regla_apr, 'Soporte': soporte, 'Confianzia': confianza, 'Elevación': elevacion}
        return (tabla)
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import creds as creds
import pickle as pkl

def load_data(schema, table):
    """
    Esta función crea la conexión con PostgreSQL para que se puedan leer los datos y correr el modelo de aprendizaje de máquina.

    Argumentos:
        schema (string): Nombre del esquema en donde se tiene la tabla con el Data Set
        table (string): Nombre de la tabla con la información de las caravanas

    Salidas:
        data (pandas DataFrame): Contiene un DataFrame con la información de la tabla de psql
    
    """
    conn_string = "host="+ creds.PGHOST + " port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER + " password="+ creds.PGPASSWORD
    conn=psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
    data = pd.read_sql(sql_command, conn)
    return data

def modelado():
    """
    Esta función recibe un conjunto de datos previamente procesado y descargado de la web mediante Bash para entrenar un modelo de regresión logística. 
    Debido a que este es un ejercicio didáctico donde no se evalúa la parte de modelado, se omite el paso de selección de variables (Feature Engineering) 
    y se toma de referencia  un trabajo reportado en https://medium.com/swlh/machine-learning-to-kaggle-caravan-insurance-challenge-on-r-f52790bc7669 donde
    se definen las variables más importantes que encontraron para realizar las predicciones de seguros de caravanas.

    Argumentos: (ninguno)

    Salidas:
        modelo (objeto): Contiene el modelo que resultó del conjunto de entrenamiento
        precision (float): Métrica de Precisión del modelo
        recall (float): Métrica de recall del modelo
        
    """
    # Lectura del conjunto de datos desde PostgreSQL
    df_train_test = load_data("public","variables")
    #df_train_test = pd.read_csv("../../ticdata2000_wh.txt", sep = "|")
    
    # Selección de variables de acuerdo al artículo
    feature_cols = ['mopllaag', 'mink123m', 'ppersaut', 'pwaoreg','pbrand','aplezier','afiets']
    
    # Separación del conjunto en entrenamiento y prueba (75% de los datos para entrenar el modelo)
    X = df_train_test[feature_cols]
    y = df_train_test.caravan
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)

    # Modelo con parámetros por default
    logreg = LogisticRegression()
    
    # Entrenamiento del modelo
    modelo = logreg.fit(X_train,y_train)

    # Predicciones en el conjunto de prueba
    y_pred=logreg.predict(X_test)

    # Métricas resultantes del modelo
    recall = metrics.recall_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)

    return modelo, precision, recall

def prediccion(listas):
    dic = {}
    columns = ['MOPLLAAG', 'MINK123M', 'PPERSAUT', 'PWAOREG','PBRAND','APLEZIER','AFIETS']
    for y in range(0,len(listas[0])):
        tmp = []
        for x in listas:
            tmp.append(x[y])
        dic[columns[y]] = tmp
    df = pd.DataFrame(dic)
    modelo, precision, recall, df_c = modelado()
    y_pred = modelo.predict(listas)
    df['pred'] = pd.Series(y_pred)
    return y_pred
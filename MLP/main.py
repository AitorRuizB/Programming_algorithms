"""Aitor Ruiz Bautista·"""
#Usar siempre lo siguiente al abrir para ejecutar
# source inteligentes/bin/activate
# export XLA_FLAGS=--xla_gpu_cuda_data_dir=/usr/lib/cuda


import logging,os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"]= "3"
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model


def Tarea_A(X_train,Y_train,X_test,Y_test):
    #Primero definimos el modelo 
    model = keras.Sequential(name="MLP_A")
    model.add(layers.Flatten(input_shape=(32,32,3))) # aplana las imágenes para que entren como un vector
    model.add(layers.Dense(32))#Capas ocultas
    model.add(layers.Activation("sigmoid")) #Funcion de activacion
    model.add(layers.Dense(10))#Numero de ultimas capas
    model.add(layers.Activation("softmax"))
    #Ahora compilamos el modelo
    model.compile(loss="categorical_crossentropy",
                  optimizer=keras.optimizers.Adam(),
                  metrics=["accuracy"])
    print("Modelo compilado")
    print("Resumen del modelo")
    model.summary() #Resumen del modelo
    #Comienzo del entenamiento
    history=model.fit(X_train,Y_train,batch_size=32,
                                    epochs=10,
                                    validation_split=0.1,
                                    verbose=1)
    test_score=model.evaluate(X_test,Y_test,verbose=1)#evaluacion con test para ver tasa de acierto
    print("Test accuracy and loss:", test_score[1], test_score[0])
    plot_results(history) #Grafico para ver progreso

def Tarea_B(X_train,Y_train,X_test,Y_test):
    
    split_values=[0.1, 0.15, 0.20, 0.25, 0.30]
    batch=32 #Aumentar para probar mas rapido
    medias_val=[]
    medias_test=[]

    for split in split_values:
        val_acc_list = []
        test_acc_list = []

        for i in range(5):
            model=define_model_keras() #Hay que definir el modelo cada vez

            history= model.fit(X_train,Y_train,batch_size=batch,epochs=50,validation_split=split,
                                verbose=0,callbacks=[early_stop])
            # Precision de validacion en entrenamiento
            val_accuracy = history.history['val_accuracy'][-1]
            val_acc_list.append(val_accuracy)
            #Precision de test
            test_score = model.evaluate(X_test, Y_test, verbose=0)
            test_accuracy = test_score[1]
            test_acc_list.append(test_accuracy)

        #Calculo de medias 
        mean_val=np.mean(val_acc_list)
        mean_test=np.mean(test_acc_list)

        medias_val.append(mean_val)
        medias_test.append(mean_test)

        print(f"Split {split:.2f} → Precisión validación: {mean_val:.4f}, Precisión test: {mean_test:.4f}")


    # Gráfico de barras
    x = np.arange(len(split_values))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, medias_val, width, label='Validación', color='skyblue')
    plt.bar(x + width/2, medias_test, width, label='Test', color='orange')
    plt.xticks(x, [f"{s:.2f}" for s in split_values])
    plt.xlabel('Validation Split')
    plt.ylabel('Precisión media')
    plt.title('Precisión media por split en validación y test')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def Tarea_C(X_train, Y_train, X_test, Y_test):

    batch_sizes = [ 256,512,1024,2048]
    epochs=20
    accuracies = []
    times = []

    for batchs in batch_sizes:
        print(f"\n Entrenando con batch size = {batchs}...")

        model = define_model_keras()  # Modelo nuevo por cada batch size
       
        start_time = time.time()

        model.fit(X_train, Y_train,
                batch_size=batchs,
                epochs=epochs,
                validation_split=0.2,
                verbose=0
        )

        elapsed_time = time.time() - start_time
        _, test_accuracy = model.evaluate(X_test, Y_test, verbose=1)

        print(f" Accuracy: {test_accuracy:.4f} -  Tiempo: {elapsed_time:.2f} s")

        accuracies.append(test_accuracy)
        times.append(elapsed_time)
        #matrices de confusion
        matriz_confusion(Y_test,X_test,model,batchs)
        

   # Conversión de datos
    batch_labels = [str(bs) for bs in batch_sizes]
    x = np.arange(len(batch_labels))  # posiciones en eje X
    width = 0.35  # ancho de cada barra

    plt.figure(figsize=(10, 6))

    # Barras de precisión
    plt.bar(x - width/2, accuracies, width, label='Precisión', color='cornflowerblue')

    # Barras de tiempo (normalizadas si hay diferencia grande)
    max_time = max(times)
    normalized_times = [t / max_time for t in times]  # escala entre 0 y 1 para que sean comparables
    plt.bar(x + width/2, normalized_times, width, label='Tiempo (normalizado)', color='lightcoral')

    # Etiquetas y título
    plt.xlabel('Batch Size')
    plt.ylabel('Valor')
    plt.title('Precisión y Tiempo de Entrenamiento por Batch Size')
    plt.xticks(x, batch_labels)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(axis='y')

    # Etiquetas encima de las barras
    for i in range(len(batch_sizes)):
        plt.text(x[i] - width/2, accuracies[i] + 0.01, f"{accuracies[i]:.2f}", ha='center', fontsize=8)
        plt.text(x[i] + width/2, normalized_times[i] + 0.01, f"{times[i]:.1f}s", ha='center', fontsize=8)

    plt.tight_layout()
    plt.show()

def Tarea_D(X_train,Y_train,X_test,Y_test):
    

    activations= ["sigmoid","swish","softmax","tanh","relu","elu"]
    batch=88
    epochs=20
    accuracies = []
    times = []


    for activation in activations:
        print(f"\n Entrenando con activacion = {activation}...")

        model = define_model_keras(activation)  # Modelo nuevo por cada batch size
       
        start_time = time.time()

        model.fit(X_train, Y_train,
                batch_size=batch,
                epochs=epochs,
                validation_split=0.2,
                verbose=0
        )

        elapsed_time = time.time() - start_time
        _, test_accuracy = model.evaluate(X_test, Y_test, verbose=1)

        print(f" Accuracy: {test_accuracy:.4f} -  Tiempo: {elapsed_time:.2f} s")

        accuracies.append(test_accuracy)
        times.append(elapsed_time)

        #Mostrar matrices de confusión
        matriz_confusion(Y_test,X_test,model,activation)

    # Conversión de datos
    activation_labels = activations
    x = np.arange(len(activation_labels))  # posiciones en eje X
    width = 0.35  # ancho de cada barra

    plt.figure(figsize=(10, 6))

    # Barras de precisión
    plt.bar(x - width/2, accuracies, width, label='Precisión', color='cornflowerblue')

    # Barras de tiempo (normalizado)
    max_time = max(times)
    normalized_times = [t / max_time for t in times]
    plt.bar(x + width/2, normalized_times, width, label='Tiempo (normalizado)', color='lightcoral')

    # Etiquetas y título
    plt.xlabel('Función de Activación')
    plt.ylabel('Valor')
    plt.title('Precisión y Tiempo de Entrenamiento por Función de Activación')
    plt.xticks(x, activation_labels)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(axis='y')

    # Etiquetas encima de las barras
    for i in range(len(activation_labels)):
        plt.text(x[i] - width/2, accuracies[i] + 0.01, f"{accuracies[i]:.2f}", ha='center', fontsize=8)
        plt.text(x[i] + width/2, normalized_times[i] + 0.01, f"{times[i]:.1f}s", ha='center', fontsize=8)

    plt.tight_layout()
    plt.show()

def Tarea_E(X_train, Y_train, X_test, Y_test):

    hidden_neurons =[32, 64, 128, 256,512,1024]
    activation = "sigmoid"  # fija la activación

    batch = 88
    epochs = 25
    accuracies = []
    times = []

    for n_neurons in hidden_neurons:
        print(f"\nEntrenando con {n_neurons} neuronas ocultas...")

        model = define_model_keras(activation, n_neurons)

        start_time = time.time()

        model.fit(X_train, Y_train,
                  batch_size=batch,
                  epochs=epochs,
                  validation_split=0.2,
                  verbose=0)

        elapsed_time = time.time() - start_time
        _, test_accuracy = model.evaluate(X_test, Y_test, verbose=1)

        print(f" Accuracy: {test_accuracy:.4f} - Tiempo: {elapsed_time:.2f} s")

        accuracies.append(test_accuracy)
        times.append(elapsed_time)

    # Gráfico comparativo final
    labels = [str(n) for n in hidden_neurons]
    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, accuracies, width, label='Precisión', color='cornflowerblue')

    max_time = max(times)
    normalized_times = [t / max_time for t in times]
    plt.bar(x + width/2, normalized_times, width, label='Tiempo (normalizado)', color='lightcoral')

    plt.xlabel('Número de Neuronas Ocultas')
    plt.ylabel('Valor')
    plt.title('Precisión y Tiempo por Número de Neuronas Ocultas')
    plt.xticks(x, labels)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(axis='y')

    for i in range(len(labels)):
        plt.text(x[i] - width/2, accuracies[i] + 0.01, f"{accuracies[i]:.2f}", ha='center', fontsize=8)
        plt.text(x[i] + width/2, normalized_times[i] + 0.01, f"{times[i]:.1f}s", ha='center', fontsize=8)

    plt.tight_layout()
    plt.show()

def Tarea_F(X_train,Y_train,X_test,Y_test):

    configuraciones = {
        "1 capa (256)": [256],
        "2 capas(200,56)": [200,56],
        "3 capas (100,56,100)": [100,56,100]
        
    }

    batch = 200
    epochs = 40

    accuracies = []
    times = []

    for nombre_config, capas in configuraciones.items():
        print(f"\nEntrenando modelo: {nombre_config} con capas = {capas}")

        model = model_tarea_F(hidden_layers=capas)

        start_time = time.time()

        history=model.fit(X_train, Y_train,
                  batch_size=batch,
                  epochs=epochs,
                  validation_split=0.2,
                  verbose=0,
                  callbacks=[early_stop])

        elapsed_time = time.time() - start_time
        _, test_accuracy = model.evaluate(X_test, Y_test, verbose=1)

        print(f"Accuracy: {test_accuracy:.4f} - Tiempo: {elapsed_time:.2f} s")

        accuracies.append(test_accuracy)
        times.append(elapsed_time)
        plot_results(history)

    # Gráfico de barras
    etiquetas = list(configuraciones.keys())
    x = np.arange(len(etiquetas))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, accuracies, width, label='Precisión', color='cornflowerblue')

    max_time = max(times)
    normalized_times = [t / max_time for t in times]
    plt.bar(x + width/2, normalized_times, width, label='Tiempo (normalizado)', color='lightcoral')

    plt.xlabel('Configuración de Capas Ocultas')
    plt.ylabel('Valor')
    plt.title('Comparación de Precisión y Tiempo por Configuración de Capas Ocultas')
    plt.xticks(x, etiquetas)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(axis='y')

    for i in range(len(etiquetas)):
        plt.text(x[i] - width/2, accuracies[i] + 0.01, f"{accuracies[i]:.2f}", ha='center', fontsize=8)
        plt.text(x[i] + width/2, normalized_times[i] + 0.01, f"{times[i]:.1f}s", ha='center', fontsize=8)

    plt.tight_layout()
    plt.show()

def Tarea_G(X_train,Y_train,X_test,Y_test):

    batch=256
    epoch=50

    """Definir el modelo CNN sin capas"""
    model= keras.Sequential(name="Model_B_CNN")
    #primera capa 16
    model.add(layers.Conv2D(16,(3,3),activation='relu',input_shape=(32,32,3)))
    #segunda capa 32
    model.add(layers.Conv2D(32,(3,3),activation='relu'))
    #para la capa de salida:
    model.add(layers.Flatten())
    #capa de salida
    model.add(layers.Dense(10,activation='softmax'))
    #Compilar modelo
    model.compile(optimizer=keras.optimizers.Adam(),loss='categorical_crossentropy',metrics=['accuracy'])

    print("Modelo CNN compilado:")
    model.summary()

    history= model.fit(X_train,Y_train,
                        batch_size=batch,
                        epochs=epoch,
                        validation_split=0.2,
                        verbose=1,
                        callbacks=[early_stop]
    )
    #Evaluacion
    test_loss, test_accuracy = model.evaluate(X_test, Y_test, verbose=1)
    print(f"Precisión en test: {test_accuracy:.4f}")
    plot_results(history)

    """Definir modelo CNN Con capas pooling"""

    model= keras.Sequential(name="Model_B_CNN_pooling")
    #primera capa 16
    model.add(layers.Conv2D(16,(3,3),activation='relu',input_shape=(32,32,3)))
    #capa pooling
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    #segunda capa 32
    model.add(layers.Conv2D(32,(3,3),activation='relu'))
    #capa pooling
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    #para la capa de salida:
    model.add(layers.Flatten())
    #capa de salida
    model.add(layers.Dense(10,activation='softmax'))
    #Compilar modelo
    model.compile(optimizer=keras.optimizers.Adam(),loss='categorical_crossentropy',metrics=['accuracy'])

    print("Modelo CNN con pooling compilado:")
    model.summary()

    history= model.fit(X_train,Y_train,
                        batch_size=batch,
                        epochs=epoch,
                        validation_split=0.2,
                        verbose=1,
                        callbacks=[early_stop]
    )
    #Evaluacion
    test_loss, test_accuracy = model.evaluate(X_test, Y_test, verbose=1)
    print(f"Precisión en test: {test_accuracy:.4f}")
    plot_results(history)

def Tarea_H(X_train,Y_train,X_test,Y_test):


    filtros =[(3,3)]
    stride=(1,1)

    batch = 256
    epochs = 100
    accuracies = []
    times = []

    for filtro in filtros:
        print(f"\nEntrenando con filtro{filtro} ...")

        model = modelo_CNN(filtro,stride)

        start_time = time.time()

        history=model.fit(X_train, Y_train,
                  batch_size=batch,
                  epochs=epochs,
                  validation_split=0.2,
                  verbose=0,
                  callbacks=[early_stop])

        elapsed_time = time.time() - start_time
        _, test_accuracy = model.evaluate(X_test, Y_test, verbose=1)
    
        print(f" Accuracy: {test_accuracy:.4f} - Tiempo: {elapsed_time:.2f} s")
        plot_results(history)
        accuracies.append(test_accuracy)
        times.append(elapsed_time)
        matriz_confusion(Y_test,X_test,model,filtro)
        mostrar_predicciones(model,X_test,Y_test)
        #model.save("Last_model.h5")#Guardar el modelo
    # Gráfico comparativo final
    labels = [str(n) for n in filtros]
    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, accuracies, width, label='Precisión', color='cornflowerblue')

    max_time = max(times)
    normalized_times = [t / max_time for t in times]
    plt.bar(x + width/2, normalized_times, width, label='Tiempo (normalizado)', color='lightcoral')

    plt.xlabel('Filtro')
    plt.ylabel('Valor')
    plt.title('Precisión y Tiempo por Filtro')
    plt.xticks(x, labels)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(axis='y')

    for i in range(len(labels)):
        plt.text(x[i] - width/2, accuracies[i] + 0.01, f"{accuracies[i]:.2f}", ha='center', fontsize=8)
        plt.text(x[i] + width/2, normalized_times[i] + 0.01, f"{times[i]:.1f}s", ha='center', fontsize=8)

    plt.tight_layout()
    plt.show()

"""Definir modelo de CNN para Tarea H"""
def modelo_CNN(filtro,stride):

    model= keras.Sequential(name="Model_B_CNN_pooling")
    model.add(layers.Conv2D(32,filtro,activation='relu',input_shape=(32,32,3),padding='same')) 

    model.add(layers.BatchNormalization()) 
    model.add(layers.Conv2D(32,filtro,activation='relu',padding='same')) 
    model.add(layers.MaxPooling2D(pool_size=(2,2))) 
    model.add(layers.Conv2D(64,filtro,activation='relu',padding='same')) 

    model.add(layers.BatchNormalization()) 
    model.add(layers.Conv2D(64,filtro,activation='relu',padding='same')) 

    model.add(layers.MaxPooling2D(pool_size=(2,2))) 
    #para la capa de salida:
    model.add(layers.Flatten())
    #capa de salida
    model.add(layers.Dense(10,activation='softmax'))
    #Compilar modelo
    model.compile(optimizer=keras.optimizers.Adam(),loss='categorical_crossentropy',metrics=['accuracy'])

    print("Modelo CNN con pooling compilado:")
    model.summary()

    return model


"""Definir el modelo keras MLP"""
def define_model_keras(activation="sigmoid",n_neuronas=32):

    model = keras.Sequential(name="MLP_A")
    model.add(layers.Flatten(input_shape=(32,32,3))) # aplana las imágenes para que entren como un vector
    model.add(layers.Dense(n_neuronas)) #numero de neuronas en las capas ocultas
    model.add(layers.Activation(activation))
    model.add(layers.Dense(10))#Numero de ultimas capas
    """ Es igual a 10 porque es el número de clases que tiene
    que clasificar"""
    model.add(layers.Activation("softmax"))

    model.compile(loss="categorical_crossentropy",
                  optimizer=keras.optimizers.Adam(),
                  metrics=["accuracy"])
    print("Modelo compilado")
    print("Resumen del modelo")
    model.summary()
    return model        
    
"""Definir el modelo para la tarea F"""
def model_tarea_F(hidden_layers=[32]):

   #Modificar segun numero de neuronas y capas  

    model = keras.Sequential(name="MLP_A")
    # Capa de entrada
    model.add(layers.Flatten(input_shape=(32, 32, 3)))

    # Capas ocultas: las recorremos todas
    for n in hidden_layers:
        model.add(layers.Dense(n))
        model.add(layers.Activation("sigmoid"))

    # Capa de salida
    model.add(layers.Dense(10))
    model.add(layers.Activation("softmax"))

    model.compile(
        loss="categorical_crossentropy",
        optimizer=keras.optimizers.Adam(),
        metrics=["accuracy"]
    )

    print("Modelo compilado")
    model.summary()
    return model

"""Mostrar matrices de confusion"""
def matriz_confusion(Y_test,X_test,model,dato):

    #Clases de etiquetas de datos:
    class_names = [
        'airplane', 'automobile', 'bird', 'cat', 'deer',
        'dog', 'frog', 'horse', 'ship', 'truck'
    ]

    if len(Y_test.shape) > 1 and Y_test.shape[1] > 1:
        y_test_labels = np.argmax(Y_test, axis=1)
    else:
        y_test_labels = Y_test

    y_pred_prob = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_prob, axis=1)

    cm = confusion_matrix(y_test_labels, y_pred)

    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=class_names, yticklabels=class_names)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.title(f'Matriz de confusión {dato})')
    plt.xlabel('Etiqueta predicha')
    plt.ylabel('Etiqueta real')
    plt.tight_layout()
    plt.show()


"""Gráfica para plotear resultados"""
def plot_results(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))

    # Precisión
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, label='Precisión de entrenamiento')
    plt.plot(epochs, val_acc, label='Precisión de validación')
    plt.title('Precisión por época')
    plt.xlabel('Época')
    plt.ylabel('Precisión')
    plt.legend()
    plt.grid(True)

    # Pérdida
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, label='Pérdida de entrenamiento')
    plt.plot(epochs, val_loss, label='Pérdida de validación')
    plt.title('Pérdida por época')
    plt.xlabel('Época')
    plt.ylabel('Pérdida')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

"""Resultados con imagenes"""
def mostrar_predicciones(model, X_test, Y_test):
    # Seleccionar índices aleatorios
    num_index=10

    class_names = [
        'airplane', 'automobile', 'bird', 'cat', 'deer',
        'dog', 'frog', 'horse', 'ship', 'truck'
    ]

    indices = np.random.choice(len(X_test), num_index, replace=False)
    imagenes = X_test[indices]
    etiquetas_reales = Y_test[indices]

    # Predecir
    predicciones = model.predict(imagenes, verbose=0)
    clases_predichas = np.argmax(predicciones, axis=1)

    # Mostrar imágenes y predicciones
    plt.figure(figsize=(10, 5))
    for i in range(num_index):
        plt.subplot(1, num_index, i + 1)
        plt.imshow(imagenes[i])
        plt.title(f"Pred: {class_names[clases_predichas[i]]}")
        plt.axis("off")
    plt.tight_layout()
    plt.show()


"""Parada para que no haya sobreentrenamiento"""
early_stop= EarlyStopping(monitor='val_accuracy',
                        patience=5,
                        min_delta=0.001, #para que haya un margen de mejora
                        start_from_epoch=5, #evita parar por cambios iniciales
                        restore_best_weights=True)

def model_train_single(X_train,Y_train,X_test,Y_test,batch=32):

    model=define_model_keras()

    split=0.2
    epoch=100
    start_time= time.time() #tiempo inicial

    history=model.fit(X_train,Y_train,batch_size=batch,
                                    epochs=epoch,
                                    validation_split=split,
                                    verbose=0,
                                    callbacks=[early_stop])

    end_time=time.time()
    elapsed_time=end_time - start_time #Segundos que tarda
   
    print(f" Tiempo de entrenamiento: {elapsed_time:.2f} segundos")
    plot_results(history)

    return history
    


if __name__=="__main__":

    #Cargar datos de Cifar10
    (X_train, Y_train), (X_test, Y_test) = keras.datasets.cifar10.load_data()
    print(X_train.shape, X_train.dtype)
    print(Y_train.shape, Y_train.dtype)
    print(X_test.shape, X_test.dtype)
    print(Y_test.shape, Y_test.dtype)
    """ Convertir imágenes en array"""
    X_train = X_train.astype("float32") / 255.0
    X_test = X_test.astype("float32") / 255.0

    """Proceso one hot encoding para preparar los datos para etiquetas"""
    Y_train = keras.utils.to_categorical(Y_train, 10)
    Y_test = keras.utils.to_categorical(Y_test, 10)

    """ Resumen en Tareas"""

    """
    Tarea_A(X_train,Y_train,X_test,Y_test)
    
    Tarea_B(X_train,Y_train,X_test,Y_test)

    Tarea_C(X_train,Y_train,X_test,Y_test)
    
    Tarea_D(X_train,Y_train,X_test,Y_test)
    
    Tarea_E(X_train,Y_train,X_test,Y_test)
    
    Tarea_F(X_train,Y_train,X_test,Y_test)
    
    Tarea_G(X_train,Y_train,X_test,Y_test)

    Tarea_H(X_train,Y_train,X_test,Y_test)
    """
    
    Tarea_A(X_train,Y_train,X_test,Y_test) #modificar la letra de la tarea para ejecutar por separado

 

    
    
    

    
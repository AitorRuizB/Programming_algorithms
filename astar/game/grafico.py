import numpy as np
import matplotlib.pyplot as plt

# 📌 Datos de ejemplo (Reemplázalos con los valores reales)
# Formato: { "MapaX": [valores de nodos explorados para cada heurística] }
datos_nodos_explorados = {
    "Mapa 1": [24, 7, 4, 9],  # Nodos explorados para cada heurística
    "Mapa 2": [56, 50, 48, 52],
    "Mapa 3": [19,11 , 8, 12],
    "Mapa 4": [104, 41, 27, 49]
}

# 📌 Configuración de gráficos
heuristicas = ["Trivial", "Euclídea", "Manhattan", "Diagonal"]
colores = ["blue", "green", "red", "purple"]  # Colores para cada heurística
fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Crear 4 subgráficos (2x2)
fig.suptitle("Número de Nodos Explorados por Heurística en Cada Mapa", fontsize=14)

# 📌 Dibujar cada gráfico en su subfigura correspondiente
for i, (mapa, valores) in enumerate(datos_nodos_explorados.items()):
    ax = axs[i // 2, i % 2]  # Ubicación en la matriz de subgráficos
    indices = np.arange(len(heuristicas))  # Posiciones en el eje X
    
    ax.bar(indices, valores, color=colores, alpha=0.7)  # Dibujar barras
    
    ax.set_title(mapa)
    ax.set_xticks(indices)
    ax.set_xticklabels(heuristicas, rotation=20)  # Etiquetas con inclinación
    ax.set_ylabel("Nodos Explorados")
    ax.set_ylim(0, max(max(valores) * 1.2, 50))  # Ajustar escala Y dinámicamente

# 📌 Ajustar diseño y mostrar gráfico
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Evita superposición con el título
plt.show()


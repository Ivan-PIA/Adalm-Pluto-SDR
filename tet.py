from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
 
# Скачиваем данные для графика.
url = 'https://python-scripts.com/wp-content/uploads/2019/3d-data.csv'
data = pd.read_csv(url)
 
# Преобразуем его в длинный формат
df = data.unstack().reset_index()
df.columns=["X", "Y", "Z"]
 
# Переименовываем старые названия столбцов в числовой формат.
df['X'] = pd.Categorical(df['X'])
df['X'] = df['X'].cat.codes
 
# Мы собираемся сделать 20 графиков, для 20 разных углов
for angle in range(70, 210, 2):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(df['Y'], df['X'], df['Z'], cmap=plt.cm.viridis, linewidth=0.2)
 
    ax.view_init(30, angle)
 
    filename = 'frames/step'+str(angle)+'.png'
    plt.savefig(filename, dpi=96)
    plt.gca()

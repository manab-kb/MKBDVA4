from flask import Flask, render_template
import json
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_distances
import plotly.express as px
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    with open('../Data/gptforall-embeddings.json', 'r') as file:
        data = json.load(file)

    vectors = [entry['Vector'] for entry in data.values()]
    vectors_array = np.array(vectors)

    distances = cosine_distances(vectors_array)

    pca = PCA(n_components=3)
    reduced_distances = pca.fit_transform(distances)

    reduced_data = {'Distance_X': reduced_distances[:, 0],
                    'Distance_Y': reduced_distances[:, 1],
                    'Distance_Z': reduced_distances[:, 2],
                    'Tut_Text': [entry['Tut_Text'] for entry in data.values()]}

    reduced_data['Contains_Python_Code'] = ['import' in text.lower()
                                            for text in reduced_data['Tut_Text']]

    scaling_factor = 0.8
    reduced_data['Text_Length'] = [
        len(text) * scaling_factor for text in reduced_data['Tut_Text']]

    df_reduced = pd.DataFrame(reduced_data)

    fig = px.scatter_3d(df_reduced, x='Distance_X',
                        y='Distance_Y', z='Distance_Z',
                        hover_data=['Tut_Text'],
                        size='Text_Length',
                        title='3D Scatter Plot of Cosine Distances',
                        color='Contains_Python_Code',
                        color_discrete_map={False: 'blue', True: 'red'},
                        size_max=80,
                        labels={'Contains_Python_Code': 'Contains Python Code'},
                        template='plotly_white')

    fig.update_layout(
        scene=dict(
            xaxis_title='Distance_X',
            yaxis_title='Distance_Y',
            zaxis_title='Distance_Z',
        ),
        legend=dict(
            title_text='Legend : Contains Python Code',
            traceorder='reversed',
        ),
        title=dict(
            x=0.5,
            y=0.9,
            text='Visualisation of Vector Embeddings',
            font=dict(size=20),
        )
    )
    camera = dict(
        eye = dict(x=0.5, y=0.5, z=0)
    )
    fig.update_layout(scene_camera=camera)

    plot_json = fig.to_json()
    return render_template('index.html', plot_json=plot_json)


if __name__ == '__main__':
    app.run(debug=True)

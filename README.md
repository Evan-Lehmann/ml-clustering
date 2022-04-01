# ml-clustering

This project demonstrates the use of clustering, an unsupervised learning method. The clustering algorithm is integrated in a web app and is used to cluster data of mall customers. This project was done primarily in Python but also uses Jupyter Notebook. A deployed demo of this app can be found under the [Deployed Demo](#demo) section.

## General Info
- Web App
  - File Info
    - [app.py](https://github.com/Evan-Lehmann/ml-clustering/blob/main/app.py) compiles the individual pages into a multipage web app.
    - [multipage.py](https://github.com/Evan-Lehmann/ml-clustering/blob/main/multipage.py) acts as a framework that allows multipage web apps.
    - [app_pages](https://github.com/Evan-Lehmann/ml-clustering/tree/main/app_pages) contains the different pages of the web app.
      - [model.py](https://github.com/Evan-Lehmann/ml-clustering/blob/main/app_pages/model.py) contains the model itself.
        - The parameter for the number of clusters can be altered. See [Algorithm](#algorithm) for more information on the algorithm and its parameter and see [Usage](#usage) for information on how to actually use the model.
        - Once the parameter is entered, several charts and datasets will be generated for the given number of clusters.
          - Two charts will be generated. The first chart is a scatter plot that shows the clustered observations on a 2d plane. The second chart is a parallel coordinates plot, which essentially shows how each cluster's values for each features compare relative to each other. 
            - You can read more about parallel coordinates [here](https://en.wikipedia.org/wiki/Parallel_coordinates) 
          - Datasets will be generated, containing statistics on the clustered data.
          - The original dataset will be returned, however now with a label column containing each observation's respective cluster.  
      - [dashboard.py](https://github.com/Evan-Lehmann/ml-clustering/blob/main/app_pages/dashboard.py)
        - Dashboard with descriptive charts and statistics from the original data. 
- Jupyter Notebook
  - The Jupyter Notebook, [ml_clustering.ipynb](https://github.com/Evan-Lehmann/ml-clustering/blob/main/ml_clustering.ipynb), was used for exploratory purposes as well as to create an initial version of the model used in the web app.
- Data
  - The original dataset can be found on Kaggle, [here](https://www.kaggle.com/datasets/lokkagle/mall-customers). 

## <a name="algorithm">Algorithm</a>
- The clustering algorithm used is K-means. 
  - The only parameter is k for the number of clusters.
  - The algorithm works by finding k centroids. Each data points is assigned to the nearest centroid.
    - A centroid is a point that represents the center of a cluster.
  - Read [here](https://en.wikipedia.org/wiki/K-means_clustering) for more information.

## <a name="usage">Usage</a>
- [app.py](https://github.com/Evan-Lehmann/ml-clustering/blob/main/app.py)
  - The web app can be launched locally by entering: 
    ```
    $ streamlit run app.py
    ```
## Dependencies
- Python Version:
 ```
 Python 3.10.1
 ```
- Python Packages:
 ```
 $ pip install -r requirements.txt
 ```
 
  ## <a name="demo">Deployed Demo</a>
 - A deployed demonstration of this app can be found at https://ml-clustering-app.herokuapp.com/. The app was hosted using Heroku, a cloud platform used to work with applications. 
 - Deployment Dependencies 
    - [Procfile](https://github.com/Evan-Lehmann/ml-clustering/blob/main/Procfile) is used to declare the commands run by the application's dynos. 
    - [setup.sh](https://github.com/Evan-Lehmann/ml-clustering/blob/main/setup.sh) is used to add shell commands.
    - [.slugignore](https://github.com/Evan-Lehmann/ml-clustering/blob/main/.slugignore) is used to remove files after code is pushed to Heroku.
    - [runtime.txt](https://github.com/Evan-Lehmann/ml-clustering/blob/main/runtime.txt) is used to declare the Python version used.      
 
 ## License 
 This project is licensed under the [MIT license](LICENSE).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

 

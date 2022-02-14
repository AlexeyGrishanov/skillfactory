import streamlit as st
import numpy as np
import pandas as pd
import lightfm as lf
import nmslib
import pickle
import scipy.sparse as sparse
import json

def nearest_products_nms(itemid, index, n=10):
    """Функция для поиска ближайших соседей, возвращает построенный индекс"""
    nn = index.knnQuery(item_embeddings[itemid], k=n)
    return nn


def get_names(index):
    """
    input - idx of products
    Функция для возвращения имени продукта
    return - list of names
    """
    titles = []
    for idx in index:
        #titles.append(idx)
        titles.append('Product:  {} '.format(mapper_titles[idx]) + '.  ASIN: {}'.format(mapper_asin[idx]))
    return titles

def read_files(folder_name='data'):
    """
    Функция для чтения файлов + преобразование к  нижнему регистру
    """

    # Загрузка json с метаданными, которые потенциально расширить данные для учучшения результатов модели
    #with open(folder_name + '/meta_Grocery_and_Gourmet_Food.json') as f:
    #    meta_list = []
    #    for line in f.readlines():
    #        meta_list.append(json.loads(line))
        
    #meta = pd.DataFrame(meta_list)
    #meta = meta[['asin','title']]
    #meta.title = meta.title.str[0:100]
    #meta.to_csv(folder_name+'/products.csv")

    products = pd.read_csv(folder_name+'/products.csv')
    products['title'] = products.title.str.lower()
    
    return products


def make_mappers():
    """
    Функция для создания отображения id в title
    """
    mapper_titles = dict(zip(products['id'],products['title']))
    mapper_asin = dict(zip(products['id'],products['asin']))
    return mapper_titles, mapper_asin


def load_embeddings(folder_name):
    """
    Функция для загрузки векторных представлений
    """
    with open(folder_name + '/item_embeddings.pickle', 'rb') as f:
        item_embeddings = pickle.load(f)

    # Тут мы используем nmslib, чтобы создать наш быстрый knn
    nms_idx = nmslib.init(method='hnsw', space='cosinesimil')
    nms_idx.addDataPointBatch(item_embeddings)
    nms_idx.createIndex(print_progress=True)
    return item_embeddings,nms_idx


pd.show_versions()

#Загружаем данные
products  = read_files(folder_name='data') 
mapper_titles, mapper_asin = make_mappers()
item_embeddings, nms_idx = load_embeddings(folder_name='data')


#Форма для ввода текста
title = st.text_input('Product Name', '')
title = title.lower()

#Наш поиск по продуктам
output = products[products.title.str.contains(title) > 0]

#Выбор продукта из списка
option = st.selectbox('Which product?', output['title'].values)

#Выводим продукт
'You selected: ', option

val_index = output[output['title'].values == option].index
index = nearest_products_nms(val_index, nms_idx, 5)

#Выводим рекомендации к продукту
'Most recommended products are: '
st.write('', get_names(index[0])[1:])
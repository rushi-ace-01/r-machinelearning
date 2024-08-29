import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Title and Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🐧 Penguin Species Prediction App</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #0F9D58;'>Predict the species of a penguin using machine learning</h3>", unsafe_allow_html=True)

with st.expander('Data'):
  st.write('**Raw Data**')
  df=pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
  df
  
  st.write('**X**')
  X_raw= df.drop('species', axis=1)
  X_raw

  st.write('**y**')
  y_raw = df.species
  y_raw
  
with st.expander('Data visualization'):
  st.scatter_chart(data=df, x='bill_length_mm', y='body_mass_g', color='species')

#Input features
with st.sidebar:
  st.header('Input Features')
  #"island","bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g","sex"
  island= st.selectbox('Island', ('Torgersen', 'Biscoe', 'Dream'))
  sex= st.selectbox('Sex', ('male', 'female'))
  bill_length_mm= st.slider('Bill length (mm)', 39.1 , 59.6,43.9)
  bill_depth_mm= st.slider('Bill depth (mm)', 13.1, 21.5, 17.2)
  body_mass_g= st.slider('Body mass(g)' , 2700.0, 6300.0, 4207.0)
  flipper_length_mm=st.slider('Flipper length (mm)', 172.0, 231.0, 201.0)
  #Create dataframe for input features
  
data = {'island': island,
         'sex': sex,
         'bill_length_mm': bill_length_mm,
         'bill_depth_mm': bill_depth_mm,
         'body_mass_g': body_mass_g, 
         'flipper_length_mm': flipper_length_mm}
         
input_df= pd.DataFrame(data, index=[0])
input_penguins = pd.concat([input_df, X_raw], axis=0)

with st.expander('Input features'):
  st.write('**Input Penguin**')
  input_df
  st.write('**Combined Penguin Data**')
  input_penguins

#Data preparation
#Encode X
encode= ['island','sex']
df_penguins= pd.get_dummies(input_penguins, prefix= encode)

X = df_penguins[1:]
input_row= df_penguins[:1]

#Encode y
target_mapper = {'Adelie': 0,
                 'Chinstrap': 1,
                 'Gentoo':2}
def target_encode(val):
  return target_mapper[val]
y= y_raw.apply(target_encode)
          
with st.expander('Data preparation'):
  st.write('**Encoded X (input penguin)**')
  input_row
  st.write('**Encoded y**')
  y

clf= RandomForestClassifier()
clf.fit(X, y)

prediction = clf.predict(input_row)
prediction_prob = clf.predict_proba(input_row)

df_prediction_prob= pd.DataFrame(prediction_prob)
df_prediction_prob.columns= ['Adelie', 'Chinstrap', 'Gentoo']
# df_prediction_prob.rename(columns= {0: 'Adelie',
#                                     1: 'Chinstrap',
#                                     2: 'Gentoo'})


st.subheader('Predicted Species')
st.dataframe(df_prediction_prob, 
             column_config={
             'Adelie': st.column_config.ProgressColumn(
              'Adelie', 
              format= '%f',
               width='medium',
               min_value=0, max_value=1
               ),
              'Chinstrap': st.column_config.ProgressColumn(
              'Chinstrap', 
              format= '%f',
               width='medium',
               min_value=0, max_value=1
               ),
               'Gentoo': st.column_config.ProgressColumn(
              'Gentoo', 
              format= '%f',
               width='medium',
               min_value=0, max_value=1
               ),
               }, hide_index= True)
penguins_species= np.array(['Adelie', 'Chinstrap', 'Gentoo'])
st.success(str(penguins_species[prediction][0]))

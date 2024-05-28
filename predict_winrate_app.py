import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objs as go


st.set_page_config(layout="wide")
st.title("Predict Winrate MTG")

def main():
    
    st.write(f"App running with Streamlit v. {st.__version__}")
    
    uploaded_file = st.file_uploader("Upload Excel file with winrate matrix")
    if uploaded_file is not None:

        # Can be used wherever a "file-like" object is accepted:
        wr_matrix = pd.read_excel(uploaded_file, index_col = 0, header = 0)
        st.write(wr_matrix)
        
        meta_decks = list(wr_matrix.columns)[1:]
        meta_predictions = {}
        
        with st.sidebar:
            st.write("Fill your metagame prediction (0 to 100)")
            for deck in meta_decks:
                label = deck
                meta_predictions[label] = st.number_input(label, min_value=0, max_value=100)

            others_meta = 100 - np.sum(list(meta_predictions.values()))
            st.write(f"Other decks: {others_meta}%")

            if others_meta < 0:
                st.write("Corrrect meta predictions to sum less than 100%")
                
            meta_vector = np.array([others_meta] + list(meta_predictions.values()))
            
        if meta_vector is not None:
            expected_wr = wr_matrix.dot(meta_vector)/100
            expected_wr.columns = ["Winrate"]
            
            st.write("Expected Winrate per deck")
            st.dataframe(expected_wr, use_container_width=True)
    
#####    
    
if __name__ == '__main__':
    main()

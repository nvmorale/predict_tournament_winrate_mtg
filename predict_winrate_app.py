import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objs as go
import io

DEFAULT_WR_MATRIX = pd.DataFrame({
    "Overall": [50,49,51,40],
    "Aggro": [50,60,40,40],
    "Midrange": [40, 50,60,40],
    "Control": [60,40,50,40],
},
    index = ["Aggro", "Midrange", "Control", "Tier 4 deck"],
)


st.set_page_config(layout="wide")
st.title("Predict Winrate MTG")

def main():
    
    st.write(f"App running with Streamlit v. {st.__version__}")
    
    
    use_default_matrix = st.toggle("Use default wr matrix")
    
    
    
    if use_default_matrix:
        st.write("""This dataframe has the required format for Excel file \r\n
Rows are the decks that you want to evaluate \r\n
Columns are the meta decks that you have info about its meta share \r\n
Overall column is required for each deck""")
        wr_matrix = DEFAULT_WR_MATRIX
    else:
        wr_matrix = None
        uploaded_file = st.file_uploader("Upload Excel file with winrate matrix")
        if uploaded_file is not None:
            # Can be used wherever a "file-like" object is accepted:
            wr_matrix = pd.read_excel(uploaded_file, index_col = 0, header = 0)
    
    if wr_matrix is not None:
            
        st.write(wr_matrix)
        
        if use_default_matrix:
            
            buffer = io.BytesIO()
            
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                wr_matrix.to_excel(writer, sheet_name='Sheet1')
                writer.close()

                st.download_button(
                    label="Download example wr matrix file",
                    data=buffer,
                    file_name="example_wr_matrix.xlsx",
                    mime="application/vnd.ms-excel",
                    type="primary",
                )

        meta_decks = list(wr_matrix.columns)[1:]
        meta_predictions = {}

        with st.sidebar:
            st.write("Fill your metagame prediction (0 to 100)")
            for deck in meta_decks:
                label = deck
                meta_predictions[label] = st.number_input(label, min_value=0.0, max_value=100.0, step = 0.1)

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

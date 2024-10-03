import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the dashboard
st.title("Dashboard Analisis Data: E-Commerce Public Dataset")

# Load your data
df = pd.read_csv('dashboard/filled_data.csv')  

# Display the questions
st.write("- **Pertanyaan 1:** Kategori produk mana yang memiliki rating tertinggi yang memiliki minimal 5% pesanan dari pesanan total")
st.write("- **Pertanyaan 2:** Kategori produk apa saja yang memiliki penjualan terendah")

# Display data
st.write("Data Overview")
st.dataframe(df.head())  # Show the first few rows of the dataframe

x = np.random.normal(15, 5, 250)
 
fig, ax = plt.subplots()
ax.hist(x=x, bins=15)
st.pyplot(fig) 
 
with st.expander("See explanation"):
    st.write(
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
        nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor 
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
        nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
        sunt in culpa qui officia deserunt mollit anim id est laborum.
        """
    )



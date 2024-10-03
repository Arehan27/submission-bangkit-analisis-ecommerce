import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the dashboard
st.title("Dashboard for Research Project")

# Load your data
df = pd.read_csv('dashboard/filled_data.csv')  # Update with your merged dataset path

st.write("Pertanyaan 1: Kategori produk mana yang memiliki rating tertinggi yang memiliki minimal 5% pesanan dari pesanan total")
st.write("Pertanyaan 2: Kategori produk apa saja yang memiliki penjualan terendah")

# Display data overview
st.write("Data Overview")
st.dataframe(df.head())  # Show the first few rows of the dataframe





# Function to show price analysis with enhanced visualization
def show_price_analysis(data):
    # Determine price range
    bins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    labels = ['0-1000', '1000-2000', '2000-3000', '3000-4000', '4000-5000', 
              '5000-6000', '6000-7000', '7000-8000', '8000-9000', '9000-10000']

    # Create a new column with price ranges
    data['price_range'] = pd.cut(data['price'], bins=bins, labels=labels, include_lowest=True)

    # Count products based on review scores for each price range
    review_stats = data.groupby(['price_range', 'review_score']).size().unstack(fill_value=0)

    # Reset index to include price_range in the DataFrame for better display
    review_stats = review_stats.reset_index()

    # Display the review statistics
    st.subheader("Jumlah Produk berdasarkan Rentang Harga dan Skor Ulasan")
    st.dataframe(review_stats)  # Display the review stats in the dashboard

    # Set Seaborn style and color palette
    sns.set(style='whitegrid')
    palette = sns.color_palette("coolwarm", as_cmap=True)

    # Enhanced visualization of price and review score using boxplot
    st.subheader("Hubungan antara Harga dan Skor Ulasan")
    plt.figure(figsize=(12, 6))
    
    # Customizing the boxplot
    sns.boxplot(
        x='review_score', 
        y='price', 
        data=data, 
        palette='coolwarm',   # Adding a color palette
        showfliers=False,     # Hiding outliers for clarity
        linewidth=1.5         # Line thickness
    )
    
    # Add titles and labels
    plt.title('Hubungan antara Harga dan Skor Ulasan', fontsize=18, fontweight='bold', color='#4C72B0')
    plt.xlabel('Skor Ulasan', fontsize=14)
    plt.ylabel('Harga', fontsize=14)
    
    # Customize the gridlines for better readability
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Display the enhanced plot in the Streamlit app
    st.pyplot(plt)

    # Optional: Clear the current figure for future plots
    plt.clf()


# Function to show average review score per price range (bar chart)
def show_average_review_score(data):
    # Determine price range
    bins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    labels = ['0-1000', '1000-2000', '2000-3000', '3000-4000', '4000-5000', 
              '5000-6000', '6000-7000', '7000-8000', '8000-9000', '9000-10000']

    # Add a new column with price ranges
    data['price_range'] = pd.cut(data['price'], bins=bins, labels=labels, right=False)

    # Calculate average review scores per price range
    average_reviews = data.groupby('price_range')['review_score'].mean().reset_index()

    # Create a bar plot for average review score
    plt.figure(figsize=(12, 6))

    sns.barplot(
        x='price_range', 
        y='review_score', 
        data=average_reviews, 
        palette='coolwarm'
    )

    # Add titles and labels
    plt.title('Rata-rata Skor Ulasan Berdasarkan Rentang Harga', fontsize=18, fontweight='bold', color='#4C72B0')
    plt.xlabel('Rentang Harga', fontsize=14)
    plt.ylabel('Rata-rata Skor Ulasan', fontsize=14)

    # Customize the gridlines for better readability
    plt.grid(True, linestyle='--', alpha=0.6)

    # Display the barplot in the Streamlit app
    st.pyplot(plt)

    # Optional: Clear the current figure for future plots
    plt.clf()

# Call the function to show price analysis
show_price_analysis(df)
show_average_review_score(df)

# Create a new expander for average review scores
with st.expander("Insight"):
    # Define price ranges
    bins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    labels = ['0-1000', '1000-2000', '2000-3000', '3000-4000', 
              '4000-5000', '5000-6000', '6000-7000', 
              '7000-8000', '8000-9000', '9000-10000']

    # Create a new column for price ranges
    df['price_range'] = pd.cut(df['price'], bins=bins, labels=labels, right=False)

    # Calculate average review scores per price range
    average_reviews = df.groupby('price_range')['review_score'].mean().reset_index()

    # Display the average review scores as a table
    st.write("Rata-rata skor ulasan per rentang harga:")
    st.dataframe(average_reviews)
    st.write(''' 
    - Sebagian besar produk (lebih dari 100 ribu produk) berada dalam rentang harga 0-1000. Ini menunjukkan bahwa produk dengan harga rendah mendominasi dalam dataset.
    - Meskipun jumlah produk di rentang harga lebih tinggi jauh lebih sedikit, skor ulasannya secara umum cenderung lebih positif dibandingkan produk dengan harga lebih rendah.
    ''')

st.subheader("Explorative Data Analysis")
st.markdown("<h4>Kategori produk mana yang memiliki rating tertinggi yang memiliki minimal 5% pesanan dari pesanan total ?</h4>", unsafe_allow_html=True)

def analyze_product_categories(data):
    # Menghitung rata-rata skor ulasan per kategori produk
    rata_rata_rating_per_kategori = data.groupby('product_category_name_english')['review_score'].mean().reset_index()

    # Menghitung jumlah produk yang terjual per kategori
    jumlah_penjualan_per_produk = data.groupby(['product_id', 'product_category_name_english']).size().reset_index(name='jumlah_penjualan')

    # Menghitung jumlah pesanan dan total pendapatan per kategori
    jumlah_penjualan_per_kategori = jumlah_penjualan_per_produk.groupby('product_category_name_english')['jumlah_penjualan'].sum().reset_index()
    jumlah_pendapatan_per_kategori = data.groupby('product_category_name_english')['price'].sum().reset_index(name='total_pendapatan')

    # Menggabungkan jumlah penjualan dengan total pendapatan
    ringkasan_kategori = pd.merge(jumlah_penjualan_per_kategori, jumlah_pendapatan_per_kategori, on='product_category_name_english')

    # Menggabungkan rata-rata rating dengan ringkasan kategori
    ringkasan_kategori = pd.merge(ringkasan_kategori, rata_rata_rating_per_kategori, on='product_category_name_english')

    # Menghitung ambang batas berdasarkan 5% dari total baris
    threshold = int(len(data) * 0.05)

    # Filter kategori dengan lebih dari ambang batas
    kategori_terfilter = ringkasan_kategori[ringkasan_kategori['jumlah_penjualan'] > threshold]

    # Menampilkan 10 kategori dengan penjualan dan rating tertinggi
    kategori_terfilter = kategori_terfilter.sort_values(by=['jumlah_penjualan', 'review_score'], ascending=False).head(10)

    # Membuat kategori rating
    def categorize_rating(rating):
        if rating < 3.90:
            return '< 3.90'
        elif 3.90 <= rating < 4.00:
            return '3.90 - 4.00'
        elif 4.00 <= rating < 4.10:
            return '4.00 - 4.10'
        elif 4.10 <= rating < 4.20:
            return '4.10 - 4.20'
        elif 4.20 <= rating < 4.30:
            return '4.20 - 4.30'
        else:
            return '>= 4.30'

    # Menerapkan fungsi kategori rating
    kategori_terfilter['rating_category'] = kategori_terfilter['review_score'].apply(categorize_rating)

    # Visualisasi: Grafik Batang Kategori Produk
    st.markdown("<h5>Kategori Produk dengan Penjualan dan Rating Tertinggi</h5>", unsafe_allow_html=True)
    
    # Set the figure size
    plt.figure(figsize=(12, 6))
    
    # Create a bar plot
    sns.barplot(data=kategori_terfilter, 
                 x='jumlah_penjualan', 
                 y='product_category_name_english', 
                 hue='rating_category',  # Menggunakan kategori rating untuk hue
                 palette='viridis')

    plt.title('Kategori Produk dengan Penjualan dan Rating Tertinggi (Minimal 5% dari Total Pesanan)')
    plt.xlabel('Jumlah Penjualan')
    plt.ylabel('Kategori Produk')
    plt.legend(title='Kategori Rating', bbox_to_anchor=(1.10, 1), loc='upper left')
    
    # Show the plot in Streamlit
    st.pyplot(plt)

    # Clear the current figure for future plots
    plt.clf()

# Membaca dataset
analyze_product_categories(df)

with st.expander("Insight"):
    st.write(
        "Kategori produk **health_beauty** yang memiliki rating tinggi dan jumlah pesanan di atas 5% total pesanan menunjukkan bahwa ada keunggulan dalam segmen pasar tertentu. "
        "Kategori ini kemungkinan memenuhi kebutuhan dan keinginan konsumen dengan baik."
    )
    
    st.write(
        "Dengan mengetahui kategori yang paling baik, perusahaan dapat menganalisis pesaing di kategori tersebut untuk memahami faktor-faktor yang berkontribusi pada kesuksesan dan rating tinggi produk."
    )

st.markdown("<h4>Kategori produk apa saja yang memiliki penjualan terendah ?</h4>", unsafe_allow_html=True)


def show_lowest_selling_products(df, num_products=10):
    # Menghitung jumlah produk yang terjual per kategori
    jumlah_penjualan_produk = df.groupby('product_category_name_english').size().reset_index(name='jumlah_penjualan')

    # Menambahkan kolom harga dan rating dengan menghitung rata-rata per kategori
    produk_terjual = df.groupby('product_category_name_english').agg({
        'price': 'mean',  # Mengambil harga rata-rata
        'review_score': 'mean'  # Mengambil rating rata-rata
    }).reset_index()

    # Menggabungkan data penjualan produk dengan informasi harga dan rating
    jumlah_penjualan_produk = pd.merge(jumlah_penjualan_produk, produk_terjual, on='product_category_name_english', how='left')

    # Mengidentifikasi kategori yang terdefinisi (tidak dalam format "Produk + angka")
    kategori_terdefinisi = jumlah_penjualan_produk[
        ~jumlah_penjualan_produk['product_category_name_english'].str.contains(r'Produk \d+', regex=True)
    ]

    # Menemukan kategori dengan penjualan terendah yang terdefinisi
    produk_berkategori = kategori_terdefinisi.nsmallest(num_products, 'jumlah_penjualan')

    # Menemukan kategori yang tidak terdefinisi
    produk_tidak_berkategori = jumlah_penjualan_produk[
        jumlah_penjualan_produk['product_category_name_english'].str.contains(r'Produk \d+', regex=True)
    ]

    # Mengambil sejumlah produk terendah untuk kategori tak terdefinisi
    produk_tidak_berkategori = produk_tidak_berkategori.nsmallest(num_products, 'jumlah_penjualan')

    st.markdown("<h5>Produk dengan Penjualan Terendah (Kategori Terdefinisi)</h5>", unsafe_allow_html=True)

    # Visualisasi untuk produk berkategori
    plt.figure(figsize=(12, 6))
    sns.barplot(data=produk_berkategori, 
                x='jumlah_penjualan', 
                y='product_category_name_english', 
                palette='Blues_d')

    plt.title('Produk dengan Penjualan Terendah (Kategori Terdefinisi)')
    plt.xlabel('Jumlah Penjualan')
    plt.ylabel('Kategori Produk')
    st.pyplot(plt)  # Display the plot in Streamlit
    plt.clf()  # Clear the current figure

    # Visualisasi untuk produk tanpa kategori
    plt.figure(figsize=(12, 6))
    sns.barplot(data=produk_tidak_berkategori, 
                x='jumlah_penjualan', 
                y='product_category_name_english', 
                palette='Reds_d')

    plt.title('Produk dengan Penjualan Terendah (Tanpa Kategori)')
    plt.xlabel('Jumlah Penjualan')
    plt.ylabel('Kategori Produk')
    st.pyplot(plt)  # Display the plot in Streamlit
    plt.clf()  # Clear the current figure


show_lowest_selling_products(df)

# Expander untuk Insight
with st.expander("Insight"):
    st.write("""
    - "Security and Services" dan "Fashion Children's Clothes" memiliki penjualan terendah dengan masing-masing 2 dan 8 unit terjual. Hal ini mungkin menunjukkan bahwa kategori-kategori ini kurang diminati oleh konsumen.
    - Kategori dengan penjualan lebih tinggi, seperti Home Comfort 2 dan Music, menunjukkan bahwa produk dalam kategori ini mungkin lebih relevan atau lebih dipromosikan dengan baik, sehingga bisa menjadi area yang bisa dikembangkan lebih lanjut.
    - Meskipun produk dalam kategori seperti Arts and Craftsmanship dan Fashion Sports memiliki penjualan yang lebih baik, harga rata-rata mereka (sekitar 75-70) dan rating yang baik (4.1 dan 4.3) menunjukkan bahwa konsumen bersedia membayar lebih untuk kategori-kategori ini.
    - Kategori Security and Services memiliki harga rata-rata tinggi (141.64) tetapi rating yang rendah (2.5), yang menunjukkan adanya masalah dengan produk atau layanan yang ditawarkan di kategori ini.
    - Banyak produk yang tidak memiliki kategori terdefinisi penjualannya sangat rendah, masing-masing hanya terjual satu unit. Ini menunjukkan bahwa produk-produk ini mungkin tidak dipromosikan dengan baik, kurang diminati konsumen, atau dikarenakan tidak mempunyai kategori spesifik sehingga hanya memiliki 1 pengelompokkan.
    """)

st.subheader("Conclution")

st.write("""
- **Kesimpulan Pertanyaan 1**  
Dari analisis yang dilakukan, termasuk penerapan RFM, kategori produk yang menunjukkan kombinasi terbaik antara rating dan jumlah penjualan adalah "health_beauty". Kategori ini tidak hanya memiliki rating tertinggi, tetapi juga volume penjualan yang signifikan. Oleh karena itu, fokus pada pengembangan produk dan strategi pemasaran dalam kategori ini dapat memberikan keuntungan jangka panjang dan meningkatkan loyalitas pelanggan.

- **Kesimpulan Pertanyaan 2**  
Dari analisis di atas, dapat disimpulkan bahwa kategori produk dengan penjualan terendah yang terdefinisi adalah "security_and_services" dengan hanya 2 penjualan, sedangkan produk tanpa kategori terdefinisi memiliki beberapa produk dengan satu penjualan. Hal ini menunjukkan bahwa ada peluang untuk meningkatkan strategi pemasaran dan pengembangan produk dalam kategori yang terdefinisi, terutama "security_and_services", untuk menarik lebih banyak konsumen. Selain itu, perhatian juga perlu diberikan pada produk tanpa kategori untuk memberikan identitas yang lebih jelas dan menarik bagi pelanggan, serta dapat lebih mudah untuk dikelompokkan.
""")

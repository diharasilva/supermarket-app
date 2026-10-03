import streamlit as st
import pandas as pd

st.title("🛒 Single Supermarket Inventory & Locator")
st.write("Welcome! This system manages supermarket stocks and indoor shelf locations.")

# Search Filter
search_term = st.text_input("Search for a product (e.g., Milk, Biscuit, Cola):")

# Sample Data matching Supabase
data = {
    "Product Name": ["Anchor Milk Powder 400g", "Munchee Lemon Puff", "Coca Cola 1.5L"],
    "Category / Section": ["Dairy & Milk", "Snacks & Biscuits", "Beverages & Drinks"],
    "Aisle Location": ["Aisle 1", "Aisle 2", "Aisle 3"],
    "Stock": [45, 120, 30],
    "Price (LKR)": [1250.00, 180.00, 450.00]
}
df = pd.DataFrame(data)

if search_term:
    filtered_df = df[df['Product Name'].str.contains(search_term, case=False, na=False)]
    st.subheader("Search Results:")
    st.dataframe(filtered_df)
    for index, row in filtered_df.iterrows():
        st.success(f"📍 **{row['Product Name']}** is located in **{row['Category / Section']} ({row['Aisle Location']})**.")
else:
    st.subheader("All Supermarket Products & Racks:")
    st.dataframe(df)

st.warning("⚠️ Low Stock Alert: Coca Cola 1.5L stock is running low (30 units left)!")

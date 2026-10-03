import streamlit as st
import pandas as pd

st.set_page_config(page_title="Supermarket Inventory System", page_icon="🛒", layout="wide")

st.title("🛒 Advanced Supermarket Inventory & Locator System")
st.write("Welcome! Manage stocks, prices, and indoor aisle locations in real-time.")

# Sidebar Navigation for Advanced Features
menu = st.sidebar.selectbox("Navigation", ["View & Search Inventory", "Add New Product", "Low Stock & Alerts"])

# Sample Data (Later can be fully linked with Supabase)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Product Name": ["Anchor Milk Powder 400g", "Munchee Lemon Puff", "Coca Cola 1.5L"],
        "Category / Section": ["Dairy & Milk", "Snacks & Biscuits", "Beverages & Drinks"],
        "Aisle Location": ["Aisle 1", "Aisle 2", "Aisle 3"],
        "Stock": [45, 120, 30],
        "Price (LKR)": [1250.00, 180.00, 450.00]
    })

if menu == "View & Search Inventory":
    st.subheader("📦 Inventory Search & Racks Locator")
    search_term = st.text_input("Search for a product (e.g., Milk, Biscuit, Cola):")
    
    if search_term:
        filtered_df = st.session_state.df[st.session_state.df['Product Name'].str.contains(search_term, case=False, na=False)]
        st.dataframe(filtered_df, use_container_width=True)
        for index, row in filtered_df.iterrows():
            st.success(f"📍 **{row['Product Name']}** is located in **{row['Category / Section']} ({row['Aisle Location']})**.")
    else:
        st.dataframe(st.session_state.df, use_container_width=True)

elif menu == "Add New Product":
    st.subheader("➕ Add a New Product to Inventory")
    with st.form("add_product_form"):
        prod_name = st.text_input("Product Name")
        category = st.selectbox("Category / Section", ["Dairy & Milk", "Snacks & Biscuits", "Beverages & Drinks", "Household", "Bakery"])
        aisle = st.text_input("Aisle Location (e.g., Aisle 4)")
        stock_qty = st.number_input("Stock Quantity", min_value=0, value=50)
        price = st.number_input("Unit Price (LKR)", min_value=0.0, value=100.0)
        
        submit_button = st.form_submit_button("Add Product")
        
        if submit_button and prod_name:
            new_row = pd.DataFrame({
                "Product Name": [prod_name],
                "Category / Section": [category],
                "Aisle Location": [aisle],
                "Stock": [stock_qty],
                "Price (LKR)": [price]
            })
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.success(f"Successfully added **{prod_name}** to the inventory!")

elif menu == "Low Stock & Alerts":
    st.subheader("⚠️ Stock Alerts & Management")
    low_stock_df = st.session_state.df[st.session_state.df['Stock'] < 40]
    
    if not low_stock_df.empty:
        st.warning("The following products are running low on stock:")
        st.dataframe(low_stock_df, use_container_width=True)
    else:
        st.success("All products have sufficient stock levels!")

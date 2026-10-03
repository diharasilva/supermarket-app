import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supermarket System & Locator", page_icon="🛒", layout="wide")

st.title("🛒 Supermarket Inventory & Interactive Indoor Map")
st.write("Manage inventory, track low stock, and navigate supermarket aisles interactively.")

# Sidebar Navigation
menu = st.sidebar.selectbox("Navigation", ["View & Search Inventory", "Add New Product", "Interactive Indoor Map & Racks", "Low Stock & Alerts"])

# Session State for Inventory & Layout
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Product Name": ["Anchor Milk Powder 400g", "Munchee Lemon Puff", "Coca Cola 1.5L", "Rio Ice Cream", "Sunlight Soap"],
        "Category / Section": ["Dairy & Milk", "Snacks & Biscuits", "Beverages", "Frozen Foods", "Household"],
        "Aisle Location": ["Aisle 1", "Aisle 2", "Aisle 3", "Aisle 4", "Aisle 5"],
        "Stock": [45, 120, 30, 15, 60],
        "Price (LKR)": [1250.00, 180.00, 450.00, 600.00, 140.00],
        "X_Coord": [2, 4, 6, 8, 10],  # Floor plan grid X position
        "Y_Coord": [5, 5, 5, 5, 5]   # Floor plan grid Y position
    })

if menu == "View & Search Inventory":
    st.subheader("📦 Inventory Search & Racks Locator")
    search_term = st.text_input("Search for a product (e.g., Milk, Biscuit, Soap):")
    
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
        category = st.selectbox("Category / Section", ["Dairy & Milk", "Snacks & Biscuits", "Beverages", "Frozen Foods", "Household"])
        aisle = st.text_input("Aisle Location (e.g., Aisle 6)")
        stock_qty = st.number_input("Stock Quantity", min_value=0, value=50)
        price = st.number_input("Unit Price (LKR)", min_value=0.0, value=100.0)
        x_c = st.slider("Floor Map X Coordinate", 1, 12, 6)
        y_c = st.slider("Floor Map Y Coordinate", 1, 10, 5)
        
        submit_button = st.form_submit_button("Add Product")
        
        if submit_button and prod_name:
            new_row = pd.DataFrame({
                "Product Name": [prod_name],
                "Category / Section": [category],
                "Aisle Location": [aisle],
                "Stock": [stock_qty],
                "Price (LKR)": [price],
                "X_Coord": [x_c],
                "Y_Coord": [y_c]
            })
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.success(f"Successfully added **{prod_name}** to the inventory and map!")

elif menu == "Interactive Indoor Map & Racks":
    st.subheader("🗺️ Supermarket 2D Floor Plan & Aisle Explorer")
    st.write("Click or hover over the rack points below to see what items are stocked in each aisle section.")
    
    # Plotly Scatter plot acting as an interactive floor map
    fig = px.scatter(
        st.session_state.df,
        x="X_Coord",
        y="Y_Coord",
        text="Aisle Location",
        color="Category / Section",
        hover_data=["Product Name", "Stock", "Price (LKR)"],
        size=[30]*len(st.session_state.df),
        title="Supermarket Floor Layout (Aisles & Racks)"
    )
    fig.update_traces(textposition='top center')
    fig.update_layout(xaxis_title="Store Width (meters)", yaxis_title="Store Length (meters)", height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
    selected_aisle = st.selectbox("Select Aisle to view details:", st.session_state.df['Aisle Location'].unique())
    aisle_items = st.session_state.df[st.session_state.df['Aisle Location'] == selected_aisle]
    st.info(f"Products available in **{selected_aisle}**:")
    st.dataframe(aisle_items, use_container_width=True)

elif menu == "Low Stock & Alerts":
    st.subheader("⚠️ Stock Alerts & Management")
    low_stock_df = st.session_state.df[st.session_state.df['Stock'] < 30]
    
    if not low_stock_df.empty:
        st.warning("The following products are running low on stock and need restocking:")
        st.dataframe(low_stock_df, use_container_width=True)
    else:
        st.success("All products have sufficient stock levels!")

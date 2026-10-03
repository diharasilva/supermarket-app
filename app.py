import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Supermarket System & Route Locator", page_icon="🛒", layout="wide")

st.title("🛒 Supermarket Inventory & Smart Indoor Route Locator")
st.write("Manage inventory, track stock, and find the shortest shopping route through aisles.")

# Navigation
menu = st.sidebar.selectbox("Navigation", ["View & Search Inventory", "Add New Product", "Smart Shopping Route (Shortest Path)", "Low Stock & Alerts"])

# Session State for Inventory
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Product Name": ["Anchor Milk Powder 400g", "Munchee Lemon Puff", "Coca Cola 1.5L", "Rio Ice Cream", "Sunlight Soap"],
        "Category / Section": ["Dairy & Milk", "Snacks & Biscuits", "Beverages", "Frozen Foods", "Household"],
        "Aisle Location": ["Aisle 1", "Aisle 2", "Aisle 3", "Aisle 4", "Aisle 5"],
        "Stock": [45, 120, 30, 15, 60],
        "Price (LKR)": [1250.00, 180.00, 450.00, 600.00, 140.00],
        "X_Coord": [2, 4, 6, 8, 10],  # Floor plan grid X
        "Y_Coord": [5, 2, 8, 3, 7]   # Floor plan grid Y
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

elif menu == "Smart Shopping Route (Shortest Path)":
    st.subheader("🛣️ Optimized Indoor Shopping Route (Nearest Neighbor Path)")
    st.write("Select the items you want to buy, and the system will plot the **shortest walking path** through the aisles!")
    
    selected_items = st.multiselect("Select items for your Shopping List:", st.session_state.df["Product Name"].tolist())
    
    if selected_items:
        # Filter selected items
        shopping_df = st.session_state.df[st.session_state.df["Product Name"].isin(selected_items)].copy()
        
        # Start at Entrance (0,0)
        route_x = [0]
        route_y = [0]
        route_labels = ["Entrance 🚪"]
        
        # Sort items by coordinate distance to simulate shortest path (Greedy Route Optimization)
        unvisited = shopping_df.to_dict('records')
        curr_x, curr_y = 0, 0
        
        while unvisited:
            # Find nearest item
            nearest = min(unvisited, key=lambda p: ((p['X_Coord']-curr_x)**2 + (p['Y_Coord']-curr_y)**2)**0.5)
            route_x.append(nearest['X_Coord'])
            route_y.append(nearest['Y_Coord'])
            route_labels.append(f"{nearest['Product Name']} ({nearest['Aisle Location']})")
            curr_x, curr_y = nearest['X_Coord'], nearest['Y_Coord']
            unvisited.remove(nearest)
            
        # Add Cashier / Exit (12, 10)
        route_x.append(12)
        route_y.append(10)
        route_labels.append("Billing & Exit 🛒")
        
        # Plot Route using Plotly
        fig = go.Figure()
        
        # Add Racks Background
        fig.add_trace(go.Scatter(
            x=st.session_state.df['X_Coord'], y=st.session_state.df['Y_Coord'],
            mode='markers+text',
            marker=dict(size=12, color='lightgrey'),
            text=st.session_state.df['Aisle Location'],
            textposition="top center",
            name="All Supermarket Racks"
        ))
        
        # Add Shortest Route Path Line
        fig.add_trace(go.Scatter(
            x=route_x, y=route_y,
            mode='lines+markers+text',
            line=dict(color='red', width=3, dash='dash'),
            marker=dict(size=16, color='blue'),
            text=route_labels,
            textposition="bottom center",
            name="Shortest Route Path"
        ))
        
        fig.update_layout(
            title="Optimized Walking Path for Shopping List",
            xaxis_title="Store Width (meters)",
            yaxis_title="Store Length (meters)",
            height=550
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.success("🧭 **Route Step-by-Step Order:** " + " ➡️ ".join(route_labels))
    else:
        st.info("Please select at least 1 item from the multiselect box above to generate your optimal route.")

elif menu == "Low Stock & Alerts":
    st.subheader("⚠️ Stock Alerts & Management")
    low_stock_df = st.session_state.df[st.session_state.df['Stock'] < 30]
    
    if not low_stock_df.empty:
        st.warning("The following products are running low on stock and need restocking:")
        st.dataframe(low_stock_df, use_container_width=True)
    else:
        st.success("All products have sufficient stock levels!")

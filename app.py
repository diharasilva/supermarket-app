import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import date

# 1. PWA Setup (Injected into Streamlit header)
pwa_header = """
<link rel="manifest" href="./manifest.json">
<meta name="theme-color" content="#1d4ed8">
<script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('./sw.js')
                .then(reg => console.log('Service Worker registered!'))
                .catch(err => console.log('Service Worker registration failed: ', err));
        });
    }
</script>
"""
components.html(pwa_header, height=0)

# 2. App Configuration
st.set_page_config(page_title="Dealz Super — Maharagama", page_icon="🛒", layout="wide")

# 3. Initial Inventory State
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "product_id": [1, 2, 3],
        "Item Name": ["Fresh Milk 1L (කිරි)", "White Bread (පාන්)", "Samba Rice 5kg (සම්බා හාල්)"],
        "Aisle": ["Aisle 2 - Dairy & Refrigerated", "Aisle 1 - Bakery", "Aisle 3 - Grocery & Rice"],
        "Barcode": ["4792011120016", "4792012345678", "4792098765432"],
        "Price (LKR)": [480.0, 320.0, 1450.0],
        "Stock Count": [25, 4, 40],
        "Reorder Level": [10, 5, 10],
        "Expiry Date": ["2026-10-25", "2026-10-12", "2027-05-15"],
        "Image": [
            "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=400&q=80"
        ]
    })

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {"order_id": 101, "customer_email": "perera.n@gmail.com", "items": "Fresh Milk 1L (x2)", "total_lkr": 960.0, "status": "Pending Pickup"},
        {"order_id": 102, "customer_email": "kumari.s@yahoo.com", "items": "Samba Rice 5kg (x1)", "total_lkr": 1450.0, "status": "Ready for Delivery"}
    ]

# 4. Navigation & Header
st.title("🛒 Dealz Super — Maharagama")
st.caption("භාණ්ඩ කළමනාකරණ සහ පාරිභෝගික පද්ධති ද්වාරය (Supermarket Management & Customer Portal)")

# Sidebar Role Switcher
st.sidebar.markdown("# ⚙️ Portal Navigation")
role = st.sidebar.radio("Select Role / කාර්යභාරය තෝරන්න", ["👤 Customer View (පාරිභෝගිකයා)", "🔒 Store Owner Dashboard (ගබඩා හිමියා)"])
st.sidebar.markdown("---")
st.sidebar.info("💡 PWA features, offline caching, and live inventory sync enabled.")

# ==================== CUSTOMER VIEW ====================
if role == "👤 Customer View (පාරිභෝගිකයා)":
    st.subheader("🛍️ Available Supermarket Products")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("🛒 Checkout & Send Email Bill", use_container_width=True):
            st.success("✅ Order placed successfully! Digital invoice sent to your email.")
    with col_btn2:
        if st.button("📍 Simulate 2km Geofence Offer", use_container_width=True):
            st.info("📍 Geofence Alert: 'Welcome near Maharagama! Flash Deal: Get 10% off Fresh Milk today!'")
    with col_btn3:
        if st.button("🔄 Refresh Catalog", use_container_width=True):
            st.rerun()

    st.markdown("---")
    
    # Display Product Grid Cards
    cols = st.columns(3)
    for index, row in st.session_state.inventory.iterrows():
        with cols[index % 3]:
            st.image(row["Image"], use_column_width=True)
            st.caption(f"📍 {row['Aisle']}")
            st.markdown(f"### **{row['Item Name']}**")
            st.write(f"Barcode: `{row['Barcode']}`")
            st.markdown(f"**LKR {row['Price (LKR)']:.2f}**")
            
            if row["Stock Count"] > row["Reorder Level"]:
                st.success(f"In Stock ({row['Stock Count']})")
            else:
                st.error(f"Low Stock ({row['Stock Count']})")
                
            if st.button(f"Add to Cart 🛒", key=f"cust_buy_{row['product_id']}"):
                st.toast(f"Added {row['Item Name']} to your pickup order!")

# ==================== STORE OWNER DASHBOARD ====================
elif role == "🔒 Store Owner Dashboard (ගබඩා හිමියා)":
    st.subheader("🔒 Store Owner Access Restricted")
    password = st.text_input("Enter Administrative Password (e.g., admin123)", type="password")
    
    if password == "admin123" or password == "admin":
        st.success("Administrative Access Granted!")
        
        tab1, tab2, tab3 = st.tabs(["📦 Inventory Control", "➕ Add Product", "📋 Customer Online Orders"])
        
        with tab1:
            st.markdown("### Live Inventory Status & Expiry Checks")
            today_str = str(date.today())
            
            for index, row in st.session_state.inventory.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                with col1:
                    st.write(f"**{row['Item Name']}**")
                    st.caption(f"Aisle: {row['Aisle']}")
                with col2:
                    if row["Stock Count"] <= row["Reorder Level"]:
                        st.error(f"Stock: {row['Stock Count']} (Low)")
                    else:
                        st.success(f"Stock: {row['Stock Count']}")
                with col3:
                    if row["Expiry Date"] < today_str:
                        st.error(f"Expired: {row['Expiry Date']}")
                    else:
                        st.info(f"Exp: {row['Expiry Date']}")
                with col4:
                    st.write(f"LKR {row['Price (LKR)']:.2f}")
                with col5:
                    if st.button("Delete", key=f"del_prod_{row['product_id']}"):
                        st.session_state.inventory = st.session_state.inventory[st.session_state.inventory["product_id"] != row["product_id"]]
                        st.rerun()
                st.divider()

        with tab2:
            st.markdown("### Add New Product to Inventory")
            with st.form("add_product_form"):
                p_name = st.text_input("Product Name (Sinhala/English)")
                col_a, col_b = st.columns(2)
                with col_a:
                    aisle = st.text_input("Aisle Location", value="Aisle 4 - General")
                    barcode = st.text_input("Barcode", value="479200001111")
                    price = st.number_input("Price (LKR)", min_value=0.0, value=500.0)
                with col_b:
                    stock = st.number_input("Stock Count", min_value=1, value=20)
                    reorder = st.number_input("Reorder Level", min_value=1, value=5)
                    expiry = st.date_input("Expiry Date")
                
                img_url = st.text_input("Image URL", value="https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80")
                
                submitted = st.form_submit_button("Save Product to Database")
                if submitted:
                    new_id = int(st.session_state.inventory["product_id"].max() + 1) if not st.session_state.inventory.empty else 1
                    new_row = pd.DataFrame({
                        "product_id": [new_id],
                        "Item Name": [p_name],
                        "Aisle": [aisle],
                        "Barcode": [barcode],
                        "Price (LKR)": [float(price)],
                        "Stock Count": [int(stock)],
                        "Reorder Level": [int(reorder)],
                        "Expiry Date": [str(expiry)],
                        "Image": [img_url]
                    })
                    st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                    st.success(f"Successfully added {p_name}!")
                    st.rerun()

        with tab3:
            st.markdown("### Incoming Customer Orders (Pickup & Delivery)")
            df_orders = pd.DataFrame(st.session_state.orders)
            st.dataframe(df_orders, use_container_width=True)

    elif password != "":
        st.error("Incorrect password! Try 'admin123'")

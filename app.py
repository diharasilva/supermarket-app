import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import date

# 1. PWA Setup (Manifest & Service Worker)
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

# 2. Page Configuration
st.set_page_config(
    page_title="Dealz Super — Maharagama",
    page_icon="🛒",
    layout="wide"
)

# 3. Initial Session State Data (Matching all 6 System Modules)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "product_id": [1, 2, 3, 4],
        "Item Name": ["Fresh Milk 1L (කිරි)", "White Bread (පාන්)", "Samba Rice 5kg (සම්බා හාල්)", "Kotmale Yogurt 80g"],
        "Aisle": ["Aisle 2 - Dairy & Refrigerated", "Aisle 1 - Bakery", "Aisle 3 - Grocery & Rice", "Aisle 2 - Dairy & Refrigerated"],
        "Barcode": ["4792011120016", "4792012345678", "4792098765432", "4792011120054"],
        "Price (LKR)": [480.0, 320.0, 1450.0, 110.0],
        "Stock Count": [25, 3, 40, 12],
        "Reorder Level": [10, 5, 10, 15],
        "Expiry Date": ["2026-10-25", "2026-10-11", "2027-05-15", "2026-10-12"],
        "Image": [
            "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=400&q=80"
        ]
    })

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {"order_id": 101, "customer_email": "perera.n@gmail.com", "items": "Fresh Milk 1L (x2)", "total_lkr": 960.0, "status": "Pending Pickup"},
        {"order_id": 102, "customer_email": "kumari.s@yahoo.com", "items": "Samba Rice 5kg (x1)", "total_lkr": 1450.0, "status": "Ready for Delivery"}
    ]

if 'customers' not in st.session_state:
    st.session_state.customers = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "Customer Name": ["Nimal Perera", "Sanduni Kumari", "Kasun Bandara"],
        "Email": ["perera.n@gmail.com", "kumari.s@yahoo.com", "kasun.b@gmail.com"],
        "Birthday": ["1998-10-15", "2000-05-20", "1995-12-01"],
        "Total Annual Purchases (LKR)": [48500.0, 125000.0, 31000.0]  # Sanduni is Yearly Best Customer!
    })

if 'promotions' not in st.session_state:
    st.session_state.promotions = [
        {"promo_id": 1, "Title": "Fresh Milk Weekend Special", "Discount": "10% Off", "Status": "Active"},
        {"promo_id": 2, "Title": "Avurudu Special Grocery Deal", "Discount": "LKR 200 Off", "Status": "Scheduled"}
    ]

# 4. App Header & Sidebar Navigation
st.title("🛒 Dealz Super — Maharagama")
st.caption("Enterprise Supermarket PWA | පාරිභෝගික සහ ගබඩා කළමනාකරණ පද්ධතිය")

st.sidebar.markdown("# 🧭 Portal Navigation")
role = st.sidebar.radio("Select System Portal", ["👤 Customer Module", "🔒 Store Owner / Admin Module"])
st.sidebar.markdown("---")
st.sidebar.info("💡 Backend: MySQL Connected | PWA Caching Active")

# ==================== MODULE 1: CUSTOMER PORTAL ====================
if role == "👤 Customer Module":
    st.subheader("🛍️ Customer Web Portal & Shelf Locator")
    
    # Customer Simulation Action Triggers
    c_col1, c_col2, c_col3, c_col4 = st.columns(4)
    with c_col1:
        if st.button("🛒 Checkout & Email Bill", use_container_width=True):
            st.success("✅ Order placed! Digital invoice automatically emailed to your address.")
    with c_col2:
        if st.button("📍 Simulate 2km Geofence", use_container_width=True):
            st.info("📍 Geofence Alert (2km radius): 'Welcome near Maharagama! Enjoy 10% off Dairy products today!'")
    with c_col3:
        if st.button("🎂 Sim. Birthday Deal Email", use_container_width=True):
            st.balloons()
            st.success("🎉 Happy Birthday! A special LKR 500 discount voucher has been emailed to you.")
    with c_col4:
        if st.button("📧 Sim. Promo Newsletter", use_container_width=True):
            st.info("📩 Weekly Deals & Supermarket Promotions broadcasted to your inbox.")

    st.markdown("---")
    st.subheader("📦 Available Products & Shelf Locator")
    
    # Search & Aisle filter
    search_query = st.text_input("🔍 Search product name or check aisle location...", "")
    
    # Filter products based on search
    df_filtered = st.session_state.inventory
    if search_query:
        df_filtered = df_filtered[df_filtered['Item Name'].str.contains(search_query, case=False) | df_filtered['Aisle'].str.contains(search_query, case=False)]

    # Display product catalog grid with Shelf Locator details
    cols = st.columns(3)
    for index, row in df_filtered.iterrows():
        with cols[index % 3]:
            st.image(row["Image"], use_column_width=True)
            st.caption(f"📍 **Store Location:** {row['Aisle']}")
            st.markdown(f"### **{row['Item Name']}**")
            st.write(f"Barcode: `{row['Barcode']}`")
            st.markdown(f"**LKR {row['Price (LKR)']:.2f}**")
            
            # Stock Availability Check for Customer
            if row["Stock Count"] > row["Reorder Level"]:
                st.success(f"In Stock ({row['Stock Count']} units available)")
            elif row["Stock Count"] > 0:
                st.warning(f"Low Stock ({row['Stock Count']} units left)")
            else:
                st.error("Out of Stock")
                
            if st.button(f"Add to Cart 🛒", key=f"cust_buy_{row['product_id']}"):
                st.toast(f"Added {row['Item Name']} to your online order cart!")

# ==================== MODULE 2: STORE OWNER / ADMIN PORTAL ====================
elif role == "🔒 Store Owner / Admin Module":
    st.subheader("🔒 Store Owner & Management Control Center")
    password = st.text_input("Enter Admin Security Password (Try: admin123)", type="password")
    
    if password == "admin123" or password == "admin":
        st.success("Secure Administrative Access Granted!")
        
        # Tabs covering all Owner requirements
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📦 Stock & Expiry Control", 
            "➕ Add/Manage Products", 
            "🏆 Loyalty & Best Customer", 
            "🏷️ Manage Promotions", 
            "📋 View Online Orders"
        ])
        
        # TAB 1: Stock Count, Availability & Expiry Monitoring
        with tab1:
            st.markdown("### 📊 Real-Time Inventory, Stock Levels & Expiry Tracking")
            today_str = str(date.today())
            
            for index, row in st.session_state.inventory.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                with col1:
                    st.write(f"**{row['Item Name']}**")
                    st.caption(f"Location: {row['Aisle']}")
                with col2:
                    if row["Stock Count"] <= row["Reorder Level"]:
                        st.error(f"Stock: {row['Stock Count']} (Low!)")
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
                    if st.button("Delete", key=f"owner_del_{row['product_id']}"):
                        st.session_state.inventory = st.session_state.inventory[st.session_state.inventory["product_id"] != row["product_id"]]
                        st.rerun()
                st.divider()

        # TAB 2: Add New Product
        with tab2:
            st.markdown("### ➕ Add New Supermarket Product to Database")
            with st.form("owner_add_form"):
                p_name = st.text_input("Product Name")
                col_a, col_b = st.columns(2)
                with col_a:
                    aisle = st.text_input("Aisle & Shelf Location", value="Aisle 4 - Household")
                    barcode = st.text_input("Barcode Number", value="479200009999")
                    price = st.number_input("Unit Price (LKR)", min_value=0.0, value=350.0)
                with col_b:
                    stock = st.number_input("Initial Stock Count", min_value=1, value=30)
                    reorder = st.number_input("Reorder Warning Level", min_value=1, value=10)
                    expiry = st.date_input("Product Expiry Date")
                
                img_url = st.text_input("Product Image URL", value="https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80")
                
                submitted = st.form_submit_button("Save Product to MySQL DB")
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
                    st.success(f"Successfully added {p_name} to database!")
                    st.rerun()

        # TAB 3: Yearly Best Customer & Loyalty Rewards
        with tab3:
            st.markdown("### 🏆 Customer Loyalty & Yearly Best Customer Identification")
            st.info("🌟 The system automatically analyzes total annual customer purchases to determine the **Yearly Best Customer** for exclusive rewards and special promotion grants.")
            
            # Identify Best Customer
            best_customer = st.session_state.customers.loc[st.session_state.customers["Total Annual Purchases (LKR)"].idxmax()]
            
            st.success(f"👑 **Yearly Best Customer Identified:** {best_customer['CustomerName']} ({best_customer['Email']}) — **Total Spent:** LKR {best_customer['Total Annual Purchases (LKR)']:.2f}")
            
            if st.button("🎁 Send Special VIP Reward & Promotion to Best Customer"):
                st.balloons()
                st.success(f"Successfully sent a special VIP 20% discount voucher via email to {best_customer['CustomerName']}!")

            st.markdown("#### Registered Customers List")
            st.dataframe(st.session_state.customers, use_container_width=True)

        # TAB 4: Manage Promotions & Deals
        with tab4:
            st.markdown("### 🏷️ Create and Manage Active Promotions & Deals")
            with st.form("promo_form"):
                p_title = st.text_input("Promotion Title / Campaign Name", value="Special Weekend Discount")
                p_discount = st.text_input("Offer Details / Discount", value="15% Off on All Beverages")
                p_status = st.selectbox("Status", ["Active", "Scheduled", "Expired"])
                
                promo_submit = st.form_submit_button("Publish Promotion & Broadcast Email")
                if promo_submit:
                    new_promo = {"promo_id": len(st.session_state.promotions)+1, "Title": p_title, "Discount": p_discount, "Status": p_status}
                    st.session_state.promotions.append(new_promo)
                    st.success(f"Promotion '{p_title}' created successfully and broadcasted via email system!")
            
            st.markdown("#### Active Store Promotions")
            st.dataframe(pd.DataFrame(st.session_state.promotions), use_container_width=True)

        # TAB 5: View Online Orders
        with tab5:
            st.markdown("### 📋 View and Manage Customer Online Orders")
            st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)

    elif password != "":
        st.error("Incorrect password! Please enter 'admin123'.")

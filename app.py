import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# 1. PWA Setup
pwa_header = """
<link rel="manifest" href="./manifest.json">
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
st.set_page_config(page_title="3D Supermarket Navigator", page_icon="🛒", layout="wide")

# 3. Initial Inventory State (Sample Data)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Item Name": ["Milk (කිරි)", "Bread (පාන්)", "Rice (හාල්)", "Apples (ඇපල්)", "Paracetamol (පැරසිටමෝල්)"],
        "Section": ["Grocery", "Bakery", "Grocery", "Grocery", "Pharmacy"],
        "Stock Count": [12, 3, 45, 8, 2], # 3 and 2 are low stock items (< 5)
        "Price (LKR)": [350.0, 220.0, 3200.0, 600.0, 50.0]
    })

# 4. Sidebar Controls & Role Access
st.sidebar.header("🔐 පරිශීලක ප්‍රවේශය (Access Control)")
user_role = st.sidebar.radio("ඔබ කවුද?", ["Customer (පාරිභෝගිකයා)", "Store Owner (ගබඩා හිමියා)"])

is_owner_authenticated = False

if user_role == "Store Owner (ගබඩා හිමියා)":
    owner_password = st.sidebar.text_input("මුරපදය ඇතුළත් කරන්න (Password):", type="password")
    if owner_password == "admin123":
        is_owner_authenticated = True
        st.sidebar.success("🔑 ප්‍රවේශය සාර්ථකයි!")
    elif owner_password != "":
        st.sidebar.error("❌ වැරදි මුරපදයකි!")

st.title("🛒 3D Supermarket Indoor Navigator")

# 5. Store Owner Interface
if user_role == "Store Owner (ගබඩා හිමියා)":
    if not is_owner_authenticated:
        st.error("🔒 මෙම පාලක පුවරුවට පිවිසීමට ගබඩා හිමියාගේ නිවැරදි මුරපදය ඇතුළත් කරන්න.")
        st.info("💡 මුරපදය: admin123")
    else:
        st.markdown("## 🛠️ Store Owner Dashboard")
        st.markdown("---")
        
        # Summary Metrics
        total_items = len(st.session_state.inventory)
        low_stock_df = st.session_state.inventory[st.session_state.inventory["Stock Count"] < 5]
        low_stock_count = len(low_stock_df)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("සම්පූර්ණ භාණ්ඩ වර්ග (Total Items)", total_items)
        col2.metric("අඩු තොග සහිත භාණ්ඩ (Low Stock Items)", low_stock_count, delta_color="inverse")
        col3.metric("පද්ධති තත්ත්වය (System Status)", "Active")
        
        # Low Stock Alert Banner
        if low_stock_count > 0:
            st.warning(f"⚠️ **අනතුරු ඇඟවීමයි:** තොග ප්‍රමාණය 5ට වඩා අඩු භාණ්ඩ {low_stock_count}ක් පවතී. කරුණාකර තොග නැවත පිරවීමට කටයුතු කරන්න!")
        
        # Section 1: Add New Item
        st.markdown("### ➕ 1. නව භාණ්ඩයක් ඇතුළත් කිරීම (Add New Item)")
        with st.form("add_item_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                new_name = st.text_input("භාණ්ඩයේ නම (Item Name)")
                new_sec = st.selectbox("අදාළ අංශය (Section)", ["Grocery", "Bakery", "Pharmacy"])
            with col_b:
                new_stock = st.number_input("තොග ප්‍රමාණය (Stock Quantity)", min_value=0, value=10, step=1)
                new_price = st.number_input("එකක මිල - LKR (Unit Price)", min_value=0.0, value=100.0, step=10.0)
            
            submit_btn = st.form_submit_button("➕ භාණ්ඩය පද්ධතියට එකතු කරන්න")
            
            if submit_btn:
                if new_name.strip() != "":
                    new_item = pd.DataFrame({
                        "Item Name": [new_name],
                        "Section": [new_sec],
                        "Stock Count": [int(new_stock)],
                        "Price (LKR)": [float(new_price)]
                    })
                    st.session_state.inventory = pd.concat([st.session_state.inventory, new_item], ignore_index=True)
                    st.success(f"✅ '{new_name}' සාර්ථකව පද්ධතියට එකතු කරන ලදී!")
                    st.rerun()
                else:
                    st.error("කරුණාකර භාණ්ඩයේ නම ඇතුළත් කරන්න.")
        
        # Section 2: Inventory Management Table
        st.markdown("---")
        st.markdown("### 📦 2. වත්මන් තොග වාර්තාව සහ පාලනය (Inventory Management)")
        
        # Highlight logic for Low Stock
        def style_low_stock(val):
            if val < 5:
                return 'background-color: #ffcccc; color: red; font-weight: bold;'
            return ''
        
        st.dataframe(
            st.session_state.inventory.style.applymap(style_low_stock, subset=['Stock Count']),
            use_container_width=True
        )

# 6. Customer View
else:
    st.sidebar.markdown("---")
    st.sidebar.header("📍 Navigation & Controls")
    selected_section = st.sidebar.selectbox("Section එක තෝරන්න:", ["Overview (සියල්ල)", "Grocery Section", "Bakery Items", "Pharmacy & Health"])
    
    st.sidebar.subheader("⚡ Shortest Path (කෙටිම මාර්ගය)")
    item_to_find = st.sidebar.selectbox("භාණ්ඩයක් තෝරන්න:", st.session_state.inventory["Item Name"].tolist())
    find_path_btn = st.sidebar.button("මාර්ගය සොයන්න")
    
    st.markdown(f"### 📍 දැනට නරඹන්නේ: {selected_section}")
    
    if find_path_btn:
        st.success(f"🚀 **{item_to_find}** වෙත ළඟ වීමට කෙටිම මාර්ගය: ප්‍රධාන පිවිසුමේ සිට කෙළින්ම ගොස් වමට හැරෙන්න.")
    
    st.markdown("#### 📋 පවතින භාණ්ඩ ලැයිස්තුව:")
    st.table(st.session_state.inventory[["Item Name", "Section", "Price (LKR)"]])

# 7. Map Placeholder
st.markdown("---")
st.markdown("### 🗺️ 3D Supermarket Map")
st.warning("⚠️ ArcGIS 3D Web Scene එක ලැබ් එකෙන් Publish කළ පසු මෙතැන සජීවීව පෙන්වනු ඇත.")

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

# 3. Sample Inventory Data Initialization
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Item Name": ["Milk (කිරි)", "Bread (පාන්)", "Rice (හාල්)", "Apples (ඇපල්)", "Paracetamol (පැරසිටමෝල්)"],
        "Section": ["Grocery", "Bakery", "Grocery", "Grocery", "Pharmacy"],
        "Stock Count": [12, 3, 45, 8, 2], # Low stock items included (< 5)
        "Price (LKR)": [350, 220, 3200, 600, 50]
    })

# 4. Role Selection & Password Protection
st.sidebar.header("🔐 පරිශීලක ප්‍රවේශය (Access Control)")
user_role = st.sidebar.radio("ඔබ කවුද?", ["Customer (පාරිභෝගිකයා)", "Store Owner (ගබඩා හිමියා)"])

is_owner_authenticated = False

if user_role == "Store Owner (ගබඩා හිමියා)":
    owner_password = st.sidebar.text_input("මුරපදය ඇතුළත් කරන්න (Password):", type="password")
    
    # Password Validation (Default Password: admin123)
    if owner_password == "admin123":
        is_owner_authenticated = True
        st.sidebar.success("🔑 ප්‍රවේශය සාර්ථකයි!")
    else:
        st.sidebar.warning("⚠️ කරුණාකර නිවැරදි මුරපදය ඇතුළත් කරන්න.")

st.title("🛒 3D Supermarket Indoor Navigator & Shortest Path")

# 5. Sidebar Navigation Controls
st.sidebar.markdown("---")
st.sidebar.header("📍 Navigation & Controls")

selected_section = st.sidebar.selectbox(
    "Supermarket Section එක තෝරන්න:",
    ["Overview (සියල්ල)", "Grocery Section", "Bakery Items", "Pharmacy & Health", "Cashier Counters"]
)

# Shortest Path Feature
st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Shortest Path (කෙටිම මාර්ගය)")
item_to_find = st.sidebar.selectbox("භාණ්ඩයක් සඳහා කෙටිම මාර්ගය සොයන්න:", st.session_state.inventory["Item Name"].tolist())
find_path_btn = st.sidebar.button("මාර්ගය පෙන්වන්න")

# 6. Main Content Display Logic
if user_role == "Store Owner (ගබඩා හිමියා)":
    if not is_owner_authenticated:
        st.error("🔒 මෙම කොටසට ප්‍රවේශ වීමට ගබඩා හිමියාගේ නිවැරදි මුරපදය (Password) ඇතුළත් කරන්න.")
        st.info("💡 සාමාන්‍ය පාරිභෝගිකයින් සඳහා වම්පස සයිඩ්බාර් එකෙන් 'Customer (පාරිභෝගිකයා)' තෝරන්න.")
    else:
        st.markdown("### 🛠️ Store Owner Dashboard")
        st.info("ගබඩා හිමියා සඳහා වූ පාලක පුවරුව: නව භාණ්ඩ ඇතුළත් කිරීම සහ තොග කළමනාකරණය.")
        
        # Add New Item Form
        with st.expander("➕ නව භාණ්ඩයක් එකතු කරන්න (Add New Item)"):
            with st.form("add_item_form"):
                new_name = st.text_input("භාණ්ඩයේ නම")
                new_sec = st.selectbox("Section එක", ["Grocery", "Bakery", "Pharmacy"])
                new_stock = st.number_input("තොග ප්‍රමාණය (Stock)", min_value=0, value=10)
                new_price = st.number_input("මිල (LKR)", min_value=0.0, value=100.0)
                submit_item = st.form_submit_button("භාණ්ඩය ඇතුළත් කරන්න")
                
                if submit_item and new_name:
                    new_row = pd.DataFrame({"Item Name": [new_name], "Section": [new_sec], "Stock Count": [new_stock], "Price (LKR)": [new_price]})
                    st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                    st.success(f"'{new_name}' සාර්ථකව එකතු කරන ලදී!")

        # Inventory Table & Low Stock Highlight
        st.markdown("#### 📦 වත්මන් තොග තත්ත්වය (Inventory & Low Stock Alert)")
        
        def highlight_low_stock(val):
            color = 'red' if val < 5 else 'black'
            return f'color: {color}; font-weight: bold;'
        
        st.dataframe(st.session_state.inventory.style.applymap(highlight_low_stock, subset=['Stock Count']))

else:
    # Customer View Logic
    st.subheader(f"📍 දැනට නරඹන ප්‍රදේශය: {selected_section}")
    
    if find_path_btn:
        st.success(f"🚀 **{item_to_find}** වෙත ළඟ වීමට කෙටිම මාර්ගය: ප්‍රධාන පිවිසුමේ සිට කෙළින්ම ගොස් වමට හැරෙන්න (Approx: 15 meters).")
    
    st.markdown("### 📋 මෙම අංශයේ ඇති ප්‍රධාන භාණ්ඩ:")
    filtered_items = st.session_state.inventory[st.session_state.inventory['Section'].str.contains(selected_section.split()[0], case=False, na=False)]
    
    if not filtered_items.empty:
        st.table(filtered_items[["Item Name", "Price (LKR)"]])
    else:
        st.table(st.session_state.inventory[["Item Name", "Section", "Price (LKR)"]])

# 7. Map Placeholder
st.markdown("---")
st.markdown("### 🗺️ 3D Supermarket Map")
st.warning("⚠️ ArcGIS 3D Web Scene එක ලැබ් එකෙන් Publish කිරීමෙන් පසු මෙතැන සජීවීව දර්ශනය වනු ඇත.")

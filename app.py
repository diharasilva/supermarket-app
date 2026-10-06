import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math

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
        "Item Name": [
            "Fresh Milk 1L (එළකිරි)", 
            "White Bread (පාන්)", 
            "Samba Rice 5kg (සම්බා හාල්)", 
            "Red Apples 1kg (ඇපල්)", 
            "Paracetamol 500mg (පැරසිටමෝල්)",
            "Cheddar Cheese 200g (චීස්)"
        ],
        "Section": ["Grocery", "Bakery", "Grocery", "Grocery", "Pharmacy", "Grocery"],
        "Stock Count": [3, 2, 50, 15, 4, 1],
        "Price (LKR)": [480.0, 190.0, 1450.0, 1200.0, 50.0, 950.0]
    })

if 'cart' not in st.session_state:
    st.session_state.cart = []

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

st.title("🛒 3D Supermarket Indoor Navigator & GPS Delivery")

# 5. Store Owner Interface
if user_role == "Store Owner (ගබඩා හිමියා)":
    if not is_owner_authenticated:
        st.error("🔒 මෙම පාලක පුවරුවට පිවිසීමට ගබඩා හිමියාගේ නිවැරදි මුරපදය ඇතුළත් කරන්න.")
        st.info("💡 මුරපදය: admin123")
    else:
        st.markdown("## 🛠️ Store Owner Dashboard")
        st.markdown("---")
        total_items = len(st.session_state.inventory)
        low_stock_count = len(st.session_state.inventory[st.session_state.inventory["Stock Count"] < 5])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("සම්පූර්ණ භාණ්ඩ වර්ග", total_items)
        col2.metric("අඩු තොග සහිත භාණ්ඩ", low_stock_count)
        col3.metric("තත්ත්වය", "Active")
        
        if low_stock_count > 0:
            st.warning(f"⚠️ තොග ප්‍රමාණය 5ට වඩා අඩු භාණ්ඩ {low_stock_count}ක් පවතී!")
        
        st.markdown("### ➕ නව භාණ්ඩයක් ඇතුළත් කිරීම")
        with st.form("add_item_form", clear_on_submit=True):
            new_name = st.text_input("භාණ්ඩයේ නම")
            new_sec = st.selectbox("අංශය", ["Grocery", "Bakery", "Pharmacy"])
            new_stock = st.number_input("තොග ප්‍රමාණය", min_value=0, value=10)
            new_price = st.number_input("මිල (LKR)", min_value=0.0, value=100.0)
            if st.form_submit_button("ඇතුළත් කරන්න") and new_name:
                new_row = pd.DataFrame({"Item Name": [new_name], "Section": [new_sec], "Stock Count": [new_stock], "Price (LKR)": [new_price]})
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                st.success(f"'{new_name}' එකතු කරන ලදී!")
                st.rerun()
                
        st.markdown("### 📦 වත්මන් තොග වාර්තාව")
        st.dataframe(st.session_state.inventory, use_container_width=True)

# 6. Customer View with GPS Location Checker
else:
    st.sidebar.markdown("---")
    st.sidebar.header("📍 Navigation & Controls")
    selected_section = st.sidebar.selectbox("Section එක තෝරන්න:", ["Overview (සියල්ල)", "Grocery Section", "Bakery Items", "Pharmacy & Health"])
    
    st.markdown(f"### 📍 දැනට නරඹන්නේ: {selected_section}")
    
    # Filtering items
    if selected_section == "Grocery Section":
        filtered_df = st.session_state.inventory[st.session_state.inventory["Section"] == "Grocery"]
    elif selected_section == "Bakery Items":
        filtered_df = st.session_state.inventory[st.session_state.inventory["Section"] == "Bakery"]
    elif selected_section == "Pharmacy & Health":
        filtered_df = st.session_state.inventory[st.session_state.inventory["Section"] == "Pharmacy"]
    else:
        filtered_df = st.session_state.inventory
        
    st.markdown("#### 📋 ඇණවුම් කිරීම සඳහා භාණ්ඩ තෝරන්න:")
    c1, c2 = st.columns([2, 1])
    with c1:
        sel_item = st.selectbox("භාණ්ඩය:", filtered_df["Item Name"].tolist())
    with c2:
        sel_qty = st.number_input("ප්‍රමාණය", min_value=1, value=1)
        
    if st.button("🛒 කරත්තයට එකතු කරන්න"):
        row = st.session_state.inventory[st.session_state.inventory["Item Name"] == sel_item].iloc[0]
        price = row["Price (LKR)"]
        st.session_state.cart.append({"Item": sel_item, "Qty": sel_qty, "Price": price, "Total": price * sel_qty})
        st.success(f"'{sel_item}' කරත්තයට එකතු විය!")

    if len(st.session_state.cart) > 0:
        st.markdown("---")
        st.markdown("### 🛍️ ඔබේ කරත්තය (Cart)")
        cart_df = pd.DataFrame(st.session_state.cart)
        st.table(cart_df)
        total_bill = cart_df["Total"].sum()
        st.markdown(f"#### 💰 භාණ්ඩවල මුළු මිල: LKR {total_bill:.2f}")
        
        st.markdown("### 🛰️ දුර පරීක්ෂා කිරීම")
        st.info("💡 පහත බොත්තම ක්ලික් කර ඔබේ ජංගම දුරකථනයේ GPS පිහිටීම ලබා දෙන්න.")

        # JavaScript Geolocation Component
        location_code = """
        <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; text-align: center;">
            <button onclick="getLocation()" style="background-color: #ff4b4b; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">📍 මගේ GPS පිහිටීම ලබා ගන්න</button>
            <p id="demo" style="margin-top: 10px; font-weight: bold;"></p>
        </div>
        
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, showError);
            } else {
                document.getElementById("demo").innerHTML = "Geolocation මෙම බ්‍රව්සරය මඟින් ක්‍රියාත්මක නොවේ.";
            }
        }

        function showPosition(position) {
            let lat = position.coords.latitude;
            let lon = position.coords.longitude;
            
            let storeLat = 7.2906; 
            let storeLon = 80.6337;
            
            let R = 6371; 
            let dLat = deg2rad(lat - storeLat);
            let dLon = deg2rad(lon - storeLon);
            let a = 
                Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(deg2rad(storeLat)) * Math.cos(deg2rad(lat)) * 
                Math.sin(dLon/2) * Math.sin(dLon/2); 
            let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
            let distance = R * c; 
            
            document.getElementById("demo").innerHTML = "📍 ඔබේ නිවස සහ සුපිරි වෙළඳපොළ අතර දුර: " + distance.toFixed(2) + " km";
        }

        function showError(error) {
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    document.getElementById("demo").innerHTML = "⚠️ පරිශීලකයා Location අවසරය ප්‍රතික්ෂේප කළේය.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    document.getElementById("demo").innerHTML = "⚠️ Location තොරතුරු ලබාගත නොහැක.";
                    break;
                case error.TIMEOUT:
                    document.getElementById("demo").innerHTML = "⚠️ ඉල්ලීම කල් ඉකුත් විය.";
                    break;
            }
        }

        function deg2rad(deg) {
            return deg * (Math.PI / 180);
        }
        </script>
        """
        components.html(location_code, height=120)
        
        customer_distance = st.number_input("ගණනය වූ දුර (km) මෙහි සටහන් කරන්න:", min_value=0.0, value=2.0, step=0.1)
        
        if customer_distance <= 3.0:
            st.success("🎉 ඔබ කිලෝමීටර් 3ක අරය තුළ සිටින නිසා **නොමිලේ බෙදාහැරීම (Free Delivery)** හිමි වේ!")
            final_delivery_fee = 0.0
        else:
            final_delivery_fee = 150.0 + ((customer_distance - 3.0) * 50.0)
            st.warning(f"⚠️ ඔබ කිලෝමීටර් 3 සීමාවෙන් ඔබ්බෙහි සිටී. බෙදාහැරීමේ ගාස්තුව: LKR {final_delivery_fee:.2f}")
            
        grand_total = total_bill + final_delivery_fee
        
        # Fixed syntax error line using proper f-string and quoted text
        st.info(f"ක්ෂණික ගෙවීම් සාරාංශය: භාණ්ඩවල මිල = LKR {total_bill:.2f} | ඩෙලිවරි ගාස්තුව = LKR {final_delivery_fee:.2f} | **මුළු ගෙවිය යුතු මුදල = LKR {grand_total:.2f}**")
        
        if st.button("✅ ඇණවුම තහවුරු කරන්න"):
            st.balloons()
            st.success("🎉 ඇණවුම සාර්ථකයි! ගබඩා හිමියා වෙත යවන ලදී.")
            st.session_state.cart = []
    else:
        st.info("🛒 ඔබේ කරත්තය හිස්ය.")

    st.markdown("#### 📋 පවතින භාණ්ඩ ලැයිස්තුව:")
    st.table(filtered_df[["Item Name", "Section", "Price (LKR)"]])

# 7. Map Placeholder
st.markdown("---")
st.markdown("### 🗺️ 3D Supermarket Map")
st.warning("⚠️ ArcGIS 3D Web Scene එක ලැබ් එකෙන් Publish කළ පසු මෙතැන සජීවීව පෙන්වනු ඇත.")

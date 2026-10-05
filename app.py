import streamlit as st
import streamlit.components.v1 as components

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

# 2. App Title & Layout Config
st.set_page_config(page_title="3D Supermarket Navigator", page_icon="🛒", layout="wide")
st.title("🛒 3D Supermarket Indoor Navigator")

# 3. Sidebar Controls (සයිඩ්බාර් එක සෑදීම)
st.sidebar.header("📍 Navigation & Controls")

# Supermarket Sections Selectbox
selected_section = st.sidebar.selectbox(
    "Supermarket Section එක තෝරන්න:",
    ["Overview (සියල්ල)", "Grocery Section", "Bakery & Bakery Items", "Pharmacy & Health", "Cashier & Checkout"]
)

# Search Bar
search_query = st.sidebar.text_input("🔍 භාණ්ඩයක් සොයන්න (Search Item):", "")

# 4. Main Display Logic (තෝරාගන්නා Section එක අනුව තොරතුරු පෙන්වීම)
st.subheader(f"දැනට නරඹන්නේ: {selected_section}")

if selected_section == "Overview (සියල්ල)":
    st.info("💡 මූලික 3D සිතියම පහතින් දැක්වේ. සයිඩ්බාර් එකෙන් ඔබට අවශ්‍ය Section එක තෝරාගත හැක.")
elif selected_section == "Grocery Section":
    st.write("🥦 **Grocery Section:** එළවළු, පලතුරු සහ වියළි ආහාර ද්‍රව්‍ය මෙහි පිහිටා ඇත.")
elif selected_section == "Bakery & Bakery Items":
    st.write("🍞 **Bakery Section:** පාන්, කේක් සහ බේකරි නිෂ්පාදන මෙහි පිහිටා ඇත.")
elif selected_section == "Pharmacy & Health":
    st.write("💊 **Pharmacy Section:** ඖෂධ සහ සෞඛ්‍ය උපකරණ මෙහි පිහිටා ඇත.")
elif selected_section == "Cashier & Checkout":
    st.write("💳 **Cashier Counters:** මුදල් ගෙවීමේ කවුන්ටර මෙහි පිහිටා ඇත.")

# Search Results display
if search_query:
    st.success(f"'{search_query}' සඳහා සෙවීම සිදු කෙරේ...")

# 5. Placeholder for 3D Map (ArcGIS Web Scene එක පසුව මෙතැනට එකතු වේ)
st.markdown("---")
st.markdown("### 🗺️ 3D Supermarket Map")
st.warning("⚠️ ArcGIS 3D Web Scene එක ලැබ් එකෙන් Publish කිරීමෙන් පසු මෙතැන සජීවීව දර්ශනය වනු ඇත.")

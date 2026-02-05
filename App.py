import streamlit as st
import pandas as pd

# =============================================================================
# SECTION 0 : Language & Page Setup
# =============================================================================
st.set_page_config(page_title="Tangkrai", page_icon="💸")

# 1. Initialize Session State for Language
if 'language' not in st.session_state:
    st.session_state['language'] = 'EN'  # Default to English

# 2. Function to toggle language
def toggle_language():
    if st.session_state['language'] == 'EN':
        st.session_state['language'] = 'TH'
    else:
        st.session_state['language'] = 'EN'

# 3. Translation Dictionary (Updated based on user request)
t = {
    # Modified title and button text as requested
    'title': {'EN': "💸 Tangkrai", 'TH': "💸 Tangkrai"},
    'btn_switch': {'EN': "Switch to Thai", 'TH': "Switch to English"},
    
    # Section 1
    'h1': {'EN': "1. Number of People", 'TH': "1. กำหนดจำนวนคน"},
    'num_people_label': {'EN': "Number of people", 'TH': "จำนวนคน"},
    
    # Section 2
    'h2': {'EN': "2. Item Price per Person", 'TH': "2. รายละเอียดสินค้าของแต่ละคน"},
    'info_msg': {'EN': "Enter only the item price for each person", 'TH': "ใส่เฉพาะราคาสินค้าของแต่ละคน"},
    'person_label': {'EN': "Person", 'TH': "คนที่"},
    'price_label': {'EN': "Item Price (THB)", 'TH': "ค่าของ (บาท)"},
    
    # Section 3
    'h3': {'EN': "3. Bill Summary", 'TH': "3. สรุปยอดบิล"},
    'subtotal_label': {'EN': "Subtotal (excluding delivery/discount)", 'TH': "ยอดรวมสินค้า (ไม่รวมส่ง/ลด)"},
    'grand_total_label': {'EN': "Grand Total (Net Payment)", 'TH': "ยอดที่ต้องจ่ายจริง (รวมส่ง/ลดแล้ว)"},
    
    # Validation & Warnings
    'warn_mismatch': {'EN': "⚠️ Warning: Sum of items ({}) does not match subtotal ({})", 
                      'TH': "⚠️ เตือน: ยอดรวมของทุกคน ({}) ไม่ตรงกับหน้าบิล ({})"},
    'success_match': {'EN': "✅ Individual total matches subtotal ({})", 
                      'TH': "✅ ยอดรวมของทุกคนตรงกับหน้าบิล ({})"},
    'err_no_items': {'EN': "Please enter item price for at least one person", 'TH': "กรุณากรอกราคาสินค้าของอย่างน้อย 1 คน"},
    'err_no_grand': {'EN': "Please enter the grand total amount", 'TH': "กรุณากรอกยอดที่ต้องจ่ายจริง (Grand Total)"},
    
    # Section 5 Button & Header
    'btn_calc': {'EN': "🚀 Calculate Payment", 'TH': "🚀 คำนวณเงินที่ต้องจ่าย"},
    'res_header': {'EN': "💰 Calculation Result", 'TH': "💰 ผลลัพธ์การคำนวณ"},
    
    # Table Columns
    'col_name': {'EN': "Name", 'TH': "ชื่อ"},
    'col_raw': {'EN': "Item Price (THB)", 'TH': "ยอดของ (บาท)"},
    'col_final': {'EN': "Final Payment (THB)", 'TH': "ต้องจ่ายจริง (บาท)"},
    
    # Section 6 Checksum
    'h_check': {'EN': "### 📝 Payment Verification", 'TH': "### 📝 ตรวจสอบยอดรวม"},
    'target_label': {'EN': "Target Grand Total", 'TH': "ยอดที่ต้องจ่ายจริง (เป้าหมาย)"},
    'calc_label': {'EN': "Calculated Total", 'TH': "ยอดรวมที่คำนวณได้"},
    'warn_high_dev': {'EN': "Note: High deviation detected. Please recheck inputs.", 
                      'TH': "หมายเหตุ: ยอดรวมมีความคลาดเคลื่อนสูง โปรดตรวจสอบตัวเลขอีกครั้ง"}
}

# Helper variable to shorten code
lang = st.session_state['language']

# =============================================================================
# UI : Language Switcher Button (Top Right corner style)
# =============================================================================
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.title(t['title'][lang])
with col_head2:
    st.button(t['btn_switch'][lang], on_click=toggle_language)

st.markdown("---")

# =============================================================================
# SECTION 1 : Set Number of People
# =============================================================================
st.subheader(t['h1'][lang])

num_people = st.number_input(
    t['num_people_label'][lang],
    min_value=2,
    value=2,
    step=1
)

# =============================================================================
# SECTION 2 : Item Price Details per Person
# =============================================================================
st.subheader(t['h2'][lang])
st.info(t['info_msg'][lang])

people_data = []

for i in range(int(num_people)):
    col1, col2 = st.columns([1, 2])
    with col1:
        # Note: keys must be unique and constant regardless of language
        default_name = f"{t['person_label'][lang]} {i+1}"
        name = st.text_input(
            f"{t['person_label'][lang]} {i+1}", 
            value=default_name, 
            key=f"name_{i}"
        )
    with col2:
        price = st.number_input(
            t['price_label'][lang], 
            min_value=0.0, 
            step=1.0, 
            key=f"price_{i}"
        )
    
    people_data.append({"name": name, "raw_price": price})

st.markdown("---")

# =============================================================================
# SECTION 3 : Bill Summary
# =============================================================================
st.subheader(t['h3'][lang])

col_summary1, col_summary2 = st.columns(2)

with col_summary1:
    subtotal_input = st.number_input(t['subtotal_label'][lang], min_value=0.0, step=1.0)

with col_summary2:
    grand_total = st.number_input(t['grand_total_label'][lang], min_value=0.0, step=1.0)

# =============================================================================
# SECTION 4 : Subtotal Validation
# =============================================================================
sum_raw_price = sum(p["raw_price"] for p in people_data)

if subtotal_input > 0:
    if sum_raw_price != subtotal_input:
        st.warning(t['warn_mismatch'][lang].format(f"{sum_raw_price:,.2f}", f"{subtotal_input:,.2f}"))
    else:
        st.success(t['success_match'][lang].format(f"{sum_raw_price:,.2f}"))

st.markdown("---")

# =============================================================================
# SECTION 5 : Calculate Final Payment
# =============================================================================
if st.button(t['btn_calc'][lang], type="primary"):
    
    if sum_raw_price == 0:
        st.error(t['err_no_items'][lang])
    elif grand_total == 0:
        st.error(t['err_no_grand'][lang])
    else:
        st.subheader(t['res_header'][lang])
        
        results = []
        total_check = 0
        
        for person in people_data:
            if sum_raw_price > 0:
                final_price = (person['raw_price'] / sum_raw_price) * grand_total
            else:
                final_price = 0
            
            final_price_rounded = round(final_price, 2)
            total_check += final_price_rounded
            
            results.append({
                t['col_name'][lang]: person['name'],
                t['col_raw'][lang]: f"{person['raw_price']:,.2f}",
                t['col_final'][lang]: f"{final_price_rounded:,.2f}"
            })

        # Display Table
        df = pd.DataFrame(results)
        st.table(df)

        # =============================================================================
        # SECTION 6 : Checksum Validation
        # =============================================================================
        st.markdown(t['h_check'][lang])
        
        col_check1, col_check2, col_check3 = st.columns(3)
        with col_check1:
            st.metric(t['target_label'][lang], f"{grand_total:,.2f}")
        with col_check2:
            st.metric(t['calc_label'][lang], f"{total_check:,.2f}")
        
        if abs(grand_total - total_check) > 1.0:
             st.warning(t['warn_high_dev'][lang])
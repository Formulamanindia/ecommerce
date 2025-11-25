import streamlit as st
from PIL import Image
import io
import pandas as pd
import base64
import numpy as np 

# --- 1. CONFIGURATION AND INITIAL SETUP ---
st.set_page_config(
    page_title="E-commerce Admin Panel",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Admin and Sub User Credentials (User ID Only Access)
USER_ACCESS = {
    "Globalite": "Admin",  # Admin User
    "User": "Sub User"     # Sub User
}
ADMIN_USER = "Globalite"

# Define mandatory CSV headers with *
SAMPLE_CSV_HEADERS = [
    'Product Name*', 'Variations (comma separated)*', 'Product Color*', 'Group Name*', 
    'Fabric Type*', 'SKU Code*', 'MRP*', 'Selling Price*', 'Brand*', 'HSN*', 
    'GST Rate*', 'Weight*', 'Inventory*', 'Country Of Origin*', 'Pack of*', 
    'Product Category*', 'Main Image*', '1 st Image', '2nd Image', '3rd Image', 
    '4th Image', 'Product Description*'
]
MANDATORY_COLS = [col for col in SAMPLE_CSV_HEADERS if col.endswith('*')]

# Initial marketplace data
DEFAULT_MARKETPLACES = {
    "Amazon": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg",
    "Flipkart": "https://upload.wikimedia.org/wikipedia/commons/3/36/Flipkart_logo.png",
    "Meesho": "https://images.meesho.com/images/branding/meesho-horizontal-logo.svg"
}

# Define the SERVICE_MAP with new descriptions for the dashboard cards
SERVICE_MAP = {
    "📝 Listing Maker": {"icon": "📝", "function": None, "color": "#00C6FF", "description": "Generate error-free bulk product listings for e-commerce."},
    "💰 Pricing Tool": {"icon": "💰", "function": None, "color": "#18D5C1", "description": "Calculate competitive selling prices and update marketplace files."},
    "🖼️ Image Uploader": {"icon": "🖼️", "function": None, "color": "#FFC107", "description": "Quickly upload, preview, and manage single product images."},
    "✨ Image Optimizer": {"icon": "✨", "function": None, "color": "#F39C12", "description": "Bulk optimize images by resizing and compressing for web."} ,
    "📈 Listing Optimizer": {"icon": "📈", "function": None, "color": "#E91E63", "description": "Improve descriptions for better conversion, SEO, and visibility."},
    "🔍 Key Word Extractor": {"icon": "🔍", "function": None, "color": "#9C27B0", "description": "Find relevant, high-ranking keywords for your product titles."},
    "🧾 GST Filing": {"icon": "🧾", "function": None, "color": "#4CAF50", "description": "Simplify monthly GST compliance, reconciliation, and filing."},
    "📊 Report Maker": {"icon": "📊", "function": None, "color": "#2196F3", "description": "Generate custom sales, inventory, and business intelligence reports."},
}

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.is_admin = False
    
if 'marketplace_logos' not in st.session_state:
    st.session_state.marketplace_logos = DEFAULT_MARKETPLACES

# New state for page management
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# --- 2. CUSTOM CSS/INTERFACE ---

# Define global color variables based on the custom CSS
SIDEBAR_BG_COLOR = "#212838"  
BACKGROUND_COLOR = "#F8F9FA"  
ACCENT_COLOR = "#00C6FF"      
PRIMARY_TEXT_COLOR = "#212838" 
SIDEBAR_TEXT_COLOR = "#FFFFFF" 
HOVER_COLOR = "#333d4f"       

def apply_custom_css():
    """Applies custom CSS for the modern dashboard look and service boxes."""
    
    custom_css = f"""
    <style>
    /* Global Styling */
    .stApp {{
        background-color: {BACKGROUND_COLOR};
        color: {PRIMARY_TEXT_COLOR};
        font-family: 'Roboto', sans-serif;
    }}
    
    /* Sidebar Styling - Targeted class for the Streamlit sidebar */
    .css-1d391kg, .css-1dp5f7e {{ 
        background-color: {SIDEBAR_BG_COLOR};
        color: {SIDEBAR_TEXT_COLOR};
    }}
    /* Sidebar Text/Headers */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg .stMarkdown, 
    .css-1d391kg .stSelectbox label, .css-1d391kg .stRadio label {{
        color: {SIDEBAR_TEXT_COLOR} !important;
    }}

    /* Sidebar Radio Button Styling (Navigation Links) */
    .stRadio > label {{
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 5px;
        color: {SIDEBAR_TEXT_COLOR};
        font-size: 1.0em;
        font-weight: 400;
        transition: background-color 0.2s, color 0.2s, border-left 0.2s;
        border-left: 3px solid transparent; 
    }}
    .stRadio > label:hover {{
        background-color: {HOVER_COLOR};
        color: {ACCENT_COLOR}; 
    }}
    /* Highlight the checked radio button as the active page */
    .stRadio > label:has(input:checked) {{
        background-color: {HOVER_COLOR} !important; 
        color: {ACCENT_COLOR} !important; 
        font-weight: 600;
        border-left: 3px solid {ACCENT_COLOR} !important; 
    }}
    .stRadio > label:has(input:checked) > div:first-child {{
        color: {ACCENT_COLOR} !important; 
    }}


    /* Headers/Titles in Main Content */
    h1, h2, h3 {{ 
        color: {PRIMARY_TEXT_COLOR}; 
        font-weight: 700; 
        border-bottom: none; 
        padding-bottom: 0; 
        margin-top: 20px; 
    }}

    /* Global Button Styling (The card look is now applied generally to all non-primary buttons in the main area) */
    .stApp .stButton>button {{
        /* Base Card Look for Dashboard and general controls */
        background-color: #FFFFFF; 
        color: {PRIMARY_TEXT_COLOR};
        border: 1px solid #e0e0e0; 
        padding: 20px 10px;
        width: 100%;
        height: 160px; 
        border-radius: 12px; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        white-space: normal; 
        line-height: 1.2;
    }}
    
    /* Global Button Hover Effect */
    .stApp .stButton>button:hover {{
        transform: translateY(-5px); 
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        background-color: #f7f7f7; 
    }}
    
    /* Revert Streamlit Primary Button for functional buttons (e.g., Download, Generate) */
    .stApp .stButton button[data-testid*="primaryButton"] {{
        background-color: {ACCENT_COLOR}; 
        color: {SIDEBAR_BG_COLOR}; 
        border: none; 
        padding: 10px 20px; 
        box-shadow: none;
        height: auto;
        transform: none; 
    }}
    .stApp .stButton button[data-testid*="primaryButton"]:hover {{
        background-color: #00B1E6;
        box-shadow: none;
    }}

    /* Info Box / Alert for cleaner look */
    .stAlert.info, .stInfo {{
        background-color: #E3F2FD; 
        border-left: 5px solid {ACCENT_COLOR}; 
        color: #1565C0; 
    }}

    /* Footer Style - Simple and Centered */
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: {BACKGROUND_COLOR}; 
        color: {PRIMARY_TEXT_COLOR};
        font-size: 0.8em;
        border-top: 1px solid #e0e0e0;
        z-index: 100;
        text-align: center; 
        padding: 10px; 
    }}
    
    /* Ensure marketplace logos are square */
    .stImage > img {{
        object-fit: contain;
    }}
    
    /* Hide the ugly radio button dot in the sidebar */
    .stRadio > label > div:first-child {{
        display: none !important;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def display_footer():
    """Displays the required footer credit only."""
    
    footer_html = f"""
    <div class="footer">
        <p style="margin: 0;">Made in Bharat | &copy; 2025 - Formula Man. All rights reserved.</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# --- 3. CORE LOGIC FUNCTIONS ---

def get_sample_csv():
    """Generates the sample CSV data for download based on defined headers."""
    data = {
        'Product Name*': ["Premium Cotton Tee"],
        'Variations (comma separated)*': ["S,M,L"],
        'Product Color*': ["Red"],
        'Group Name*': ["G_TS_RED"],
        'Fabric Type*': ["Cotton"],
        'SKU Code*': ["TS-R-01"],
        'MRP*': [999],
        'Selling Price*': [499],
        'Brand*': ["Formula Man"],
        'HSN*': [6109],
        'GST Rate*': [5],
        'Weight*': [100],
        'Inventory*': [1],
        'Country Of Origin*': ["India"],
        'Pack of*': [1],
        'Product Category*': ["T-Shirt"],
        'Main Image*': ["https://i.imgur.com/8Q9j0rX.png"],
        '1 st Image': ["(Optional)"],
        '2nd Image': ["(Optional)"],
        '3rd Image': ["(Optional)"],
        '4th Image': ["(Optional)"],
        'Product Description*': [""]
    }
    df = pd.DataFrame(data, columns=SAMPLE_CSV_HEADERS)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue().encode()

def generate_description_mock(row):
    """
    MOCK FUNCTION: Generates a conversion-focused product description (under 1400 characters) 
    if the existing description field is empty, with no markdown bolding.
    """
    title = row.get('Product Name*')
    category = row.get('Product Category*')
    color = row.get('Product Color*')
    fabric = row.get('Fabric Type*', 'premium material')
    brand = row.get('Brand*', 'a trusted source')
    sizes = row.get('Variations (comma separated)*', 'various sizes').replace(',', ', ')
    
    if pd.isna(title) or pd.isna(category):
        return "No comprehensive description generated due to missing product name or category."
        
    description = (
        f"Elevate your wardrobe with this exquisite {category} from {brand}. "
        f"Crafted from ultra-soft {fabric}, this piece guarantees all-day COMFORT and a premium feel. "
        f"The stunning {color} shade offers a versatile, MODERN look, effortlessly transitioning "
        f"from casual outings to relaxed evening wear. Designed for a comfortable FIT, it provides ease of "
        f"movement while maintaining a sharp silhouette. Available in sizes {sizes}, finding your "
        f"PERFECT match is simple. Invest in quality and style that lasts, ensuring you look and feel your best "
        f"every time you wear it. A must-have staple for your collection. "
        f"(Keywords: {title.replace(' ', ', ').replace('-', ',')}, {category}, {fabric}, {color})"
    )
    
    MAX_CHARS = 1400
    if len(description) > MAX_CHARS:
        description = description[:MAX_CHARS - 3] + '...'
    
    return description


def generate_sku_listings(df):
    """
    Processes the DataFrame to explode variations into individual SKUs,
    creates unique SKU codes (SKU--COLOR--SIZE), and sorts by Group Name.
    """
    
    size_col = 'Variations (comma separated)*'
    sku_col = 'SKU Code*'
    group_col = 'Group Name*'
    color_col = 'Product Color*'
    desc_col = 'Product Description*'

    # 1. Mandatory Column Check
    for col in MANDATORY_COLS:
        if col not in df.columns:
            st.error(f"Mandatory column missing: '{col}'. Please correct your CSV header.")
            return None
            
    # --- FEATURE: Generate/Update Product Description ---
    # Apply the generation ONLY if the description field is empty/missing 
    df[desc_col] = df.apply(
        lambda row: generate_description_mock(row) 
        if pd.isna(row[desc_col]) or str(row[desc_col]).strip() == "" 
        else row[desc_col], 
        axis=1
    )
    # -----------------------------------------------------
    
    # 2. Split and Explode
    df[size_col] = df[size_col].fillna('').astype(str).str.replace(' ', '').str.upper().str.split(',')
    df = df[df[size_col].apply(lambda x: len(x) > 0 and x != [''])]
    df_expanded = df.explode(size_col, ignore_index=True)
    df_expanded.rename(columns={size_col: 'Size'}, inplace=True)
    
    # 3. Create a unique SKU for each variation (SKU--COLOR--SIZE)
    cleaned_color = df_expanded[color_col].astype(str).str.replace(' ', '').str.upper()
    
    df_expanded['New SKU'] = (
        df_expanded[sku_col].astype(str) + 
        '--' + 
        cleaned_color + 
        '--' + 
        df_expanded['Size'].astype(str)
    )
    
    df_expanded.drop(columns=[sku_col], inplace=True)
    df_expanded.rename(columns={'New SKU': sku_col}, inplace=True)

    # 4. Sort and Reorder 
    df_sorted = df_expanded.sort_values(by=group_col, ascending=True)
    
    cols = list(df_sorted.columns)
    
    if 'Size' in cols:
        cols.insert(1, cols.pop(cols.index('Size')))
    if color_col in cols:
        cols.insert(2, cols.pop(cols.index(color_col)))
    if sku_col in cols:
        cols.insert(0, cols.pop(cols.index(sku_col)))

    df_sorted = df_expanded[cols]
    
    return df_sorted

# --- 4. SERVICE PAGE DEFINITIONS ---

def listing_maker_tab():
    st.title("📝 Listing Maker")
    
    # --- Channel Category Selector ---
    st.subheader("1. Select Channel Type and Destination")
    channel_category = st.radio(
        "Channel Category", 
        ("Ecommerce", "Quick Commerce"),
        horizontal=True,
        key="channel_category_radio"
    )
    
    ecommerce_channels = [
        'Amazon', 'Flipkart', 'Myntra', 'Meesho', 'Ajio', 'Jio Mart', 
        'Nykaa', 'Mens XP', 'Tata Cliq', 'First Cry', 'Paytm Mall', 
        'Snapdeal', 'IndiaMart', 'Shopify'
    ]
    
    if channel_category == "Ecommerce":
        channels = ecommerce_channels
        selected_channels = st.multiselect(
            "Select Ecommerce Channels",
            options=channels,
            default=channels[0]
        )
        st.subheader("2. Download Sample CSV Header")
        st.download_button(
            label="Download Ecommerce Sample CSV",
            data=get_sample_csv(),
            file_name="Ecommerce_Listing_Sample_Template.csv",
            mime="text/csv",
            type="primary" # Use primary type for functional buttons
        )
        st.subheader("3. Upload Product CSV")
        uploaded_file = st.file_uploader(
            "Choose a CSV file (must match the template header)", 
            type="csv", 
            key="listing_maker_uploader"
        )
        
        header_option = st.checkbox("CSV file includes header row", value=True)

        if uploaded_file is not None:
            try:
                header = 0 if header_option else None
                df_uploaded = pd.read_csv(uploaded_file, header=header)
                
                if header is None:
                    st.warning("Assuming generic column names since 'CSV file includes header row' is unchecked.")
                    df_uploaded.columns = [f"C{i+1}" for i in range(df_uploaded.shape[1])]
                
                st.success(f"File uploaded successfully. {df_uploaded.shape[0]} base products found.")
                
                if st.button("Generate SKU Listings and Download", key="generate_sku_btn", type="primary"):
                    with st.spinner('Generating SKU listings and descriptions...'):
                        df_final = generate_sku_listings(df_uploaded.copy())
                        
                        if df_final is not None:
                            st.subheader("4. Generated Listings Preview")
                            st.write(f"Total SKU-level listings generated: **{df_final.shape[0]}**")
                            
                            try:
                                sample_sku = df_final['SKU Code*'].iloc[0]
                                with st.expander(f"View Sample Generated Description for SKU: {sample_sku}"):
                                    st.markdown(df_final['Product Description*'].iloc[0])
                            except IndexError:
                                st.warning("No listings were generated. Check if the 'Variations (comma separated)*' column is correctly filled.")
                                return
                                
                            column_configuration = {
                                "Main Image*": st.column_config.ImageColumn(
                                    "Product Image", 
                                    help="Visual reference for the main image URL.",
                                    width="small" 
                                ),
                                "1 st Image": st.column_config.TextColumn(disabled=True),
                                "2nd Image": st.column_config.TextColumn(disabled=True),
                                "3rd Image": st.column_config.TextColumn(disabled=True),
                                "4th Image": st.column_config.TextColumn(disabled=True),
                            }
                            
                            st.dataframe(
                                df_final.head(10), 
                                use_container_width=True, 
                                column_config=column_configuration,
                                hide_index=True 
                            )
                            
                            csv_buffer = io.StringIO()
                            df_final.to_csv(csv_buffer, index=False)
                            csv_data = csv_buffer.getvalue().encode()
                            
                            st.download_button(
                                label="Download Final SKU CSV",
                                data=csv_data,
                                file_name=f"SKU_Listings_for_{'_'.join(selected_channels)}.csv",
                                mime="text/csv",
                                type="primary"
                            )
                            st.success("Listings generated and ready for download.")

            except Exception as e:
                st.error(f"Error processing file: {e}")
                st.warning("Please ensure the uploaded file is a valid CSV and includes the correct columns.")
        
    elif channel_category == "Quick Commerce":
        st.subheader("2. Quick Commerce Integration")
        st.info("🚧 **Work in Progress:** Quick Commerce listing templates and channel integration are currently under development. Please check back later.")

def pricing_tool_tab():
    st.title("💰 Pricing Tool")
    st.info("Calculate competitive selling prices and net profit across different marketplaces.")

    marketplace_names = list(st.session_state.marketplace_logos.keys())
    
    if not marketplace_names:
        st.warning("No marketplaces configured. Please ask an Admin to add marketplaces in the Configuration tab.")
        return

    # Dynamically create tabs based on configured marketplaces
    tabs = st.tabs(marketplace_names)

    for i, name in enumerate(marketplace_names):
        with tabs[i]:
            # Logo Display
            logo_url = st.session_state.marketplace_logos.get(name, "")
            col1, col2 = st.columns([1, 6])
            with col1:
                 if logo_url:
                     try:
                         st.image(logo_url, width=50, height=50) 
                     except Exception:
                         st.markdown("No Logo Set")
                 else:
                     st.markdown("No Logo Set")
            with col2:
                 st.markdown(f"### {name} Channel Details")

            
            if name == "Flipkart":
                st.subheader("Flipkart Price Increase Tool")
                st.info("Upload your Flipkart file and increase **'Bank Settlement'** prices within a specified range.")

                # --- Calculation Inputs ---
                col_calc_1, col_calc_2, col_calc_3 = st.columns(3)
                
                with col_calc_1:
                    min_bs = st.number_input("Min Bank Settlement (₹)", value=100.0, min_value=0.0, key=f'{name}_min_bs')
                
                with col_calc_2:
                    max_bs = st.number_input("Max Bank Settlement (₹)", value=500.0, min_value=min_bs, key=f'{name}_max_bs')
                
                with col_calc_3:
                    increase_percent_options = [f"{p}%" for p in range(1, 11)]
                    increase_percent_str = st.selectbox(
                        "Price Increase Limit", 
                        options=increase_percent_options, 
                        index=0, 
                        key=f'{name}_increase_percent'
                    )
                    increase_percent = int(increase_percent_str.replace('%', '')) 

                st.markdown("---")
                
                # --- File Uploader and Processing ---
                uploaded_file = st.file_uploader(
                    "Upload Flipkart Listing File (CSV/Excel compatible)",
                    type=["csv", "xlsx", "xls"],
                    key=f'{name}_uploader'
                )

                if uploaded_file is not None and st.button("Calculate & Prepare Download", key=f'{name}_calculate_btn', type="primary"):
                    
                    df = None
                    
                    file_extension = uploaded_file.name.split('.')[-1].lower()

                    if file_extension == 'csv':
                        try:
                            df = pd.read_csv(uploaded_file, keep_default_na=False) 
                        except UnicodeDecodeError:
                            st.warning("UTF-8 decoding failed. Trying alternative encodings (cp1252/latin-1)...")
                            try:
                                uploaded_file.seek(0)
                                df = pd.read_csv(uploaded_file, keep_default_na=False, encoding='cp1252')
                            except:
                                uploaded_file.seek(0)
                                df = pd.read_csv(uploaded_file, keep_default_na=False, encoding='latin-1')
                        except Exception as e:
                            st.error(f"Error reading CSV file: {e}")
                            return
                    elif file_extension in ['xlsx', 'xls']:
                        try:
                            df = pd.read_excel(uploaded_file, keep_default_na=False)
                        except Exception as e:
                            st.error(f"Error reading Excel file: {e}")
                            st.error("Error: Missing optional dependency for .xls files. Please run `pip install xlrd` or convert the file to .xlsx or .csv.")
                            return
                    else:
                        st.error("Unsupported file format. Please upload a CSV or XLSX/XLS file.")
                        return

                    if df is None or 'Bank Settlement' not in df.columns:
                        st.error("Error: The uploaded file must contain a column named 'Bank Settlement' and be a readable format.")
                        return

                    st.success(f"File loaded successfully. Processing {df.shape[0]} rows...")
                    
                    # 2. Calculation Logic
                    multiplier = 1 + (increase_percent / 100)
                    
                    df['BS_Num'] = pd.to_numeric(df['Bank Settlement'], errors='coerce')

                    condition = (
                        (df['BS_Num'] >= min_bs) & 
                        (df['BS_Num'] <= max_bs) & 
                        (~df['BS_Num'].isna())
                    )

                    df.loc[condition, 'Bank Settlement'] = (
                        np.floor(df.loc[condition, 'BS_Num'] * multiplier)
                    ).astype(int)
                    
                    df.drop(columns=['BS_Num'], inplace=True)

                    st.subheader("✅ Calculation Complete")
                    st.write(f"Updated **{condition.sum()}** rows out of {df.shape[0]}.")
                    
                    # 3. Download Preparation
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)
                    csv_data = csv_buffer.getvalue().encode('utf-8')
                    
                    st.download_button(
                        label="Download Updated Flipkart File (CSV)",
                        data=csv_data,
                        file_name=f"Flipkart_Price_Updated_{min_bs}_{max_bs}_plus{increase_percent}%.csv",
                        mime="text/csv",
                        type="primary"
                    )
                    st.dataframe(df.head(5))

            else:
                st.subheader(f"Pricing Calculator for {name}")
                st.info("🚧 **Work in Progress:** Advanced pricing tools and channel integration for this marketplace are currently under development. Please check back later.")
                
def image_uploader_tab():
    st.title("🖼️ Image Uploader")
    st.info("Upload and review your product images before processing.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)
                quality = st.slider("Compression Quality (0=Max, 100=Min)", 10, 95, 85)
                max_width = st.number_input("Max Width (px)", value=1000, min_value=100)
            if st.button("Optimize Image", key="optimize_image_btn", type="primary"):
                if image.width > max_width:
                    ratio = max_width / image.width
                    new_height = int(image.height * ratio)
                    optimized_image = image.resize((max_width, new_height))
                else:
                    optimized_image = image
                buffer = io.BytesIO()
                optimized_image.save(buffer, format="JPEG", quality=quality)
                buffer.seek(0)
                with col2:
                    st.subheader("Optimized Image")
                    st.image(optimized_image, use_column_width=True)
                    st.success("Optimization Complete!")
                    st.download_button(
                        label="Download Optimized Image",
                        data=buffer,
                        file_name=f"optimized_{uploaded_file.name}",
                        mime="image/jpeg",
                        type="primary"
                    )
        except Exception as e:
            st.error(f"An error occurred during optimization: {e}")

def image_optimizer_tab():
    st.title("✨ Image Optimizer")
    st.info("Bulk optimize images by resizing and compressing them for faster loading on marketplaces.")
    st.warning("This is a simplified mock-up of a bulk optimization feature.")
    uploaded_files = st.file_uploader("Upload multiple images to optimize", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        st.subheader(f"Files Uploaded: {len(uploaded_files)}")
        st.number_input("Target Max Width (px)", value=800, min_value=100, key="opt_width")
        st.slider("Target JPEG Quality", 70, 95, 80, key="opt_quality")
        
        if st.button("Run Bulk Optimization", key="run_bulk_opt_btn", type="primary"):
            with st.spinner("Optimizing images..."):
                # Mock processing loop
                import time
                time.sleep(2)
            st.success(f"Successfully optimized {len(uploaded_files)} images (simulated).")
            st.info("A ZIP file containing all optimized images would typically be generated for download here.")
            
def listing_optimizer_tab():
    st.title("📈 Listing Optimizer")
    st.info("Analyze and improve your current product listing text for better conversion and SEO.")
    listing_text = st.text_area("Paste your current product listing description here:", height=300)
    if st.button("Analyze & Suggest Improvements", key="analyze_listing_btn", type="primary"):
        if listing_text:
            st.subheader("Analysis Results (Placeholder)")
            st.markdown("* **Keyword Density:** Low - Focus on 'Cotton T-Shirt'")
            st.markdown("* **Readability:** Good")
            st.markdown("* **Call-to-Action:** Missing - Suggest adding phrases like 'Buy Now' or 'Add to Cart'")
            st.subheader("Optimized Suggestion (Simulated)")
            st.success(listing_text.replace("product", "high-quality product listing"))
        else:
            st.warning("Please paste some listing text to analyze.")
            
def keyword_extractor_tab():
    st.title("🔍 Key Word Extractor")
    st.info("Extract relevant, high-ranking keywords from competitors or product ideas.")
    seed_phrase = st.text_input("Enter a seed phrase or competitor's product name:")
    if st.button("Extract Keywords", key="extract_keywords_btn", type="primary"):
        if seed_phrase:
            st.subheader(f"Keywords for: **{seed_phrase}** (Simulated)")
            keywords = [
                f"{seed_phrase} best price",
                f"{seed_phrase} for sale",
                "e-commerce product keyword",
                "top trending listing keyword",
                "formula man's suggestion"
            ]
            df = pd.DataFrame({"Keyword": keywords, "Search Volume (Sim)": [8500, 3200, 5000, 1500, 900]})
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Please enter a seed phrase.")

def gst_filing_tab():
    st.title("🧾 GST Filing")
    st.info("Simplify your monthly and quarterly GST compliance, reconciliation, and filing process.")
    
    st.subheader("GST Filing Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pending Returns", "GSTR-1 (Oct)", "1 month due")
    with col2:
        st.metric("Last Filed Date", "2025-10-20", "GSTR-3B")
    with col3:
        st.metric("Input Tax Credit (ITC)", "₹1,25,000", "Simulated")
    
    st.markdown("---")
    st.subheader("Upload Data for Reconciliation")
    st.file_uploader("Upload Sales Data (GSTR-1, GSTR-3B)", type=["csv", "xlsx"])
    st.file_uploader("Upload Purchase Data (GSTR-2A/2B)", type=["csv", "xlsx"])
    
    if st.button("Generate Reconciliation Report", key="generate_report_btn", type="primary"):
        st.success("Reconciliation report generated successfully (simulated). Discrepancies: 5.")

def report_maker_tab():
    st.title("📊 Report Maker")
    st.info("Generate custom reports, analytics, and business intelligence dashboards.")
    
    st.subheader("Report Type Selection")
    report_type = st.selectbox(
        "Choose a Report Template",
        ["Sales Performance by Channel", "Inventory Health Report", "Profit & Loss Statement (Simplified)"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
        
    if st.button("Generate Report", key="report_gen_btn", type="primary"):
        st.success(f"Generating **{report_type}** from {start_date} to {end_date} (simulated).")
        st.dataframe(pd.DataFrame({
            'Metric': ['Revenue', 'Expenses', 'Profit'],
            'Value': ['₹1,50,000', '₹80,000', '₹70,000']
        }))

def configuration_tab():
    st.title("🔧 Configuration (Admin Only)")
    if st.session_state.is_admin:
        st.success(f"Welcome Admin **{st.session_state.username}**. You have full access.")
        
        st.subheader("User Management (Placeholder)")
        st.table(pd.DataFrame({
            "User ID": ["Globalite", "User"],
            "Role": ["Admin", "Sub User"],
            "Status": ["Active", "Active"]
        }))
        
        # --- MARKETPLACE ADDER ---
        st.subheader("Marketplace and Logo Management")
        st.info("Use this tool to add new marketplaces or edit existing logos.")
        
        with st.expander("➕ Add New Marketplace", expanded=False):
            with st.form("marketplace_adder", clear_on_submit=True):
                new_name = st.text_input("Marketplace Name (e.g., Nykaa)", key="new_mp_name").strip()
                new_logo_url = st.text_input("Logo Link/URL (e.g., https://logo.com/nykaa.png)", key="new_mp_logo").strip()
                submitted = st.form_submit_button("Add Marketplace", type="primary")

                if submitted:
                    if new_name and new_logo_url:
                        if new_name not in st.session_state.marketplace_logos:
                            st.session_state.marketplace_logos[new_name] = new_logo_url
                            st.success(f"Marketplace '{new_name}' added successfully!")
                            st.rerun() 
                        else:
                            st.warning(f"Marketplace '{new_name}' already exists.")
                    else:
                        st.error("Please enter both a name and a logo link.")
        
        # --- MARKETPLACE LOGO EDITOR (NEW FEATURE) ---
        
        if st.session_state.marketplace_logos:
            st.subheader("Marketplace Logo Editor")
            
            marketplace_to_edit = st.selectbox(
                "Select Marketplace to Edit Logo",
                options=list(st.session_state.marketplace_logos.keys()),
                key="mp_edit_selector"
            )
            
            current_logo_url = st.session_state.marketplace_logos.get(marketplace_to_edit, "")
            
            with st.form("marketplace_editor", clear_on_submit=False):
                new_logo_url_edit = st.text_input(
                    f"New Logo Link/URL for **{marketplace_to_edit}**", 
                    value=current_logo_url,
                    key="new_mp_logo_edit"
                ).strip()
                
                submitted_edit = st.form_submit_button("Update Logo", type="primary")
                
                if submitted_edit:
                    if new_logo_url_edit:
                        st.session_state.marketplace_logos[marketplace_to_edit] = new_logo_url_edit
                        st.success(f"Logo for '{marketplace_to_edit}' updated successfully! The app will refresh now.")
                        st.rerun()
                    else:
                        st.error("Logo link cannot be empty.")
        
        st.markdown("---")
        st.markdown("#### Current Marketplaces:")
        current_mps = pd.DataFrame(st.session_state.marketplace_logos.items(), columns=['Marketplace', 'Logo URL'])
        st.dataframe(current_mps, use_container_width=True)
        
    else:
        st.error("🛑 Access Denied. This section is for Admin access only.")

# --- Map the service names to their actual functions ---
SERVICE_MAP["📝 Listing Maker"]["function"] = listing_maker_tab
SERVICE_MAP["💰 Pricing Tool"]["function"] = pricing_tool_tab
SERVICE_MAP["🖼️ Image Uploader"]["function"] = image_uploader_tab
SERVICE_MAP["✨ Image Optimizer"]["function"] = image_optimizer_tab
SERVICE_MAP["📈 Listing Optimizer"]["function"] = listing_optimizer_tab
SERVICE_MAP["🔍 Key Word Extractor"]["function"] = keyword_extractor_tab
SERVICE_MAP["🧾 GST Filing"]["function"] = gst_filing_tab
SERVICE_MAP["📊 Report Maker"]["function"] = report_maker_tab

# --- 5. DASHBOARD FUNCTION (Service Card View) ---

def service_dashboard_tab():
    """Renders the main landing page with service cards in a responsive grid."""
    
    st.title("👋 Welcome to Formula Man")
    st.subheader("Your E-commerce Automation Toolkit")
    st.markdown("---")
    
    services = list(SERVICE_MAP.items())
    num_services = len(services)
    
    # Define columns for a responsive grid (3 cards per row)
    num_cols = 3
    num_rows = (num_services + num_cols - 1) // num_cols
    
    for i in range(num_rows):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            index = i * num_cols + j
            if index < num_services:
                service_name, service_data = services[index]
                
                # Use custom HTML for the card content layout (Icon, Title, Description)
                card_content_html = f"""
                <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%; text-align: center;'>
                    <div style='color: {service_data['color']}; font-size: 2.5em; margin-bottom: 5px;'>
                        {service_data['icon']}
                    </div>
                    <div style='font-weight: 700; font-size: 1.1em; color: {PRIMARY_TEXT_COLOR}; margin-bottom: 5px;'>
                        {service_name.split(' ', 1)[1]} 
                    </div>
                    <div style='font-size: 0.8em; color: #555; height: 30px; overflow: hidden;'>
                        {service_data['description']}
                    </div>
                </div>
                """
                
                with cols[j]:
                    # Use a standard button with unique key. Clicking it sets the new page state.
                    if st.button(
                        card_content_html,
                        key=f"card_btn_{service_name.replace(' ', '_')}", # Unique key for stability
                        help=service_data['description'],
                        unsafe_allow_html=True,
                        use_container_width=True
                    ):
                        st.session_state.current_page = service_name
                        st.rerun()

# --- 6. MAIN APP EXECUTION ---

def run_app():
    """Manages login and main application flow."""
    
    apply_custom_css()

    # --- A. LOGIN INTERFACE ---
    if not st.session_state.logged_in:
        st.title("🔐 E-commerce Solution Access")
        st.info("Enter your User ID to gain access. (User IDs: 'Globalite' or 'User')")
        
        with st.form("login_form"):
            username_input = st.text_input("User ID", key="user_id_input").strip()
            submitted = st.form_submit_button("Access App", type="primary")
            
            if submitted:
                if username_input in USER_ACCESS:
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.session_state.is_admin = (username_input == ADMIN_USER)
                    st.session_state.current_page = "Dashboard" # Redirect to the new dashboard
                    st.rerun() 
                else:
                    st.error("Invalid User ID.")
        
    # --- B. MAIN APPLICATION INTERFACE (After Login) ---
    else:
        # Sidebar Header
        st.sidebar.markdown(f"## **E-Commerce Solution**")
        st.sidebar.markdown(f"**User:** {st.session_state.username}")
        st.sidebar.markdown(f"**Role:** {USER_ACCESS.get(st.session_state.username, 'N/A')}")
        st.sidebar.markdown("---")
        
        # --- Sidebar Navigation Logic (UPDATED TO SHOW ALL SERVICES) ---
        
        # List of all available pages, including Dashboard and Config
        main_nav_options = ["Dashboard"] + list(SERVICE_MAP.keys())
        if st.session_state.is_admin:
             main_nav_options.append("🔧 Configuration (Admin)")
             
        # Determine the currently active page for the sidebar highlighting
        current_index = 0
        try:
            current_index = main_nav_options.index(st.session_state.current_page)
        except ValueError:
            current_index = 0 # Default to Dashboard if page is unknown

        # Use st.sidebar.radio with all pages for complete navigation
        selected_option = st.sidebar.radio(
            "Navigation", 
            main_nav_options,
            index=current_index,
            key="main_sidebar_nav"
        )
        
        # If the user clicks on a sidebar link, update the current page and rerun
        if selected_option != st.session_state.current_page:
            st.session_state.current_page = selected_option
            st.rerun()

        st.sidebar.markdown("---")

        if st.sidebar.button("Logout", type="primary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_admin = False
            st.session_state.current_page = "Dashboard" # Reset page
            st.rerun()

        # --- Main Content Execution ---
        current_page = st.session_state.current_page
        
        if current_page == "Dashboard":
            service_dashboard_tab()
        elif current_page == "🔧 Configuration (Admin)":
            configuration_tab()
        elif current_page in SERVICE_MAP:
            # Execute the function for the selected service (navigated from radio button)
            SERVICE_MAP[current_page]["function"]()
        else:
            st.title("Page Not Found")


    # Display the required footer credit only
    display_footer()

if __name__ == "__main__":
    run_app()

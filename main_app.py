## main_app.py - FINAL VERSION WITH PRICING TOOL & CONFIGURATION

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

# Initial marketplace data (used for first-time session initialization)
DEFAULT_MARKETPLACES = {
    "Amazon": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg",
    "Flipkart": "https://upload.wikimedia.org/wikipedia/commons/3/36/Flipkart_logo.png",
    "Meesho": "https://images.meesho.com/images/branding/meesho-horizontal-logo.svg"
}

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.is_admin = False
    
if 'show_social_icons' not in st.session_state: 
    st.session_state.show_social_icons = True 
    
if 'marketplace_logos' not in st.session_state:
    st.session_state.marketplace_logos = DEFAULT_MARKETPLACES

# --- 2. CUSTOM CSS/INTERFACE ---

def apply_custom_css():
    """Applies custom CSS for the Admin Panel look, referencing bankco's style."""
    
    PRIMARY_COLOR = "#0A2463"         
    BACKGROUND_COLOR = "#ffffff"     
    SIDEBAR_BG_COLOR = "#f0f0f0"     
    ACCENT_BLUE = "#007bff"          

    custom_css = f"""
    <style>
    /* Global Styling */
    .stApp {{
        background-color: {BACKGROUND_COLOR};
        color: {PRIMARY_COLOR};
        font-family: Arial, sans-serif;
    }}
    
    /* Sidebar Styling */
    .css-1d391kg {{ 
        background-color: {SIDEBAR_BG_COLOR};
        color: {PRIMARY_COLOR};
    }}
    
    /* Sidebar Radio Button Styling (Navigation Links) */
    .stRadio > label {{
        padding: 8px 15px;
        margin: 5px 0;
        border-radius: 5px;
        color: {PRIMARY_COLOR};
        font-size: 1.1em;
        font-weight: 500;
        transition: background-color 0.2s, color 0.2s;
    }}
    .stRadio > label:has(input:checked) {{
        background-color: {ACCENT_BLUE} !important;
        color: white !important;
        font-weight: bold;
    }}
    
    /* Headers/Titles */
    h1, h2, h3 {{ 
        color: {PRIMARY_COLOR}; 
        font-weight: 700; 
        border-bottom: 2px solid {ACCENT_BLUE}; 
        padding-bottom: 5px; 
        margin-top: 15px; 
    }}

    /* Primary Buttons */
    .stButton>button {{ 
        background-color: {ACCENT_BLUE}; 
        color: white; 
        border: none; 
        padding: 10px 20px; 
        border-radius: 3px; 
        transition: background-color 0.3s; 
    }}
    .stButton>button:hover {{ 
        background-color: #0056b3; 
    }}
    
    /* Footer Style */
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: {SIDEBAR_BG_COLOR};
        color: {PRIMARY_COLOR};
        text-align: center;
        padding: 10px;
        font-size: 0.8em;
        border-top: 1px solid #e0e0e0;
        z-index: 100;
    }}
    .social-icons a {{
        color: {ACCENT_BLUE};
        margin: 0 10px;
        font-size: 1.2em;
        text-decoration: none;
    }}
    
    /* Ensure marketplace logos are square */
    .stImage > img {{
        object-fit: contain;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def display_footer():
    """Displays the required footer credit and social icons."""
    
    social_icons_html = ""
    if st.session_state.show_social_icons:
        social_icons_html = """
        <div class="social-icons" style="margin-bottom: 5px;">
            <a href="https://twitter.com/Streamlit" target="_blank">🐦 Twitter</a>
            <a href="https://linkedin.com/" target="_blank">🔗 LinkedIn</a>
            <a href="https://github.com/" target="_blank">🐈 GitHub</a>
            <a href="https://www.youtube.com/" target="_blank">▶️ YouTube</a>
        </div>
        """

    footer_html = f"""
    <div class="footer">
        {social_icons_html}
        Made in Bharat | © 2025 - Formula Man. All rights reserved.
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# --- 3. CORE LOGIC FUNCTIONS ---

def get_sample_csv():
    # ... (omitted for brevity, remains unchanged)
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
        'Main Image*': ["https://sample.com/image.jpg"],
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
    # ... (omitted for brevity, remains unchanged except for the description generation)
    size_col = 'Variations (comma separated)*'
    sku_col = 'SKU Code*'
    group_col = 'Group Name*'
    color_col = 'Product Color*'
    desc_col = 'Product Description*'

    for col in MANDATORY_COLS:
        if col not in df.columns:
            st.error(f"Mandatory column missing: '{col}'. Please correct your CSV header.")
            return None
            
    # Apply the generation ONLY if the description field is empty/missing 
    df[desc_col] = df.apply(
        lambda row: generate_description_mock(row) 
        if pd.isna(row[desc_col]) or str(row[desc_col]).strip() == "" 
        else row[desc_col], 
        axis=1
    )
    
    df[size_col] = df[size_col].fillna('').astype(str).str.replace(' ', '').str.upper().str.split(',')
    df = df[df[size_col].apply(lambda x: len(x) > 0 and x != [''])]
    df_expanded = df.explode(size_col, ignore_index=True)
    df_expanded.rename(columns={size_col: 'Size'}, inplace=True)
    
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

    df_sorted = df_expanded.sort_values(by=group_col, ascending=True)
    
    cols = list(df_sorted.columns)
    
    if 'Size' in cols:
        cols.insert(1, cols.pop(cols.index('Size')))
    if color_col in cols:
        cols.insert(2, cols.pop(cols.index(color_col)))
    if sku_col in cols:
        cols.insert(0, cols.pop(cols.index(sku_col)))

    df_sorted = df_sorted[cols]
    
    return df_sorted

# --- 4. FEATURE IMPLEMENTATION ---

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
            # Logo Display: 50x50 pixels enforcement
            logo_url = st.session_state.marketplace_logos.get(name, "")
            
            col1, col2 = st.columns([1, 6])
            with col1:
                 # Enforce 50x50 size for the logo
                 if logo_url:
                     st.image(logo_url, width=50, height=50) 
                 else:
                     st.markdown("Logo Missing")
            with col2:
                 st.markdown(f"### {name} Channel Details")

            # Pricing Inputs (Placeholder logic for demonstration)
            cost_of_product = st.number_input(f"Cost of Product (Excl. Tax) - {name}", value=100.0, min_value=0.0, key=f'{name}_cost')
            target_margin = st.slider(f"Target Margin (%) - {name}", 5, 50, 20, key=f'{name}_margin')
            
            # Mock Fee Calculation (This is highly simplified and fixed for this demo)
            if name == "Amazon":
                commission_rate = 0.12
                shipping_fee = 70.0
                channel_details = "FBA/Easy Ship"
            elif name == "Flipkart":
                commission_rate = 0.15
                shipping_fee = 65.0
                channel_details = "Smart/Standard"
            elif name == "Meesho":
                commission_rate = 0.00 # Zero Commission
                shipping_fee = 80.0
                channel_details = "Zero Commission"
            else:
                commission_rate = 0.10
                shipping_fee = 50.0
                channel_details = "Custom Marketplace"
            
            # Simple inverse calculation for selling price based on margin and mock fees
            if 1 - (target_margin/100) - commission_rate > 0:
                recommended_selling_price = (cost_of_product + shipping_fee) / (1 - (target_margin/100) - commission_rate)
            else:
                recommended_selling_price = (cost_of_product + shipping_fee) * 2 # Fallback
                
            st.write("---")
            st.subheader("Estimated Fees & Final Price")
            st.markdown(f"* Channel Model: **{channel_details}**")
            st.markdown(f"* Commission Fee ({commission_rate*100:.0f}%): **₹{cost_of_product * commission_rate:.2f}**")
            st.markdown(f"* Shipping/Service Fee: **₹{shipping_fee:.2f}**")
            st.success(f"Recommended Selling Price: **₹{recommended_selling_price:.2f}**")


def image_uploader_tab():
    st.title("🖼️ Image Uploader")
    st.info("Upload and review your product images before processing.")
    # ... (omitted for brevity, remains unchanged)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            st.success(f"Image uploaded successfully! Original size: {uploaded_file.size / (1024*1024):.2f} MB")
        except Exception as e:
            st.error(f"Error loading image: {e}")

def listing_maker_tab():
    st.title("📝 Listing Maker")
    # ... (omitted for brevity, remains unchanged)
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
            mime="text/csv"
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
                
                if st.button("Generate SKU Listings and Download"):
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
                                
                            st.dataframe(df_final.head(10), use_container_width=True)
                            
                            csv_buffer = io.StringIO()
                            df_final.to_csv(csv_buffer, index=False)
                            csv_data = csv_buffer.getvalue().encode()
                            
                            st.download_button(
                                label="Download Final SKU CSV",
                                data=csv_data,
                                file_name=f"SKU_Listings_for_{'_'.join(selected_channels)}.csv",
                                mime="text/csv"
                            )
                            st.success("Listings generated and ready for download.")

            except Exception as e:
                st.error(f"Error processing file: {e}")
                st.warning("Please ensure the uploaded file is a valid CSV and includes the correct columns.")
        
    elif channel_category == "Quick Commerce":
        st.subheader("2. Quick Commerce Integration")
        st.info("🚧 **Work in Progress:** Quick Commerce listing templates and channel integration are currently under development. Please check back later.")


def image_optimizer_tab():
    st.title("🖼️ Image Optimizer")
    st.info("Compress and resize images to improve page load times.")
    # ... (omitted for brevity, remains unchanged)
    uploaded_file = st.file_uploader("Upload Image to Optimize", type=["jpg", "jpeg", "png"], key="optimizer_uploader")
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)
                quality = st.slider("Compression Quality (0=Max, 100=Min)", 10, 95, 85)
                max_width = st.number_input("Max Width (px)", value=1000, min_value=100)
            if st.button("Optimize Image"):
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
                        mime="image/jpeg"
                    )
        except Exception as e:
            st.error(f"An error occurred during optimization: {e}")

def listing_optimizer_tab():
    st.title("📈 Listing Optimizer")
    st.info("Analyze and improve your current product listing text for better conversion and SEO.")
    # ... (omitted for brevity, remains unchanged)
    listing_text = st.text_area("Paste your current product listing description here:", height=300)
    if st.button("Analyze & Suggest Improvements"):
        if listing_text:
            st.subheader("Analysis Results (Placeholder)")
            st.markdown("* **Keyword Density:** Low")
            st.markdown("* **Readability:** Good")
            st.markdown("* **Call-to-Action:** Missing")
            st.subheader("Optimized Suggestion (Simulated)")
            st.success(listing_text.replace("product", "high-quality product listing"))
        else:
            st.warning("Please paste some listing text to analyze.")
            
def keyword_extractor_tab():
    st.title("🔍 Key Word Extractor")
    st.info("Extract relevant, high-ranking keywords from competitors or product ideas.")
    # ... (omitted for brevity, remains unchanged)
    seed_phrase = st.text_input("Enter a seed phrase or competitor's product name:")
    if st.button("Extract Keywords"):
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

def configuration_tab():
    st.title("🔧 Configuration (Admin Only)")
    if st.session_state.is_admin:
        st.success(f"Welcome Admin **{st.session_state.username}**. You have full access.")
        
        st.subheader("Interface Controls")
        
        st.session_state.show_social_icons = st.toggle(
            "Show Social Media Icons in Footer", 
            value=st.session_state.show_social_icons, 
            help="Toggle visibility of the social links in the app footer."
        )

        st.subheader("User Management (Placeholder)")
        st.table(pd.DataFrame({
            "User ID": ["Globalite", "User"],
            "Role": ["Admin", "Sub User"],
            "Status": ["Active", "Active"]
        }))
        
        st.subheader("Marketplace and Logo Management")
        st.info("Use this tool to add new marketplaces and their corresponding logo links for use in the Pricing Tool.")
        
        # --- Marketplace Name and Logo Link Adder ---
        with st.form("marketplace_adder", clear_on_submit=True):
            new_name = st.text_input("Marketplace Name (e.g., Nykaa)", key="new_mp_name").strip()
            new_logo_url = st.text_input("Logo Link/URL (e.g., https://logo.com/nykaa.png)", key="new_mp_logo").strip()
            submitted = st.form_submit_button("Add Marketplace")

            if submitted:
                if new_name and new_logo_url:
                    if new_name not in st.session_state.marketplace_logos:
                        st.session_state.marketplace_logos[new_name] = new_logo_url
                        st.success(f"Marketplace '{new_name}' added successfully! Please refresh the Pricing Tool tab.")
                    else:
                        st.warning(f"Marketplace '{new_name}' already exists.")
                else:
                    st.error("Please enter both a name and a logo link.")
        
        st.markdown("#### Current Marketplaces:")
        current_mps = pd.DataFrame(st.session_state.marketplace_logos.items(), columns=['Marketplace', 'Logo URL'])
        st.dataframe(current_mps, use_container_width=True)
        
    else:
        st.error("🛑 Access Denied. This section is for Admin access only.")

# --- 5. MAIN APP EXECUTION ---

def run_app():
    """Manages login and main application flow."""
    
    apply_custom_css()

    # --- A. LOGIN INTERFACE (User ID Only) ---
    if not st.session_state.logged_in:
        st.title("🔐 E-commerce Solution Access")
        st.info("Enter your User ID to gain access. (User IDs: 'Globalite' or 'User')")
        
        with st.form("login_form"):
            username_input = st.text_input("User ID", key="user_id_input").strip()
            submitted = st.form_submit_button("Access App")
            
            if submitted:
                if username_input in USER_ACCESS:
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.session_state.is_admin = (username_input == ADMIN_USER)
                    st.rerun() 
                else:
                    st.error("Invalid User ID.")
        
    # --- B. MAIN APPLICATION INTERFACE (After Login) ---
    else:
        # Define mapping of feature names to functions
        tabs_map = {
            "📝 Listing Maker": listing_maker_tab,
            "💰 Pricing Tool": pricing_tool_tab,
            "🖼️ Image Uploader": image_uploader_tab,
            "✨ Image Optimizer": image_optimizer_tab,
            "📈 Listing Optimizer": listing_optimizer_tab,
            "🔍 Key Word Extractor": keyword_extractor_tab,
        }
        
        if st.session_state.is_admin:
            tabs_map["🔧 Configuration (Admin)"] = configuration_tab

        # Sidebar Header
        st.sidebar.markdown(f"# **{st.session_state.username}'s Dashboard**")
        st.sidebar.markdown(f"**Role:** {USER_ACCESS.get(st.session_state.username, 'N/A')}")
        st.sidebar.markdown("---")
        
        # Sidebar Navigation
        selected_option = st.sidebar.radio("Navigation", list(tabs_map.keys()))
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_admin = False
            st.rerun()

        # Execute the function corresponding to the selected option
        tabs_map[selected_option]()

    # Display the required footer credit and social icons
    display_footer()

if __name__ == "__main__":
    run_app()

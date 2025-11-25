## main_app.py - PASSWORD REMOVED

import streamlit as st
from PIL import Image
import io
import pandas as pd
import base64

# --- 1. CONFIGURATION AND INITIAL SETUP ---
# Set the page configuration for a wider layout
st.set_page_config(
    page_title="E-commerce Solution App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Admin and Sub User Credentials (Now only storing User IDs for access control)
USER_ACCESS = {
    "Globalite": "Admin",  # Admin User
    "User": "Sub User"     # Sub User
}
ADMIN_USER = "Globalite"

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.is_admin = False
    
# --- 2. CUSTOM CSS/INTERFACE (To mimic the design aesthetic) ---

def apply_custom_css():
    """Applies custom CSS for styling (trying to match the 'Bankco' theme look)"""
    
    PRIMARY_COLOR = "#007bff" 
    BACKGROUND_COLOR = "#ffffff"
    SECONDARY_BACKGROUND_COLOR = "#f7f7f7" 
    TEXT_COLOR = "#333333"

    custom_css = f"""
    <style>
    /* Global Background and Text */
    .stApp {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{ /* Selector for the main sidebar element */
        background-color: {SECONDARY_BACKGROUND_COLOR};
    }}
    
    /* Headers/Titles */
    h1, h2, h3 {{
        color: {PRIMARY_COLOR};
        font-weight: 600;
        border-bottom: 2px solid {SECONDARY_BACKGROUND_COLOR};
        padding-bottom: 5px;
        margin-top: 15px;
    }}

    /* Primary Buttons */
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
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
        background-color: {SECONDARY_BACKGROUND_COLOR};
        color: {TEXT_COLOR};
        text-align: center;
        padding: 10px;
        font-size: 0.8em;
        border-top: 1px solid #e0e0e0;
        z-index: 100;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def display_footer():
    """Displays the required footer credit."""
    footer_html = """
    <div class="footer">
        Made in Bharat | &copy; 2025 - Formula Man. All rights reserved.
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# --- 3. FEATURE FUNCTIONS (PLACEHOLDERS) ---

def image_uploader_tab():
    st.header("🖼️ Image Uploader")
    st.info("Upload and review your product images before processing.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            st.success(f"Image uploaded successfully! Original size: {uploaded_file.size / (1024*1024):.2f} MB")
        except Exception as e:
            st.error(f"Error loading image: {e}")

def listing_maker_tab():
    st.header("📝 Listing Maker")
    st.info("Generate or manually input product details for your e-commerce platform.")
    
    product_title = st.text_input("Product Title (Required)")
    description = st.text_area("Product Description")
    category = st.selectbox("Category", ["Electronics", "Clothing", "Home Goods", "Other"])
    price = st.number_input("Price (in currency)", min_value=0.01, format="%.2f")
    
    if st.button("Generate Listing Summary"):
        if product_title:
            st.subheader("Generated Listing Preview")
            st.write(f"**Title:** {product_title}")
            st.write(f"**Category:** {category}")
            st.write(f"**Price:** ${price:.2f}")
            st.markdown(f"**Description:** \n{description}")
        else:
            st.warning("Please enter a Product Title.")

def image_optimizer_tab():
    st.header("✨ Image Optimizer")
    st.info("Compress and resize images to improve page load times.")
    
    uploaded_file = st.file_uploader("Upload Image to Optimize", type=["jpg", "jpeg", "png"], key="optimizer_uploader")
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)
                st.write(f"Size: {image.width}x{image.height}")
                
                # Optimization parameters
                quality = st.slider("Compression Quality (0=Max, 100=Min)", 10, 95, 85)
                max_width = st.number_input("Max Width (px)", value=1000, min_value=100)
                
            if st.button("Optimize Image"):
                # 1. Resize if needed
                if image.width > max_width:
                    ratio = max_width / image.width
                    new_height = int(image.height * ratio)
                    optimized_image = image.resize((max_width, new_height))
                else:
                    optimized_image = image

                # 2. Compress (to a buffer)
                buffer = io.BytesIO()
                optimized_image.save(buffer, format="JPEG", quality=quality)
                buffer.seek(0)
                
                with col2:
                    st.subheader("Optimized Image")
                    st.image(optimized_image, use_column_width=True)
                    st.success("Optimization Complete!")
                    st.write(f"New Size: {optimized_image.width}x{optimized_image.height}")
                    st.write(f"File Size: {buffer.getbuffer().nbytes / (1024*1024):.2f} MB")
                    
                    # Download button
                    st.download_button(
                        label="Download Optimized Image",
                        data=buffer,
                        file_name=f"optimized_{uploaded_file.name}",
                        mime="image/jpeg"
                    )
        except Exception as e:
            st.error(f"An error occurred during optimization: {e}")


def listing_optimizer_tab():
    st.header("📈 Listing Optimizer")
    st.info("Analyze and improve your current product listing text for better conversion and SEO.")
    
    listing_text = st.text_area("Paste your current product listing description here:", height=300)
    
    if st.button("Analyze & Suggest Improvements"):
        if listing_text:
            st.subheader("Analysis Results (Placeholder)")
            st.markdown("* **Keyword Density:** Low (Need more target keywords from Key Word Extractor)")
            st.markdown("* **Readability:** Good (Flesch-Kincaid Grade Level: 8)")
            st.markdown("* **Call-to-Action:** Missing (Suggest adding a strong CTA like 'Buy Now!')")
            
            st.subheader("Optimized Suggestion (Simulated)")
            st.success(listing_text.replace("product", "high-quality product listing"))
        else:
            st.warning("Please paste some listing text to analyze.")
            
def keyword_extractor_tab():
    st.header("🔍 Key Word Extractor")
    st.info("Extract relevant, high-ranking keywords from competitors or product ideas.")
    
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
    st.header("🔧 Configuration (Admin Only)")
    if st.session_state.is_admin:
        st.success(f"Welcome Admin **{st.session_state.username}**. You have full access.")
        st.subheader("API Key Management")
        st.text_input("OpenAI/Image Optimization API Key", disabled=True, value="No password required for this app!")
        
        st.subheader("User Management (Placeholder)")
        st.table(pd.DataFrame({
            "User ID": ["Globalite", "User"],
            "Role": ["Admin", "Sub User"],
            "Status": ["Active", "Active"]
        }))
        st.text_area("System Logs", "2025-11-25: System started. User 'Globalite' logged in.", height=150)
    else:
        st.error("🛑 Access Denied. This section is for Admin access only.")

# --- 4. MAIN APP EXECUTION ---

def run_app():
    """Manages login and main application flow."""
    
    # Apply custom styling first
    apply_custom_css()

    # --- A. LOGIN INTERFACE (User ID Only) ---
    if not st.session_state.logged_in:
        st.title("🔐 E-commerce Solution Access")
        st.info("Enter your User ID to gain access. (No password required)")
        
        with st.form("login_form"):
            username_input = st.text_input("User ID", key="user_id_input").strip() # .strip() cleans whitespace
            submitted = st.form_submit_button("Access App")
            
            if submitted:
                if username_input in USER_ACCESS:
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.session_state.is_admin = (username_input == ADMIN_USER)
                    st.success(f"Access granted! Welcome, {st.session_state.username}")
                    st.rerun() # Refresh app to show main interface
                else:
                    st.error("Invalid User ID. Please use 'Globalite' (Admin) or 'User' (Sub User).")
        
    # --- B. MAIN APPLICATION INTERFACE (After Login) ---
    else:
        # Define tabs based on access level
        tabs = [
            "🖼️ Image Uploader",
            "📝 Listing Maker",
            "✨ Image Optimizer",
            "📈 Listing Optimizer",
            "🔍 Key Word Extractor",
        ]
        
        # Only show Configuration to Admin
        if st.session_state.is_admin:
            tabs.append("🔧 Configuration (Admin)")
            
        # Sidebar Navigation
        st.sidebar.header(f"👋 Welcome, {st.session_state.username}")
        st.sidebar.markdown("---")
        selected_tab = st.sidebar.radio("Navigation", tabs)
        st.sidebar.markdown("---")
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_admin = False
            st.rerun() # Refresh to show login screen

        # --- Tab Content Routing ---
        if selected_tab == "🖼️ Image Uploader":
            image_uploader_tab()
        elif selected_tab == "📝 Listing Maker":
            listing_maker_tab()
        elif selected_tab == "✨ Image Optimizer":
            image_optimizer_tab()
        elif selected_tab == "📈 Listing Optimizer":
            listing_optimizer_tab()
        elif selected_tab == "🔍 Key Word Extractor":
            keyword_extractor_tab()
        elif selected_tab == "🔧 Configuration (Admin)":
            configuration_tab()

    # Display the required footer credit at the end
    display_footer()

if __name__ == "__main__":
    run_app()

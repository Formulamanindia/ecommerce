## main_app.py - TAB BASED INTERFACE & SOCIAL ICONS

import streamlit as st
from PIL import Image
import io
import pandas as pd
import base64

# --- 1. CONFIGURATION AND INITIAL SETUP ---
st.set_page_config(
    page_title="E-commerce Solution App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Admin and Sub User Credentials (User ID Only Access)
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
    # New state for social icon visibility
    st.session_state.show_social_icons = True 
    
# --- 2. CUSTOM CSS/INTERFACE ---

def apply_custom_css():
    """Applies custom CSS for styling and social icon display."""
    
    PRIMARY_COLOR = "#007bff" 
    BACKGROUND_COLOR = "#ffffff"
    SECONDARY_BACKGROUND_COLOR = "#f7f7f7" 
    TEXT_COLOR = "#333333"

    custom_css = f"""
    <style>
    /* Global Styling */
    .stApp {{ background-color: {BACKGROUND_COLOR}; color: {TEXT_COLOR}; }}
    .css-1d391kg {{ background-color: {SECONDARY_BACKGROUND_COLOR}; }}
    h1, h2, h3 {{ color: {PRIMARY_COLOR}; font-weight: 600; border-bottom: 2px solid {SECONDARY_BACKGROUND_COLOR}; padding-bottom: 5px; margin-top: 15px; }}
    
    /* Primary Buttons */
    .stButton>button {{ background-color: {PRIMARY_COLOR}; color: white; border: none; padding: 10px 20px; border-radius: 5px; transition: background-color 0.3s; }}
    .stButton>button:hover {{ background-color: #0056b3; }}
    
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
    .social-icons a {{
        color: {PRIMARY_COLOR};
        margin: 0 10px;
        font-size: 1.2em;
        text-decoration: none;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def display_footer():
    """Displays the required footer credit and social icons."""
    
    # Simple social icons using emojis and basic HTML structure
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
        Made in Bharat | &copy; 2025 - Formula Man. All rights reserved.
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# --- 3. FEATURE FUNCTIONS (UNCHANGED FUNCTIONALITY) ---

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
                    st.write(f"File Size: {buffer.getbuffer().nbytes / (1024*1024):.2f} MB")
                    
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
            st.markdown("* **Keyword Density:** Low")
            st.markdown("* **Readability:** Good")
            st.markdown("* **Call-to-Action:** Missing")
            
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
        
        st.subheader("Interface Controls")
        
        # Admin control to show/hide social icons
        st.session_state.show_social_icons = st.toggle(
            "Show Social Media Icons in Footer", 
            value=st.session_state.show_social_icons, 
            help="Toggle visibility of the Twitter, LinkedIn, and GitHub links in the app footer."
        )

        st.subheader("User Management (Placeholder)")
        st.table(pd.DataFrame({
            "User ID": ["Globalite", "User"],
            "Role": ["Admin", "Sub User"],
            "Status": ["Active", "Active"]
        }))
    else:
        st.error("🛑 Access Denied. This section is for Admin access only.")

# --- 4. MAIN APP EXECUTION ---

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
                    # We use st.switch_page or st.rerun() here to transition to the main app view
                    st.rerun() 
                else:
                    st.error("Invalid User ID.")
        
    # --- B. MAIN APPLICATION INTERFACE (After Login) ---
    else:
        st.sidebar.header(f"👋 Welcome, {st.session_state.username}")
        st.sidebar.markdown(f"**Access Level:** {USER_ACCESS.get(st.session_state.username, 'N/A')}")
        st.sidebar.markdown("---")
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_admin = False
            st.rerun()

        # Define tabs list dynamically, ensuring Admin tab is last
        tabs_list = [
            "Image Uploader",
            "Listing Maker",
            "Image Optimizer",
            "Listing Optimizer",
            "Key Word Extractor",
        ]
        if st.session_state.is_admin:
            tabs_list.append("Configuration (Admin)")

        # Create the tabs
        tab_uploader, tab_listing_maker, tab_img_opt, tab_list_opt, tab_keywords, *optional_tab = st.tabs(tabs_list)

        # --- Tab Content Routing ---
        with tab_uploader:
            image_uploader_tab()
        with tab_listing_maker:
            listing_maker_tab()
        with tab_img_opt:
            image_optimizer_tab()
        with tab_list_opt:
            listing_optimizer_tab()
        with tab_keywords:
            keyword_extractor_tab()
        
        # Configuration tab is only visible and accessible if the user is Admin
        if st.session_state.is_admin and optional_tab:
            with optional_tab[0]:
                configuration_tab()

    # Display the required footer credit and social icons
    display_footer()

if __name__ == "__main__":
    run_app()

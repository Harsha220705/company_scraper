"""
Company Scraper UI - Streamlit Application
Web interface for the company scraper tool.
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from company_scrapper.runner import run

# Page configuration
st.set_page_config(
    page_title="Company Scraper",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-section">
    <h1>🕷️ Company Web Scraper</h1>
    <p>Extract detailed company information from any website</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for input
with st.sidebar:
    st.header("⚙️ Scraper Settings")
    
    website_url = st.text_input(
        "Enter Company Website URL",
        value="https://www.notion.so",
        placeholder="https://example.com"
    )
    
    if website_url and not website_url.startswith("http"):
        website_url = "https://" + website_url
    
    scrape_button = st.button("🚀 Start Scraping", use_container_width=True)
    
    st.divider()
    
    # Display recent scrapes
    st.subheader("📁 Recent Scrapes")
    examples_dir = Path(__file__).parent / "examples"
    if examples_dir.exists():
        json_files = sorted(examples_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        if json_files:
            for idx, json_file in enumerate(json_files[:5]):
                # Extract company name from JSON file
                try:
                    with open(json_file) as f:
                        file_data = json.load(f)
                        company_name = file_data.get("identity", {}).get("company_name", json_file.stem)
                except:
                    company_name = json_file.stem
                
                # Use unique key for each button
                if st.button(f"📄 {company_name}", use_container_width=True, key=f"recent_scrape_{idx}"):
                    with open(json_file) as f:
                        st.session_state.last_result = json.load(f)
        else:
            st.info("No previous scrapes found")
    else:
        st.info("Examples folder not found")

# Main content
if scrape_button and website_url:
    with st.spinner("🔍 Scraping website... This may take a minute..."):
        try:
            result = run(website_url)
            st.session_state.last_result = result
            
            # Save to examples folder
            examples_dir = Path(__file__).parent / "examples"
            examples_dir.mkdir(exist_ok=True)
            
            company_name = result['identity']['company_name'].lower().replace(" ", "_").replace("/", "_")
            filename = f"{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = examples_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=2)
            
            st.success(f"✅ Saved to: examples/{filename}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display results if available
if "last_result" in st.session_state:
    result = st.session_state.last_result
    
    # Company Identity Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Company Name",
            result["identity"]["company_name"]
        )
    
    with col2:
        st.metric(
            "Pages Crawled",
            result["metadata"]["pages_crawled"]
        )
    
    with col3:
        st.metric(
            "Timestamp",
            result["metadata"]["timestamp"].split("T")[0]
        )
    
    # Raw JSON Data - moved to top
    with st.expander("📊 View Raw JSON Data"):
        st.json(result)
    
    st.divider()
    
    # Website and Tagline
    st.subheader("📋 Company Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Website:** {result['identity']['website']}")
    
    with col2:
        if result["identity"]["tagline"]:
            st.success(f"**Tagline:** {result['identity']['tagline']}")
    
    # What They Do
    st.subheader("📝 What They Do")
    description = result["description"]
    if len(description) > 500:
        with st.expander("View Full Description"):
            st.write(description)
        st.write(description[:500] + "...")
    else:
        st.write(description)
    
    st.divider()
    
    # Business Information
    st.subheader("💼 Business Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Pricing")
        pricing = result["business_info"]["pricing"]
        if pricing:
            st.write(f"**Tiers:** {', '.join(pricing['tiers']) if pricing['tiers'] else 'N/A'}")
            st.write(f"**Prices:** {', '.join(pricing['prices'][:2]) if pricing['prices'] else 'N/A'}")
            st.write(f"**Free Option:** {'✅ Yes' if pricing['free_option'] else '❌ No'}")
            st.write(f"**Trial:** {'✅ Yes' if pricing['trial_available'] else '❌ No'}")
        else:
            st.info("No pricing information found")
    
    with col2:
        st.subheader("👥 Target Customers")
        if result["business_info"]["target_customers"]:
            for customer in result["business_info"]["target_customers"][:8]:
                st.write(f"• {customer}")
        else:
            st.info("No customer info found")
    
    with col3:
        st.subheader("🛠️ Services")
        if result["business_info"]["services"]:
            for service in result["business_info"]["services"][:5]:
                st.write(f"• {service}")
        else:
            st.info("No services found")
    
    st.divider()
    
    # Contact Information
    st.subheader("📞 Contact Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Emails:**")
        if result["contacts"]["emails"]:
            for email in result["contacts"]["emails"]:
                st.write(f"📧 {email}")
        else:
            st.info("No emails found")
    
    with col2:
        st.write("**Phone Numbers:**")
        if result["contacts"]["phones"]:
            for phone in result["contacts"]["phones"]:
                st.write(f"☎️ {phone}")
        else:
            st.info("No phone numbers found")
    
    st.divider()
    
    # Social Links
    st.subheader("🔗 Social Media Links")
    
    cols = st.columns(min(5, len(result["social_links"])) if result["social_links"] else 1)
    
    if result["social_links"]:
        for idx, (platform, link) in enumerate(result["social_links"].items()):
            with cols[idx % len(cols)]:
                st.write(f"**{platform.upper()}**")
                st.write(f"[Visit →]({link})")
    else:
        st.info("No social links found")
    
    st.divider()
    
    # Pages Visited
    st.subheader("📄 Pages Visited")
    
    for idx, page in enumerate(result["key_pages"]["visited"], 1):
        st.write(f"{idx}. [{page}]({page})")
    
    st.divider()
    # Download button
    json_str = json.dumps(result, indent=2)
    st.download_button(
        label="📥 Download JSON",
        data=json_str,
        file_name=f"{result['identity']['company_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

else:
    st.info("👈 Enter a website URL in the sidebar and click 'Start Scraping' to begin!")

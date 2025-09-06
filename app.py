import streamlit as st
import pyshorteners
import validators
import qrcode
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="QuickLink Shortener",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* General Body Styling */
    body {
        background-color: #f0f2f6; /* Fallback color */
    }
    
    /* Main container with glassmorphism effect */
    .main-container {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8.5px);
        -webkit-backdrop-filter: blur(8.5px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Styling for the output box */
    .output-box {
        background-color: #e8e8e8;
        border-left: 5px solid #1E90FF;
        padding: 10px 20px;
        border-radius: 8px;
        margin-top: 1rem;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
    }
    
    /* Styling for buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #1E90FF;
        background-color: #1E90FF;
        color: white;
    }
    .stButton>button:hover {
        background-color: #0073e6;
        color: white;
        border: 1px solid #0073e6;
    }

</style>
""", unsafe_allow_html=True)


# --- App Header ---
st.title("✨ QuickLink URL Shortener")
st.markdown("Transform long, cumbersome URLs into short, shareable links in an instant!")


# --- Main Application Logic ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    with st.form("shorten_form"):
        long_url = st.text_input(
            "Enter your long URL here",
            placeholder="https://example.com/a-very-long-and-complex-url",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("Generate Short Link")

    if submitted and long_url:
        if not validators.url(long_url):
            st.error("Please enter a valid URL, including http:// or https://")
        else:
            with st.spinner("Creating your magic link..."):
                try:
                    # Initialize the shortener and shorten the URL
                    s = pyshorteners.Shortener()
                    short_url = s.tinyurl.short(long_url)

                    st.success("Success! Your link is ready.")

                    # Display the shortened URL in a styled box
                    st.markdown(f'<div class="output-box">{short_url}</div>', unsafe_allow_html=True)

                    # Generate QR code
                    qr_img = qrcode.make(short_url)
                    buf = BytesIO()
                    qr_img.save(buf, format="PNG")
                    byte_im = buf.getvalue()

                    col1, col2 = st.columns([1, 0.4])

                    with col1:
                        # Add a download button for the QR code
                        st.download_button(
                            label="Download QR Code",
                            data=byte_im,
                            file_name="shortlink_qr.png",
                            mime="image/png"
                        )
                    with col2:
                        # Add a button to go to the URL
                        st.link_button("Visit Link", short_url)

                    # Display QR Code
                    st.image(byte_im, caption="Scan me!", width=150)

                except Exception as e:
                    st.error(f"Could not shorten the URL. Please try again. Error: {e}")

    elif submitted:
        st.warning("You forgot to enter a URL!")

    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown(
    """
    <div style='text-align: center; color: grey; margin-top: 2rem;'>
        <p>Created by Shubh with Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)


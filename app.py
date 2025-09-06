import streamlit as st
import pyshorteners
import validators
import qrcode
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="QuickLinkz",
    page_icon="🔗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Initialize Session State for History ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Custom CSS for Advanced Styling ---
st.markdown("""
<style>
    /* Animated Gradient Background */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    /* Main container with glassmorphism effect */
    .main-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #FFFFFF; /* White text for better contrast */
    }

    /* Make titles and text more visible on the gradient */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #FFFFFF !important;
    }
    .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Styling for the output box */
    .output-box {
        background-color: rgba(0, 0, 0, 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 5px solid #00FF7F; /* Bright green accent */
    }

    /* Style the text area to show the link */
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 1.1rem;
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }

</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.title("🔗 QuickLinkz")
st.markdown("Your friendly link shortening assistant. Create clean, memorable links in seconds.")

# --- Main Application Form ---
with st.form("shorten_form"):
    long_url = st.text_input(
        "Enter a long URL to shorten",
        placeholder="https://www.example.com/...",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("✨ Shorten It!")

# --- Logic for Shortening and Displaying ---
if submitted and long_url:
    if not validators.url(long_url):
        st.error("Oops! That doesn't look like a valid URL. Please include http:// or https://")
    else:
        with st.spinner("Brewing your short link..."):
            try:
                s = pyshorteners.Shortener()
                short_url = s.tinyurl.short(long_url)
                
                # Add to history
                st.session_state.history.insert(0, {"long": long_url, "short": short_url})

                # --- Display Results ---
                st.success("Your short link is ready!")
                
                st.text_area(
                    "Shortened URL (easy to copy)",
                    short_url,
                    height=50,
                    disabled=True,
                    label_visibility="collapsed",
                )
                
                # --- QR Code Section ---
                with st.expander("📲 Get QR Code"):
                    qr_img = qrcode.make(short_url)
                    buf = BytesIO()
                    qr_img.save(buf, format="PNG")
                    byte_im = buf.getvalue()

                    st.image(byte_im, caption="Scan me!", width=120)
                    st.download_button(
                        label="Download QR Code",
                        data=byte_im,
                        file_name=f"qr_code_{short_url.split('/')[-1]}.png",
                        mime="image/png"
                    )

            except Exception as e:
                st.error(f"Something went wrong. Please try again. Details: {e}")
elif submitted:
    st.warning("Please enter a URL first!")

st.markdown('</div>', unsafe_allow_html=True)


# --- History Section ---
if st.session_state.history:
    st.markdown("<div class='main-container' style='margin-top: 2rem;'>", unsafe_allow_html=True)
    st.subheader("📜 Your Recent Links")
    for item in st.session_state.history:
        with st.container():
            st.markdown(f"**Original:** `{item['long']}`")
            st.markdown(f"**Short:** <span class='output-box' style='display:inline-block; padding: 5px 10px;'>{item['short']}</span>", unsafe_allow_html=True)
            st.divider()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown(
    "<div style='text-align: center; color: white; margin-top: 2rem; font-weight: bold;'>"
    "<p>Made with ❤️ by Shubh</p>"
    "</div>",
    unsafe_allow_html=True
)


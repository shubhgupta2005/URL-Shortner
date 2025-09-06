import streamlit as st
import pyshorteners
import validators

# Set the page configuration for a cleaner look
st.set_page_config(page_title="URL Shortener", page_icon="🔗", layout="centered")

# --- UI Elements ---
st.title("🔗 URL Shortener")
st.markdown("Enter a long URL below to make it short and easy to share.")

# Using a form for better control
with st.form("shorten_form"):
    long_url = st.text_input(
        "Enter your long URL",
        placeholder="https://example.com/very/long/url/to/shorten",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Shorten URL")

# --- Logic ---
if submitted and long_url:
    # Validate the URL to make sure it's a real web address
    if not validators.url(long_url):
        st.error("Invalid URL. Please enter a valid and complete URL (e.g., https://www.google.com)")
    else:
        try:
            # Initialize the shortener (TinyURL is a good choice as it requires no API key)
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(long_url)

            st.success("Here is your shortened URL:")

            # Display the shortened URL in a way that's easy to copy
            st.code(short_url, language="text")

            # Add a button to copy the URL to the clipboard
            st.link_button("Go to Short URL", short_url)

        except Exception as e:
            st.error(f"An error occurred: {e}")
elif submitted:
    st.warning("Please enter a URL to shorten.")

# --- Footer ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: gray;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>A simple app by Shubh</p>
    </div>
    """,
    unsafe_allow_html=True
)

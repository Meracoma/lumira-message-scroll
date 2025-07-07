# --- Filter Scrolls ---
from filters import filter_by_category, filter_by_name, filter_by_keyword

st.markdown("---")
st.subheader("🔍 Filter Scrolls")

filter_option = st.selectbox("Filter by", ["All", "Category", "Name", "Keyword"])
filter_input = st.text_input("Enter filter value (if applicable):", "")

# Load all messages
messages = load_messages()

# Apply selected filter
if filter_option == "Category":
    messages = filter_by_category(messages, filter_input)
elif filter_option == "Name":
    messages = filter_by_name(messages, filter_input)
elif filter_option == "Keyword":
    messages = filter_by_keyword(messages, filter_input)

# Display messages
for entry in reversed(messages[-50:]):  # Show last 50 scrolls
    st.markdown(parse_markdown(entry), unsafe_allow_html=True)
    st.markdown("---")# Streamlit app with image upload and tag filtering - v0.4

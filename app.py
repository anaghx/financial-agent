import streamlit as st
from agent import get_country_financial_data

st.set_page_config(page_title="Global Financial Agent", layout="wide")

st.title("🌍 Global Financial Intelligence Agent")

country = st.text_input("Enter Country Name")

if st.button("Get Details"):
    if country:
        data = get_country_financial_data(country)

        if isinstance(data, str):
            st.error(data)
        else:
            st.subheader(f"📍 {data['country']}")

            col1, col2 = st.columns(2)

            # LEFT COLUMN
            with col1:
                st.write("### 💰 Official Currency")
                st.success(data["currency"])

                st.write("### 🔄 Exchange Rates (1 Unit →)")
                rates = data["exchange_rates"]
                st.write(f"USD: {rates['USD']}")
                st.write(f"INR: {rates['INR']}")
                st.write(f"GBP: {rates['GBP']}")
                st.write(f"EUR: {rates['EUR']}")

                st.write("### 📈 Stock Exchange")
                st.info(data["stock_exchange"])

                st.write("### 📊 Index Value")
                st.write("### 📊 Index Value")

                if isinstance(data["index_value"], float):
                    st.write(f"{data['index_symbol']} : {round(data['index_value'], 2)}")
                else:
                    st.warning(data["index_value"])


            # RIGHT COLUMN
            with col2:
                st.write("### 🗺 Stock Exchange Location")

                map_query = data["stock_exchange"].replace(" ", "+")
                map_url = f"https://www.google.com/maps?q={map_query}&output=embed"

                st.markdown(
                    f'<iframe width="100%" height="400" src="{map_url}"></iframe>',
                    unsafe_allow_html=True
                )

    else:
        st.warning("Please enter a country name.")

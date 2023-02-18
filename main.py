import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="SALES_2022.xlsx",
        sheet_name="Продажи",
        engine="openpyxl",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    df["source/medium"] = df["utm_source"] + "/" + df["utm_medium"]
    df[['date', 'time']] = df["Время и дата подачи заявки"].str.split(" ", 1).tolist()
    df.drop("Время и дата подачи заявки", axis=1)
    # Add 'hour' column to dataframe

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
get_data_from_excel = st.sidebar.multiselect(
    "Выбрать дату:",
    options=df["Время и дата подачи заявки"].unique(),
    default=df["Время и дата подачи заявки"].unique()
)

source_medium = st.sidebar.multiselect(
    "Select the Source/Medium Type:",
    options=df["source/medium"].unique(),
    default=df["source/medium"].unique(),
)

traffic = st.sidebar.multiselect(
    "Sort by traffic:",
    options=df["utm_source"].unique(),
    default=df["utm_source"].unique()
)

df_selection = df.query(
    "data == @c & Customer_type ==@customer_type & Gender == @gender"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Количество единиц услуги"].sum())
average_rating = round(df_selection["Стоимость услуги"].mean(), 1)
#star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_day = df_selection.groupby(by=["date"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_day,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
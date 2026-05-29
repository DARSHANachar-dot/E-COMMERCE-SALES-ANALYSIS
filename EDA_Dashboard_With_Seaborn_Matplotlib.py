
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Advanced EDA Dashboard", layout="wide")

st.markdown("""
<h1 style='text-align:center; color:#00FFFF;'>
Advanced Interactive EDA Dashboard
</h1>
""", unsafe_allow_html=True)

st.sidebar.title("Dashboard Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

theme = st.sidebar.selectbox(
    "Select Theme",
    ["plotly_dark", "plotly", "ggplot2"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Dataset Uploaded Successfully")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Information")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicates", int(df.duplicated().sum()))

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    st.sidebar.subheader("Visualization Filters")

    chart_type = st.sidebar.selectbox(
        "Select Chart",
        [
            "Histogram",
            "Scatter Plot",
            "Line Chart",
            "Box Plot",
            "Pie Chart",
            "Correlation Heatmap",
            "Treemap",
            "Seaborn Pairplot",
            "Seaborn Countplot",
            "Seaborn Violin Plot",
            "Matplotlib Histogram",
            "Matplotlib Scatter"
        ]
    )

    if chart_type == "Histogram":
        if numeric_cols:
            col = st.selectbox("Select Numeric Column", numeric_cols)
            fig = px.histogram(df, x=col, nbins=30, template=theme)
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot":
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("Select X-axis", numeric_cols)
            y_col = st.selectbox("Select Y-axis", numeric_cols, index=1)

            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                color=y_col,
                size=y_col,
                template=theme
            )
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line Chart":
        if numeric_cols:
            x_col = st.selectbox("Select X-axis", df.columns)
            y_col = st.selectbox("Select Y-axis", numeric_cols)

            fig = px.line(df, x=x_col, y=y_col, template=theme)
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        if numeric_cols:
            col = st.selectbox("Select Column", numeric_cols)
            fig = px.box(df, y=col, template=theme)
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart":
        if cat_cols:
            col = st.selectbox("Select Categorical Column", cat_cols)
            pie_data = df[col].value_counts().reset_index()
            pie_data.columns = [col, "Count"]

            fig = px.pie(
                pie_data,
                names=col,
                values="Count",
                template=theme
            )
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Correlation Heatmap":
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            fig = px.imshow(
                corr,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu"
            )
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Treemap":
        if cat_cols and numeric_cols:
            fig = px.treemap(
                df,
                path=[cat_cols[0]],
                values=numeric_cols[0]
            )
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- SEABORN ----------------

    elif chart_type == "Seaborn Pairplot":
        if len(numeric_cols) >= 2:
            selected_cols = st.multiselect(
                "Select Numeric Columns",
                numeric_cols,
                default=numeric_cols[:3]
            )

            if len(selected_cols) >= 2:
                pair_fig = sns.pairplot(df[selected_cols])
                st.pyplot(pair_fig.figure)

    elif chart_type == "Seaborn Countplot":
        if cat_cols:
            col = st.selectbox("Select Category Column", cat_cols)

            fig, ax = plt.subplots(figsize=(8, 5))
            sns.countplot(data=df, x=col, ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    elif chart_type == "Seaborn Violin Plot":
        if numeric_cols:
            num_col = st.selectbox("Select Numeric Column", numeric_cols)

            fig, ax = plt.subplots(figsize=(8, 5))
            sns.violinplot(y=df[num_col], ax=ax)
            st.pyplot(fig)

    # ---------------- MATPLOTLIB ----------------

    elif chart_type == "Matplotlib Histogram":
        if numeric_cols:
            col = st.selectbox("Select Numeric Column", numeric_cols)

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(df[col], bins=30)
            ax.set_title(f"Histogram of {col}")
            st.pyplot(fig)

    elif chart_type == "Matplotlib Scatter":
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("Select X Column", numeric_cols)
            y_col = st.selectbox("Select Y Column", numeric_cols, index=1)

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(df[x_col], df[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{x_col} vs {y_col}")
            st.pyplot(fig)

    st.subheader("Data Types")
    st.write(df.dtypes)

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    if numeric_cols:
        st.subheader("Statistical Summary")
        st.write(df[numeric_cols].describe())

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a dataset from the sidebar.")

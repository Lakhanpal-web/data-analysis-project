import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# App Title
st.title("📊 Stock Market Analysis Dashboard for Nifty 50")

# Directory containing datasets
DATA_DIR = "data"

# Load datasets from the folder
if os.path.exists(DATA_DIR):
    # List all CSV files in the `data` folder
    dataset_files = [file for file in os.listdir(DATA_DIR) if file.endswith(".csv")]
    
    if dataset_files:
        # Sidebar to select a dataset
        st.sidebar.header("Select Dataset")
        selected_file = st.sidebar.selectbox("Choose a dataset", dataset_files)
        
        # Load the selected dataset
        file_path = os.path.join(DATA_DIR, selected_file)
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            st.error(f"Error loading the file: {e}")
            st.stop()

        st.success(f"Dataset '{selected_file}' successfully loaded!")

        # Validate dataset
        if df.empty:
            st.warning("The selected dataset is empty. Please check the file.")
            st.stop()

        st.subheader(f"Dataset Overview - {selected_file}")
        st.write("**First 5 Rows:**")
        try:
            st.dataframe(df.head(), use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying the data: {e}")
            st.stop()

        # Missing Data Check
        st.subheader("🔍 Missing Data Check")
        missing_data = df.isnull().sum().reset_index()
        missing_data.columns = ["Column", "Missing Values"]
        st.dataframe(missing_data, use_container_width=True)

        # Descriptive Statistics
        st.subheader("📈 Descriptive Statistics")
        try:
            st.write(df.describe())
        except Exception as e:
            st.error(f"Error generating descriptive statistics: {e}")

        # Sidebar Controls for Visualizations
        st.sidebar.header("Visualization Options")
        show_close_price = st.sidebar.checkbox("Show Closing Price Over Time", value=True)
        show_volume = st.sidebar.checkbox("Show Volume Over Time", value=True)
        show_correlation = st.sidebar.checkbox("Show Correlation Heatmap", value=True)
        custom_analysis = st.sidebar.checkbox("Enable Custom Column Analysis", value=True)

        # Visualization - Closing Price Over Time
        if show_close_price and "Date" in df.columns and "Close" in df.columns:
            try:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                st.subheader("📉 Closing Price Over Time")
                fig = px.line(
                    df,
                    x="Date",
                    y="Close",
                    title="Closing Price Over Time",
                    labels={"Close": "Closing Price", "Date": "Date"},
                    template="plotly_dark",
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Unable to display closing price over time: {e}")

        # Visualization - Volume Over Time
        if show_volume and "Date" in df.columns and "Volume" in df.columns:
            try:
                st.subheader("📊 Volume Over Time")
                fig = px.bar(
                    df,
                    x="Date",
                    y="Volume",
                    title="Volume Over Time",
                    labels={"Volume": "Volume", "Date": "Date"},
                    template="plotly",
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Unable to display volume over time: {e}")

        # Correlation Heatmap
        if show_correlation:
            try:
                st.subheader("📊 Correlation Heatmap")
                numerical_data = df.select_dtypes(include=["float64", "int64"])
                if numerical_data.empty:
                    st.warning("No numerical data available for correlation heatmap.")
                else:
                    corr = numerical_data.corr()
                    fig = go.Figure(
                        data=go.Heatmap(
                            z=corr.values,
                            x=corr.columns,
                            y=corr.columns,
                            colorscale="Viridis",
                            hoverongaps=False,
                        )
                    )
                    fig.update_layout(
                        title="Correlation Heatmap",
                        xaxis_title="Features",
                        yaxis_title="Features",
                        template="plotly_dark",
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating correlation heatmap: {e}")

        # Custom Column Analysis
       # Custom Column Analysis
if custom_analysis:
    try:
        st.subheader("🔎 Custom Column Analysis")
        st.write("Create a line chart by selecting the x-axis and y-axis columns.")
        
        # Dropdowns for selecting columns
        x_column = st.selectbox("Select X-axis column", df.columns, key="x_axis")
        y_column = st.selectbox("Select Y-axis column", df.columns, key="y_axis")

        if x_column and y_column:
            # Line Chart
            st.write(f"**Line Chart of {y_column} vs {x_column}:**")
            fig = px.line(
                df,
                x=x_column,
                y=y_column,
                title=f"Line Chart: {y_column} vs {x_column}",
                labels={x_column: x_column, y_column: y_column},
                template="plotly",
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error during custom column analysis: {e}")

    else:
        st.warning(f"No datasets found in the '{DATA_DIR}' directory. Please add CSV files.")
else:
    st.error(f"The directory '{DATA_DIR}' does not exist. Please create it and add your datasets.")
    
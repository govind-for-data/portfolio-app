import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

def show():
    st.set_page_config(page_title="Data Explorer", layout="wide")

    # ---------- Config ----------
    DEFAULT_SQL_VIEW = "dbo.Device_Inventory_View"  # change per your DB
    DATE_COL = "Purchase_date"  # change per your data

    # ---------- Helpers ----------
    @st.cache_data(ttl=600)
    def get_engine():
        # Use env vars: MSSQL_DSN or host/port/credentials
        # Example DSN conn string (recommended): "mssql+pyodbc://@MyDSN"
        dsn = os.getenv("MSSQL_DSN")
        if dsn:
            return create_engine(dsn)
        host = os.getenv("MSSQL_HOST", "192.168.1.5,21443")
        db   = os.getenv("MSSQL_DB", "Asset_CMDB")
        user = os.getenv("MSSQL_USER")
        pwd  = os.getenv("MSSQL_PASSWORD")
        driver = os.getenv("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")
        if user and pwd:
            return create_engine(f"mssql+pyodbc://{user}:{pwd}@{host}/{db}?driver={driver}")
        return create_engine(f"mssql+pyodbc://{host}/{db}?driver={driver}&trusted_connection=yes")

    @st.cache_data(ttl=600)
    def load_sql(view_name: str, date_from=None, date_to=None, search_col=None, search_text=None, extra_filters=None):
        where = []
        params = {}
        if date_from:
            where.append(f"{DATE_COL} >= :dfrom")
            params["dfrom"] = pd.to_datetime(date_from)
        if date_to:
            where.append(f"{DATE_COL} < :dto")
            params["dto"] = pd.to_datetime(date_to) + pd.Timedelta(days=1)
        if search_col and search_text:
            where.append(f"{search_col} LIKE :q")
            params["q"] = f"%{search_text}%"
        if extra_filters:
            for col, val in extra_filters.items():
                if val not in (None, "", "All"):
                    where.append(f"{col} = :{col}")
                    params[col] = val

        sql = f"SELECT * FROM {view_name}"
        if where:
            sql += " WHERE " + " AND ".join(where)

        with get_engine().connect() as conn:
            return pd.read_sql(text(sql), conn, params=params)

    def load_file(uploaded):
        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        # Best-effort type fix for dates:
        if DATE_COL in df.columns:
            df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
        return df

    def safe_int(x):
        try: return int(x)
        except: return x

    # ---------- UI ----------
    st.title("🔍 Data Explorer")

    # @st.dialog("Select Data Source")
    # def data_source_dialog():
    #     choice = st.radio("Data source", ["MS SQL (view)", "Upload file"])
    #     if st.button("Confirm"):
    #         st.session_state["data_source"] = choice
    #     st.rerun()
    #     return(choice)    

    # # Button to trigger the dialog
    # if st.button("Open Data Source Selector"):
    #     data_source_dialog()

    st.write("Selected:", st.session_state.get("data_source", "Not chosen yet"))
    src = st.sidebar.radio("Data source", ["MS SQL (view)", "Upload file"], horizontal=True)
    if src == "MS SQL (view)":
        view = st.sidebar.text_input("SQL View/Table", value=DEFAULT_SQL_VIEW)
        date_range = st.sidebar.date_input("Date range (optional)", [])
        date_from, date_to = (date_range[0], date_range[1]) if len(date_range) == 2 else (None, None)
        search_col = st.sidebar.text_input("Search column (optional)")
        search_txt = st.sidebar.text_input("Search text (optional)")
    else:
        uploaded = st.sidebar.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])
        date_range = st.sidebar.date_input("Date range (optional)", [])
        date_from, date_to = (date_range[0], date_range[1]) if len(date_range) == 2 else (None, None)
        search_col = st.sidebar.text_input("Search column (optional)")
        search_txt = st.sidebar.text_input("Search text (optional)")

    with st.spinner("Loading data..."):
        try:
            if src == "MS SQL (view)":
                df = load_sql(view, date_from, date_to, search_col, search_txt, extra_filters=None)
            else:
                if not uploaded:
                    st.info("Upload a file to explore.")
                    st.stop()
                df = load_file(uploaded)
                # Apply optional client-side filters
                if date_from or date_to:
                    if DATE_COL in df.columns:
                        m = pd.Series(True, index=df.index)
                        if date_from: m &= df[DATE_COL] >= pd.to_datetime(date_from)
                        if date_to:   m &= df[DATE_COL] < (pd.to_datetime(date_to) + pd.Timedelta(days=1))
                        df = df[m]
                if search_col and search_txt and search_col in df.columns:
                    df = df[df[search_col].astype(str).str.contains(search_txt, case=False, na=False)]
        except Exception:
            st.error("⚠️ Could not load data. Please check the view/file and filters.")
            st.stop()

    if df.empty:
        st.warning("No rows found for the selected criteria.")
        st.stop()

    # Quick KPIs
    left, mid, right = st.columns(3)
    with left:  st.metric("Rows", f"{len(df):,}")
    with mid:   st.metric("Columns", f"{df.shape[1]:,}")
    with right: st.metric("Distinct Devices (if column exists)", df["Serial_number"].nunique() if "Serial_number" in df else "—")

    st.dataframe(df, use_container_width=True)

    # Download
    st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"), "data_explorer.csv", "text/csv")

import os
import pandas as pd
import streamlit as st
import io, json, os
import numpy as np
from pandas import json_normalize
from datetime import timedelta

def show():
    
    st.set_page_config(page_title="Data Explorer", layout="wide")

    # ---------- Config ----------
    DATE_COL_GUESS = None  # put "Purchase_date" if you want a default
    DOWNLOAD_NAME = "data_explorer.csv"

    # ---------- Helpers ----------
    def _coerce_dates(df: pd.DataFrame, date_col_hint: str | None):
        # try explicit hint first, then any column that looks like a date
        candidates = []
        if date_col_hint and date_col_hint in df.columns:
            candidates.append(date_col_hint)
        candidates += [c for c in df.columns if "date" in c.lower() or c.lower().endswith("_at")]
        seen = set()
        for c in candidates:
            if c in seen or c not in df.columns:
                continue
            seen.add(c)
            try:
                df[c] = pd.to_datetime(df[c], errors="coerce")
            except Exception:
                pass
        return df

    def _flatten_json(obj):
        """
        Accepts: dict, list[dict], or mixed JSON.
        Returns: DataFrame flattened on best-effort basis.
        """
        if isinstance(obj, list):
            # list of records or values
            if len(obj) == 0:
                return pd.DataFrame()
            if isinstance(obj[0], dict):
                return json_normalize(obj, max_level=1)
            # list of scalars -> wrap
            return pd.DataFrame({"value": obj})
        elif isinstance(obj, dict):
            # Try common record/records shapes
            for key in ["data", "items", "results", "records"]:
                if key in obj and isinstance(obj[key], list):
                    return json_normalize(obj[key], max_level=1)
            # Single object -> one-row frame
            return json_normalize(obj, max_level=1)
        else:
            # fallback: raw value
            return pd.DataFrame({"value": [obj]})

    def load_json_from_file(uploaded_file):
        raw = uploaded_file.read()
        # Allow JSON Lines too
        txt = raw.decode("utf-8", errors="ignore")
        try:
            # try standard JSON first
            parsed = json.loads(txt)
            return _flatten_json(parsed)
        except json.JSONDecodeError:
            # try JSON Lines
            buf = io.StringIO(txt)
            try:
                df = pd.read_json(buf, lines=True)
                return df
            except Exception as e:
                raise ValueError("Not valid JSON or JSONL") from e

    def load_json_from_url(url: str):
        # No external requests if you’re sandboxed; in real app use requests.get(url).json()
        import requests  # ensure this is in your env
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        payload = r.json()
        return _flatten_json(payload)

    def apply_date_filter(df, date_col, date_from, date_to):
        if not date_col or date_col not in df.columns:
            return df
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            # if not datetime yet, try to parse
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        mask = pd.Series(True, index=df.index)
        if date_from: mask &= df[date_col] >= pd.to_datetime(date_from)
        if date_to:   mask &= df[date_col] < (pd.to_datetime(date_to) + pd.Timedelta(days=1))
        return df[mask]

    # ---------- UI ----------
    st.title("🔍 Data Explorer (JSON-friendly)")

    src = st.sidebar.radio("Data source", ["JSON (file/url)", "CSV/XLSX (file)"], horizontal=True)

    # Common filter controls
    date_hint = st.sidebar.text_input("Date column hint (optional)", value=DATE_COL_GUESS or "")
    date_range = st.sidebar.date_input("Date range (optional)", [])
    date_from, date_to = (date_range[0], date_range[1]) if len(date_range) == 2 else (None, None)
    search_col = st.sidebar.text_input("Search column (optional)")
    search_txt = st.sidebar.text_input("Search text (optional)")

    df = None
    with st.spinner("Loading data..."):
        try:
            if src == "JSON (file/url)":
                mode = st.sidebar.radio("JSON input", ["Upload file", "Fetch from URL"], horizontal=True)
                if mode == "Upload file":
                    up = st.sidebar.file_uploader("Upload .json or .jsonl", type=["json", "jsonl"])
                    if not up:
                        st.info("Upload a JSON/JSONL file to explore.")
                        st.stop()
                    df = load_json_from_file(up)
                else:
                    url = st.sidebar.text_input("Enter JSON API URL (GET)")
                    fetch_btn = st.sidebar.button("Fetch JSON")
                    if not url or not fetch_btn:
                        st.info("Enter a URL and click Fetch.")
                        st.stop()
                    df = load_json_from_url(url)

            elif src == "CSV/XLSX (file)":
                up = st.sidebar.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])
                if not up:
                    st.info("Upload a CSV/XLSX to explore.")
                    st.stop()
                if up.name.endswith(".csv"):
                    df = pd.read_csv(up)
                else:
                    df = pd.read_excel(up)

            # Type cleanup
            df = _coerce_dates(df, date_hint.strip() or None)

            # Apply optional filters
            if date_from or date_to:
                df = apply_date_filter(df, date_hint.strip(), date_from, date_to)

            if search_col and search_txt and search_col in df.columns:
                df = df[df[search_col].astype(str).str.contains(search_txt, case=False, na=False)]

        except Exception:
            st.error("⚠️ Could not load/parse the data. Please check the source and options.")
            st.stop()

    if df is None or df.empty:
        st.warning("No rows to display.")
        st.stop()

    # Quick KPIs
    left, mid, right = st.columns(3)
    with left:  st.metric("Rows", f"{len(df):,}")
    with mid:   st.metric("Columns", f"{df.shape[1]:,}")
    with right: st.metric("Null cells", f"{int(df.isna().sum().sum()):,}")

    st.dataframe(df, use_container_width=True)

    st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"), DOWNLOAD_NAME, "text/csv")


# def show():
#     st.set_page_config(page_title="Data Explorer", layout="wide")

#     # ---------- Config ----------
#     DEFAULT_SQL_VIEW = "dbo.Device_Inventory_View"  # change per your DB
#     DATE_COL = "Purchase_date"  # change per your data

#     # ---------- Helpers ----------
#     @st.cache_data(ttl=600)
#     def get_engine():
#         # Use env vars: MSSQL_DSN or host/port/credentials
#         # Example DSN conn string (recommended): "mssql+pyodbc://@MyDSN"
#         dsn = os.getenv("MSSQL_DSN")
#         if dsn:
#             return create_engine(dsn)
#         host = os.getenv("MSSQL_HOST", "192.168.1.5,21443")
#         db   = os.getenv("MSSQL_DB", "Asset_CMDB")
#         user = os.getenv("MSSQL_USER")
#         pwd  = os.getenv("MSSQL_PASSWORD")
#         driver = os.getenv("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")
#         if user and pwd:
#             return create_engine(f"mssql+pyodbc://{user}:{pwd}@{host}/{db}?driver={driver}")
#         return create_engine(f"mssql+pyodbc://{host}/{db}?driver={driver}&trusted_connection=yes")

#     @st.cache_data(ttl=600)
#     def load_sql(view_name: str, date_from=None, date_to=None, search_col=None, search_text=None, extra_filters=None):
#         where = []
#         params = {}
#         if date_from:
#             where.append(f"{DATE_COL} >= :dfrom")
#             params["dfrom"] = pd.to_datetime(date_from)
#         if date_to:
#             where.append(f"{DATE_COL} < :dto")
#             params["dto"] = pd.to_datetime(date_to) + pd.Timedelta(days=1)
#         if search_col and search_text:
#             where.append(f"{search_col} LIKE :q")
#             params["q"] = f"%{search_text}%"
#         if extra_filters:
#             for col, val in extra_filters.items():
#                 if val not in (None, "", "All"):
#                     where.append(f"{col} = :{col}")
#                     params[col] = val

#         sql = f"SELECT * FROM {view_name}"
#         if where:
#             sql += " WHERE " + " AND ".join(where)

#         with get_engine().connect() as conn:
#             return pd.read_sql(text(sql), conn, params=params)

#     def load_file(uploaded):
#         df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
#         # Best-effort type fix for dates:
#         if DATE_COL in df.columns:
#             df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
#         return df

#     def safe_int(x):
#         try: return int(x)
#         except: return x

#     # ---------- UI ----------
#     st.title("🔍 Data Explorer")

#     # @st.dialog("Select Data Source")
#     # def data_source_dialog():
#     #     choice = st.radio("Data source", ["MS SQL (view)", "Upload file"])
#     #     if st.button("Confirm"):
#     #         st.session_state["data_source"] = choice
#     #     st.rerun()
#     #     return(choice)    

#     # # Button to trigger the dialog
#     # if st.button("Open Data Source Selector"):
#     #     data_source_dialog()

#     st.write("Selected:", st.session_state.get("data_source", "Not chosen yet"))
#     src = st.sidebar.radio("Data source", ["MS SQL (view)", "Upload file"], horizontal=True)
#     if src == "MS SQL (view)":
#         view = st.sidebar.text_input("SQL View/Table", value=DEFAULT_SQL_VIEW)
#         date_range = st.sidebar.date_input("Date range (optional)", [])
#         date_from, date_to = (date_range[0], date_range[1]) if len(date_range) == 2 else (None, None)
#         search_col = st.sidebar.text_input("Search column (optional)")
#         search_txt = st.sidebar.text_input("Search text (optional)")
#     else:
#         uploaded = st.sidebar.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])
#         date_range = st.sidebar.date_input("Date range (optional)", [])
#         date_from, date_to = (date_range[0], date_range[1]) if len(date_range) == 2 else (None, None)
#         search_col = st.sidebar.text_input("Search column (optional)")
#         search_txt = st.sidebar.text_input("Search text (optional)")

#     with st.spinner("Loading data..."):
#         try:
#             if src == "MS SQL (view)":
#                 df = load_sql(view, date_from, date_to, search_col, search_txt, extra_filters=None)
#             else:
#                 if not uploaded:
#                     st.info("Upload a file to explore.")
#                     st.stop()
#                 df = load_file(uploaded)
#                 # Apply optional client-side filters
#                 if date_from or date_to:
#                     if DATE_COL in df.columns:
#                         m = pd.Series(True, index=df.index)
#                         if date_from: m &= df[DATE_COL] >= pd.to_datetime(date_from)
#                         if date_to:   m &= df[DATE_COL] < (pd.to_datetime(date_to) + pd.Timedelta(days=1))
#                         df = df[m]
#                 if search_col and search_txt and search_col in df.columns:
#                     df = df[df[search_col].astype(str).str.contains(search_txt, case=False, na=False)]
#         except Exception:
#             st.error("⚠️ Could not load data. Please check the view/file and filters.")
#             st.stop()

#     if df.empty:
#         st.warning("No rows found for the selected criteria.")
#         st.stop()

#     # Quick KPIs
#     left, mid, right = st.columns(3)
#     with left:  st.metric("Rows", f"{len(df):,}")
#     with mid:   st.metric("Columns", f"{df.shape[1]:,}")
#     with right: st.metric("Distinct Devices (if column exists)", df["Serial_number"].nunique() if "Serial_number" in df else "—")

#     st.dataframe(df, use_container_width=True)

#     # Download
#     st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"), "data_explorer.csv", "text/csv")

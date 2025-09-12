# pages/3_PIVOT.py
import io
import pandas as pd
import numpy as np
import streamlit as st

def show():
    st.set_page_config(page_title="PIVOT", layout="wide")

    st.title("📊 Pivot Builder")

    # 1) Get a DataFrame
    def _load_df():
        if "df" in st.session_state and isinstance(st.session_state["df"], pd.DataFrame):
            return st.session_state["df"]
        st.info("No DataFrame found in session. Upload a CSV/Excel to proceed.")
        up = st.file_uploader("Upload a CSV or Excel", type=["csv", "xlsx", "xls"])
        if up is None:
            return None
        if up.name.lower().endswith(".csv"):
            return pd.read_csv(up)
        return pd.read_excel(up)

    df = _load_df()
    if df is None:
        st.stop()

    st.caption(f"Rows: {len(df):,} • Columns: {len(df.columns):,}")

    # 2) Sidebar controls
    with st.sidebar:
        st.header("⚙️ Pivot Settings")

        # Optional quick filter block
        with st.expander("🔎 Quick Filter (optional)"):
            filter_cols = st.multiselect(
                "Choose columns to filter", df.columns.tolist(), key="filter_cols"
            )
            filtered_df = df.copy()
            for c in filter_cols:
                # Use unique values for categorical-like filters
                unique_vals = filtered_df[c].dropna().unique()
                # Keep it small for big numeric columns
                if len(unique_vals) <= 200:
                    chosen = st.multiselect(f"Filter values for `{c}`", unique_vals.tolist(), default=unique_vals.tolist())
                    if chosen:
                        filtered_df = filtered_df[filtered_df[c].isin(chosen)]
                else:
                    # Fallback to text query on large-cardinality columns
                    q = st.text_input(f"Query substring for `{c}` (contains)", "")
                    if q:
                        filtered_df = filtered_df[filtered_df[c].astype(str).str.contains(q, case=False, na=False)]
        if 'filtered_df' not in locals():
            filtered_df = df

        # Field selectors
        rows = st.multiselect("Rows (index)", filtered_df.columns.tolist())
        cols = st.multiselect("Columns (pivoted across)", [c for c in filtered_df.columns if c not in rows])

        # Values must be numeric or count-like; still let the user choose anything, then validate
        value_candidates = filtered_df.columns.tolist()
        values = st.multiselect(
            "Values (metrics)", 
            value_candidates,
            # auto-suggest first numeric column if available
            default=[next((c for c in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[c])), value_candidates[0])]
        )

        agg_map = {
            "sum": "sum",
            "mean": "mean",
            "count": "count",
            "nunique": pd.Series.nunique,
            "min": "min",
            "max": "max",
        }
        agg_choices = st.multiselect("Aggregations", list(agg_map.keys()), default=["sum"])
        chosen_aggs = [agg_map[a] for a in agg_choices] if agg_choices else ["sum"]

        fill_missing = st.checkbox("Fill missing values with 0", value=True)
        show_margins = st.checkbox("Show totals (margins)", value=True)
        dropna = st.checkbox("Drop NA group keys", value=True)
        sort_totals = st.checkbox("Sort by grand total (desc)", value=False)

        decimals = st.number_input("Decimal places for display", min_value=0, max_value=10, value=2, step=1)

    # Safety checks
    if not rows and not cols:
        st.warning("Pick at least one of **Rows** or **Columns**.")
        st.stop()
    if not values:
        st.warning("Pick at least one **Value** column.")
        st.stop()

    # 3) Build pivot
    try:
        pivot = pd.pivot_table(
            filtered_df,
            index=rows if rows else None,
            columns=cols if cols else None,
            values=values,
            aggfunc=chosen_aggs if len(values) == 1 else {v: chosen_aggs for v in values},
            margins=show_margins,
            margins_name="Total",
            dropna=dropna,
            observed=False,  # keep all categories if categorical
        )
    except Exception as e:
        st.error(f"Failed to build pivot: {e}")
        st.stop()

    # Optional fill missing
    if fill_missing:
        pivot = pivot.fillna(0)

    # If multiindex columns, flatten for neat display/download
    def _flatten_cols(cols):
        if isinstance(cols, pd.MultiIndex):
            return [" | ".join([str(x) for x in tup if str(x) != ""]) for tup in cols.values]
        return cols

    if isinstance(pivot.columns, pd.MultiIndex):
        pivot.columns = _flatten_cols(pivot.columns)

    # 4) Optional sort by grand total
    if sort_totals and rows:
        # Try to find a "Total" column if margins across columns; else compute row totals
        if "Total" in pivot.columns:
            sort_series = pivot["Total"]
            # If "Total" is itself multi-metric, sum across
            if isinstance(sort_series, pd.DataFrame):
                sort_series = sort_series.sum(axis=1, numeric_only=True)
        else:
            sort_series = pivot.select_dtypes(include=[np.number]).sum(axis=1)
        pivot = pivot.loc[sort_series.sort_values(ascending=False).index]

    # 5) Display
    st.subheader("Result")
    styled = pivot.copy()
    # Number formatting
    def _fmt(x):
        try:
            if isinstance(x, (int, np.integer)):
                return f"{x:,}"
            if isinstance(x, (float, np.floating)):
                return f"{x:,.{decimals}f}"
        except Exception:
            pass
        return x

    styled = styled.applymap(_fmt)
    st.dataframe(styled, use_container_width=True)

    # 6) Downloads
    def to_csv_bytes(df_):
        return df_.to_csv(index=True).encode("utf-8")

    def to_excel_bytes(df_):
        bio = io.BytesIO()
        with pd.ExcelWriter(bio, engine="xlsxwriter") as writer:
            df_.to_excel(writer, sheet_name="Pivot", index=True)
        return bio.getvalue()

    c1, c2 = st.columns(2)
    c1.download_button(
        "⬇️ Download CSV",
        data=to_csv_bytes(pivot),
        file_name="pivot.csv",
        mime="text/csv",
    )
    c2.download_button(
        "⬇️ Download Excel",
        data=to_excel_bytes(pivot),
        file_name="pivot.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # 7) Notes / tips
    with st.expander("ℹ️ Tips"):
        st.markdown(
            """
    - You can load your base DataFrame into `st.session_state["df"]` anywhere in your app; this page will pick it up.
    - **Multiple values & multiple aggregations** are supported. If you select multiple values and multiple aggs, you'll get a metric×agg layered header.
    - If your date column needs quarter/half-year pivots, add helper columns first (e.g., `df['Quarter']=df['date'].dt.to_period('Q').dt.to_timestamp()`, `df['HalfYear']=np.where(df['date'].dt.quarter<=2, 'H1','H2')`) and then use them as Rows/Columns.
    - “Sort by grand total” looks for a **Total** margin column; if not found, it sums all numeric columns per row.
            """
        )

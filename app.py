import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

st.set_page_config(
    page_title="Personal Expense Dashboard",
    page_icon="💰",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "expenses.csv")
BUDGET_FILE = os.path.join(BASE_DIR, "budget.txt")


st.markdown("""
<style>
.stApp {
    background-color: #F5F3FA;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 36px;
    font-weight: 700;
    color: #3F3D56;
}

.subtitle {
    font-size: 16px;
    color: #77758A;
    margin-bottom: 25px;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(63, 61, 86, 0.08);
}

div[data-testid="stMetricLabel"] {
    color: #77758A;
}

div[data-testid="stMetricValue"] {
    color: #3F3D56;
}

.section-title {
    color: #3F3D56;
    font-size: 22px;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 15px;
}

.insight-box,
.budget-box,
.edit-box,
.summary-box {
    background-color: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(63, 61, 86, 0.08);
    margin-bottom: 20px;
    color: #3F3D56;
}

.summary-box {
    text-align: center;
}

[data-testid="stSidebar"] {
    background-color: #EFEDF7;
}

.stButton > button,
[data-testid="stBaseButton-primary"] {
    border-radius: 12px !important;
    background-color: #BFDCC8 !important;
    color: #274C36 !important;
    border: 1px solid #A8CCB3 !important;
    font-weight: 700 !important;
}

.stButton > button:hover,
[data-testid="stBaseButton-primary"]:hover {
    background-color: #A9CFB5 !important;
    color: #203F2D !important;
    border-color: #94BFA0 !important;
}

[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border-color: #BFDCC8 !important;
    background-color: #F3F8F4 !important;
}

[data-baseweb="select"] span {
    color: #315B43 !important;
}

[role="option"] {
    background-color: #F7FBF8 !important;
    color: #315B43 !important;
}

[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background-color: #DDEFE3 !important;
    color: #28543A !important;
}

[data-baseweb="tag"] {
    background-color: #DDEFE3 !important;
    color: #315B43 !important;
}

[data-baseweb="tag"] span {
    color: #315B43 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #F3F8F4 !important;
    border-color: #BFDCC8 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #315B43 !important;
}

[data-testid="stSidebar"] input {
    background-color: #F8F7FC;
    color: #3F3D56;
    border: 1px solid #D8D3E8;
    border-radius: 10px;
}

[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    background-color: #F8F7FC;
    color: #3F3D56;
}

[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    background-color: #F8F7FC;
    color: #3F3D56;
}

.stDownloadButton > button {
    border-radius: 12px;
    background-color: #E7E3F2;
    color: #3F3D56;
    border: 1px solid #D2CDE2;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background-color: #DCD7EA;
    color: #302E45;
}

div[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


def load_data():
    columns = [
        "Date",
        "Category",
        "Amount",
        "Description",
        "Payment"
    ]

    if not os.path.exists(FILE_NAME):
        return pd.DataFrame(columns=columns)

    try:
        data = pd.read_csv(FILE_NAME)

        if data.empty:
            return pd.DataFrame(columns=columns)

        for column in columns:
            if column not in data.columns:
                data[column] = ""

        data["Date"] = pd.to_datetime(
            data["Date"],
            errors="coerce"
        )

        data["Amount"] = pd.to_numeric(
            data["Amount"],
            errors="coerce"
        )

        data = data.dropna(
            subset=["Date", "Amount"]
        )

        return data[columns].reset_index(drop=True)

    except Exception as e:
        st.error(f"Unable to read expenses.csv: {e}")
        return pd.DataFrame(columns=columns)


def load_budget():
    if not os.path.exists(BUDGET_FILE):
        return 10000.0

    try:
        with open(BUDGET_FILE, "r") as file:
            return float(file.read())
    except Exception:
        return 10000.0


def save_data(data):
    data.to_csv(
        FILE_NAME,
        index=False
    )


def reset_filters():
    st.session_state["filter_dates"] = (
        st.session_state["filter_min_date"],
        st.session_state["filter_max_date"]
    )

    st.session_state["filter_category"] = (
        st.session_state["filter_all_categories"]
    )

    st.session_state["filter_payment"] = (
        st.session_state["filter_all_payments"]
    )

    st.session_state["filter_search"] = ""


df = load_data()
monthly_budget = load_budget()


st.markdown(
    '<div class="main-title">💰 Personal Expense Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Track • Analyze • Understand your spending</div>',
    unsafe_allow_html=True
)


if "budget_message" in st.session_state:
    st.success(st.session_state["budget_message"])
    del st.session_state["budget_message"]

if "success_message" in st.session_state:
    st.success(st.session_state["success_message"])
    del st.session_state["success_message"]

if "edit_message" in st.session_state:
    st.success(st.session_state["edit_message"])
    del st.session_state["edit_message"]

if "delete_message" in st.session_state:
    st.success(st.session_state["delete_message"])
    del st.session_state["delete_message"]


st.sidebar.header("💰 Monthly Budget")

new_budget = st.sidebar.number_input(
    "Set Monthly Budget (₹)",
    min_value=0.0,
    value=float(monthly_budget),
    step=500.0
)

if st.sidebar.button(
    "💾 Save Budget",
    use_container_width=True
):
    if new_budget <= 0:
        st.sidebar.error(
            "Please enter a budget greater than ₹0."
        )
    else:
        try:
            with open(BUDGET_FILE, "w") as file:
                file.write(str(new_budget))

            st.session_state["budget_message"] = (
                "🎉 Monthly budget saved successfully!"
            )

            st.rerun()

        except Exception as e:
            st.sidebar.error(
                f"❌ Error saving budget: {e}"
            )


st.sidebar.markdown("---")
st.sidebar.header("➕ Add New Expense")


expense_date = st.sidebar.date_input(
    "Date",
    value=date.today()
)


category = st.sidebar.selectbox(
    "Category",
    [
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Bills",
        "Entertainment",
        "Health",
        "Other"
    ],
    key="add_category"
)


amount = st.sidebar.number_input(
    "Amount (₹)",
    min_value=0.0,
    value=0.0,
    step=100.0
)


description = st.sidebar.text_input(
    "Description",
    placeholder="Example: Lunch"
)


payment = st.sidebar.selectbox(
    "Payment Method",
    [
        "UPI",
        "Cash",
        "Card",
        "Bank Transfer"
    ],
    key="add_payment"
)


if st.sidebar.button(
    "➕ Add Expense",
    use_container_width=True,
    type="primary"
):

    if amount <= 0:
        st.sidebar.error(
            "Please enter amount greater than ₹0."
        )

    else:

        new_expense = pd.DataFrame([
            {
                "Date": pd.Timestamp(expense_date),
                "Category": category,
                "Amount": float(amount),
                "Description": description,
                "Payment": payment
            }
        ])

        try:
            df = pd.concat(
                [df, new_expense],
                ignore_index=True
            )

            save_data(df)

            st.session_state["success_message"] = (
                "🎉 Expense added successfully!"
            )

            st.rerun()

        except Exception as e:
            st.sidebar.error(
                f"❌ Error saving expense: {e}"
            )


st.sidebar.markdown("---")
st.sidebar.header("🔎 Filter & Search")


if not df.empty:

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    all_categories = sorted(
        df["Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    all_payments = sorted(
        df["Payment"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    st.session_state["filter_min_date"] = min_date
    st.session_state["filter_max_date"] = max_date
    st.session_state["filter_all_categories"] = all_categories
    st.session_state["filter_all_payments"] = all_payments


    if "filter_dates" not in st.session_state:
        st.session_state["filter_dates"] = (
            min_date,
            max_date
        )

    if "filter_category" not in st.session_state:
        st.session_state["filter_category"] = all_categories

    if "filter_payment" not in st.session_state:
        st.session_state["filter_payment"] = all_payments

    if "filter_search" not in st.session_state:
        st.session_state["filter_search"] = ""


    search_text = st.sidebar.text_input(
        "🔎 Search Expense",
        placeholder="Search description, category or payment...",
        key="filter_search"
    )


    selected_dates = st.sidebar.date_input(
        "📅 Date Range",
        key="filter_dates"
    )


    selected_category = st.sidebar.multiselect(
        "🏷️ Category",
        options=all_categories,
        key="filter_category"
    )


    selected_payment = st.sidebar.multiselect(
        "💳 Payment Method",
        options=all_payments,
        key="filter_payment"
    )


    st.sidebar.button(
        "🔄 Reset Filters",
        use_container_width=True,
        on_click=reset_filters
    )


    filtered_df = df.copy()


    if isinstance(
        selected_dates,
        (tuple, list)
    ):

        if len(selected_dates) == 2:

            start_date = selected_dates[0]
            end_date = selected_dates[1]

            filtered_df = filtered_df[
                (
                    filtered_df["Date"].dt.date
                    >= start_date
                )
                &
                (
                    filtered_df["Date"].dt.date
                    <= end_date
                )
            ]

    elif isinstance(selected_dates, date):

        filtered_df = filtered_df[
            filtered_df["Date"].dt.date
            == selected_dates
        ]


    filtered_df = filtered_df[
        filtered_df["Category"].isin(
            selected_category
        )
    ]


    filtered_df = filtered_df[
        filtered_df["Payment"].isin(
            selected_payment
        )
    ]


    if search_text.strip():

        search_value = (
            search_text
            .strip()
            .lower()
        )

        description_match = (
            filtered_df["Description"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_value,
                na=False
            )
        )

        category_match = (
            filtered_df["Category"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_value,
                na=False
            )
        )

        payment_match = (
            filtered_df["Payment"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_value,
                na=False
            )
        )

        filtered_df = filtered_df[
            description_match
            | category_match
            | payment_match
        ]

else:

    filtered_df = df.copy()


if df.empty:

    st.info(
        "👋 No expenses available yet."
    )

    st.markdown(
        '<div class="section-title">🌿 Start Tracking</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Add your first expense from the sidebar."
    )

    st.stop()


if filtered_df.empty:

    st.warning(
        "⚠️ No expenses found."
    )

    st.info(
        "Try another search or change the filters."
    )

    st.stop()


total_expense = filtered_df["Amount"].sum()

highest_expense = filtered_df["Amount"].max()

average_expense = filtered_df["Amount"].mean()

transaction_count = len(filtered_df)


today = pd.Timestamp.today()


current_month_df = df[
    (df["Date"].dt.month == today.month)
    &
    (df["Date"].dt.year == today.year)
]


monthly_expense = (
    current_month_df["Amount"].sum()
)


budget_used = monthly_expense

budget_remaining = (
    monthly_budget - budget_used
)


if monthly_budget > 0:

    budget_percentage = (
        budget_used
        / monthly_budget
    ) * 100

else:

    budget_percentage = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Total Expense",
        f"₹{total_expense:,.0f}"
    )


with col2:

    st.metric(
        "📅 This Month",
        f"₹{monthly_expense:,.0f}"
    )


with col3:

    st.metric(
        "🔝 Highest Expense",
        f"₹{highest_expense:,.0f}"
    )


with col4:

    st.metric(
        "🧾 Transactions",
        transaction_count
    )


st.markdown(
    '<div class="section-title">🎯 Monthly Budget</div>',
    unsafe_allow_html=True
)


budget_col1, budget_col2, budget_col3 = st.columns(3)


with budget_col1:

    st.metric(
        "💵 Monthly Budget",
        f"₹{monthly_budget:,.0f}"
    )


with budget_col2:

    st.metric(
        "📊 Budget Used",
        f"₹{budget_used:,.0f}"
    )


with budget_col3:

    if budget_remaining >= 0:

        st.metric(
            "💚 Remaining Budget",
            f"₹{budget_remaining:,.0f}"
        )

    else:

        st.metric(
            "🔴 Over Budget",
            f"₹{abs(budget_remaining):,.0f}"
        )


st.markdown(
    '<div class="budget-box">',
    unsafe_allow_html=True
)


progress_value = min(
    max(
        budget_percentage / 100,
        0
    ),
    1.0
)


st.progress(progress_value)


st.write(
    f"**₹{budget_used:,.0f}** spent out of "
    f"**₹{monthly_budget:,.0f}**"
)


st.write(
    f"Budget usage: "
    f"**{budget_percentage:.1f}%**"
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


if budget_percentage >= 100:

    st.error(
        f"🚨 Monthly budget exceeded by "
        f"₹{abs(budget_remaining):,.0f}."
    )

elif budget_percentage >= 80:

    st.warning(
        f"⚠️ You have used "
        f"{budget_percentage:.1f}% "
        f"of your monthly budget."
    )

else:

    st.success(
        f"✅ You are within your budget. "
        f"{budget_percentage:.1f}% used."
    )


st.markdown(
    '<div class="section-title">📊 Quick Statistics</div>',
    unsafe_allow_html=True
)


quick1, quick2, quick3, quick4 = st.columns(4)


with quick1:

    st.metric(
        "📌 Average Expense",
        f"₹{average_expense:,.0f}"
    )


with quick2:

    st.metric(
        "📋 Filtered Records",
        len(filtered_df)
    )


with quick3:

    st.metric(
        "🔎 Search Status",
        "Active"
        if search_text.strip()
        else "All"
    )


with quick4:

    unique_categories = (
        filtered_df["Category"]
        .nunique()
    )

    st.metric(
        "🏷️ Categories Used",
        unique_categories
    )


st.markdown(
    '<div class="section-title">📊 Expense Analytics</div>',
    unsafe_allow_html=True
)


chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    category_data = (
        filtered_df
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )


    pie_chart = px.pie(
        category_data,
        names="Category",
        values="Amount",
        hole=0.55,
        title="🥧 Expense by Category"
    )


    pie_chart.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            color="#3F3D56"
        )
    )


    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )


with chart_col2:

    daily_data = (
        filtered_df
        .groupby("Date")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )


    line_chart = px.line(
        daily_data,
        x="Date",
        y="Amount",
        markers=True,
        title="📈 Daily Expense Trend"
    )


    line_chart.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            color="#3F3D56"
        ),
        xaxis_title="Date",
        yaxis_title="Expense (₹)"
    )


    st.plotly_chart(
        line_chart,
        use_container_width=True
    )


st.markdown(
    '<div class="section-title">📅 Monthly Expense Analysis</div>',
    unsafe_allow_html=True
)


monthly_data = filtered_df.copy()


monthly_data["Month"] = (
    monthly_data["Date"]
    .dt.to_period("M")
    .astype(str)
)


monthly_data = (
    monthly_data
    .groupby("Month")["Amount"]
    .sum()
    .reset_index()
)


bar_chart = px.bar(
    monthly_data,
    x="Month",
    y="Amount",
    title="📊 Monthly Expenses",
    text_auto=True
)


bar_chart.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        color="#3F3D56"
    ),
    xaxis_title="Month",
    yaxis_title="Expense (₹)"
)


st.plotly_chart(
    bar_chart,
    use_container_width=True
)


st.markdown(
    '<div class="section-title">💳 Payment Method Analysis</div>',
    unsafe_allow_html=True
)


payment_data = (
    filtered_df
    .groupby("Payment")["Amount"]
    .sum()
    .reset_index()
)


payment_chart = px.bar(
    payment_data,
    x="Payment",
    y="Amount",
    title="💳 Spending by Payment Method",
    text_auto=True
)


payment_chart.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        color="#3F3D56"
    ),
    xaxis_title="Payment Method",
    yaxis_title="Expense (₹)"
)


st.plotly_chart(
    payment_chart,
    use_container_width=True
)


st.markdown(
    '<div class="section-title">🏆 Category Comparison</div>',
    unsafe_allow_html=True
)


category_compare = (
    filtered_df
    .groupby("Category")["Amount"]
    .sum()
    .reset_index()
    .sort_values(
        "Amount",
        ascending=False
    )
)


comparison_chart = px.bar(
    category_compare,
    x="Category",
    y="Amount",
    title="🏆 Category-wise Spending Comparison",
    text_auto=True
)


comparison_chart.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        color="#3F3D56"
    ),
    xaxis_title="Category",
    yaxis_title="Amount (₹)"
)


st.plotly_chart(
    comparison_chart,
    use_container_width=True
)


st.markdown(
    '<div class="section-title">💡 Spending Insights</div>',
    unsafe_allow_html=True
)


category_totals = (
    filtered_df
    .groupby("Category")["Amount"]
    .sum()
    .sort_values(
        ascending=False
    )
)


top_category = category_totals.index[0]

top_category_amount = category_totals.iloc[0]


category_percentage = (
    top_category_amount
    / total_expense
) * 100


payment_totals = (
    filtered_df
    .groupby("Payment")["Amount"]
    .sum()
    .sort_values(
        ascending=False
    )
)


top_payment = payment_totals.index[0]

top_payment_amount = payment_totals.iloc[0]


st.markdown(
    f"""
    <div class="insight-box">

    💡 Your highest spending category is
    <b>{top_category}</b> with
    <b>₹{top_category_amount:,.0f}</b>.

    <br><br>

    📊 This represents approximately
    <b>{category_percentage:.1f}%</b>
    of your total expenses.

    <br><br>

    💳 Your highest spending payment method is
    <b>{top_payment}</b> with
    <b>₹{top_payment_amount:,.0f}</b>.

    <br><br>

    📌 Average expense per transaction:
    <b>₹{average_expense:,.0f}</b>

    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-title">🧾 Recent Expenses</div>',
    unsafe_allow_html=True
)


display_expenses = (
    filtered_df
    .sort_values(
        "Date",
        ascending=False
    )
    .head(10)
    .copy()
)


display_expenses["Date"] = (
    display_expenses["Date"]
    .dt.strftime("%d %b %Y")
)


display_expenses["Amount"] = (
    display_expenses["Amount"]
    .apply(
        lambda x: f"₹{x:,.0f}"
    )
)


st.dataframe(
    display_expenses,
    use_container_width=True,
    hide_index=True
)


st.markdown(
    '<div class="section-title">✏️ Edit Expense</div>',
    unsafe_allow_html=True
)


edit_options = filtered_df.index.tolist()


edit_labels = {}


for expense_id in edit_options:

    edit_labels[expense_id] = (
        f"#{expense_id + 1} | "
        f"{filtered_df.loc[expense_id, 'Date'].strftime('%d %b %Y')} | "
        f"{filtered_df.loc[expense_id, 'Category']} | "
        f"₹{filtered_df.loc[expense_id, 'Amount']:,.0f} | "
        f"{filtered_df.loc[expense_id, 'Description']}"
    )


if (
    "edit_selected_id" not in st.session_state
    or
    st.session_state["edit_selected_id"]
    not in edit_options
):

    st.session_state["edit_selected_id"] = (
        edit_options[0]
    )


edit_id = st.selectbox(
    "Select expense to edit",
    options=edit_options,
    index=edit_options.index(
        st.session_state["edit_selected_id"]
    ),
    format_func=lambda x: edit_labels[x],
    key="edit_selector"
)


st.session_state["edit_selected_id"] = edit_id


selected_expense = filtered_df.loc[edit_id]


st.markdown(
    '<div class="edit-box">',
    unsafe_allow_html=True
)


st.success(
    f"Selected: "
    f"{selected_expense['Date'].strftime('%d %b %Y')} | "
    f"{selected_expense['Category']} | "
    f"₹{selected_expense['Amount']:,.0f} | "
    f"{selected_expense['Description']} | "
    f"{selected_expense['Payment']}"
)


edit_col1, edit_col2 = st.columns(2)


with edit_col1:

    edit_date = st.date_input(
        "Date",
        value=selected_expense["Date"].date(),
        key=f"edit_date_{edit_id}"
    )


    category_options = [
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Bills",
        "Entertainment",
        "Health",
        "Other"
    ]


    current_category = str(
        selected_expense["Category"]
    )


    if current_category not in category_options:

        category_options.append(
            current_category
        )


    edit_category = st.selectbox(
        "Category",
        category_options,
        index=category_options.index(
            current_category
        ),
        key=f"edit_category_{edit_id}"
    )


    edit_amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        value=float(
            selected_expense["Amount"]
        ),
        step=100.0,
        key=f"edit_amount_{edit_id}"
    )


with edit_col2:

    edit_description = st.text_input(
        "Description",
        value=str(
            selected_expense["Description"]
        ),
        key=f"edit_description_{edit_id}"
    )


    payment_options = [
        "UPI",
        "Cash",
        "Card",
        "Bank Transfer"
    ]


    current_payment = str(
        selected_expense["Payment"]
    )


    if current_payment not in payment_options:

        payment_options.append(
            current_payment
        )


    edit_payment = st.selectbox(
        "Payment Method",
        payment_options,
        index=payment_options.index(
            current_payment
        ),
        key=f"edit_payment_{edit_id}"
    )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


if st.button(
    "💾 Update Expense",
    use_container_width=True,
    type="primary"
):

    if edit_amount <= 0:

        st.error(
            "Please enter an amount greater than ₹0."
        )

    else:

        try:

            df.loc[edit_id, "Date"] = (
                pd.Timestamp(edit_date)
            )

            df.loc[edit_id, "Category"] = (
                edit_category
            )

            df.loc[edit_id, "Amount"] = (
                float(edit_amount)
            )

            df.loc[edit_id, "Description"] = (
                edit_description
            )

            df.loc[edit_id, "Payment"] = (
                edit_payment
            )

            save_data(df)

            st.session_state["edit_message"] = (
                "🎉 Expense updated successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"❌ Error updating expense: {e}"
            )


st.markdown(
    '<div class="section-title">🗑️ Delete Expense</div>',
    unsafe_allow_html=True
)


delete_options = filtered_df.index.tolist()


delete_labels = {}


for expense_id in delete_options:

    delete_labels[expense_id] = (
        f"#{expense_id + 1} | "
        f"{filtered_df.loc[expense_id, 'Date'].strftime('%d %b %Y')} | "
        f"{filtered_df.loc[expense_id, 'Category']} | "
        f"₹{filtered_df.loc[expense_id, 'Amount']:,.0f}"
    )


delete_id = st.selectbox(
    "Select expense to delete",
    options=delete_options,
    format_func=lambda x: delete_labels[x],
    key="delete_select"
)


if st.button(
    "🗑️ Delete Selected Expense",
    use_container_width=True
):

    try:

        df = df.drop(
            index=delete_id
        ).reset_index(
            drop=True
        )

        save_data(df)

        st.session_state["delete_message"] = (
            "✅ Expense deleted successfully!"
        )

        st.rerun()

    except Exception as e:

        st.error(
            f"❌ Error deleting expense: {e}"
        )


st.markdown(
    '<div class="section-title">📥 Download Data</div>',
    unsafe_allow_html=True
)


download_col1, download_col2 = st.columns(2)


with download_col1:

    filtered_csv = (
        filtered_df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="📥 Download Filtered CSV",
        data=filtered_csv,
        file_name="personal_expenses_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )


with download_col2:

    complete_csv = (
        df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="📥 Download Complete CSV",
        data=complete_csv,
        file_name="personal_expenses_complete.csv",
        mime="text/csv",
        use_container_width=True
    )


st.markdown("---")


st.markdown(
    """
    <div class="summary-box">

    <b>💰 Personal Expense Visualization Dashboard</b>

    <br><br>

    Track your expenses • Manage your budget • Analyze spending •

    Make better financial decisions

    <br><br>

    Built with Python • Streamlit • Pandas • Plotly

    </div>
    """,
    unsafe_allow_html=True
)
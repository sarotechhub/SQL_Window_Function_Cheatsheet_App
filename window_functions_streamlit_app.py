import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
from typing import List, Tuple

# Page Configuration
st.set_page_config(
    page_title="SQL Window Functions Cheat Sheet",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: bold;
    }
    .function-title {
        color: #1f77b4;
        font-size: 1.3rem;
        font-weight: bold;
        margin-top: 20px;
    }
    .code-block {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
    }
    .output-box {
        background-color: #f9f9f9;
        border-left: 4px solid #1f77b4;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== Sample Data Generation ====================

def create_sample_data():
    """Create sample data for demonstrations"""
    # Employees data
    employees_data = {
        'employee_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'employee_name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Iris', 'Jack'],
        'department': ['Sales', 'Sales', 'Sales', 'IT', 'IT', 'IT', 'HR', 'HR', 'Finance', 'Finance'],
        'salary': [60000, 75000, 55000, 85000, 90000, 80000, 65000, 70000, 72000, 68000],
        'hire_date': ['2020-01-15', '2019-03-20', '2021-06-10', '2018-02-01', '2017-08-15', '2019-11-30', '2020-05-10', '2021-02-20', '2019-04-15', '2022-01-10']
    }
    
    # Sales data
    sales_data = {
        'sale_id': list(range(1, 21)),
        'sale_date': [datetime(2024, 1, 1) + timedelta(days=i*2) for i in range(20)],
        'product': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B'],
        'amount': [100, 150, 120, 200, 180, 140, 220, 160, 130, 210, 190, 150, 230, 170, 140, 250, 200, 160, 240, 210],
        'region': ['North', 'South', 'North', 'South', 'East', 'West', 'East', 'West', 'North', 'South', 'North', 'South', 'East', 'West', 'East', 'West', 'North', 'South', 'North', 'South']
    }
    
    # Orders data
    orders_data = {
        'order_id': list(range(1, 21)),
        'customer_id': [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8, 9],
        'customer_name': ['John', 'John', 'John', 'Jane', 'Jane', 'Jane', 'Mike', 'Mike', 'Sarah', 'Sarah', 'Tom', 'Tom', 'Tom', 'Alice', 'Alice', 'Bob', 'Bob', 'Carol', 'Carol', 'David'],
        'order_date': [datetime(2024, 1, i*2+1) if i*2+1 <= 31 else datetime(2024, 2, (i*2+1)%31) for i in range(20)],
        'order_amount': [100, 250, 150, 200, 300, 250, 120, 180, 90, 140, 250, 200, 180, 160, 220, 140, 190, 230, 200, 150]
    }
    
    # Performance data
    performance_data = {
        'employee_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'month': ['Jan 2024', 'Jan 2024', 'Jan 2024', 'Jan 2024', 'Jan 2024', 
                  'Feb 2024', 'Feb 2024', 'Feb 2024', 'Feb 2024', 'Feb 2024'],
        'revenue': [5000, 7500, 4500, 8500, 9000, 6000, 8000, 5500, 9500, 7000],
        'target': [5000, 6000, 5000, 8000, 8500, 5000, 6000, 5000, 8000, 8500]
    }
    
    return (
        pd.DataFrame(employees_data),
        pd.DataFrame(sales_data),
        pd.DataFrame(orders_data),
        pd.DataFrame(performance_data)
    )


def execute_query(query: str, connection) -> Tuple[pd.DataFrame, str]:
    """Execute SQL query and return results"""
    try:
        result = pd.read_sql_query(query, connection)
        return result, None
    except Exception as e:
        return None, str(e)


# ==================== Initialize Database ====================

@st.cache_resource
def init_database():
    """Initialize SQLite database with sample data"""
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    
    employees_df, sales_df, orders_df, performance_df = create_sample_data()
    
    employees_df.to_sql('employees', conn, if_exists='replace', index=False)
    sales_df.to_sql('sales', conn, if_exists='replace', index=False)
    orders_df.to_sql('orders', conn, if_exists='replace', index=False)
    performance_df.to_sql('performance', conn, if_exists='replace', index=False)
    
    return conn


# ==================== Main App ====================

st.title("📊 SQL Window Functions Interactive Cheat Sheet")
st.markdown("Master SQL Window Functions with Real-Time Examples...")

conn = init_database()

# Sidebar Navigation
with st.sidebar:
    st.header("📊 SQL Window Functions")
    page = st.radio(
        "Select a Section:",
        [
            "Home",
            "Aggregate Functions",
            "Ranking Functions",
            "Analytical Functions",
            "Sample Data",
            "Custom Query",
            "Quick Reference"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📚 Available Tables")
    st.markdown("""
    - **employees**: employee_id, employee_name, department, salary, hire_date
    - **sales**: sale_id, sale_date, product, amount, region
    - **orders**: order_id, customer_id, customer_name, order_date, order_amount
    - **performance**: employee_id, month, revenue, target
    """)

    st.markdown("---")
    st.markdown("### 🧠 Quick Tips")
    st.markdown("""
    - Window functions are **not** the same as regular aggregate functions
    - Always use `OVER()` clause to define window frame
    - Use `PARTITION BY` to group rows for calculations
    - Use `ORDER BY` within `OVER()` to define row order in window
    """)
    
    
    st.markdown("---")
    st.markdown("### 👍 Rate This App")

    col1, col2, col3 = st.columns(3)

    # Initialize session state for per-button disabled flags and counts (idempotent)
    if "disabled_love" not in st.session_state:
        st.session_state.disabled_love = False
    if "disabled_like" not in st.session_state:
        st.session_state.disabled_like = False
    if "disabled_smile" not in st.session_state:
        st.session_state.disabled_smile = False
    if "loves" not in st.session_state:
        st.session_state.loves = 0
    if "likes" not in st.session_state:
        st.session_state.likes = 0
    if "smiles" not in st.session_state:
        st.session_state.smiles = 0

    with col1:
        if st.button("❤️ Love", key="love_btn", disabled=st.session_state.disabled_love):
            st.session_state.loves += 1
            st.session_state.disabled_love = True
            st.session_state.disabled_like = True
            st.session_state.disabled_smile = True
            st.rerun()

    with col2:
        if st.button("👍 Like", key="like_btn", disabled=st.session_state.disabled_like):
            st.session_state.likes += 1
            st.session_state.disabled_like = True
            st.session_state.disabled_love = True
            st.session_state.disabled_smile = True
            st.rerun()

    with col3:
        if st.button("😊 Smile", key="smile_btn", disabled=st.session_state.disabled_smile):
            st.session_state.smiles += 1
            st.session_state.disabled_smile = True
            st.session_state.disabled_like = True
            st.session_state.disabled_love = True
            st.rerun()

    if st.session_state.disabled_love or st.session_state.disabled_like or st.session_state.disabled_smile:
        st.success("Thanks for your rating! 😊")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("❤️ Loves", st.session_state.get("loves", 0))
    with col2:
        st.metric("👍 Likes", st.session_state.get("likes", 0))
    with col3:
        st.metric("😊 Smiles", st.session_state.get("smiles", 0))

# ==================== HOME PAGE ====================

if page == "Home":
    st.header("Welcome to Window Functions Cheat Sheet! 👋")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### What are Window Functions?
        Window functions perform calculations across a set of rows, 
        maintaining all original rows without condensing results.
        
        ### Key Benefits:
        - ✅ Keep row-level detail with aggregate calculations
        - ✅ Compare individual values to group statistics
        - ✅ Rank and score data efficiently
        - ✅ Solve complex analytics in single query
        """)
    
    with col2:
        st.info("""
        ### Quick Start:
        1. Choose a function category from the sidebar
        2. View real examples with descriptions
        3. See query and output
        4. Try custom queries in "Custom Query" section
        5. Reference syntax in "Quick Reference"
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h1 style='color: #1f77b4; font-size: 2.5rem; font-weight: bold;'>
            🎯 Core Window Function Categories
        </h1>
        <p style='color: #666; font-size: 1.1rem;'>Master all 15+ window functions</p>
    </div>
    """, unsafe_allow_html=True)
    
    categories = {
        "📊 Aggregate": {
            "icon": "📈",
            "color": "#e80c0c",
            "funcs": ["SUM", "AVG", "COUNT", "MIN", "MAX"],
            "desc": "Calculate aggregates within windows"
        },
        "🏆 Ranking": {
            "icon": "🥇",
            "color": "#312279",
            "funcs": ["ROW_NUMBER", "RANK", "DENSE_RANK", "NTILE", "PERCENT_RANK"],
            "desc": "Rank and position rows"
        },
        "📍 Analytical": {
            "icon": "📊",
            "color": "#3fb433",
            "funcs": ["LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE", "NTH_VALUE"],
            "desc": "Access relative row values"
        }
    }
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    for col, (cat, info) in zip([col1, col2, col3], categories.items()):
        with col:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, {info["color"]}20 0%, {info["color"]}05 100%);
                border-left: 5px solid {info["color"]};
                border-radius: 10px;
                padding: 5px;
                margin: 5px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            '>
                <h2 style='color: {info["color"]}; font-size: 1.8rem; margin-bottom: 10px; font-weight: bold;'>
                    {cat}
                </h2>
                <p style='color: #666; font-size: 0.95rem; margin-bottom: 20px; font-style: italic;'>
                    {info["desc"]}
                </p>
                <div style='background: white; padding: 15px; border-radius: 8px;'>
            """, unsafe_allow_html=True)
            
            for func in info["funcs"]:
                st.markdown(f"""
                <div style='
                    background: {info["color"]}15;
                    padding: 10px 12px;
                    margin: 8px 0;
                    border-radius: 6px;
                    border-left: 3px solid {info["color"]};
                    font-weight: bold;
                    font-size: 1.05rem;
                '>
                    ▶️ <code style='color: {info["color"]}; font-size: 1.1rem;'>{func}()</code>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==================== AGGREGATE FUNCTIONS ====================

elif page == "Aggregate Functions":
    st.header("Aggregate Window Functions")
    st.markdown("Functions that perform calculations: SUM, AVG, COUNT, MIN, MAX")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["SUM()", "AVG()", "COUNT()", "MIN()/MAX()", "Combined"])
    
    # SUM TAB
    with tab1:
        st.markdown("### SUM() - Running Total & Department Sum")
        st.markdown("""
        **Syntax:**
        ```sql
        SUM(column) OVER ([PARTITION BY ...] [ORDER BY ...] [ROWS BETWEEN ...])
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Running Total by Department")
            query = """
            SELECT 
                employee_id,
                employee_name,
                department,
                salary,
                SUM(salary) OVER (
                    PARTITION BY department 
                    ORDER BY employee_id
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) AS running_total
            FROM employees
            ORDER BY department, employee_id;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Total Department Salary")
            query = """
            SELECT 
                employee_id,
                employee_name,
                department,
                salary,
                SUM(salary) OVER (PARTITION BY department) AS dept_total
            FROM employees
            ORDER BY department, salary DESC;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # AVG TAB
    with tab2:
        st.markdown("### AVG() - Average with Comparison")
        st.markdown("""
        **Syntax:**
        ```sql
        AVG(column) OVER ([PARTITION BY ...] [ORDER BY ...])
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Compare to Department Average")
            query = """
            SELECT 
                employee_name,
                department,
                salary,
                ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS dept_avg,
                ROUND(salary - AVG(salary) OVER (PARTITION BY department), 2) AS diff_from_avg
            FROM employees
            ORDER BY department, salary DESC;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # COUNT TAB
    with tab3:
        st.markdown("### COUNT() - Order Count per Customer")
        st.markdown("""
        **Syntax:**
        ```sql
        COUNT(column) OVER ([PARTITION BY ...] [ORDER BY ...])
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Orders per Customer")
            query = """
            SELECT 
                order_id,
                customer_id,
                customer_name,
                order_amount,
                COUNT(*) OVER (PARTITION BY customer_id) AS customer_order_count,
                ROUND(AVG(order_amount) OVER (PARTITION BY customer_id), 2) AS avg_order_amount
            FROM orders
            ORDER BY customer_id, order_date;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # MIN/MAX TAB
    with tab4:
        st.markdown("### MIN() / MAX() - Range Analysis")
        st.markdown("""
        **Syntax:**
        ```sql
        MIN(column) OVER (...) / MAX(column) OVER (...)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Salary Range by Department")
            query = """
            SELECT 
                employee_name,
                department,
                salary,
                MAX(salary) OVER (PARTITION BY department) AS max_salary,
                MIN(salary) OVER (PARTITION BY department) AS min_salary,
                MAX(salary) OVER (PARTITION BY department) - salary AS gap_to_max
            FROM employees
            ORDER BY department, salary DESC;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # COMBINED TAB
    with tab5:
        st.markdown("### Combined Aggregates - Comprehensive Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Department Summary")
            query = """
            SELECT 
                department,
                employee_name,
                salary,
                COUNT(*) OVER (PARTITION BY department) AS emp_count,
                SUM(salary) OVER (PARTITION BY department) AS total_salary,
                ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS avg_salary,
                MAX(salary) OVER (PARTITION BY department) AS max_salary,
                MIN(salary) OVER (PARTITION BY department) AS min_salary
            FROM employees
            ORDER BY department, salary DESC;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)


# ==================== RANKING FUNCTIONS ====================

elif page == "Ranking Functions":
    st.header("Ranking Window Functions")
    st.markdown("Functions for ranking: ROW_NUMBER, RANK, DENSE_RANK, NTILE, PERCENT_RANK")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["ROW_NUMBER()", "RANK()", "DENSE_RANK()", "NTILE()", "PERCENT_RANK()"])
    
    # ROW_NUMBER TAB
    with tab1:
        st.markdown("### ROW_NUMBER() - Unique Sequential Numbering")
        st.markdown("""
        **Key Point:** Always returns unique numbers, even for ties
        
        **Syntax:**
        ```sql
        ROW_NUMBER() OVER ([PARTITION BY ...] ORDER BY ...)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Performers per Department")
            query = """
            SELECT 
                ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
                employee_name,
                department,
                salary
            FROM employees
            ORDER BY department, rank;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # RANK TAB
    with tab2:
        st.markdown("### RANK() - Ranking with Gaps on Ties")
        st.markdown("""
        **Key Point:** Has gaps when there are tied values
        
        **Syntax:**
        ```sql
        RANK() OVER ([PARTITION BY ...] ORDER BY ...)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sales Amount Ranking by Region")
            query = """
            SELECT 
                RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS rank,
                product,
                region,
                amount
            FROM sales
            ORDER BY region, rank;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # DENSE_RANK TAB
    with tab3:
        st.markdown("### DENSE_RANK() - Consecutive Ranking")
        st.markdown("""
        **Key Point:** No gaps in ranking, consecutive numbers even with ties
        
        **Syntax:**
        ```sql
        DENSE_RANK() OVER ([PARTITION BY ...] ORDER BY ...)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dense Ranking by Product")
            query = """
            SELECT 
                DENSE_RANK() OVER (PARTITION BY product ORDER BY amount DESC) AS rank,
                product,
                region,
                amount
            FROM sales
            ORDER BY product, rank;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # NTILE TAB
    with tab4:
        st.markdown("### NTILE() - Divide into N Groups")
        st.markdown("""
        **Key Point:** Divides rows into N equal (or near-equal) groups
        
        **Syntax:**
        ```sql
        NTILE(n) OVER ([PARTITION BY ...] ORDER BY ...)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Quartile Analysis - Sales by Quartile")
            query = """
            SELECT 
                NTILE(4) OVER (ORDER BY order_amount DESC) AS quartile,
                customer_name,
                order_amount
            FROM orders
            ORDER BY quartile, order_amount DESC;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # PERCENT_RANK TAB
    with tab5:
        st.markdown("### PERCENT_RANK() - Percentile Ranking (0-1)")
        st.markdown("""
        **Key Point:** Returns value between 0 and 1 representing percentile
        
        **Syntax:**
        ```sql
        PERCENT_RANK() OVER ([PARTITION BY ...] ORDER BY ...)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Salary Percentile by Department")
            query = """
            SELECT 
                employee_name,
                department,
                salary,
                ROUND(PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary), 4) AS pct_rank,
                ROUND(PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary) * 100, 2) AS pct
            FROM employees
            ORDER BY department, salary;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)


# ==================== ANALYTICAL FUNCTIONS ====================

elif page == "Analytical Functions":
    st.header("Analytical Window Functions")
    st.markdown("Functions for accessing relative rows: LAG, LEAD, FIRST_VALUE, LAST_VALUE, NTH_VALUE")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["LAG()", "LEAD()", "FIRST_VALUE()", "LAST_VALUE()", "NTH_VALUE()"])
    
    # LAG TAB
    with tab1:
        st.markdown("### LAG() - Access Previous Row")
        st.markdown("""
        **Syntax:**
        ```sql
        LAG(column, offset, default_value) OVER ([PARTITION BY ...] ORDER BY ...)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Order-over-Order Comparison")
            query = """
            SELECT 
                order_id,
                customer_name,
                order_amount,
                LAG(order_amount) OVER (PARTITION BY customer_id ORDER BY order_id) AS prev_order,
                order_amount - LAG(order_amount) OVER (PARTITION BY customer_id ORDER BY order_id) AS change
            FROM orders
            ORDER BY customer_id, order_id;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # LEAD TAB
    with tab2:
        st.markdown("### LEAD() - Access Next Row")
        st.markdown("""
        **Syntax:**
        ```sql
        LEAD(column, offset, default_value) OVER ([PARTITION BY ...] ORDER BY ...)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Next Sale Prediction")
            query = """
            SELECT 
                sale_id,
                product,
                amount,
                LEAD(amount) OVER (PARTITION BY product ORDER BY sale_id) AS next_amount,
                LEAD(sale_date) OVER (PARTITION BY product ORDER BY sale_id) AS next_date
            FROM sales
            ORDER BY product, sale_id;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # FIRST_VALUE TAB
    with tab3:
        st.markdown("### FIRST_VALUE() - First Row Value")
        st.markdown("""
        **Syntax:**
        ```sql
        FIRST_VALUE(column) OVER ([PARTITION BY ...] ORDER BY ... [ROWS ...])
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Compare to First Order")
            query = """
            SELECT 
                order_id,
                customer_name,
                order_amount,
                FIRST_VALUE(order_amount) OVER (
                    PARTITION BY customer_id 
                    ORDER BY order_id
                ) AS first_order,
                order_amount - FIRST_VALUE(order_amount) OVER (
                    PARTITION BY customer_id 
                    ORDER BY order_id
                ) AS growth
            FROM orders
            ORDER BY customer_id, order_id;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # LAST_VALUE TAB
    with tab4:
        st.markdown("### LAST_VALUE() - Last Row Value (Full Frame Required)")
        st.markdown("""
        **Syntax:**
        ```sql
        LAST_VALUE(column) OVER ([PARTITION BY ...] ORDER BY ... 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Latest Order Amount")
            query = """
            SELECT 
                order_id,
                customer_name,
                order_amount,
                LAST_VALUE(order_amount) OVER (
                    PARTITION BY customer_id 
                    ORDER BY order_id
                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                ) AS latest_order,
                LAST_VALUE(order_id) OVER (
                    PARTITION BY customer_id 
                    ORDER BY order_id
                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                ) AS latest_order_id
            FROM orders
            ORDER BY customer_id, order_id;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)
    
    # NTH_VALUE TAB
    with tab5:
        st.markdown("### NTH_VALUE() - Nth Row Value")
        st.markdown("""
        **Syntax:**
        ```sql
        NTH_VALUE(column, n) OVER ([PARTITION BY ...] ORDER BY ... [ROWS ...])
        ```
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Get 2nd Highest Salary per Department")
            query = """
            WITH ranked_employees AS (
                SELECT
                    department,
                    employee_name,
                    salary,
                    NTH_VALUE(salary, 2) OVER (
                        PARTITION BY department 
                        ORDER BY salary DESC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                    ) AS second_highest_salary,
                    NTH_VALUE(employee_name, 2) OVER (
                        PARTITION BY department 
                        ORDER BY salary DESC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                    ) AS second_highest_emp
                FROM employees
            )
            SELECT DISTINCT
                department,
                second_highest_salary,
                second_highest_emp
            FROM ranked_employees
            WHERE second_highest_salary IS NOT NULL;
            """
            st.code(query, language="sql")
        
        with col2:
            result, error = execute_query(query, conn)
            if error:
                st.error(f"Error: {error}")
            else:
                st.dataframe(result, use_container_width=True)


# ==================== SAMPLE DATA ====================

elif page == "Sample Data":
    st.header("Sample Datasets")
    st.markdown("Preview the databases used in all examples")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Employees", "Sales", "Orders", "Performance"])
    
    employees_df, sales_df, orders_df, performance_df = create_sample_data()
    
    with tab1:
        st.subheader("Employees Table")
        st.info("10 employees across 4 departments with various salary levels")
        st.dataframe(employees_df, use_container_width=True)
    
    with tab2:
        st.subheader("Sales Table")
        st.info("20 sales transactions across 3 products and 4 regions")
        st.dataframe(sales_df, use_container_width=True)
    
    with tab3:
        st.subheader("Orders Table")
        st.info("20 orders from 9 customers at different dates")
        st.dataframe(orders_df, use_container_width=True)
    
    with tab4:
        st.subheader("Performance Table")
        st.info("Monthly performance metrics comparing revenue vs target")
        st.dataframe(performance_df, use_container_width=True)


# ==================== CUSTOM QUERY ====================

elif page == "Custom Query":
    st.header("Custom Query Runner")
    st.markdown("Write your own SQL queries using the sample tables available")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Available Tables & Columns:")
        st.markdown("""
        **employees**
        - employee_id (INTEGER)
        - employee_name (TEXT)
        - department (TEXT)
        - salary (INTEGER)
        - hire_date (TEXT)
        
        **sales**
        - sale_id (INTEGER)
        - sale_date (DATETIME)
        - product (TEXT)
        - amount (INTEGER)
        - region (TEXT)
        
        **orders**
        - order_id (INTEGER)
        - customer_id (INTEGER)
        - customer_name (TEXT)
        - order_date (DATETIME)
        - order_amount (INTEGER)
        
        **performance**
        - employee_id (INTEGER)
        - month (TEXT)
        - revenue (INTEGER)
        - target (INTEGER)
        """)
    
    with col2:
        st.markdown("### Query Examples:")
        st.markdown("""
        ```sql
        -- Running Total of Sales Amount
        SELECT 
            sale_id,
            product,
            amount,
            SUM(amount) OVER (ORDER BY sale_id)
        FROM sales;
        ```
        
        ```sql
        -- Top 3 Sales by Region
        SELECT * FROM (
            SELECT 
            *,
            ROW_NUMBER() OVER (PARTITION BY region 
                        ORDER BY amount DESC)
            FROM sales
        ) WHERE ROW_NUMBER <= 3;
        ```
        ```sql
        -- Moving Average of Sales Amount
        SELECT 
            sale_id,
            sale_date,
            amount,
            AVG(amount) OVER (
            ORDER BY sale_id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) as moving_avg
        FROM sales;
        ```
        
        """)
    
    st.markdown("---")
    
    # Query Input
    query_input = st.text_area(
        "**Enter your SQL query:**",
        height=300,
        value="""SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as avg_salary
FROM employees
ORDER BY department, salary DESC;"""
    )
    
    if st.button("🚀 Execute Query", key="execute_query"):
        result, error = execute_query(query_input, conn)
        
        if error:
            st.error(f"❌ Query Error: {error}")
        else:
            st.success("✅ Query executed successfully!")
            st.dataframe(result, use_container_width=True)
            
            # Show statistics
            if len(result) > 0:
                col1, col2, col3 = st.columns(3)
                col1.metric("Rows Returned", len(result))
                col2.metric("Columns", len(result.columns))
                col3.metric("Memory Usage", f"{result.memory_usage(deep=True).sum() / 1024:.2f} KB")


# ==================== QUICK REFERENCE ====================

elif page == "Quick Reference":
    st.header("Quick Reference Guide")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Syntax", "Common Patterns", "Mistakes", "Tips"])
    
    with tab1:
        st.markdown("### Basic Window Function Syntax")
        st.code("""
SELECT
    column1,
    column2,
    WINDOW_FUNCTION() OVER (
        [PARTITION BY column]
        [ORDER BY column [ASC|DESC]]
        [ROWS BETWEEN ... AND ...]
    ) AS window_result
FROM table_name;
        """, language="sql")
        
        st.markdown("### Frame Boundaries")
        st.code("""
ROWS BETWEEN
    UNBOUNDED PRECEDING      -- From first row
    | n PRECEDING            -- n rows before
    | CURRENT ROW
    AND
    CURRENT ROW
    | n FOLLOWING            -- n rows after
    | UNBOUNDED FOLLOWING    -- To last row
        """, language="sql")
        
        st.markdown("### RANGE vs ROWS")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**ROWS (Physical)**")
            st.code("""ROWS BETWEEN 5 PRECEDING 
AND CURRENT ROW""", language="sql")
        with col2:
            st.markdown("**RANGE (Value-based)**")
            st.code("""RANGE BETWEEN INTERVAL '7 days' PRECEDING 
AND CURRENT ROW""", language="sql")
    
    with tab2:
        st.markdown("### Running Total Pattern")
        st.code("""
SELECT 
    date,
    amount,
    SUM(amount) OVER (
        ORDER BY date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM transactions;
        """, language="sql")
        
        st.markdown("### Top N Per Group Pattern")
        st.code("""
SELECT * FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY department 
            ORDER BY salary DESC
        ) as rank
    FROM employees
) ranked
WHERE rank <= 3;
        """, language="sql")
        
        st.markdown("### Comparison to Group Average Pattern")
        st.code("""
SELECT 
    name,
    value,
    AVG(value) OVER (PARTITION BY group) as avg,
    value - AVG(value) OVER (PARTITION BY group) as diff
FROM data;
        """, language="sql")
        
        st.markdown("### Month-over-Month Change Pattern")
        st.code("""
SELECT 
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as prev_revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) as change,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) 
        / LAG(revenue) OVER (ORDER BY month), 2) as pct_change
FROM monthly_data;
        """, language="sql")
    
    with tab3:
        st.markdown("### ❌ Mistake 1: Missing ORDER BY")
        col1, col2 = st.columns(2)
        with col1:
            st.error("**Wrong**")
            st.code("""SELECT 
    SUM(salary) OVER (
        PARTITION BY department
    )
FROM employees;
-- Returns department total, not running total!
            """, language="sql")
        with col2:
            st.success("**Correct**")
            st.code("""SELECT 
    SUM(salary) OVER (
        PARTITION BY department
        ORDER BY employee_id
        ROWS BETWEEN UNBOUNDED PRECEDING 
            AND CURRENT ROW
    )
FROM employees;
-- Returns running total
            """, language="sql")
        
        st.markdown("### ❌ Mistake 2: Wrong Frame for LAST_VALUE()")
        col1, col2 = st.columns(2)
        with col1:
            st.error("**Wrong**")
            st.code("""SELECT 
    LAST_VALUE(salary) OVER (
        PARTITION BY department 
        ORDER BY employee_id
    )
-- Returns current or next row only!
            """, language="sql")
        with col2:
            st.success("**Correct**")
            st.code("""SELECT 
    LAST_VALUE(salary) OVER (
        PARTITION BY department 
        ORDER BY employee_id
        ROWS BETWEEN UNBOUNDED PRECEDING 
            AND UNBOUNDED FOLLOWING
    )
-- Returns actual last value
            """, language="sql")
        
        st.markdown("### ❌ Mistake 3: Using Window Function in GROUP BY")
        col1, col2 = st.columns(2)
        with col1:
            st.error("**Wrong**")
            st.code("""SELECT 
    department,
    ROW_NUMBER() OVER (...) as num
FROM employees
GROUP BY department
-- Error! Can't use window in GROUP BY
            """, language="sql")
        with col2:
            st.success("**Correct**")
            st.code("""WITH ranked AS (
    SELECT 
        department,
        salary,
        ROW_NUMBER() OVER (...) as num
    FROM employees
)
SELECT * FROM ranked
-- Use CTE first
            """, language="sql")
    
    with tab4:
        st.markdown("### ✅ Performance Tips")
        st.markdown("""
        1. **Index Partition Columns**: Create index on columns used in PARTITION BY
           ```sql
           CREATE INDEX idx_dept_id ON employees(department, employee_id);
           ```
        
        2. **Check Execution Plan**: Understand query performance
           ```sql
           EXPLAIN SELECT ... FROM employees WHERE ...;
           ```
        
        3. **Materialize Complex Results**: Store intermediate results
           ```sql
           CREATE TEMP TABLE ranked_data AS
           SELECT *, ROW_NUMBER() OVER (...) FROM ...;
           ```
        
        4. **Use Specific Frames**: Narrow frames perform better
           ```sql
           -- Better: Specific frame
           ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
           -- Instead of: Full frame
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ```
        
        5. **Reuse Window Definitions**: Use WINDOW clause (some SQL dialects)
           ```sql
           SELECT *, 
               ROW_NUMBER() OVER w as rn,
               RANK() OVER w as rank
           FROM employees
           WINDOW w AS (PARTITION BY department ORDER BY salary DESC);
           ```
        """)
        
        st.markdown("### When to Use Which Function")
        reference_df = pd.DataFrame({
            "Use Case": [
                "Get running total",
                "Top N per group",
                "Compare individuals to group",
                "Date-over-date change",
                "Rank with gaps on ties",
                "Rank without gaps",
                "Divide into quartiles",
                "Get previous row value",
                "Access first value",
                "Complex relative position"
            ],
            "Function": [
                "SUM + ORDER BY + ROWS",
                "ROW_NUMBER + PARTITION BY",
                "AVG + PARTITION BY",
                "LAG or LEAD",
                "RANK()",
                "DENSE_RANK()",
                "NTILE(4)",
                "LAG()",
                "FIRST_VALUE()",
                "NTH_VALUE()"
            ]
        })
        st.dataframe(reference_df, use_container_width=True)


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Created by Saravanakumar on February 2026</p>
    <p>Compatible with: PostgreSQL, SQL Server, MySQL 8.0+, Oracle, Snowflake</p>
</div>
""", unsafe_allow_html=True)

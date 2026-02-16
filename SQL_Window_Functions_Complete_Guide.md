# SQL Window Functions - Complete Comprehensive Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Window Functions Overview](#window-functions-overview)
3. [Core Concepts](#core-concepts)
4. [Aggregate Window Functions](#aggregate-window-functions)
5. [Ranking Window Functions](#ranking-window-functions)
6. [Analytical Window Functions](#analytical-window-functions)
7. [Frame Specifications](#frame-specifications)
8. [Top 5 Interview Questions](#top-5-interview-questions)
9. [Real-World Use Cases](#real-world-use-cases)
10. [Performance Optimization Tips](#performance-optimization-tips)

---

## Introduction

Window functions are a powerful SQL feature that allows you to perform calculations across sets of rows that are related to the current row. Unlike GROUP BY which condenses results, window functions maintain all original rows while providing aggregated data alongside them.

### Why Window Functions Matter?
- **Trending Analysis**: Track performance over time
- **Comparative Analysis**: Compare individual records against aggregates
- **Ranking & Leaderboards**: Rank products, employees, students
- **Running Totals**: Calculate cumulative sums
- **Gap Analysis**: Identify differences between consecutive rows

---

## Window Functions Overview

### Basic Syntax

```sql
SELECT
    column1,
    column2,
    WINDOW_FUNCTION() OVER (
        [PARTITION BY column]
        [ORDER BY column]
        [ROWS BETWEEN ... AND ...]
    ) AS window_result
FROM table_name;
```

### Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **PARTITION BY** | Divides rows into groups | `PARTITION BY department` |
| **ORDER BY** | Defines row order within partition | `ORDER BY salary DESC` |
| **ROWS/RANGE** | Specifies frame boundaries | `ROWS BETWEEN 3 PRECEDING AND CURRENT ROW` |
| **CURRENT ROW** | Current row in frame | `PRECEDING or CURRENT ROW` |

---

## Core Concepts

### 1. Window Frame

A window frame is a set of rows relative to the current row within a partition.

**Types of Frames:**
- **ROWS**: Physical row-based frame
- **RANGE**: Value-based frame

**Frame Boundaries:**
```sql
UNBOUNDED PRECEDING      -- From first row in partition
n PRECEDING              -- n rows before current
CURRENT ROW             -- Current row only
n FOLLOWING             -- n rows after current
UNBOUNDED FOLLOWING     -- Till last row in partition
```

### 2. Logical Flow of Window Functions

```
┌─────────────────────────────────────┐
│       Source Data (All Rows)        │
├─────────────────────────────────────┤
│   Group rows by PARTITION BY        │
├─────────────────────────────────────┤
│   Sort within partition by ORDER BY │
├─────────────────────────────────────┤
│   Define frame boundary (ROWS/RANGE)│
├─────────────────────────────────────┤
│   Calculate window function         │
├─────────────────────────────────────┤
│   Return all rows with results      │
└─────────────────────────────────────┘
```

---

## Aggregate Window Functions

### SUM() OVER()

**What it does**: Calculates cumulative or partitioned sum
**Syntax**:
```sql
SUM(column) OVER (
    [PARTITION BY partition_column]
    [ORDER BY sort_column]
    [ROWS BETWEEN ... AND ...]
)
```

**Example 1: Running Total by Department**
```sql
SELECT
    employee_id,
    employee_name,
    salary,
    department,
    SUM(salary) OVER (
        PARTITION BY department 
        ORDER BY employee_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_salary
FROM employees;
```

**Output Example**:
```
employee_id | employee_name | salary | department | running_total_salary
------------|---------------|--------|-----------|--------------------
1           | John          | 50000  | Sales      | 50000
2           | Jane          | 60000  | Sales      | 110000
3           | Mike          | 55000  | Sales      | 165000
4           | Alice         | 70000  | IT         | 70000
5           | Bob           | 65000  | IT         | 135000
```

**Example 2: Total Department Salary (No ORDER BY)**
```sql
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    SUM(salary) OVER (PARTITION BY department) AS dept_total_salary
FROM employees;
```

**Output Example**:
```
employee_id | employee_name | department | salary | dept_total_salary
------------|---------------|-----------|--------|------------------
1           | John          | Sales      | 50000  | 165000
2           | Jane          | Sales      | 60000  | 165000
3           | Mike          | Sales      | 55000  | 165000
4           | Alice         | IT         | 70000  | 135000
5           | Bob           | IT         | 65000  | 135000
```

---

### AVG() OVER()

**What it does**: Calculates average within a window
**Syntax**:
```sql
AVG(column) OVER (
    [PARTITION BY partition_column]
    [ORDER BY sort_column]
)
```

**Example: Compare to Department Average**
```sql
SELECT
    employee_name,
    department,
    salary,
    ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS dept_avg_salary,
    ROUND(salary - AVG(salary) OVER (PARTITION BY department), 2) AS diff_from_avg
FROM employees;
```

**Output Example**:
```
employee_name | department | salary | dept_avg_salary | diff_from_avg
--------------|-----------|--------|-----------------|-------------
John          | Sales      | 50000  | 55000.00        | -5000.00
Jane          | Sales      | 60000  | 55000.00        | 5000.00
Mike          | Sales      | 55000  | 55000.00        | 0.00
Alice         | IT         | 70000  | 67500.00        | 2500.00
Bob           | IT         | 65000  | 67500.00        | -2500.00
```

---

### COUNT() OVER()

**What it does**: Counts rows within a window
**Syntax**:
```sql
COUNT(column) OVER ([PARTITION BY ...] [ORDER BY ...])
```

**Example: Purchase Frequency**
```sql
SELECT
    customer_id,
    order_date,
    order_amount,
    COUNT(*) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS purchase_count_to_date
FROM orders;
```

**Output Example**:
```
customer_id | order_date | order_amount | purchase_count_to_date
------------|------------|--------------|---------------------
1           | 2024-01-15 | 100          | 1
1           | 2024-02-20 | 150          | 2
1           | 2024-03-10 | 200          | 3
2           | 2024-01-05 | 50           | 1
2           | 2024-02-14 | 75           | 2
```

---

### MAX() / MIN() OVER()

**What it does**: Finds maximum/minimum within a window

**Example: Highest and Lowest Salary in Department**
```sql
SELECT
    employee_name,
    department,
    salary,
    MAX(salary) OVER (PARTITION BY department) AS max_dept_salary,
    MIN(salary) OVER (PARTITION BY department) AS min_dept_salary,
    MAX(salary) OVER (PARTITION BY department) - salary AS gap_to_max
FROM employees;
```

**Output Example**:
```
employee_name | department | salary | max_dept_salary | min_dept_salary | gap_to_max
--------------|-----------|--------|-----------------|-----------------|----------
John          | Sales      | 50000  | 60000           | 50000           | 10000
Jane          | Sales      | 60000  | 60000           | 50000           | 0
Mike          | Sales      | 55000  | 60000           | 50000           | 5000
Alice         | IT         | 70000  | 70000           | 65000           | 0
Bob           | IT         | 65000  | 70000           | 65000           | 5000
```

---

## Ranking Window Functions

### ROW_NUMBER()

**What it does**: Assigns unique sequential number to each row
**Syntax**:
```sql
ROW_NUMBER() OVER (
    [PARTITION BY column]
    ORDER BY column [ASC|DESC]
)
```

**Key Characteristics**:
- Always returns unique numbers
- Assigns consecutive integers
- Useful for finding duplicates or specific rankings

**Example: Top Performers by Department**
```sql
SELECT
    ROW_NUMBER() OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) AS rank_in_dept,
    employee_name,
    department,
    salary
FROM employees;
```

**Output Example**:
```
rank_in_dept | employee_name | department | salary
-------------|---------------|-----------|-------
1            | Jane          | Sales      | 60000
2            | Mike          | Sales      | 55000
3            | John          | Sales      | 50000
1            | Alice         | IT         | 70000
2            | Bob           | IT         | 65000
```

---

### RANK()

**What it does**: Assigns rank with gaps for ties
**Syntax**:
```sql
RANK() OVER (
    [PARTITION BY column]
    ORDER BY column [ASC|DESC]
)
```

**Key Characteristics**:
- Gaps in rank when there are ties
- Multiple rows can have same rank
- Next rank skips numbers based on ties

**Example: Leaderboard with Skipped Ranks**
```sql
SELECT
    RANK() OVER (ORDER BY score DESC) AS rank,
    player_name,
    game,
    score
FROM game_scores;
```

**Output Example**:
```
rank | player_name | game    | score
-----|-------------|---------|-------
1    | Alice       | Fortnite| 2500
1    | Bob         | Fortnite| 2500
3    | Charlie     | Fortnite| 2300
4    | Diana       | Fortnite| 2100
```

---

### DENSE_RANK()

**What it does**: Assigns rank with no gaps
**Syntax**:
```sql
DENSE_RANK() OVER (
    [PARTITION BY column]
    ORDER BY column [ASC|DESC]
)
```

**Key Characteristics**:
- No gaps in ranking
- Same as RANK() but consecutive
- Useful for "Top N" without rank gaps

**Example: Top 3 Scores Per Category**
```sql
SELECT
    DENSE_RANK() OVER (
        PARTITION BY category 
        ORDER BY sales DESC
    ) AS dense_rank,
    product_name,
    category,
    sales
FROM product_sales
WHERE DENSE_RANK() OVER (
    PARTITION BY category 
    ORDER BY sales DESC
) <= 3;
```

**Output Example**:
```
dense_rank | product_name | category   | sales
-----------|--------------|-----------|-------
1          | Product A    | Electronics| 50000
2          | Product B    | Electronics| 45000
3          | Product C    | Electronics| 40000
1          | Widget X     | Hardware   | 35000
2          | Widget Y     | Hardware   | 30000
3          | Widget Z     | Hardware   | 28000
```

---

### PERCENT_RANK()

**What it does**: Calculates percentile rank (0 to 1)
**Syntax**:
```sql
PERCENT_RANK() OVER ([PARTITION BY ...] ORDER BY ...)
```

**Formula**: `(rank - 1) / (total rows - 1)`

**Example: Performance Percentile**
```sql
SELECT
    employee_name,
    performance_score,
    ROUND(PERCENT_RANK() OVER (
        ORDER BY performance_score DESC
    ), 4) AS percentile_rank,
    ROUND(PERCENT_RANK() OVER (
        ORDER BY performance_score DESC
    ) * 100, 2) AS percentile_rank_pct
FROM performance_reviews;
```

**Output Example**:
```
employee_name | performance_score | percentile_rank | percentile_rank_pct
--------------|-------------------|-----------------|-------------------
Alice         | 95                | 1.0             | 100.00
Bob           | 85                | 0.75            | 75.00
Charlie       | 75                | 0.5             | 50.00
Diana         | 65                | 0.25            | 25.00
Eve           | 55                | 0.0             | 0.00
```

---

### NTILE()

**What it does**: Divides rows into N equal groups
**Syntax**:
```sql
NTILE(n) OVER ([PARTITION BY ...] ORDER BY ...)
```

**Example: Quartile Analysis**
```sql
SELECT
    customer_id,
    total_purchases,
    NTILE(4) OVER (ORDER BY total_purchases DESC) AS quartile
FROM customer_purchases;
```

**Output Example**:
```
customer_id | total_purchases | quartile
------------|-----------------|----------
1           | 5000            | 1
2           | 4500            | 1
3           | 4000            | 1
4           | 3500            | 2
5           | 3000            | 2
6           | 2500            | 3
7           | 2000            | 3
8           | 1000            | 4
9           | 500             | 4
```

---

## Analytical Window Functions

### LAG()

**What it does**: Accesses data from previous row
**Syntax**:
```sql
LAG(column, [offset], [default_value]) OVER (
    [PARTITION BY ...]
    ORDER BY ...
)
```

**Parameters**:
- `column`: Column to retrieve
- `offset`: Number of rows back (default: 1)
- `default_value`: Value for first row (default: NULL)

**Example 1: Month-over-Month Comparison**
```sql
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) AS revenue_change,
    ROUND(((revenue - LAG(revenue) OVER (ORDER BY month)) 
        / LAG(revenue) OVER (ORDER BY month) * 100), 2) AS pct_change
FROM monthly_sales;
```

**Output Example**:
```
month      | revenue | previous_month_revenue | revenue_change | pct_change
-----------|---------|----------------------|----------------|----------
Jan 2024   | 10000   | NULL                 | NULL           | NULL
Feb 2024   | 12000   | 10000                | 2000           | 20.00
Mar 2024   | 11000   | 12000                | -1000          | -8.33
Apr 2024   | 15000   | 11000                | 4000           | 36.36
```

**Example 2: Identifying Gaps in Sequences**
```sql
SELECT
    id,
    student_name,
    attendance_date,
    LAG(attendance_date) OVER (
        PARTITION BY student_id 
        ORDER BY attendance_date
    ) AS previous_attendance_date,
    attendance_date - LAG(attendance_date) OVER (
        PARTITION BY student_id 
        ORDER BY attendance_date
    ) AS days_gap
FROM attendance_log;
```

**Output Example**:
```
id | student_name | attendance_date | previous_attendance_date | days_gap
---|--------------|-----------------|--------------------------|-------
1  | John         | 2024-01-01      | NULL                     | NULL
2  | John         | 2024-01-02      | 2024-01-01              | 1
3  | John         | 2024-01-05      | 2024-01-02              | 3
4  | John         | 2024-01-06      | 2024-01-05              | 1
```

---

### LEAD()

**What it does**: Accesses data from next row
**Syntax**:
```sql
LEAD(column, [offset], [default_value]) OVER (
    [PARTITION BY ...]
    ORDER BY ...
)
```

**Example: Detect Promotions/Demotions**
```sql
SELECT
    employee_id,
    employee_name,
    year,
    salary,
    LEAD(salary) OVER (
        PARTITION BY employee_id 
        ORDER BY year
    ) AS next_year_salary,
    LEAD(salary) OVER (
        PARTITION BY employee_id 
        ORDER BY year
    ) - salary AS salary_change
FROM employee_salary_history;
```

**Output Example**:
```
employee_id | employee_name | year | salary | next_year_salary | salary_change
------------|---------------|------|--------|------------------|-------------
1           | John          | 2022 | 50000  | 52000            | 2000
1           | John          | 2023 | 52000  | 55000            | 3000
1           | John          | 2024 | 55000  | NULL             | NULL
2           | Jane          | 2022 | 60000  | 61000            | 1000
2           | Jane          | 2023 | 61000  | 62000            | 1000
```

---

### FIRST_VALUE()

**What it does**: Returns value from first row in frame
**Syntax**:
```sql
FIRST_VALUE(column) OVER (
    [PARTITION BY ...]
    ORDER BY ...
    [ROWS/RANGE ...]
)
```

**Example: Compare to First Order**
```sql
SELECT
    order_id,
    customer_id,
    order_date,
    order_amount,
    FIRST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS first_order_amount,
    order_amount - FIRST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS growth_from_first
FROM orders;
```

**Output Example**:
```
order_id | customer_id | order_date | order_amount | first_order_amount | growth_from_first
---------|-------------|------------|--------------|-------------------|----------------
1        | 1           | 2024-01-15 | 100          | 100                | 0
2        | 1           | 2024-02-20 | 150          | 100                | 50
3        | 1           | 2024-03-10 | 200          | 100                | 100
4        | 2           | 2024-01-05 | 50           | 50                 | 0
5        | 2           | 2024-02-14 | 75           | 50                 | 25
```

---

### LAST_VALUE()

**What it does**: Returns value from last row in frame
**Syntax**:
```sql
LAST_VALUE(column) OVER (
    [PARTITION BY ...]
    ORDER BY ...
    [ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING]
)
```

**Important**: Must explicitly set frame to get correct last value

**Example: Latest Status**
```sql
SELECT
    ticket_id,
    ticket_status,
    status_date,
    LAST_VALUE(ticket_status) OVER (
        PARTITION BY ticket_id 
        ORDER BY status_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS current_status
FROM ticket_history;
```

**Output Example**:
```
ticket_id | ticket_status | status_date | current_status
-----------|--------------|-------------|---------------
1          | Open         | 2024-01-10  | Closed
1          | In Progress  | 2024-01-15  | Closed
1          | Closed       | 2024-01-20  | Closed
2          | Open         | 2024-02-05  | In Progress
2          | In Progress  | 2024-02-10  | In Progress
```

---

### NTH_VALUE()

**What it does**: Returns value from Nth row in frame
**Syntax**:
```sql
NTH_VALUE(column, n) OVER (
    [PARTITION BY ...]
    ORDER BY ...
    [ROWS BETWEEN ...]
)
```

**Example: Get 2nd Highest Salary**
```sql
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    NTH_VALUE(salary, 2) OVER (
        PARTITION BY department
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS second_highest_salary
FROM employees;
```

**Output Example**:
```
employee_id | employee_name | department | salary | second_highest_salary
------------|---------------|-----------|--------|---------------------
2           | Jane          | Sales      | 60000  | 55000
3           | Mike          | Sales      | 55000  | 55000
1           | John          | Sales      | 50000  | 55000
4           | Alice         | IT         | 70000  | 65000
5           | Bob           | IT         | 65000  | 65000
```

---

## Frame Specifications

### ROWS vs RANGE

| Aspect | ROWS | RANGE |
|--------|------|-------|
| **Scope** | Physical rows | Value-based |
| **Example** | "Next 5 rows" | "Values from 100 to 500" |
| **Ties** | Treats ties separately | Treats peers together |

### Frame Boundaries

**Example 1: Last 3 Rows**
```sql
SELECT
    date,
    sales,
    SUM(sales) OVER (
        ORDER BY date
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS three_day_total
FROM daily_sales;
```

**Example 2: Full Partition**
```sql
SELECT
    employee_id,
    date,
    hours_worked,
    SUM(hours_worked) OVER (
        PARTITION BY employee_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS total_hours
FROM timesheet;
```

**Example 3: Range Frame**
```sql
SELECT
    date,
    price,
    AVG(price) OVER (
        ORDER BY date
        RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
    ) AS seven_day_avg
FROM stock_prices;
```

---

## Top 5 Interview Questions

### Question 1: Difference Between RANK(), DENSE_RANK(), and ROW_NUMBER()

**What Companies Want to Know**: 
- Do you understand subtle differences in ranking functions?
- Can you choose correct function for requirement?
- Problem-solving ability

**Answer with Examples**:

Given scores: 100, 90, 90, 80

```
ROW_NUMBER()   RANK()   DENSE_RANK()
    1            1          1
    2            2          2
    3            2          2
    4            3          3
```

**Code**:
```sql
SELECT
    score,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank
FROM scores;
```

**When to Use**:
- **ROW_NUMBER()**: Finding nth occurrence, pagination
- **RANK()**: Competition rankings, leader boards
- **DENSE_RANK()**: Top N products, rankings without gaps

---

### Question 2: How to Get Top N Records Per Group?

**What Companies Want to Know**:
- Complex filtering combining window functions
- Data filtration logic
- Query optimization thinking

**Answer**:
```sql
SELECT * FROM (
    SELECT
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department 
            ORDER BY salary DESC
        ) as rank
    FROM employees
) ranked_employees
WHERE rank <= 3;
```

**Alternative with QUALIFY (modern SQL)**:
```sql
SELECT
    employee_name,
    department,
    salary
FROM employees
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY department 
    ORDER BY salary DESC
) <= 3;
```

---

### Question 3: Calculate Running Total

**What Companies Want to Know**:
- Understanding of ORDER BY in window functions
- Frame specification comprehension
- Real-world data analysis ability

**Answer**:
```sql
SELECT
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders;
```

**Key Points**:
- Without `ORDER BY`: Returns total for entire partition
- With `ORDER BY` + `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: Running total
- Without `ROWS`: All rows up to current per ORDER BY

---

### Question 4: Identify Gaps and Islands

**What Companies Want to Know**:
- Advanced window function usage
- Data quality assessment skills
- Complex problem solving

**Answer - Find Consecutive Dates (Islands)**:
```sql
SELECT
    customer_id,
    attendance_date,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY attendance_date
    ) - 
    EXTRACT(DAY FROM attendance_date) as island_id
FROM attendance;
```

**Answer - Find Gaps**:
```sql
SELECT
    customer_id,
    order_date,
    LAG(order_date) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as previous_order_date,
    order_date - LAG(order_date) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as days_since_last_order
FROM orders
WHERE order_date - LAG(order_date) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date
) > 30;
```

---

### Question 5: Month-over-Month Growth Calculation

**What Companies Want to Know**:
- Business metrics understanding
- LAG/LEAD usage
- Complex calculations with aggregations

**Answer**:
```sql
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as prev_month_revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) as absolute_growth,
    ROUND(
        100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) 
        / LAG(revenue) OVER (ORDER BY month), 2
    ) as growth_percentage
FROM monthly_revenue
ORDER BY month;
```

**Output Example**:
```
month      | revenue | prev_month_revenue | absolute_growth | growth_percentage
-----------|---------|-------------------|-----------------|----------------
2024-01    | 100000  | NULL              | NULL            | NULL
2024-02    | 120000  | 100000            | 20000           | 20.00
2024-03    | 110000  | 120000            | -10000          | -8.33
2024-04    | 135000  | 110000            | 25000           | 22.73
```

---

## Real-World Use Cases

### Use Case 1: E-Commerce - Customer Lifetime Value Analysis

```sql
SELECT
    customer_id,
    customer_name,
    last_purchase_date,
    ROUND(SUM(order_amount) OVER (
        PARTITION BY customer_id
    ), 2) as total_spent,
    ROUND(AVG(order_amount) OVER (
        PARTITION BY customer_id
    ), 2) as avg_order_value,
    COUNT(*) OVER (
        PARTITION BY customer_id
    ) as total_orders,
    ROUND(SUM(order_amount) OVER (
        PARTITION BY customer_id
    ) / 
    CAST((CURRENT_DATE - first_purchase_date) AS FLOAT) 
    * 365, 2) as annual_spending_rate,
    CASE 
        WHEN DENSE_RANK() OVER (ORDER BY SUM(order_amount) OVER (
            PARTITION BY customer_id
        ) DESC) <= 20 THEN 'VIP'
        WHEN DENSE_RANK() OVER (ORDER BY SUM(order_amount) OVER (
            PARTITION BY customer_id
        ) DESC) <= 100 THEN 'Premium'
        ELSE 'Standard'
    END as customer_segment
FROM customer_orders
GROUP BY customer_id;
```

---

### Use Case 2: Finance - Churn Detection

```sql
SELECT
    customer_id,
    customer_name,
    last_activity_date,
    DATEDIFF(day, last_activity_date, CURRENT_DATE) as days_inactive,
    LAG(purchase_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY transaction_date
    ) as previous_purchase,
    purchase_amount as current_purchase,
    CASE 
        WHEN DATEDIFF(day, last_activity_date, CURRENT_DATE) > 90 
        THEN 'At Risk'
        WHEN LAG(purchase_amount) OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date
        ) > purchase_amount * 1.2
        THEN 'Declining'
        ELSE 'Active'
    END as churn_status
FROM transactions
WHERE DATEDIFF(day, last_activity_date, CURRENT_DATE) > 30;
```

---

### Use Case 3: HR - Salary Benchmarking

```sql
SELECT
    employee_id,
    employee_name,
    department,
    job_title,
    salary,
    ROUND(AVG(salary) OVER (
        PARTITION BY department, job_title
    ), 2) as avg_salary_role,
    salary - ROUND(AVG(salary) OVER (
        PARTITION BY department, job_title
    ), 2) as salary_variance,
    PERCENT_RANK() OVER (
        PARTITION BY department 
        ORDER BY salary
    ) * 100 as salary_percentile,
    CASE 
        WHEN salary > AVG(salary) OVER (
            PARTITION BY department, job_title
        ) * 1.1 THEN 'Above Average'
        WHEN salary < AVG(salary) OVER (
            PARTITION BY department, job_title
        ) * 0.9 THEN 'Below Average'
        ELSE 'Average'
    END as salary_status
FROM employee_salary;
```

---

### Use Case 4: Marketing - Campaign Performance

```sql
SELECT
    campaign_id,
    campaign_name,
    click_date,
    clicks,
    conversions,
    SUM(clicks) OVER (
        PARTITION BY campaign_id 
        ORDER BY click_date
        ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
    ) as seven_day_clicks,
    SUM(conversions) OVER (
        PARTITION BY campaign_id 
        ORDER BY click_date
        ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
    ) as seven_day_conversions,
    ROUND(100.0 * SUM(conversions) OVER (
        PARTITION BY campaign_id 
        ORDER BY click_date
        ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
    ) / 
    SUM(clicks) OVER (
        PARTITION BY campaign_id 
        ORDER BY click_date
        ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
    ), 2) as seven_day_conversion_rate,
    RANK() OVER (
        PARTITION BY DATE(click_date)
        ORDER BY conversions DESC
    ) as daily_campaign_rank
FROM campaign_metrics;
```

---

### Use Case 5: Manufacturing - Quality Control

```sql
SELECT
    production_date,
    product_id,
    defect_count,
    units_produced,
    ROUND(100.0 * defect_count / units_produced, 2) as defect_rate,
    AVG(ROUND(100.0 * defect_count / units_produced, 2)) OVER (
        PARTITION BY product_id 
        ORDER BY production_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as thirty_day_avg_defect_rate,
    CASE 
        WHEN ROUND(100.0 * defect_count / units_produced, 2) > 
        AVG(ROUND(100.0 * defect_count / units_produced, 2)) OVER (
            PARTITION BY product_id
        ) * 1.5
        THEN 'Alert'
        ELSE 'Normal'
    END as quality_status,
    ROW_NUMBER() OVER (
        PARTITION BY product_id 
        ORDER BY defect_count DESC
    ) as worst_day_rank
FROM production_quality
WHERE production_date >= DATEADD(day, -60, CAST(CURRENT_DATE AS DATE));
```

---

## Performance Optimization Tips

### 1. Indexing Strategy

```sql
-- Bad: Full table scan for each window partition
SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY purchase_date)
FROM orders;

-- Good: Create index on partition and order columns
CREATE INDEX idx_orders_customer_date ON orders(customer_id, purchase_date);
SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY purchase_date)
FROM orders;
```

### 2. Materialization Strategy

```sql
-- Instead of complex window function in filter
CREATE TEMPORARY TABLE ranked_data AS
SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;

SELECT * FROM ranked_data WHERE rank <= 3;
```

### 3. Window Function Reuse

```sql
-- Bad: Computing same window twice
SELECT
    employee_id,
    SUM(salary) OVER (PARTITION BY department) as total,
    AVG(salary) OVER (PARTITION BY department) as average,
    COUNT(*) OVER (PARTITION BY department) as cnt
FROM employees;

-- Same execution plan - window is computed once
-- SQL engine optimizes multiple references
```

### 4. Frame Specification Impact

```sql
-- Slow: Full frame conversion for each row
SELECT SUM(salary) OVER (ORDER BY employee_id)
FROM employees;

-- Fast: Specific frame (if applicable)
SELECT SUM(salary) OVER (
    ORDER BY employee_id
    ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
)
FROM employees;
```

### 5. Data Type Considerations

```sql
-- Bad: Type conversion in window function
SELECT 
    CAST(salary AS DECIMAL) / 
    SUM(CAST(salary AS DECIMAL)) 
    OVER (PARTITION BY department)
FROM employees;

-- Good: Consistent data types
SELECT 
    salary / 
    SUM(salary) OVER (PARTITION BY department)
FROM employees;
```

---

## Best Practices Summary

| Practice | Benefit |
|----------|---------|
| **Always specify ORDER BY in ranking functions** | Ensures consistent results |
| **Use PARTITION BY to divide logical groups** | Improves performance and accuracy |
| **Specify ROWS when using ORDER BY** | Prevents unexpected results |
| **Index partition and order columns** | Significant performance improvement |
| **Materialize large results** | Avoid recomputation |
| **Use WINDOW clauses for multiple calculations** | Cleaner, faster code |
| **Test with EXPLAIN PLAN** | Understand execution strategy |

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Forgetting ORDER BY in Aggregates
```sql
-- Returns entire partition sum, not running total
SELECT SUM(salary) OVER (PARTITION BY department)
FROM employees;

-- ✅ Correct: Specify ORDER BY for running total
SELECT SUM(salary) OVER (PARTITION BY department ORDER BY employee_id)
FROM employees;
```

### ❌ Mistake 2: Wrong Frame for LAST_VALUE()
```sql
-- Returns NULL or current row only
SELECT LAST_VALUE(salary) OVER (PARTITION BY department ORDER BY employee_id)
FROM employees;

-- ✅ Correct: Specify full frame
SELECT LAST_VALUE(salary) OVER (
    PARTITION BY department 
    ORDER BY employee_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
FROM employees;
```

### ❌ Mistake 3: Aggregating Window Results
```sql
-- Error: Can't apply GROUP BY to windowed functions
SELECT department, AVG(ROW_NUMBER() OVER (ORDER BY salary)) 
FROM employees
GROUP BY department;

-- ✅ Correct: Use CTE or subquery
WITH ranked AS (
    SELECT department, ROW_NUMBER() OVER (ORDER BY salary) as rank
    FROM employees
)
SELECT department, AVG(rank)
FROM ranked
GROUP BY department;
```

---

## Conclusion

Window functions are indispensable for modern SQL analysis. They allow you to:
- ✅ Maintain row-level detail while performing aggregations
- ✅ Compare individual records against group statistics
- ✅ Rank and score data efficiently
- ✅ Calculate complex analytics in single query
- ✅ Solve business problems elegantly

Master these functions to unlock advanced data analysis capabilities!

---

**Last Updated**: February 2026
**Compatibility**: SQL Server, PostgreSQL, MySQL 8.0+, Oracle, Snowflake

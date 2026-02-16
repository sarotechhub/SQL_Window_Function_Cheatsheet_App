# SQL Window Functions - Complete Guide & Interactive Cheat Sheet

## 📁 Contents

This repository contains a comprehensive guide and interactive tool for mastering SQL Window Functions:

### 1. **SQL_Window_Functions_Complete_Guide.md**
A detailed 5000+ word markdown guide covering:
- ✅ Introduction and core concepts
- ✅ All 15+ window functions with syntax and examples
- ✅ Aggregate functions (SUM, AVG, COUNT, MIN, MAX)
- ✅ Ranking functions (ROW_NUMBER, RANK, DENSE_RANK, NTILE, PERCENT_RANK)
- ✅ Analytical functions (LAG, LEAD, FIRST_VALUE, LAST_VALUE, NTH_VALUE)
- ✅ Frame specifications and ROWS vs RANGE
- ✅ **Top 5 Interview Questions** with detailed answers
- ✅ **Real-world use cases**: E-commerce, Finance, HR, Marketing, Manufacturing
- ✅ Performance optimization tips
- ✅ Best practices and common mistakes

### 2. **window_functions_streamlit_app.py**
An interactive Streamlit application with:
- ✅ Live query executor with sample data
- ✅ 8 interactive sections:
  - Home page with overview
  - Aggregate functions (SUM, AVG, COUNT, MIN, MAX)
  - Ranking functions (ROW_NUMBER, RANK, DENSE_RANK, NTILE, PERCENT_RANK)
  - Analytical functions (LAG, LEAD, FIRST_VALUE, LAST_VALUE, NTH_VALUE)
  - Sample data viewer
  - Custom query runner
  - Quick reference guide
- ✅ Built-in sample datasets (employees, sales, orders, performance)
- ✅ Real-time SQL execution and result visualization
- ✅ Side-by-side query and output display
- ✅ Common patterns and mistakes reference

---

## 🚀 Quick Start

### Option 1: Read the Complete Guide

Simply open `SQL_Window_Functions_Complete_Guide.md` in any markdown viewer to read the comprehensive guide with all examples and explanations.

### Option 2: Run the Interactive Streamlit App

#### Installation

```bash
# Install required packages
pip install streamlit pandas numpy

# Optional: If using specific database
pip install sqlite3  # Usually comes with Python
```

#### Running the Application

```bash
# Navigate to the directory
cd "c:\SARAVANA\SQL\Window Functions"

# Run the Streamlit app
streamlit run window_functions_streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 📊 Sample Datasets

The Streamlit app includes 4 pre-built sample datasets:

### Employees
```
employee_id, employee_name, department, salary, hire_date
10 employees across 4 departments (Sales, IT, HR, Finance)
Salary range: $50,000 - $90,000
```

### Sales
```
sale_id, sale_date, product, amount, region
20 transactions of products A, B, C
Regions: North, South, East, West
Amount range: $100 - $250
```

### Orders
```
order_id, customer_id, customer_name, order_date, order_amount
20 orders from 9 customers
Order amount range: $50 - $300
```

### Performance
```
employee_id, month, revenue, target
Monthly revenue vs target metrics
```

---

## 🎓 Learning Path

### For Beginners
1. Start with the **Home** section in the Streamlit app
2. Read the **Core Concepts** in the markdown guide
3. Try each aggregate function example in the app (SUM, AVG, COUNT, MIN, MAX)
4. Experiment with custom queries

### For Intermediate Users
1. Study the **Using Cases** section in the markdown guide
2. Explore ranking functions in the app (ROW_NUMBER, RANK, DENSE_RANK)
3. Master the differences between RANK vs DENSE_RANK vs ROW_NUMBER
4. Work through the "Top 5 Interview Questions"

### For Advanced Users
1. Deep dive into **Analytical Functions** (LAG, LEAD, NTH_VALUE)
2. Study **Frame Specifications** and optimize performance
3. Review **Real-World Use Cases**
4. Understand performance optimization strategies

---

## 📚 Key Topics Covered

### Window Function Categories

#### 1. Aggregate Window Functions
| Function | Purpose | Use Case |
|----------|---------|----------|
| **SUM()** | Running totals or partition sum | Track cumulative sales |
| **AVG()** | Average within window | Compare to group average |
| **COUNT()** | Count rows in window | Frequency analysis |
| **MIN()** | Minimum value | Find lowest price |
| **MAX()** | Maximum value | Find highest salary |

#### 2. Ranking Window Functions
| Function | Behavior | Use Case |
|----------|----------|----------|
| **ROW_NUMBER()** | Unique sequential numbers | Pagination, duplicates |
| **RANK()** | Ranks with gaps | Leaderboards, competitions |
| **DENSE_RANK()** | Consecutive ranks | Top N without gaps |
| **NTILE()** | Divide into N groups | Quartiles, deciles |
| **PERCENT_RANK()** | Percentile (0-1) | Performance percentiles |

#### 3. Analytical Window Functions
| Function | Purpose | Use Case |
|----------|---------|----------|
| **LAG()** | Access previous row | Month-over-month change |
| **LEAD()** | Access next row | Predict next value |
| **FIRST_VALUE()** | First row in frame | Compare to baseline |
| **LAST_VALUE()** | Last row in frame | Latest status |
| **NTH_VALUE()** | Nth row in frame | Access specific position |

---

## 💡 Common Use Cases

### 1. Running Total
Track cumulative amounts over time
```sql
SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

### 2. Top N Per Group
Get top 3 employees by department
```sql
WHERE ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) <= 3
```

### 3. Comparison to Average
See how each salary compares to department average
```sql
salary - AVG(salary) OVER (PARTITION BY department)
```

### 4. Month-over-Month Growth
Calculate percentage change from previous month
```sql
100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) ...
```

### 5. Customer Segments
Divide customers into quartiles by spend
```sql
NTILE(4) OVER (ORDER BY total_spent DESC)
```

---

## 🔧 Technical Details

### Supported SQL Dialects
- ✅ PostgreSQL 9.3+
- ✅ SQL Server 2012+
- ✅ MySQL 8.0+
- ✅ Oracle 8.1+
- ✅ Snowflake
- ✅ SQLite (via Streamlit app)

### Streamlit App Features

**Interactive Elements:**
- Live SQL query runner
- Real-time result visualization
- Side-by-side code and output
- Sample data browser
- Quick reference panels
- Copy-friendly code blocks

**Sample Data Management:**
- In-memory SQLite database
- 4 pre-configured tables
- 40+ sample records
- Fast query execution

---

## ❓ Frequently Asked Questions

### Q: What's the difference between RANK() and DENSE_RANK()?
**A:** 
- **RANK()**: Has gaps when there are ties (1, 2, 2, 4)
- **DENSE_RANK()**: No gaps (1, 2, 2, 3)

See the detailed explanation in the markdown guide and try both in the Streamlit app!

### Q: When should I use ROW_NUMBER() vs RANK()?
**A:**
- **ROW_NUMBER()**: When you need unique numbers (pagination)
- **RANK()**: When you need competition rankings

### Q: How do I get the top 3 from each department?
**A:**
```sql
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
    FROM employees
) WHERE rank <= 3;
```

### Q: Why is LAST_VALUE() returning only NULL or current row?
**A:** You need to specify the frame explicitly:
```sql
LAST_VALUE(salary) OVER (
    ORDER BY id
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

### Q: What's the performance impact of window functions?
**A:** Minimal if you:
- Index PARTITION BY columns
- Use specific ROWS frames instead of full frames
- Materialize large intermediate results
- Group similar window definitions

---

## 📖 Top Interview Questions Answered

The markdown guide includes the **Top 5 Questions Companies Ask**:

1. **Difference between RANK(), DENSE_RANK(), and ROW_NUMBER()**
   - Detailed comparison with examples
   - When to use each

2. **How to get Top N records per group?**
   - Multiple solutions
   - Modern SQL alternatives

3. **Calculate running total**
   - Understanding ORDER BY and frames
   - Real-world patterns

4. **Identify gaps and islands**
   - Advanced problem solving
   - Data quality assessment

5. **Month-over-month growth calculation**
   - Business metrics
   - Complex calculations

---

## 🎯 Learning Tips

1. **Start Simple**: Begin with basic aggregates (SUM, AVG)
2. **Try Examples**: Run examples in the Streamlit app before writing your own
3. **Modify Queries**: Change the queries to understand how they work
4. **Practice Ranking**: Compare ROW_NUMBER, RANK, and DENSE_RANK side-by-side
5. **Understand Frames**: ROWS BETWEEN is key to correct results
6. **Check Output**: Always verify results make sense
7. **Performance**: Use EXPLAIN to understand query plans

---

## 🚨 Common Mistakes

### ❌ Forgetting ORDER BY in Running Totals
```sql
-- Wrong: Returns partition total, not running total
SUM(salary) OVER (PARTITION BY department)

-- Correct: Specify ORDER BY
SUM(salary) OVER (PARTITION BY department ORDER BY employee_id)
```

### ❌ Wrong Frame for LAST_VALUE()
```sql
-- Wrong: May return current row only
LAST_VALUE(salary) OVER (PARTITION BY department ORDER BY id)

-- Correct: Specify full frame
LAST_VALUE(salary) OVER (
    PARTITION BY department 
    ORDER BY id
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

### ❌ Using Window Function in GROUP BY
```sql
-- Wrong: Can't use window function in GROUP BY
SELECT department, ROW_NUMBER() OVER (...) FROM employees GROUP BY department

-- Correct: Use CTE or subquery
WITH ranked AS (SELECT *, ROW_NUMBER() OVER (...) FROM employees)
SELECT * FROM ranked
```

---

## 📞 Getting Help

**Within the Streamlit App:**
- Use the "Quick Reference" tab for syntax
- View "Common Patterns" for typical use cases
- Check the "Sample Data" tab to understand tables
- Try "Custom Query" to experiment

**In the Markdown Guide:**
- Read the "Best Practices Summary"
- Study the "Common Mistakes to Avoid"
- Review the "Top 5 Interview Questions"

---

## 🔄 Workflow Recommendations

### For Learning
1. Open the markdown guide in a browser/editor
2. Run the Streamlit app in another window
3. Read concept in guide
4. Try example in app
5. Modify and experiment

### For Reference
- Keep the markdown guide bookmarked
- Use Quick Reference tab in app for syntax
- Copy-paste and modify existing queries

### For Practice
- Use custom query runner
- Try to write queries from scratch
- Verify results before moving on

---

## 📊 Performance Optimization

Key strategies covered in the guide:

1. **Index Smart**: Create indexes on PARTITION BY and ORDER BY columns
2. **Frame Carefully**: Use specific frames instead of full partitions
3. **Materialize Early**: Store intermediate results
4. **Monitor Execution**: Use EXPLAIN to understand plans
5. **Data Types**: Ensure consistent types in calculations

---

## 🎓 Certification Readiness

The materials prepare you for:
- ✅ SQL certification exams
- ✅ Database professional interviews
- ✅ Data analyst interviews
- ✅ Advanced SQL courses

Topic coverage matches:
- Microsoft SQL Server Certifications
- AWS Database Specialty
- Google Cloud Associate Cloud Engineer
- Azure Data Engineer Associate

---

## 📝 Version History

- **v1.0** (February 2026): Initial comprehensive guide and Streamlit app
- Complete coverage of 15+ window functions
- 5000+ word markdown guide
- Interactive Streamlit application
- 40+ real-world examples

---

## 💼 Professional Use

These materials are suitable for:
- **Self-Learning**: Comprehensive guide for individuals
- **Team Training**: Share guide and Streamlit app with team
- **Reference**: Quick reference for complex queries
- **Interview Prep**: Study top 5 interview questions
- **Teaching**: Use real-world use cases in classroom

---

## 🔗 Quick Links

- **Markdown Guide**: See SQL_Window_Functions_Complete_Guide.md
- **Streamlit App**: Run window_functions_streamlit_app.py
- **Sample Data**: View in Streamlit app "Sample Data" tab
- **Interview Prep**: See markdown guide "Top 5 Interview Questions"

---

## 📧 Notes

- All examples use standard SQL syntax
- Compatible with most modern SQL servers
- Sample data is in-memory (no external DB needed)
- Streamlit app is read-only (for learning)
- Markdown guide is exportable to PDF

---

**Happy Learning! Master Window Functions and Elevate Your SQL Skills! 🚀**

---

*Last Updated: February 2026*
*Designed for: Beginners to Professionals*
*Scope: Complete Window Functions Coverage*

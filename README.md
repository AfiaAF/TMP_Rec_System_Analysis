# Recommendation System Analysis
## Project Overview
This project focuses on building a recommendation system that uses historical user data to deliver personalized suggestions across various domains, such as product recommendations, service enhancements, etc.

---

## Project Objectives

1. Develop Personalized Recommendations based on user behavior and past interactions.
2. Address Diverse Use Cases including products, content, and services.
3. Utilize Historical Data to enhance predictive performance.
4. Enhance User Engagement and retention with relevant recommendations.
5. Ensure Scalability and Real-Time Performance under large data volumes.
6. Boost Business Metrics such as sales and conversion rates.
7. Balance Accuracy & Diversity to avoid recommendation monotony.

---

## Dataset Description

The dataset, collected from a real-world e-commerce site, consists of three main files:

### 1. `events.csv`
- Contains user interactions: `view`, `addtocart`, `transaction`
- ~2.7 million events from ~1.4 million users

### 2. `item_properties.csv`
- Describes item metadata: price, category, availability
- Includes timestamped snapshots of properties to track changes over time

### 3. `category_tree.csv`
- Maps category hierarchies: child-parent relationships

---

## Tools & Technologies Used

| Tool | Description |
|------|-------------|
| Python | Core language for data manipulation, modeling, and evaluation |
| Pandas / NumPy | Data loading, cleaning, transformation |
| Matplotlib / Seaborn / Plotly | Visualizations and insights |
| Scikit-learn | Machine learning algorithms for classification and anomaly detection |
| Jupyter Notebook | Interactive development environment |
| Git / GitHub | Version control and project tracking |

---

## Methodology: CRISP-DM Framework

### 1. Business Understanding

We aim to improve personalization in recommendations. Business questions include:

- What are the most viewed, added to cart, and purchased products overall?
- What is the average conversion rate from view → cart → purchase?
- Which categories drive the most purchases?
- What are the top products users tend to add to cart after viewing?
- Are there user behavior patterns that indicate bots or abnormal activity?
- What proportion of items are currently available versus unavailable?
- How has the number of recorded events changed over time?

### 2. Data Understanding

- Loaded and explored `events.csv`, `item_properties.csv`, and `category_tree.csv`
- Identified key distributions, missing data, event types, and temporal trends

### 3. Data Preparation

- Merged user events with item metadata
- Feature engineering: session-level stats, item-category mapping
- Detected and filtered **abnormal users** (see below)
- Handled time-based property changes

---

## Summary of Abnormal User Detection and Interpretation

An **Isolation Forest** model was used to detect abnormal users from a total of **436,810** users. Using a contamination parameter of `0.06`, the model flagged **26,191 users**, resulting in an **anomaly rate of 6.0%**.

### Key Findings

#### 1. Top Users by Views
- Users with extremely high views (e.g., 2,420 views, 214 cart events, 163 purchases) likely represent **bot or scripted behaviors**.

#### 2. Top Users by Session Duration
- Some users had session durations exceeding **72 days**, yet minimal interaction — a strong signal of **tracking issues** or **misbehaving clients**.

#### 3. Top Users by Transactions
- Several users had **100+ transactions**, which could suggest **heavy buyers** or **automated activity**.

### Anomaly Type Breakdown

| Type                      | Count  |
|---------------------------|--------|
| Other                     | 22,422 |
| Long Session              | 3,718  |
| High Views (Possible Bot) | 15     |
| Heavy Buyer               | 36     |
| **Total Abnormal Users**  | 26,191 |

### Contamination Tuning

| Contamination | Abnormal Users | % of Total |
|---------------|----------------|------------|
| 0.01          | 4,366          | 1.00%      |
| 0.03          | 13,105         | 3.00%      |
| 0.05          | 21,776         | 4.99%      |
| **0.06**      | **26,191**     | **6.00%**  |
| 0.10          | 43,661         | 10.00%     |

A contamination level of **6%** provided a good balance between sensitivity and specificity.

### Conclusion

The anomaly detection process successfully detected:

- **Bots or scripted users**
- **Passive anomalies** (e.g., stuck sessions)
- **Unusually active buyers**

These users were **excluded** from downstream modeling to improve recommendation accuracy and reduce noise.

---

## Visualizations & Insights

Visualizations developed include:

- Funnel analysis from views → cart → purchase
- Distribution of item availability
- Temporal event analysis
- PCA projection showing separation between normal and abnormal users
- Charts showing interaction patterns of abnormal users

---


---

## Deliverables

| Deliverable | Description |
|------------|-------------|
| **Model & Visualizations** | Trained recommender model, anomaly detection model, and business insight visualizations |
| **Documentation** | This README file, code notebooks, modeling explanations, and evaluation reports |
| **Presentation** | Summary of business problems, methodology, insights, and model performance |

---

## TL;DR of findings

- Isolation Forest detected **6% of users as abnormal**
- Abnormal users showed **unusual behavior** like extremely high views or long sessions
- PCA visualization showed clear separation between normal and abnormal users
- Dataset was cleaned by **removing these users** to improve model performance and reduce noise



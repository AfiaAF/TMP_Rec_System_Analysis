# Recommendation System Analysis

## Project Overview

This project focuses on building a recommendation system that uses historical user data to deliver personalized suggestions across various domains, such as product recommendations, service enhancements, and more.

## Project Objectives

* Develop personalized recommendations based on user behavior and past interactions.
* Address diverse use cases including products, content, and services.
* Utilize historical data to enhance predictive performance.
* Enhance user engagement and retention with relevant recommendations.
* Ensure scalability and real-time performance under large data volumes.
* Boost business metrics such as sales and conversion rates.
* Balance accuracy and diversity to avoid recommendation monotony.

## Dataset Description

The dataset, collected from a real-world e-commerce site, consists of three main files:

1. **events.csv**
   Contains user interactions: view, addtocart, transaction
   Approximately 2.7 million events from \~1.4 million users

2. **item\_properties.csv**
   Describes item metadata: price, category, availability
   Includes timestamped snapshots of properties to track changes over time

3. **category\_tree.csv**
   Maps category hierarchies: child-parent relationships

## Tools & Technologies Used

| Tool                          | Description                                                          |
| ----------------------------- | -------------------------------------------------------------------- |
| Python                        | Core language for data manipulation, modeling, and evaluation        |
| Pandas / NumPy                | Data loading, cleaning, transformation                               |
| Matplotlib / Seaborn / Plotly | Visualizations and insights                                          |
| Scikit-learn                  | Machine learning algorithms for classification and anomaly detection |
| Jupyter Notebook              | Interactive development environment                                  |
| Git / GitHub                  | Version control and project tracking                                 |

## Methodology: CRISP-DM Framework

### 1. Business Understanding

The goal was to improve personalization in recommendations. Key business questions included:

* What are the most viewed, added to cart, and purchased products overall?
* What is the average conversion rate from view → cart → purchase?
* Which categories drive the most purchases?
* What are the top products users tend to add to cart after viewing?
* Are there user behavior patterns that indicate bots or abnormal activity?
* What proportion of items are currently available versus unavailable?
* How has the number of recorded events changed over time?

### 2. Data Understanding

* Loaded and explored `events.csv`, `item_properties.csv`, and `category_tree.csv`.
* Identified key distributions, missing data, event types, and temporal trends.

### 3. Data Preparation

* Merged user events with item metadata.
* Engineered features such as session-level stats and item-category mappings.
* Detected and filtered abnormal users (described below).
* Handled time-based property changes.

---

## Task 1: Multi-class Classification of User Events

### Findings

1. **Logistic Regression with Balanced Class Weights**

   * Achieved \~97% accuracy, but this was misleading due to severe class imbalance.
   * Model predominantly predicted the majority class (`view`) and failed to detect rare classes (`addtocart` and `transaction`) with zero precision, recall, and F1 scores.

2. **XGBoost with SMOTE**

   * Improved recall for minority class `addtocart`, though precision remained low.
   * Overall accuracy dropped to \~62%, reflecting challenges in handling imbalanced data.
   * Failed to detect the rarest class (`transaction`).
   * Suggested approaches include hierarchical classification, class-specific oversampling, or focal loss.

3. **ROC Curve Analysis (One-vs-Rest)**

   * AUC scores for `addtocart` (0.48), `transaction` (0.40), and `view` (0.44) were below 0.5, indicating poor discrimination.
   * Possible causes: misalignment between labels and predictions, inconsistent feature processing, or overfitting on synthetic data.

4. **Feature Importance (XGBoost Gain)**

   * `user_total_views` was the most important feature, followed by `event_index`, `item_total_views`, and `view_count_per_item`.
   * Indicated model reliance on user behavior and event timing rather than item-specific features.

### Recommendations

* Verify label-probability alignment and ensure feature consistency between datasets.
* Use confusion matrix analysis to understand misclassification patterns.
* Explore targeted binary classification for rare classes, advanced sampling, and alternative loss functions.
* Engineer additional user/session-level temporal features for improved predictive performance.

---

## Task 2: Abnormal User Detection and Interpretation

An Isolation Forest model was used to identify abnormal users from a total of 436,810 users. With a contamination parameter of 0.06, the model flagged 26,191 users (\~6%) as abnormal.

### Key Findings

* **High Views:** Some users had extremely high views (e.g., 2,420 views, 214 cart events, 163 purchases), likely bots or scripted behaviors.
* **Long Sessions:** Certain users exhibited session durations exceeding 72 days but had minimal interactions, indicating tracking issues or client malfunctions.
* **High Transactions:** A few users with 100+ transactions may represent heavy buyers or automated activity.

### Anomaly Breakdown

| Type                      | Count  |
| ------------------------- | ------ |
| Other                     | 22,422 |
| Long Session              | 3,718  |
| High Views (Possible Bot) | 15     |
| Heavy Buyer               | 36     |
| **Total Abnormal Users**  | 26,191 |

### Contamination Tuning

| Contamination | Abnormal Users | % of Total |
| ------------- | -------------- | ---------- |
| 0.01          | 4,366          | 1.00%      |
| 0.03          | 13,105         | 3.00%      |
| 0.05          | 21,776         | 4.99%      |
| **0.06**      | **26,191**     | **6.00%**  |
| 0.10          | 43,661         | 10.00%     |

A contamination level of 6% balanced sensitivity and specificity effectively.

### Conclusion

* The anomaly detection process successfully identified bots, passive anomalies (e.g., stuck sessions), and unusual buyers.
* These users were excluded from downstream modeling to improve recommendation accuracy and reduce noise.

---

## Visualizations & Insights

* Funnel analysis from views → cart → purchase
* Distribution of item availability
* Temporal event analysis
* PCA projections showing clear separation between normal and abnormal users
* Charts illustrating abnormal user interaction patterns

---

## Deliverables

| Deliverable            | Description                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------- |
| Model & Visualizations | Trained recommender and anomaly detection models, business insights visualizations |
| Documentation          | README, code notebooks, modeling explanations, evaluation reports                  |
| Presentation           | Summary of business problems, methodology, insights, and model performance         |

---

## TL;DR

* Logistic regression struggled with imbalanced classes despite high accuracy.
* XGBoost with SMOTE improved minority class recall but had poor overall discrimination.
* Feature importance highlighted user behavior and event timing as key predictors.
* Isolation Forest detected \~6% of users as abnormal, including bots, long sessions, and heavy buyers.
* Removing abnormal users improved recommendation system accuracy and reduced noise.


## Business Recommendations
Based on the analysis and modeling results, the following actions are recommended:

- **Leveraging user behavior and event sequence features** to improve recommendation accuracy and relevance is advised.  
- **Exclude bots and abnormal users** from model training to reduce noise and enhance predictive performance.  
- **Implement real-time anomaly detection** to flag suspicious activity and protect system integrity.  
- **Prioritize users with high conversion likelihood** for targeted marketing and promotional efforts.  
- **Investigate and resolve session tracking issues** that lead to unrealistically long session durations.  
- **Rerun A/B tests using cleaned datasets** to ensure more reliable and valid experimental results.  
- **Set up monitoring for unexpected spikes** in views or session lengths to maintain data quality.

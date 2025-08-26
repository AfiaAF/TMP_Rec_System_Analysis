import streamlit as st
import joblib
import pandas as pd

# === Load model and label mappings ===
@st.cache_resource
def load_model():
    model = joblib.load("xgb_multiclass_model.pkl")
    event_mapping = joblib.load("event_mapping.pkl")
    return model, event_mapping

model, event_mapping = load_model()
reverse_mapping = {v: k for k, v in event_mapping.items()}

# === Page Configuration ===
st.set_page_config(page_title="Next Event Predictor", layout="centered")

st.title("🧠 Next Event Prediction")
st.markdown("Predict what a user is most likely to do next after viewing a product.")

# === Input Interface ===
st.header("📥 User Behavior Inputs")

# Input: view_count_per_item
view_count = st.slider(
    "🔁 Views of this item by user (view_count_per_item)", 
    min_value=0, max_value=20, value=1
)

# Input: item_total_views
item_total_views = st.number_input(
    "👁️ Total views for this item (item_total_views)", 
    min_value=0, max_value=5000, value=100
)

# Input: user_total_views
user_total_views = st.number_input(
    "🙋‍♂️ Total items viewed by user (user_total_views)", 
    min_value=0, max_value=1000, value=20
)

# Input: event_index
event_index = st.slider(
    "🕓 Position of this event in session (event_index)", 
    min_value=0, max_value=100, value=3
)

# === Prepare DataFrame for Prediction ===
input_data = pd.DataFrame([{
    "view_count_per_item": view_count,
    "item_total_views": item_total_views,
    "user_total_views": user_total_views,
    "event_index": event_index
}])

# === Predict ===
if st.button("Predict Next Event"):
    pred_label = model.predict(input_data)[0]
    pred_event = reverse_mapping.get(pred_label, "Unknown")

    st.success(f"🧾 Predicted next event: **{pred_event.upper()}**")
    
    # Optionally show probabilities
    proba = model.predict_proba(input_data)[0]
    st.subheader("🔍 Prediction Probabilities")
    proba_df = pd.DataFrame({
        'Event': [reverse_mapping[i] for i in range(len(proba))],
        'Probability': [round(p, 4) for p in proba]
    }).sort_values(by='Probability', ascending=False)
    
    st.table(proba_df.reset_index(drop=True))

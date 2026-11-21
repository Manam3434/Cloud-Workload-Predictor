# streamlit_app.py
import numpy as np
import streamlit as st

st.set_page_config(page_title="Cloud Workload Predictor")
st.title("Cloud Workload Predictor")

raw_history = st.text_input("Historical workload values (comma-separated)", "22, 25, 29, 34, 41, 48, 55")
steps = st.number_input("Forecast steps", min_value=1, max_value=20, value=3, step=1)

if st.button("Predict Workload"):
    try:
        history = [float(x.strip()) for x in raw_history.split(",") if x.strip()]
        if len(history) < 2:
            st.error("Enter at least 2 numeric values.")
        else:
            arr = np.array(history, dtype=float)
            diffs = np.diff(arr)
            # Damped trend projection using NumPy
            trend = float(np.mean(diffs[-3:]))
            preds = []
            last_val = float(arr[-1])
            for i in range(int(steps)):
                last_val = round(last_val + trend * (0.85 ** i), 2)
                preds.append(last_val)

            st.success("Forecast generated")
            st.json({"input_points": len(history), "predicted_workload": preds})
            st.line_chart(list(arr) + preds)
    except ValueError:
        st.error("Please enter valid numbers separated by commas.")
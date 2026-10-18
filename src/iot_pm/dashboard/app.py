"""Local Streamlit demonstration dashboard using synthetic telemetry."""
import pandas as pd
import streamlit as st
from iot_pm.simulation.generator import simulate

st.set_page_config(page_title="Predictive Maintenance Research",layout="wide")
st.title("Industrial equipment monitoring")
st.caption("Synthetic demonstration data — not live industrial equipment.")
n=st.sidebar.slider("Sensor readings",100,5000,700,100)
machines=st.sidebar.slider("Machines",2,25,6)
data=simulate(n=n,machines=machines)
machine=st.selectbox("Equipment",sorted(data.machine_id.unique()))
view=data[data.machine_id==machine].set_index("timestamp")
a,b,c=st.columns(3)
a.metric("Mean temperature °C",f"{view.temperature_c.mean():.1f}")
b.metric("Mean vibration mm/s",f"{view.vibration_mm_s.mean():.2f}")
c.metric("Simulated failure labels",str(view.failure.sum()))
st.subheader("Sensor history")
st.line_chart(view[["temperature_c","vibration_mm_s","pressure_bar"]])
st.subheader("Events")
st.dataframe(view.tail(20),use_container_width=True)
st.warning("Rule thresholds and trained synthetic models need site-specific verification before use.")

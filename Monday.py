import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy.signal import find_peaks
import secrets
from datetime import datetime

# --- SYSTEM UTILITIES ---
class MondayTelemetry:
    @staticmethod
    def get_trace_id():
        return f"DEV-{secrets.token_hex(4).upper()}"

    @staticmethod
    def log_event(msg):
        # Professional-grade logging for the terminal
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{MondayTelemetry.get_trace_id()}] {msg}")

# --- ANALYTICS ENGINE ---
class MondayAnalytics:
    def __init__(self, hours):
        self.hours = hours
        self.time_series = np.linspace(hours.min(), hours.max(), 500)

    def smooth_curve(self, y):
        """B-Spline interpolation for medical-grade telemetry look."""
        spline = make_interp_spline(self.hours, y, k=3)
        return spline(self.time_series)

    def detect_panics(self, y):
        """Identify Kernel Panic events (Stress > 85%)."""
        peaks, _ = find_peaks(y, height=85)
        return self.hours[peaks], np.array(y)[peaks]

# --- SIMULATION DATA ---
MondayTelemetry.log_event("Pulling Human Kernel Telemetry from LRAM...")

hours = np.arange(8, 19) # 8 AM to 6 PM

# Employee Load (Meetings, Admin, Scrums)
emp_raw = [25, 80, 98, 75, 62, 45, 55, 68, 82, 94, 35] 

# Job Hunter Load (Applications, Ghosting Anxiety, LinkedIn Lurking)
job_raw = [98, 92, 85, 70, 58, 48, 62, 78, 88, 96, 105] 

# Add Stochastic 'Coffee Noise' (The jitter factor)
noise = np.random.normal(0, 3, len(hours))
emp_raw = np.array(emp_raw) + noise
job_raw = np.array(job_raw) + noise

# --- PROCESS DATA ---
engine = MondayAnalytics(hours)
emp_smooth = engine.smooth_curve(emp_raw)
job_smooth = engine.smooth_curve(job_raw)

# Detect Failure Points
emp_panics_x, emp_panics_y = engine.detect_panics(emp_raw)
job_panics_x, job_panics_y = engine.detect_panics(job_raw)

# --- VISUALIZATION DASHBOARD ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(16, 9), dpi=120)

# The 'Future-State' Narrative Curves
ax.plot(engine.time_series, emp_smooth, color='#00FFCC', lw=4, label='Employee: Internal VPC Traffic (Scrum Overhead)')
ax.fill_between(engine.time_series, emp_smooth, alpha=0.15, color='#00FFCC')

ax.plot(engine.time_series, job_smooth, color='#FFD700', lw=4, ls='--', label='Job Hunter: North-South Requests (Application Race Condition)')
ax.fill_between(engine.time_series, job_smooth, alpha=0.1, color='#FFD700')

# Label Failure Points (Kernel Panics)
ax.scatter(emp_panics_x, emp_panics_y, color='#FF3131', s=200, marker='X', zorder=5, label='Kernel Panic: Resource Contention')
ax.scatter(job_panics_x, job_panics_y, color='#FF8C00', s=200, marker='*', zorder=5, label='Race Condition: Email Ghosting Spike')

# NARRATIVE ANNOTATIONS
ax.annotate('10:00 AM: SCALED SCRUM HELL\nContext-Switching @ 98% CPU', 
            xy=(10, 98), xytext=(8.2, 110),
            arrowprops=dict(arrowstyle='fancy', color='#00FFCC', lw=2), 
            fontsize=11, fontweight='bold', bbox=dict(facecolor='black', alpha=0.6))

ax.annotate('5:00 PM: REJECTION ANXIETY\nRetry Limit: EXCEEDED', 
            xy=(17, 96), xytext=(14.5, 115),
            arrowprops=dict(arrowstyle='fancy', color='#FFD700', lw=2), 
            fontsize=11, fontweight='bold', bbox=dict(facecolor='black', alpha=0.6))

# DASHBOARD STYLING
ax.set_title("MONDAY KERNEL AUDIT: HUMAN RESOURCE CONTENTION (v3.0)\n[Trace Analysis: Auburn Hills Tech Hub Node]", 
             fontsize=22, fontweight='bold', pad=40, color='white')
ax.set_xlabel("SYSTEM CHRONOLOGY (24HR CLOCK)", fontsize=14, color='gray', labelpad=15)
ax.set_ylabel("COGNITIVE LOAD % (CPU UTILIZATION)", fontsize=14, color='gray')

ax.set_xticks(hours)
ax.set_xticklabels([f"{h}:00" for h in hours])
ax.set_ylim(0, 130)

ax.grid(True, linestyle='--', alpha=0.1)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, fontsize=13)

plt.tight_layout()
MondayTelemetry.log_event("Telemetry Visualization Complete. Ready for Production Deployment.")
plt.show()
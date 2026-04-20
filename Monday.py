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
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{MondayTelemetry.get_trace_id()}] {msg}")

# --- ANALYTICS ENGINE ---
class MondayAnalytics:
    def __init__(self, hours):
        self.hours = hours
        self.time_series = np.linspace(hours.min(), hours.max(), 600)

    def smooth_curve(self, y):
        spline = make_interp_spline(self.hours, y, k=3)
        return spline(self.time_series)

    def detect_panics(self, y):
        peaks, _ = find_peaks(y, height=85)
        return self.hours[peaks], np.array(y)[peaks]

# --- SIMULATION DATA & JITTER ---
MondayTelemetry.log_event("Accessing Neural Mesh... Coffee Levels: CRITICAL.")

hours = np.arange(8, 19)
# Base Data
emp_raw = np.array([25, 80, 98, 75, 62, 45, 55, 68, 82, 94, 35])
job_raw = np.array([98, 92, 85, 70, 58, 48, 62, 78, 88, 96, 105])

# Add Stochastic Caffeine Jitter
def add_jitter(arr):
    return arr + np.random.normal(0, 2.5, len(arr))

emp_raw = add_jitter(emp_raw)
job_raw = add_jitter(job_raw)

# Smooth and Create High-Freq 'Vibrations'
engine = MondayAnalytics(hours)
emp_smooth = engine.smooth_curve(emp_raw)
job_smooth = engine.smooth_curve(job_raw)

# Simulating the 'Shaking' from too much espresso
jitter_noise = np.sin(engine.time_series * 50) * 0.8
emp_smooth += jitter_noise
job_smooth += jitter_noise

emp_panics_x, emp_panics_y = engine.detect_panics(emp_raw)
job_panics_x, job_panics_y = engine.detect_panics(job_raw)

# --- VISUALIZATION HUD ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(18, 11), dpi=110)
gs = fig.add_gridspec(4, 1, height_ratios=[3, 0.5, 0.5, 0.5])
ax = fig.add_subplot(gs[0:2, :]) # Main HUD
ax_vitals = fig.add_subplot(gs[3, :]) # Heartbeat/Vitals

# 1. NEON GLOW EFFECT (Stacking lines for bloom)
for i in range(1, 12, 2):
    ax.plot(engine.time_series, emp_smooth, color='#00FFCC', lw=i, alpha=0.04)
    ax.plot(engine.time_series, job_smooth, color='#FFD700', lw=i, alpha=0.04)

ax.plot(engine.time_series, emp_smooth, color='#00FFCC', lw=2.5, label='Employee: Internal VPC Traffic (Cold Boot)')
ax.plot(engine.time_series, job_smooth, color='#FFD700', lw=2.5, ls='--', label='Job Hunter: Application Race Condition')

# 2. VITALS SUBPLOT (The 'Detail' Part)
pulse_time = np.linspace(0, 10, 600)
pulse_signal = np.sin(pulse_time * 8) * np.exp(-np.cos(pulse_time * 2))
ax_vitals.plot(engine.time_series, pulse_signal, color='#FF3131', lw=1, alpha=0.7)
ax_vitals.fill_between(engine.time_series, pulse_signal, color='#FF3131', alpha=0.1)
ax_vitals.set_title(f"SYSTEM HEARTBEAT // PACKET LOSS: 1.2% // NODE_STATUS: OVERLOAD // TRACE: {MondayTelemetry.get_trace_id()}", 
                    loc='left', color='gray', fontsize=9, family='monospace')
ax_vitals.axis('off')

# 3. FAILURE MARKERS (Glow circles)
ax.scatter(emp_panics_x, emp_panics_y, color='#FF3131', s=350, marker='o', alpha=0.2)
ax.scatter(emp_panics_x, emp_panics_y, color='#FF3131', s=100, marker='X', label='KERNEL PANIC: RESOURCE DEADLOCK')

ax.scatter(job_panics_x, job_panics_y, color='#FFD700', s=350, marker='o', alpha=0.2)
ax.scatter(job_panics_x, job_panics_y, color='#FFD700', s=100, marker='*', label='RACE CONDITION: THREAD TIMEOUT')

# 4. FUNNY ANNOTATIONS (The Story)
ax.annotate('10:00 AM: THE UNPLANNED SCRUM\nMemory Leak: Weekend.dll not found', 
            xy=(10, 98), xytext=(8.5, 115),
            arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2", color='#00FFCC'),
            fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", fc="black", ec="#00FFCC", alpha=0.8))

ax.annotate('5:00 PM: REJECTION_LOOP.sh\nStatus: 404 Talent Not Found', 
            xy=(17, 96), xytext=(14.5, 120),
            arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.2", color='#FFD700'),
            fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", fc="black", ec="#FFD700", alpha=0.8))

# 5. FINAL HUD STYLING
ax.set_title("MONDAY KERNEL AUDIT // SYSTEM_LOAD: DANGEROUS\n[Location: Auburn Hills Tech Hub Node]", 
             fontsize=22, fontweight='bold', pad=35, family='monospace')
ax.set_ylabel("COGNITIVE LOAD (CPU %)", color='gray', fontsize=12)

# Custom Scanlines
for y_pos in range(0, 140, 10):
    ax.axhline(y_pos, color='white', alpha=0.03, lw=0.5)

ax.set_xticks(hours)
ax.set_xticklabels([f"{h}:00" for h in hours], color='gray')
ax.set_ylim(0, 140)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=11)

plt.tight_layout()
MondayTelemetry.log_event("Dashboard Synced to Neural Link. Happy Monday, Sai.")
plt.show()
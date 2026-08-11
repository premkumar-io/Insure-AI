# 📖 InsureAI™ User & Underwriter Guide

User manual for operating the **InsureAI™** web dashboard and understanding risk evaluation metrics.

---

## 1. Navigating the Dashboard

Open [http://localhost:8501](http://localhost:8501) in your browser.

```
+-----------------------------------------------------------------------+
| 🛡️ InsureAI PRO v1.0   AI Risk Analytics       [🟢 API Connected]    |
+-----------------------------------------------------------------------+
| [Quick Profiles]  |  Applicant Demographics  | Prediction Results     |
| - Young Executive |  - Age: 30              | - Low Premium          |
| - High-Risk Smoker|  - Weight / Height      | - Confidence: 78%      |
| - Fitness Fan     |  - Income & Smoker      | - Donut Chart          |
| - Senior Citizen  |  - City & Occupation    | - Policy Guidance      |
+-----------------------------------------------------------------------+
```

---

## 2. Using Quick Profile Presets

Click any button in the left sidebar to pre-fill test applicant scenarios:

- **👨‍💼 Young Executive**: 28 yrs, non-smoker, high income in Bangalore metro.
- **🚬 High-Risk Smoker**: 46 yrs, smoker, overweight in Delhi metro.
- **🏃 Healthy Fitness Enthusiast**: 31 yrs, normal BMI, non-smoker in Pune.
- **👴 Senior Citizen**: 64 yrs, retired, non-smoker in Jaipur.

---

## 3. Understanding Health Metrics & Predictions

### Instant Health Indicators
- **BMI (Body Mass Index)**: Automatically calculated ($\text{weight} / \text{height}^2$).
  - `Normal Weight`: $18.5 - 24.9$ kg/m²
  - `Overweight`: $25.0 - 29.9$ kg/m²
  - `Obese`: $\ge 30.0$ kg/m²
- **Lifestyle Risk**: Evaluated from smoking habit and BMI thresholds.
- **City Tier**: Maps location to Metro vs Non-Metro risk adjustments.

### Risk Category Classifications
- **Low Premium Category**: Low risk, eligible for standard policy rates & max discounts.
- **Medium Premium Category**: Moderate risk, standard rates with slight loading or wellness riders.
- **High Premium Category**: Elevated risk due to health metrics/smoking. Comprehensive medical checkup & loading applies.

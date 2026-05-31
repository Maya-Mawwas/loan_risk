# generative_report_generator.py
import pandas as pd
import random

def generate_customer_report(age, salary, debt, loans_count, work_years, approval):
    """
    Generates an AI-powered text report about the customer
    """
    
    # Financial assessment
    if salary < 3000:
        salary_status = "Very Low"
    elif salary < 5000:
        salary_status = "Medium"
    else:
        salary_status = "Very Good"
    
    if debt > 15000:
        debt_status = "High"
    elif debt > 8000:
        debt_status = "Medium"
    else:
        debt_status = "Low"
    
    # Generate recommendations
    recommendations = []
    if salary < 5000:
        recommendations.append("Increase monthly income")
    if debt > 10000:
        recommendations.append("Reduce debt level")
    if loans_count < 2:
        recommendations.append("Build credit history with small loans")
    if work_years < 3:
        recommendations.append("Gain more work experience")
    
    # Final report
    report = f"""
    ==================================================
    📄 AI-Generated Customer Credit Assessment Report
    ==================================================
    
    👤 Customer Information:
    • Age: {age} years
    • Monthly Salary: ${salary:,}
    • Debt Level: ${debt:,}
    • Previous Loans: {loans_count}
    • Work Experience: {work_years} years
    
    📊 Financial Assessment:
    • Salary Status: {salary_status}
    • Debt Status: {debt_status}
    • Risk Level: {'High' if debt > 15000 else 'Medium' if debt > 8000 else 'Low'}
    
    🎯 Loan Decision: {'✅ APPROVED' if approval == 1 else '❌ REJECTED'}
    
    💡 AI Recommendations:
    """
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            report += f"\n    {i}. {rec}"
    else:
        report += "\n    ✅ Customer meets all requirements"
    
    report += "\n    ==================================================\n"
    
    return report

# Test the report
print("=" * 50)
print("TEST CASE 1: Approved Customer")
print("=" * 50)
print(generate_customer_report(35, 6000, 12000, 4, 8, 1))

print("\n" + "=" * 50)
print("TEST CASE 2: Rejected Customer")
print("=" * 50)
print(generate_customer_report(22, 2000, 8000, 1, 1, 0))

# Batch report generation from CSV
print("\n" + "=" * 50)
print("BATCH REPORT: First 5 Customers from Dataset")
print("=" * 50)

df = pd.read_csv("loan_risk_dataset.csv")
for i in range(min(5, len(df))):
    row = df.iloc[i]
    print(generate_customer_report(
        row['age'], 
        row['salary'], 
        row['debt'], 
        row['loans_count'], 
        row['work_years'], 
        row['approved']
    ))
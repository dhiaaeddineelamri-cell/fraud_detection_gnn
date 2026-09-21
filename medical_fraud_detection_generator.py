import csv
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
random.seed(42)

# Define data pools
medicine_names = [
    "Amoxicillin", "Ibuprofen", "Metformin", "Lisinopril", "Atorvastatin",
    "Levothyroxine", "Omeprazole", "Amlodipine", "Gabapentin", "Hydrochlorothiazide",
    "Losartan", "Sertraline", "Simvastatin", "Clopidogrel", "Montelukast",
    "Escitalopram", "Rosuvastatin", "Albuterol", "Methylprednisolone", "Ciprofloxacin",
    "Azithromycin", "Prednisone", "Tramadol", "Oxycodone", "Morphine"
]

pharmacy_names = [
    "HealthPlus Pharmacy", "MediCare Drug Store", "Wellness Pharmacy", "QuickMeds",
    "City Pharmacy", "Central Drug Store", "Family Pharmacy", "Express Meds",
    "Corner Pharmacy", "Main Street Pharmacy", "Community Health Pharmacy",
    "Prime Pharmacy", "TrustedMeds", "CarePlus Pharmacy", "Metro Pharmacy"
]

doctor_specialties = [
    "Cardiology", "Neurology", "Orthopedics", "Dermatology", "Pediatrics",
    "Oncology", "Psychiatry", "Internal Medicine", "General Practice", "Endocrinology"
]

insurance_companies = [
    "BlueCross BlueShield", "UnitedHealth", "Aetna", "Cigna", "Humana",
    "Kaiser Permanente", "Anthem", "Medicare", "Medicaid", "Self-Pay"
]

diagnosis_codes = [
    "E11.9", "I10", "J44.9", "M54.5", "F41.9", "E78.5", "K21.9", "M79.7",
    "G89.29", "R51", "J45.909", "N18.3", "F33.1", "M25.551", "I25.10"
]

# Generate 1000 records
num_records = 1000

# Create fraud patterns - some doctors consistently refer to same pharmacies
fraud_doctor_ids = [f"DOC{str(i).zfill(4)}" for i in range(1, 21)]  # 20 fraudulent doctors
fraud_pharmacies = ["HealthPlus Pharmacy", "QuickMeds", "Express Meds", "TrustedMeds"]

# Helper function to generate random float
def random_float(min_val, max_val, decimals=2):
    return round(random.uniform(min_val, max_val), decimals)

# Generate data rows
rows = []
fraud_count = 0

for i in range(num_records):
    # Determine if this is a fraudulent record
    doctor_id = random.choice(fraud_doctor_ids) if random.random() < 0.3 else f"DOC{str(random.randint(21, 500)).zfill(4)}"
    is_fraud = 1 if doctor_id in fraud_doctor_ids else 0
    
    if is_fraud:
        fraud_count += 1
        pharmacy_name = random.choice(fraud_pharmacies)
        doctor_pharmacy_referral_count = random.randint(100, 500)
        fraud_risk_score = random_float(70, 100)
        doctor_pharmacy_distance = random_float(0.1, 5)
        price_variance = random_float(50, 200)
    else:
        pharmacy_name = random.choice(pharmacy_names)
        doctor_pharmacy_referral_count = random.randint(0, 500)
        fraud_risk_score = random_float(0, 100)
        doctor_pharmacy_distance = random_float(0.1, 100)
        price_variance = random_float(-50, 200)
    
    row = {
        # Prescription Information
        "prescription_id": f"RX{str(i+1).zfill(8)}",
        "prescription_date": (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d"),
        "prescription_time": f"{random.randint(8, 18):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}",
        "fill_date": (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d"),
        "refill_number": random.randint(0, 12),
        "days_supply": random.choice([30, 60, 90]),
        
        # Medicine Information
        "medicine_name": random.choice(medicine_names),
        "generic_name": random.choice(medicine_names),
        "ndc_code": f"{random.randint(10000, 99999)}-{random.randint(100, 999)}-{random.randint(10, 99)}",
        "dosage": random.choice(["10mg", "20mg", "50mg", "100mg", "250mg", "500mg"]),
        "dosage_form": random.choice(["Tablet", "Capsule", "Syrup", "Injection", "Cream"]),
        "quantity_prescribed": random.randint(10, 180),
        "quantity_dispensed": random.randint(10, 180),
        "unit_price": random_float(0.5, 500),
        "total_price": random_float(10, 5000),
        "ingredient_cost": random_float(5, 4500),
        "dispensing_fee": random_float(5, 50),
        "controlled_substance_class": random.choice(["None", "Schedule II", "Schedule III", "Schedule IV", "Schedule V"]),
        
        # Pharmacist Information
        "pharmacist_id": f"PH{str(random.randint(1, 200)).zfill(4)}",
        "pharmacist_name": f"Pharmacist_{random.randint(1, 200)}",
        "pharmacist_license": f"RPH{random.randint(100000, 999999)}",
        "pharmacist_license_state": random.choice(["CA", "NY", "TX", "FL", "IL", "PA", "OH"]),
        "pharmacist_years_experience": random.randint(1, 35),
        
        # Pharmacy Information
        "pharmacy_id": f"PHM{str(random.randint(1, 50)).zfill(4)}",
        "pharmacy_name": pharmacy_name,
        "pharmacy_chain": random.choice(["Independent", "CVS", "Walgreens", "Rite Aid", "Independent"]),
        "pharmacy_address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Washington', 'Park'])} St",
        "pharmacy_city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]),
        "pharmacy_state": random.choice(["CA", "NY", "TX", "FL", "IL", "PA", "OH"]),
        "pharmacy_zip": f"{random.randint(10000, 99999)}",
        "pharmacy_phone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
        "pharmacy_license": f"PHL{random.randint(10000, 99999)}",
        "pharmacy_npi": f"{random.randint(1000000000, 9999999999)}",
        "pharmacy_dea": f"F{chr(random.randint(65, 90))}{random.randint(1000000, 9999999)}",
        
        # Doctor Information
        "doctor_id": doctor_id,
        "doctor_name": f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller'])} {chr(random.randint(65, 90))}",
        "doctor_npi": f"{random.randint(1000000000, 9999999999)}",
        "doctor_dea": f"A{chr(random.randint(65, 90))}{random.randint(1000000, 9999999)}",
        "doctor_license": f"MD{random.randint(100000, 999999)}",
        "doctor_specialty": random.choice(doctor_specialties),
        "doctor_address": f"{random.randint(100, 9999)} {random.choice(['Medical', 'Hospital', 'Clinic', 'Health'])} Blvd",
        "doctor_city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
        "doctor_state": random.choice(["CA", "NY", "TX", "FL", "IL"]),
        "doctor_zip": f"{random.randint(10000, 99999)}",
        "doctor_phone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
        "doctor_years_practice": random.randint(1, 40),
        
        # Patient Information
        "patient_id": f"PAT{str(random.randint(1, 5000)).zfill(6)}",
        "patient_age": random.randint(18, 90),
        "patient_gender": random.choice(["M", "F", "Other"]),
        "patient_zip": f"{random.randint(10000, 99999)}",
        "patient_state": random.choice(["CA", "NY", "TX", "FL", "IL", "PA", "OH"]),
        
        # Insurance Information
        "insurance_company": random.choice(insurance_companies),
        "insurance_plan_id": f"INS{random.randint(10000, 99999)}",
        "insurance_group_number": f"GRP{random.randint(1000, 9999)}",
        "insurance_bin": f"{random.randint(100000, 999999)}",
        "insurance_pcn": f"PCN{random.randint(1000, 9999)}",
        "copay_amount": random_float(0, 100),
        "insurance_paid": random_float(0, 4500),
        "patient_paid": random_float(0, 500),
        
        # Clinical Information
        "diagnosis_code": random.choice(diagnosis_codes),
        "diagnosis_description": random.choice(["Hypertension", "Diabetes", "Depression", "Arthritis", "Asthma"]),
        "therapeutic_class": random.choice(["Cardiovascular", "Analgesic", "Antibiotic", "Antidiabetic", "Psychotherapeutic"]),
        "indication": random.choice(["Pain", "Infection", "Chronic Disease", "Acute Condition", "Preventive"]),
        
        # Transaction Details
        "submission_clarification_code": random.choice(["00", "01", "02", "03", "04"]),
        "days_since_last_fill": random.randint(0, 365),
        "early_refill_days": random.randint(-30, 30),
        "prescription_origin": random.choice(["Written", "Phone", "Electronic", "Fax"]),
        "transmission_type": random.choice(["Electronic", "Paper", "Phone", "Fax"]),
        
        # Fraud Indicators
        "doctor_pharmacy_distance_miles": doctor_pharmacy_distance,
        "patient_pharmacy_distance_miles": random_float(0.1, 50),
        "prescriptions_by_doctor_this_month": random.randint(1, 500),
        "prescriptions_to_pharmacy_this_month": random.randint(1, 1000),
        "doctor_pharmacy_referral_count": doctor_pharmacy_referral_count,
        "unusual_dosage_flag": random.choice([0, 1]),
        "duplicate_therapy_flag": random.choice([0, 1]),
        "price_variance_from_average": price_variance,
        "multiple_prescribers_same_drug": random.randint(0, 5),
        "pharmacy_shopping_indicator": random.randint(0, 10),
        "doctor_shopping_indicator": random.randint(0, 8),
        
        # Additional Metadata
        "day_of_week": random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
        "time_of_day": random.choice(["Morning", "Afternoon", "Evening", "Night"]),
        "rush_prescription": random.choice([0, 1]),
        "prior_authorization_required": random.choice([0, 1]),
        "prior_authorization_approved": random.choice([0, 1]),
        "formulary_status": random.choice(["Tier 1", "Tier 2", "Tier 3", "Non-Formulary"]),
        "generic_available": random.choice([0, 1]),
        "daw_code": random.choice(["0", "1", "2", "3", "4"]),
        
        # Payment Details
        "payment_method": random.choice(["Insurance", "Cash", "Credit Card", "Debit Card", "Check"]),
        "claim_status": random.choice(["Paid", "Rejected", "Pending", "Reversed"]),
        "rejection_code": random.choice(["None", "75", "76", "79", "88"]),
        "reversal_indicator": random.choice([0, 1]),
        
        # Additional Clinical
        "allergies_checked": random.choice([0, 1]),
        "drug_interaction_checked": random.choice([0, 1]),
        "counseling_provided": random.choice([0, 1]),
        "medication_therapy_management": random.choice([0, 1]),
        
        # Risk Scores
        "fraud_risk_score": fraud_risk_score,
        "abuse_risk_score": random_float(0, 100),
        "cost_variance_score": random_float(-100, 100),
        
        # Fraud Label
        "is_fraud": is_fraud
    }
    
    rows.append(row)

# Write to CSV
with open('medical_fraud_detection_dataset.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = rows[0].keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Dataset created with {num_records} records and {len(rows[0])} columns")
print(f"Fraudulent records: {fraud_count}")
print(f"Non-fraudulent records: {num_records - fraud_count}")
print("\nDataset saved to: medical_fraud_detection_dataset.csv")
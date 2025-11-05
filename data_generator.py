import sqlite3
import random
from datetime import datetime, timedelta

# Comprehensive name lists
FIRST_NAMES_MALE = ["Rajesh", "Amit", "Vikram", "Suresh", "Ramesh", "Arun", "Sanjay", "Manoj", "Kiran", "Rahul",
                    "Vijay", "Ashok", "Prakash", "Dinesh", "Ravi", "Arjun", "Krishna", "Ganesh", "Mahesh", "Naresh",
                    "Rakesh", "Sachin", "Rohan", "Varun", "Nikhil", "Ankit", "Vishal", "Kunal", "Aditya", "Harsh"]
FIRST_NAMES_FEMALE = ["Priya", "Sneha", "Anjali", "Kavita", "Deepa", "Meera", "Pooja", "Divya", "Nisha", "Lakshmi",
                      "Sunita", "Rekha", "Anita", "Geeta", "Seema", "Swati", "Asha", "Usha", "Neha", "Riya", "Simran",
                      "Pallavi", "Megha", "Shruti", "Preeti", "Kavya", "Aisha", "Ayesha", "Aditi", "Ananya"]
LAST_NAMES = ["Kumar", "Sharma", "Patel", "Reddy", "Nair", "Iyer", "Rao", "Singh", "Gupta", "Verma", "Menon",
              "Krishnan", "Joshi", "Desai", "Mehta", "Shah", "Agarwal", "Bansal", "Chopra", "Malhotra"]
CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Kochi", "Jaipur",
          "Lucknow", "Chandigarh", "Indore", "Nagpur"]
AILMENTS = ["Fever", "Common Cold", "Cough", "Headache", "Body Pain", "Gastritis", "Acidity", "Diabetes Management",
            "Hypertension", "Skin Infection", "Throat Infection", "Viral Fever", "Migraine", "Back Pain", "Joint Pain",
            "Stomach Upset", "Diarrhea", "Constipation", "Allergic Rhinitis", "Asthma", "Bronchitis", "UTI", "Anxiety",
            "Insomnia"]

# Comprehensive medicines list (183 medicines - BIG PHARMACY HOUSE)
MEDICINES = [
    # ============= FEVER & PAIN (30+ medicines) =============
    # Paracetamol - Multiple manufacturers
    {"name": "Dolo 650", "generic": "Paracetamol 650mg", "cat": "Antipyretic", "mfr": "Micro Labs", "price": 15.50,
     "rx": False, "stock": 5000},
    {"name": "Dolo 500", "generic": "Paracetamol 500mg", "cat": "Antipyretic", "mfr": "Micro Labs", "price": 12.00,
     "rx": False, "stock": 4800},
    {"name": "Crocin 650", "generic": "Paracetamol 650mg", "cat": "Antipyretic", "mfr": "GSK", "price": 18.00,
     "rx": False, "stock": 4500},
    {"name": "Crocin 500", "generic": "Paracetamol 500mg", "cat": "Antipyretic", "mfr": "GSK", "price": 14.00,
     "rx": False, "stock": 4300},
    {"name": "Crocin Advance", "generic": "Paracetamol 500mg", "cat": "Antipyretic", "mfr": "GSK", "price": 16.00,
     "rx": False, "stock": 4200},
    {"name": "Calpol 650", "generic": "Paracetamol 650mg", "cat": "Antipyretic", "mfr": "GSK", "price": 17.50,
     "rx": False, "stock": 4000},
    {"name": "Calpol 500", "generic": "Paracetamol 500mg", "cat": "Antipyretic", "mfr": "GSK", "price": 13.50,
     "rx": False, "stock": 3900},
    {"name": "Pacimol 500", "generic": "Paracetamol 500mg", "cat": "Antipyretic", "mfr": "Cadila", "price": 10.00,
     "rx": False, "stock": 5200},
    {"name": "Pyrigesic 650", "generic": "Paracetamol 650mg", "cat": "Antipyretic", "mfr": "Wockhardt", "price": 11.50,
     "rx": False, "stock": 4700},
    {"name": "Metacin 500", "generic": "Paracetamol 500mg", "cat": "Antipyretic", "mfr": "Cipla", "price": 9.50,
     "rx": False, "stock": 5100},
    # Ibuprofen combinations
    {"name": "Combiflam", "generic": "Ibuprofen + Paracetamol", "cat": "Analgesic", "mfr": "Sanofi", "price": 25.00,
     "rx": False, "stock": 3800},
    {"name": "Ibugesic Plus", "generic": "Ibuprofen + Paracetamol", "cat": "Analgesic", "mfr": "Cipla", "price": 24.00,
     "rx": False, "stock": 3600},
    {"name": "Brufen 400", "generic": "Ibuprofen 400mg", "cat": "Anti-inflammatory", "mfr": "Abbott", "price": 22.50,
     "rx": True, "stock": 3200},
    {"name": "Brufen 600", "generic": "Ibuprofen 600mg", "cat": "Anti-inflammatory", "mfr": "Abbott", "price": 32.00,
     "rx": True, "stock": 2800},
    {"name": "Ibugesic 400", "generic": "Ibuprofen 400mg", "cat": "Anti-inflammatory", "mfr": "Cipla", "price": 20.00,
     "rx": True, "stock": 3400},
    # Diclofenac
    {"name": "Voveran 50", "generic": "Diclofenac 50mg", "cat": "Anti-inflammatory", "mfr": "Novartis", "price": 28.00,
     "rx": True, "stock": 2900},
    {"name": "Voveran 75", "generic": "Diclofenac 75mg", "cat": "Anti-inflammatory", "mfr": "Novartis", "price": 38.00,
     "rx": True, "stock": 2600},
    {"name": "Voveran SR 100", "generic": "Diclofenac 100mg SR", "cat": "Anti-inflammatory", "mfr": "Novartis",
     "price": 45.00, "rx": True, "stock": 2400},
    {"name": "Diclomol", "generic": "Diclofenac + Paracetamol", "cat": "Analgesic", "mfr": "Mankind", "price": 32.00,
     "rx": True, "stock": 2700},
    {"name": "Diclowin Plus", "generic": "Diclofenac + Paracetamol", "cat": "Analgesic", "mfr": "Win Medicare",
     "price": 30.00, "rx": True, "stock": 2800},
    # Other NSAIDs
    {"name": "Nimesulide 100", "generic": "Nimesulide 100mg", "cat": "Anti-inflammatory", "mfr": "Multiple",
     "price": 12.00, "rx": True, "stock": 3100},
    {"name": "Nise 100", "generic": "Nimesulide 100mg", "cat": "Anti-inflammatory", "mfr": "Dr Reddy's", "price": 15.00,
     "rx": True, "stock": 3000},
    {"name": "Nicip 100", "generic": "Nimesulide 100mg", "cat": "Anti-inflammatory", "mfr": "Cipla", "price": 13.50,
     "rx": True, "stock": 3050},
    {"name": "Nimulid 100", "generic": "Nimesulide 100mg", "cat": "Anti-inflammatory", "mfr": "Panacea", "price": 14.00,
     "rx": True, "stock": 2950},
    # Mefenamic Acid
    {"name": "Meftal Spas", "generic": "Mefenamic Acid + Dicyclomine", "cat": "Analgesic", "mfr": "Blue Cross",
     "price": 55.00, "rx": True, "stock": 2200},
    {"name": "Meftal 500", "generic": "Mefenamic Acid 500mg", "cat": "Analgesic", "mfr": "Blue Cross", "price": 48.00,
     "rx": True, "stock": 2300},
    {"name": "Mefenamic 250", "generic": "Mefenamic Acid 250mg", "cat": "Analgesic", "mfr": "Multiple", "price": 28.00,
     "rx": True, "stock": 2600},
    # Aspirin
    {"name": "Disprin", "generic": "Aspirin 325mg", "cat": "Analgesic", "mfr": "Reckitt Benckiser", "price": 18.00,
     "rx": False, "stock": 3300},
    {"name": "Ecosprin 75", "generic": "Aspirin 75mg", "cat": "Antiplatelet", "mfr": "USV", "price": 8.00, "rx": True,
     "stock": 4200},
    {"name": "Ecosprin 150", "generic": "Aspirin 150mg", "cat": "Antiplatelet", "mfr": "USV", "price": 12.00,
     "rx": True, "stock": 3900},
    # Advanced combinations
    {"name": "Zerodol SP", "generic": "Aceclofenac + Paracetamol + Serratiopeptidase", "cat": "Analgesic",
     "mfr": "Ipca", "price": 85.00, "rx": True, "stock": 1800},
    {"name": "Zerodol P", "generic": "Aceclofenac + Paracetamol", "cat": "Analgesic", "mfr": "Ipca", "price": 72.00,
     "rx": True, "stock": 2000},
    {"name": "Ultracet", "generic": "Tramadol + Paracetamol", "cat": "Analgesic", "mfr": "Janssen", "price": 95.00,
     "rx": True, "stock": 1500},
    {"name": "Proxyvon", "generic": "Dextropropoxyphene + Paracetamol", "cat": "Analgesic", "mfr": "Wockhardt",
     "price": 48.00, "rx": True, "stock": 1700},

    # ============= ANTIBIOTICS (40+ medicines) =============
    # Azithromycin
    {"name": "Azithral 500", "generic": "Azithromycin 500mg", "cat": "Antibiotic", "mfr": "Alembic", "price": 95.00,
     "rx": True, "stock": 2800},
    {"name": "Azithral 250", "generic": "Azithromycin 250mg", "cat": "Antibiotic", "mfr": "Alembic", "price": 65.00,
     "rx": True, "stock": 3000},
    {"name": "Zithromax 500", "generic": "Azithromycin 500mg", "cat": "Antibiotic", "mfr": "Pfizer", "price": 125.00,
     "rx": True, "stock": 2400},
    {"name": "Azee 500", "generic": "Azithromycin 500mg", "cat": "Antibiotic", "mfr": "Cipla", "price": 88.00,
     "rx": True, "stock": 2900},
    {"name": "Azee 250", "generic": "Azithromycin 250mg", "cat": "Antibiotic", "mfr": "Cipla", "price": 58.00,
     "rx": True, "stock": 3100},
    # Amoxicillin combinations
    {"name": "Augmentin 625", "generic": "Amoxicillin 500mg + Clavulanic Acid 125mg", "cat": "Antibiotic", "mfr": "GSK",
     "price": 145.00, "rx": True, "stock": 2600},
    {"name": "Augmentin 375", "generic": "Amoxicillin 250mg + Clavulanic Acid 125mg", "cat": "Antibiotic", "mfr": "GSK",
     "price": 95.00, "rx": True, "stock": 2800},
    {"name": "Augmentin 1000", "generic": "Amoxicillin 875mg + Clavulanic Acid 125mg", "cat": "Antibiotic",
     "mfr": "GSK", "price": 195.00, "rx": True, "stock": 2200},
    {"name": "Clavam 625", "generic": "Amoxicillin + Clavulanic Acid", "cat": "Antibiotic", "mfr": "Alkem",
     "price": 128.00, "rx": True, "stock": 2700},
    {"name": "Mox 500", "generic": "Amoxicillin 500mg", "cat": "Antibiotic", "mfr": "Ranbaxy", "price": 65.00,
     "rx": True, "stock": 3200},
    {"name": "Amoxyclav 625", "generic": "Amoxicillin + Clavulanic Acid", "cat": "Antibiotic", "mfr": "Cipla",
     "price": 135.00, "rx": True, "stock": 2650},
    # Ciprofloxacin
    {"name": "Cifran 500", "generic": "Ciprofloxacin 500mg", "cat": "Antibiotic", "mfr": "Ranbaxy", "price": 68.00,
     "rx": True, "stock": 2900},
    {"name": "Cifran 250", "generic": "Ciprofloxacin 250mg", "cat": "Antibiotic", "mfr": "Ranbaxy", "price": 45.00,
     "rx": True, "stock": 3100},
    {"name": "Ciplox 500", "generic": "Ciprofloxacin 500mg", "cat": "Antibiotic", "mfr": "Cipla", "price": 62.00,
     "rx": True, "stock": 3000},
    {"name": "Ciprofloxacin 500", "generic": "Ciprofloxacin 500mg", "cat": "Antibiotic", "mfr": "Multiple",
     "price": 55.00, "rx": True, "stock": 3300},
    # Levofloxacin
    {"name": "Levoflox 500", "generic": "Levofloxacin 500mg", "cat": "Antibiotic", "mfr": "Cipla", "price": 135.00,
     "rx": True, "stock": 2400},
    {"name": "Levoflox 250", "generic": "Levofloxacin 250mg", "cat": "Antibiotic", "mfr": "Cipla", "price": 85.00,
     "rx": True, "stock": 2600},
    {"name": "Levaquin 500", "generic": "Levofloxacin 500mg", "cat": "Antibiotic", "mfr": "Janssen", "price": 165.00,
     "rx": True, "stock": 2100},
    {"name": "Levoday 500", "generic": "Levofloxacin 500mg", "cat": "Antibiotic", "mfr": "Lupin", "price": 125.00,
     "rx": True, "stock": 2500},
    # Cephalosporins
    {"name": "Cefixime 200", "generic": "Cefixime 200mg", "cat": "Antibiotic", "mfr": "Multiple", "price": 85.00,
     "rx": True, "stock": 2700},
    {"name": "Cepodem XP 200", "generic": "Cefpodoxime 200mg", "cat": "Antibiotic", "mfr": "Micro Labs",
     "price": 225.00, "rx": True, "stock": 1900},
    {"name": "Ceftas 200", "generic": "Cefixime 200mg", "cat": "Antibiotic", "mfr": "Lupin", "price": 92.00, "rx": True,
     "stock": 2650},
    {"name": "Taxim O 200", "generic": "Cefixime 200mg", "cat": "Antibiotic", "mfr": "Alkem", "price": 95.00,
     "rx": True, "stock": 2600},
    {"name": "Cefpodoxime 200", "generic": "Cefpodoxime 200mg", "cat": "Antibiotic", "mfr": "Multiple", "price": 195.00,
     "rx": True, "stock": 2000},
    # Metronidazole
    {"name": "Metrogyl 400", "generic": "Metronidazole 400mg", "cat": "Antibiotic", "mfr": "J B Chemicals",
     "price": 28.00, "rx": True, "stock": 3500},
    {"name": "Flagyl 400", "generic": "Metronidazole 400mg", "cat": "Antibiotic", "mfr": "Abbott", "price": 32.00,
     "rx": True, "stock": 3300},
    {"name": "Metronidazole 400", "generic": "Metronidazole 400mg", "cat": "Antibiotic", "mfr": "Multiple",
     "price": 22.00, "rx": True, "stock": 3700},
    # Norfloxacin
    {"name": "Norflox 400", "generic": "Norfloxacin 400mg", "cat": "Antibiotic", "mfr": "Cipla", "price": 45.00,
     "rx": True, "stock": 3200},
    {"name": "Norflox TZ", "generic": "Norfloxacin + Tinidazole", "cat": "Antibiotic", "mfr": "Cipla", "price": 68.00,
     "rx": True, "stock": 2800},
    {"name": "Norbactin 400", "generic": "Norfloxacin 400mg", "cat": "Antibiotic", "mfr": "Ranbaxy", "price": 48.00,
     "rx": True, "stock": 3100},
    # Ofloxacin
    {"name": "Ofloxacin 200", "generic": "Ofloxacin 200mg", "cat": "Antibiotic", "mfr": "Multiple", "price": 38.00,
     "rx": True, "stock": 3150},
    {"name": "Zanocin 200", "generic": "Ofloxacin 200mg", "cat": "Antibiotic", "mfr": "Ranbaxy", "price": 45.00,
     "rx": True, "stock": 3000},
    {"name": "Oflox 200", "generic": "Ofloxacin 200mg", "cat": "Antibiotic", "mfr": "Cipla", "price": 42.00, "rx": True,
     "stock": 3050},
    # Doxycycline
    {"name": "Doxycycline 100", "generic": "Doxycycline 100mg", "cat": "Antibiotic", "mfr": "Multiple", "price": 35.00,
     "rx": True, "stock": 3000},
    {"name": "Doxy 100", "generic": "Doxycycline 100mg", "cat": "Antibiotic", "mfr": "Cipla", "price": 38.00,
     "rx": True, "stock": 2950},
    {"name": "Doxt SL", "generic": "Doxycycline 100mg", "cat": "Antibiotic", "mfr": "Alkem", "price": 42.00, "rx": True,
     "stock": 2900},
    # Erythromycin
    {"name": "Erythromycin 250", "generic": "Erythromycin 250mg", "cat": "Antibiotic", "mfr": "Abbott", "price": 42.00,
     "rx": True, "stock": 2750},
    {"name": "Erythromycin 500", "generic": "Erythromycin 500mg", "cat": "Antibiotic", "mfr": "Multiple",
     "price": 65.00, "rx": True, "stock": 2500},
    # Clindamycin
    {"name": "Clindamycin 300", "generic": "Clindamycin 300mg", "cat": "Antibiotic", "mfr": "Multiple", "price": 125.00,
     "rx": True, "stock": 2200},
    {"name": "Dalacin C 300", "generic": "Clindamycin 300mg", "cat": "Antibiotic", "mfr": "Pfizer", "price": 185.00,
     "rx": True, "stock": 1800},

    # ============= COLD, COUGH & ALLERGY (25+ medicines) =============
    # Cold combinations
    {"name": "Sinarest", "generic": "Paracetamol + Phenylephrine + Chlorpheniramine", "cat": "Cold", "mfr": "Centaur",
     "price": 30.00, "rx": False, "stock": 4200},
    {"name": "D-Cold Total", "generic": "Paracetamol + Phenylephrine + Cetirizine", "cat": "Cold", "mfr": "Paras",
     "price": 28.00, "rx": False, "stock": 4300},
    {"name": "Coldact", "generic": "Phenylephrine + Chlorpheniramine", "cat": "Cold", "mfr": "Sanofi", "price": 45.00,
     "rx": False, "stock": 3800},
    {"name": "Actifed", "generic": "Pseudoephedrine + Triprolidine", "cat": "Cold", "mfr": "GSK", "price": 52.00,
     "rx": False, "stock": 3500},
    {"name": "Okacet Cold", "generic": "Paracetamol + Phenylephrine", "cat": "Cold", "mfr": "Cipla", "price": 26.00,
     "rx": False, "stock": 4100},
    # Cough syrups
    {"name": "Chericof Syrup", "generic": "Dextromethorphan", "cat": "Cough Syrup", "mfr": "Emcure", "price": 85.00,
     "rx": False, "stock": 2400},
    {"name": "Benadryl Cough Syrup", "generic": "Diphenhydramine", "cat": "Cough Syrup", "mfr": "J&J", "price": 95.00,
     "rx": False, "stock": 2200},
    {"name": "Grilinctus Syrup", "generic": "Guaifenesin + Terbutaline", "cat": "Cough Syrup", "mfr": "Pfizer",
     "price": 105.00, "rx": False, "stock": 2100},
    {"name": "Ascoril Syrup", "generic": "Terbutaline + Bromhexine + Guaifenesin", "cat": "Cough Syrup",
     "mfr": "Glenmark", "price": 112.00, "rx": True, "stock": 1900},
    {"name": "Alex Syrup", "generic": "Chlorpheniramine + Phenylephrine", "cat": "Cough Syrup", "mfr": "Glenmark",
     "price": 68.00, "rx": False, "stock": 2500},
    {"name": "Corex Syrup", "generic": "Chlorpheniramine + Codeine", "cat": "Cough Syrup", "mfr": "Pfizer",
     "price": 95.00, "rx": True, "stock": 1800},
    {"name": "Cofsils Syrup", "generic": "Dextromethorphan", "cat": "Cough Syrup", "mfr": "Cipla", "price": 78.00,
     "rx": False, "stock": 2300},
    {"name": "Koflet Syrup", "generic": "Herbal Cough Formula", "cat": "Cough Syrup", "mfr": "Himalaya", "price": 95.00,
     "rx": False, "stock": 2000},
    # Antihistamines
    {"name": "Cetrizine 10", "generic": "Cetirizine 10mg", "cat": "Antihistamine", "mfr": "Multiple", "price": 12.00,
     "rx": False, "stock": 5500},
    {"name": "Alerid 10", "generic": "Cetirizine 10mg", "cat": "Antihistamine", "mfr": "Cipla", "price": 14.00,
     "rx": False, "stock": 5200},
    {"name": "Zyrtec 10", "generic": "Cetirizine 10mg", "cat": "Antihistamine", "mfr": "UCB", "price": 25.00,
     "rx": False, "stock": 4500},
    {"name": "Avil 25", "generic": "Pheniramine 25mg", "cat": "Antihistamine", "mfr": "Sanofi", "price": 18.00,
     "rx": False, "stock": 4200},
    {"name": "Phenergan 25", "generic": "Promethazine 25mg", "cat": "Antihistamine", "mfr": "Abbott", "price": 28.00,
     "rx": True, "stock": 3500},
    {"name": "Levocetirizine 5", "generic": "Levocetirizine 5mg", "cat": "Antihistamine", "mfr": "Multiple",
     "price": 45.00, "rx": True, "stock": 3800},
    {"name": "Allegra 120", "generic": "Fexofenadine 120mg", "cat": "Antihistamine", "mfr": "Sanofi", "price": 125.00,
     "rx": True, "stock": 2800},
    {"name": "Allegra 180", "generic": "Fexofenadine 180mg", "cat": "Antihistamine", "mfr": "Sanofi", "price": 145.00,
     "rx": True, "stock": 2500},
    {"name": "Montair LC", "generic": "Montelukast + Levocetirizine", "cat": "Anti-allergic", "mfr": "Cipla",
     "price": 115.00, "rx": True, "stock": 3200},
    {"name": "Montair 10", "generic": "Montelukast 10mg", "cat": "Anti-allergic", "mfr": "Cipla", "price": 85.00,
     "rx": True, "stock": 3400},
    # Nasal preparations
    {"name": "Otrivin Nasal Drops", "generic": "Xylometazoline", "cat": "Nasal", "mfr": "Novartis", "price": 85.00,
     "rx": False, "stock": 2200},
    {"name": "Nasivion Drops", "generic": "Oxymetazoline", "cat": "Nasal", "mfr": "Merck", "price": 78.00, "rx": False,
     "stock": 2300},

    # ============= GASTRIC & DIGESTIVE (30+ medicines) =============
    # Proton Pump Inhibitors
    {"name": "Pan 40", "generic": "Pantoprazole 40mg", "cat": "PPI", "mfr": "Alkem", "price": 75.00, "rx": True,
     "stock": 3800},
    {"name": "Pan 20", "generic": "Pantoprazole 20mg", "cat": "PPI", "mfr": "Alkem", "price": 45.00, "rx": True,
     "stock": 4000},
    {"name": "Pantop 40", "generic": "Pantoprazole 40mg", "cat": "PPI", "mfr": "Aristo", "price": 68.00, "rx": True,
     "stock": 3900},
    {"name": "Omez 20", "generic": "Omeprazole 20mg", "cat": "PPI", "mfr": "Dr Reddy's", "price": 68.00, "rx": True,
     "stock": 3700},
    {"name": "Omez 10", "generic": "Omeprazole 10mg", "cat": "PPI", "mfr": "Dr Reddy's", "price": 38.00, "rx": True,
     "stock": 4100},
    {"name": "Omez D", "generic": "Omeprazole + Domperidone", "cat": "PPI", "mfr": "Dr Reddy's", "price": 95.00,
     "rx": True, "stock": 3300},
    {"name": "Rabeprazole 20", "generic": "Rabeprazole 20mg", "cat": "PPI", "mfr": "Multiple", "price": 85.00,
     "rx": True, "stock": 3400},
    {"name": "Razo 20", "generic": "Rabeprazole 20mg", "cat": "PPI", "mfr": "Dr Reddy's", "price": 88.00, "rx": True,
     "stock": 3350},
    {"name": "Razo D", "generic": "Rabeprazole + Domperidone", "cat": "PPI", "mfr": "Dr Reddy's", "price": 112.00,
     "rx": True, "stock": 3000},
    {"name": "Esomeprazole 40", "generic": "Esomeprazole 40mg", "cat": "PPI", "mfr": "Multiple", "price": 95.00,
     "rx": True, "stock": 3200},
    {"name": "Nexium 40", "generic": "Esomeprazole 40mg", "cat": "PPI", "mfr": "AstraZeneca", "price": 145.00,
     "rx": True, "stock": 2600},
    {"name": "Lansoprazole 30", "generic": "Lansoprazole 30mg", "cat": "PPI", "mfr": "Multiple", "price": 78.00,
     "rx": True, "stock": 3300},
    # H2 Blockers
    {"name": "Aciloc 150", "generic": "Ranitidine 150mg", "cat": "H2 Blocker", "mfr": "Cadila", "price": 32.00,
     "rx": False, "stock": 4200},
    {"name": "Zinetac 150", "generic": "Ranitidine 150mg", "cat": "H2 Blocker", "mfr": "GSK", "price": 28.00,
     "rx": False, "stock": 4400},
    {"name": "Rantac 150", "generic": "Ranitidine 150mg", "cat": "H2 Blocker", "mfr": "J B Chemicals", "price": 30.00,
     "rx": False, "stock": 4300},
    {"name": "Famotidine 20", "generic": "Famotidine 20mg", "cat": "H2 Blocker", "mfr": "Multiple", "price": 42.00,
     "rx": True, "stock": 3600},
    # Antacids
    {"name": "Digene Gel", "generic": "Al + Mg Hydroxide", "cat": "Antacid", "mfr": "Abbott", "price": 35.00,
     "rx": False, "stock": 4800},
    {"name": "ENO", "generic": "Sodium Bicarbonate", "cat": "Antacid", "mfr": "GSK", "price": 15.00, "rx": False,
     "stock": 5200},
    {"name": "Gelusil", "generic": "Al + Mg Hydroxide", "cat": "Antacid", "mfr": "Pfizer", "price": 32.00, "rx": False,
     "stock": 4600},
    {"name": "Mucaine Gel", "generic": "Oxethazaine + Al + Mg", "cat": "Antacid", "mfr": "Pfizer", "price": 75.00,
     "rx": False, "stock": 3200},
    {"name": "Acigel", "generic": "Al + Mg Hydroxide", "cat": "Antacid", "mfr": "Micro Labs", "price": 28.00,
     "rx": False, "stock": 4500},
    # Digestive enzymes & others
    {"name": "Pudin Hara", "generic": "Pudina + Ajwain Oil", "cat": "Digestive", "mfr": "Dabur", "price": 45.00,
     "rx": False, "stock": 3800},
    {"name": "Cremaffin", "generic": "Liquid Paraffin", "cat": "Laxative", "mfr": "Abbott", "price": 85.00, "rx": False,
     "stock": 2800},
    {"name": "Cremaffin Plus", "generic": "Liquid Paraffin + Milk of Magnesia", "cat": "Laxative", "mfr": "Abbott",
     "price": 95.00, "rx": False, "stock": 2600},
    {"name": "Isabgol", "generic": "Psyllium Husk", "cat": "Laxative", "mfr": "Dabur", "price": 125.00, "rx": False,
     "stock": 2400},
    {"name": "Dulcolax", "generic": "Bisacodyl 5mg", "cat": "Laxative", "mfr": "Sanofi", "price": 45.00, "rx": False,
     "stock": 3200},
    {"name": "Sporlac", "generic": "Lactobacillus", "cat": "Probiotic", "mfr": "Sanzyme", "price": 95.00, "rx": False,
     "stock": 3000},
    {"name": "Econorm", "generic": "Saccharomyces boulardii", "cat": "Probiotic", "mfr": "Aventis", "price": 115.00,
     "rx": False, "stock": 2700},
    # Antiemetics
    {"name": "Eldoper", "generic": "Domperidone 10mg", "cat": "Antiemetic", "mfr": "Elder", "price": 42.00, "rx": True,
     "stock": 3500},
    {"name": "Domstal 10", "generic": "Domperidone 10mg", "cat": "Antiemetic", "mfr": "Torrent", "price": 38.00,
     "rx": True, "stock": 3600},
    {"name": "Vomikind", "generic": "Ondansetron 4mg", "cat": "Antiemetic", "mfr": "Mankind", "price": 65.00,
     "rx": True, "stock": 2800},

    # ============= DIABETES (15+ medicines) =============
    # Metformin
    {"name": "Glycomet 500", "generic": "Metformin 500mg", "cat": "Anti-diabetic", "mfr": "USV", "price": 45.00,
     "rx": True, "stock": 4200},
    {"name": "Glycomet 850", "generic": "Metformin 850mg", "cat": "Anti-diabetic", "mfr": "USV", "price": 65.00,
     "rx": True, "stock": 3800},
    {"name": "Glycomet 1000", "generic": "Metformin 1000mg", "cat": "Anti-diabetic", "mfr": "USV", "price": 85.00,
     "rx": True, "stock": 3400},
    {"name": "Glycomet SR 500", "generic": "Metformin SR 500mg", "cat": "Anti-diabetic", "mfr": "USV", "price": 52.00,
     "rx": True, "stock": 4000},
    {"name": "Metformin 500", "generic": "Metformin 500mg", "cat": "Anti-diabetic", "mfr": "Multiple", "price": 38.00,
     "rx": True, "stock": 4400},
    # Combinations
    {"name": "Glycomet GP1", "generic": "Metformin + Glimepiride 1mg", "cat": "Anti-diabetic", "mfr": "USV",
     "price": 125.00, "rx": True, "stock": 3200},
    {"name": "Glycomet GP2", "generic": "Metformin + Glimepiride 2mg", "cat": "Anti-diabetic", "mfr": "USV",
     "price": 145.00, "rx": True, "stock": 3000},
    {"name": "Gluconorm G1", "generic": "Metformin + Glimepiride 1mg", "cat": "Anti-diabetic", "mfr": "Lupin",
     "price": 115.00, "rx": True, "stock": 3300},
    {"name": "Gemer 1", "generic": "Metformin + Glimepiride 1mg", "cat": "Anti-diabetic", "mfr": "Sun Pharma",
     "price": 118.00, "rx": True, "stock": 3250},
    # Sulfonylureas
    {"name": "Amaryl 1mg", "generic": "Glimepiride 1mg", "cat": "Anti-diabetic", "mfr": "Sanofi", "price": 95.00,
     "rx": True, "stock": 2800},
    {"name": "Amaryl 2mg", "generic": "Glimepiride 2mg", "cat": "Anti-diabetic", "mfr": "Sanofi", "price": 125.00,
     "rx": True, "stock": 2600},
    {"name": "Glynase 5", "generic": "Glipizide 5mg", "cat": "Anti-diabetic", "mfr": "Pfizer", "price": 85.00,
     "rx": True, "stock": 2700},
    {"name": "Glibenclamide 5", "generic": "Glibenclamide 5mg", "cat": "Anti-diabetic", "mfr": "Multiple",
     "price": 32.00, "rx": True, "stock": 3400},
    # DPP-4 Inhibitors
    {"name": "Januvia 50", "generic": "Sitagliptin 50mg", "cat": "Anti-diabetic", "mfr": "MSD", "price": 385.00,
     "rx": True, "stock": 1600},
    {"name": "Januvia 100", "generic": "Sitagliptin 100mg", "cat": "Anti-diabetic", "mfr": "MSD", "price": 485.00,
     "rx": True, "stock": 1400},
    {"name": "Galvus Met 50/500", "generic": "Vildagliptin + Metformin", "cat": "Anti-diabetic", "mfr": "Novartis",
     "price": 425.00, "rx": True, "stock": 1500},

    # ============= HYPERTENSION & CARDIAC (25+ medicines) =============
    # Amlodipine
    {"name": "Amlong 5", "generic": "Amlodipine 5mg", "cat": "Anti-HTN", "mfr": "Micro Labs", "price": 55.00,
     "rx": True, "stock": 4000},
    {"name": "Amlong 10", "generic": "Amlodipine 10mg", "cat": "Anti-HTN", "mfr": "Micro Labs", "price": 75.00,
     "rx": True, "stock": 3600},
    {"name": "Stamlo 5", "generic": "Amlodipine 5mg", "cat": "Anti-HTN", "mfr": "Dr Reddy's", "price": 52.00,
     "rx": True, "stock": 4100},
    {"name": "Norvasc 5", "generic": "Amlodipine 5mg", "cat": "Anti-HTN", "mfr": "Pfizer", "price": 85.00, "rx": True,
     "stock": 3400},
    # Telmisartan
    {"name": "Telma 40", "generic": "Telmisartan 40mg", "cat": "Anti-HTN", "mfr": "Glenmark", "price": 95.00,
     "rx": True, "stock": 3500},
    {"name": "Telma 20", "generic": "Telmisartan 20mg", "cat": "Anti-HTN", "mfr": "Glenmark", "price": 65.00,
     "rx": True, "stock": 3700},
    {"name": "Telma H", "generic": "Telmisartan + HCTZ", "cat": "Anti-HTN", "mfr": "Glenmark", "price": 125.00,
     "rx": True, "stock": 3200},
    {"name": "Telma AM", "generic": "Telmisartan + Amlodipine", "cat": "Anti-HTN", "mfr": "Glenmark", "price": 145.00,
     "rx": True, "stock": 3000},
    {"name": "Telmisartan 40", "generic": "Telmisartan 40mg", "cat": "Anti-HTN", "mfr": "Multiple", "price": 78.00,
     "rx": True, "stock": 3600},
    # Losartan
    {"name": "Losar 50", "generic": "Losartan 50mg", "cat": "Anti-HTN", "mfr": "Cipla", "price": 65.00, "rx": True,
     "stock": 3700},
    {"name": "Losar 25", "generic": "Losartan 25mg", "cat": "Anti-HTN", "mfr": "Cipla", "price": 45.00, "rx": True,
     "stock": 3900},
    {"name": "Losar H", "generic": "Losartan + HCTZ", "cat": "Anti-HTN", "mfr": "Cipla", "price": 95.00, "rx": True,
     "stock": 3300},
    {"name": "Cozaar 50", "generic": "Losartan 50mg", "cat": "Anti-HTN", "mfr": "MSD", "price": 125.00, "rx": True,
     "stock": 2800},
    # Olmesartan
    {"name": "Olmesar 20", "generic": "Olmesartan 20mg", "cat": "Anti-HTN", "mfr": "Macleods", "price": 85.00,
     "rx": True, "stock": 3200},
    {"name": "Olmesar 40", "generic": "Olmesartan 40mg", "cat": "Anti-HTN", "mfr": "Macleods", "price": 115.00,
     "rx": True, "stock": 2900},
    {"name": "Olmesar H", "generic": "Olmesartan + HCTZ", "cat": "Anti-HTN", "mfr": "Macleods", "price": 135.00,
     "rx": True, "stock": 2700},
    # Beta Blockers
    {"name": "Atenolol 50", "generic": "Atenolol 50mg", "cat": "Beta Blocker", "mfr": "Multiple", "price": 18.00,
     "rx": True, "stock": 4500},
    {"name": "Atenolol 25", "generic": "Atenolol 25mg", "cat": "Beta Blocker", "mfr": "Multiple", "price": 12.00,
     "rx": True, "stock": 4700},
    {"name": "Metoprolol 50", "generic": "Metoprolol 50mg", "cat": "Beta Blocker", "mfr": "Multiple", "price": 28.00,
     "rx": True, "stock": 4000},
    {"name": "Concor 2.5", "generic": "Bisoprolol 2.5mg", "cat": "Beta Blocker", "mfr": "Merck", "price": 95.00,
     "rx": True, "stock": 3100},
    {"name": "Concor 5", "generic": "Bisoprolol 5mg", "cat": "Beta Blocker", "mfr": "Merck", "price": 125.00,
     "rx": True, "stock": 2900},
    {"name": "Carvedilol 3.125", "generic": "Carvedilol 3.125mg", "cat": "Beta Blocker", "mfr": "Multiple",
     "price": 42.00, "rx": True, "stock": 3400},
    {"name": "Carvedilol 6.25", "generic": "Carvedilol 6.25mg", "cat": "Beta Blocker", "mfr": "Multiple",
     "price": 58.00, "rx": True, "stock": 3200},
    # ACE Inhibitors
    {"name": "Enalapril 5", "generic": "Enalapril 5mg", "cat": "ACE Inhibitor", "mfr": "Multiple", "price": 32.00,
     "rx": True, "stock": 3600},
    {"name": "Ramipril 5", "generic": "Ramipril 5mg", "cat": "ACE Inhibitor", "mfr": "Multiple", "price": 48.00,
     "rx": True, "stock": 3400},

    # ============= VITAMINS & SUPPLEMENTS (20+ medicines) =============
    {"name": "Becosules", "generic": "Vitamin B Complex", "cat": "Vitamin", "mfr": "Pfizer", "price": 35.00,
     "rx": False, "stock": 4500},
    {"name": "Neurobion Forte", "generic": "Vitamin B Complex", "cat": "Vitamin", "mfr": "P&G", "price": 42.00,
     "rx": False, "stock": 4200},
    {"name": "Shelcal 500", "generic": "Calcium + Vit D3", "cat": "Supplement", "mfr": "Elder", "price": 125.00,
     "rx": False, "stock": 3800},
    {"name": "Calcirol Sachet", "generic": "Vit D3 60K IU", "cat": "Vitamin", "mfr": "Cadila", "price": 35.00,
     "rx": True, "stock": 4200},
    {"name": "Evion 400", "generic": "Vitamin E 400IU", "cat": "Vitamin", "mfr": "Merck", "price": 55.00, "rx": False,
     "stock": 3900},
    {"name": "Zincovit", "generic": "Multivit + Zinc", "cat": "Supplement", "mfr": "Apex", "price": 95.00, "rx": False,
     "stock": 3500},
    {"name": "Revital", "generic": "Multivit + Minerals", "cat": "Supplement", "mfr": "Ranbaxy", "price": 165.00,
     "rx": False, "stock": 3000},
    {"name": "A to Z", "generic": "Multivitamin", "cat": "Supplement", "mfr": "Alkem", "price": 145.00, "rx": False,
     "stock": 3200},
    {"name": "Ferrous Sulfate", "generic": "Iron 200mg", "cat": "Supplement", "mfr": "Multiple", "price": 28.00,
     "rx": False, "stock": 4300},
    {"name": "Folic Acid 5mg", "generic": "Folic Acid", "cat": "Vitamin", "mfr": "Multiple", "price": 12.00,
     "rx": False, "stock": 4800},
    {"name": "Vitamin C 500", "generic": "Ascorbic Acid", "cat": "Vitamin", "mfr": "Multiple", "price": 38.00,
     "rx": False, "stock": 4100},
    {"name": "Omega-3 Caps", "generic": "Omega-3 Fatty Acids", "cat": "Supplement", "mfr": "Multiple", "price": 195.00,
     "rx": False, "stock": 2600},
]

print(f"✓ Total medicines loaded: {len(MEDICINES)}")

# Ailment mappings - updated for comprehensive catalog
AILMENT_MEDS = {
    "Fever": ["Dolo 650", "Dolo 500", "Crocin 650", "Crocin 500", "Calpol 650", "Pacimol 500", "Combiflam",
              "Ibugesic Plus"],
    "Common Cold": ["Sinarest", "D-Cold Total", "Coldact", "Okacet Cold", "Cetrizine 10", "Alerid 10"],
    "Cough": ["Chericof Syrup", "Benadryl Cough Syrup", "Grilinctus Syrup", "Ascoril Syrup", "Alex Syrup",
              "Cofsils Syrup", "Koflet Syrup"],
    "Headache": ["Dolo 650", "Crocin 650", "Combiflam", "Brufen 400", "Ibugesic Plus"],
    "Body Pain": ["Combiflam", "Brufen 600", "Brufen 400", "Voveran 50", "Voveran 75", "Zerodol P"],
    "Gastritis": ["Pan 40", "Omez 20", "Pantop 40", "Razo 20", "Digene Gel", "Mucaine Gel"],
    "Acidity": ["Digene Gel", "ENO", "Gelusil", "Acigel", "Omez 10", "Pan 20"],
    "Diabetes Management": ["Glycomet 500", "Glycomet 850", "Glycomet GP1", "Glycomet GP2", "Amaryl 1mg", "Amaryl 2mg",
                            "Gluconorm G1"],
    "Hypertension": ["Amlong 5", "Amlong 10", "Telma 40", "Telma 20", "Losar 50", "Losar 25", "Atenolol 50",
                     "Olmesar 20"],
    "Throat Infection": ["Azithral 500", "Augmentin 625", "Azee 500", "Mox 500"],
    "Allergic Rhinitis": ["Allegra 120", "Montair LC", "Cetrizine 10", "Levocetirizine 5", "Avil 25"],
    "Skin Infection": ["Augmentin 625", "Azithral 500", "Cefixime 200"],
    "Viral Fever": ["Dolo 650", "Crocin 650", "Paracetamol combinations"],
    "Migraine": ["Combiflam", "Brufen 400", "Zerodol SP"],
    "Back Pain": ["Voveran 50", "Zerodol P", "Brufen 600", "Diclomol"],
    "Joint Pain": ["Voveran 75", "Voveran SR 100", "Zerodol SP", "Brufen 600"],
    "Stomach Upset": ["Digene Gel", "ENO", "Pan 40", "Eldoper", "Domstal 10"],
    "Diarrhea": ["Metrogyl 400", "Norflox TZ", "Ofloxacin 200", "Sporlac", "Econorm"],
    "Constipation": ["Cremaffin", "Isabgol", "Dulcolax", "Pudin Hara"],
    "Asthma": ["Montair 10", "Montair LC"],
    "Bronchitis": ["Azithral 500", "Azee 500", "Levoflox 500", "Ascoril Syrup"],
    "UTI": ["Norflox 400", "Norflox TZ", "Ciprofloxacin 500", "Levoflox 500"],
    "Anxiety": ["No specific meds - refer to specialist"],
    "Insomnia": ["No specific meds - refer to specialist"],
}


def create_db():
    conn = sqlite3.connect('medical_pharmacy.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT,
        age INTEGER, gender TEXT, phone TEXT, city TEXT, registration_date DATE, 
        is_chronic BOOLEAN, chronic_condition TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS consultations (
        consultation_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER,
        consultation_date DATETIME, ailment TEXT, diagnosis TEXT, consultation_fee REAL,
        follow_up_required BOOLEAN, FOREIGN KEY(patient_id) REFERENCES patients(patient_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS medicines (
        medicine_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, generic_name TEXT,
        category TEXT, manufacturer TEXT, price REAL, prescription_required BOOLEAN,
        stock_quantity INTEGER, reorder_level INTEGER, last_restocked DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS prescriptions (
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT, consultation_id INTEGER,
        medicine_id INTEGER, dosage TEXT, duration_days INTEGER, quantity INTEGER,
        FOREIGN KEY(consultation_id) REFERENCES consultations(consultation_id),
        FOREIGN KEY(medicine_id) REFERENCES medicines(medicine_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER,
        consultation_id INTEGER, transaction_date DATETIME, total_amount REAL,
        payment_mode TEXT, prescription_linked BOOLEAN,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY(consultation_id) REFERENCES consultations(consultation_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS transaction_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id INTEGER,
        medicine_id INTEGER, quantity INTEGER, price_per_unit REAL, total_price REAL,
        FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id),
        FOREIGN KEY(medicine_id) REFERENCES medicines(medicine_id))''')
    conn.commit()
    return conn


def populate_meds(conn):
    c = conn.cursor()
    for m in MEDICINES:
        c.execute('''INSERT INTO medicines (name, generic_name, category, manufacturer,
                   price, prescription_required, stock_quantity, reorder_level, last_restocked)
                   VALUES (?,?,?,?,?,?,?,100,?)''',
                  (m['name'], m['generic'], m['cat'], m['mfr'], m['price'], m['rx'], m['stock'],
                   (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')))
    conn.commit()
    print(f"✓ Added {len(MEDICINES)} medicines")


def gen_patients(conn, n=1000):
    c = conn.cursor()
    start = datetime.now() - timedelta(days=365)
    chronic_conds = ["Diabetes", "Hypertension", "Asthma"]
    for i in range(n):
        gender = random.choice(['Male', 'Female'])
        fname = random.choice(FIRST_NAMES_MALE if gender == 'Male' else FIRST_NAMES_FEMALE)
        lname = random.choice(LAST_NAMES)
        age = random.randint(5, 80)
        phone = f"+91{random.randint(7000000000, 9999999999)}"
        city = random.choice(CITIES)
        reg = start + timedelta(days=random.randint(0, 300))
        is_chronic = i < n * 0.15
        chronic = random.choice(chronic_conds) if is_chronic else None
        c.execute('''INSERT INTO patients (first_name, last_name, age, gender, phone, city,
                   registration_date, is_chronic, chronic_condition)
                   VALUES (?,?,?,?,?,?,?,?,?)''',
                  (fname, lname, age, gender, phone, city, reg.strftime('%Y-%m-%d'), is_chronic, chronic))
    conn.commit()
    print(f"✓ Generated {n} patients")


def gen_consults(conn):
    c = conn.cursor()
    c.execute("SELECT patient_id, registration_date, is_chronic, chronic_condition FROM patients")
    patients = c.fetchall()
    c.execute("SELECT medicine_id, name, price, prescription_required FROM medicines")
    meds = c.fetchall()
    med_dict = {m[1]: {'id': m[0], 'price': m[2]} for m in meds}

    total_c, total_t = 0, 0
    for pid, reg, is_chr, chr_cond in patients:
        num_c = random.randint(8, 20) if is_chr else random.randint(1, 6)
        reg_dt = datetime.strptime(reg, '%Y-%m-%d')
        for _ in range(num_c):
            days = random.randint(0, min((datetime.now() - reg_dt).days, 365))
            cdate = reg_dt + timedelta(days=days)
            if is_chr and random.random() < 0.6:
                ailment = chr_cond + " Management"
            else:
                ailment = random.choice(AILMENTS)
            fee = random.choice([300, 400, 500, 600, 700])
            c.execute('''INSERT INTO consultations (patient_id, consultation_date, ailment,
                       diagnosis, consultation_fee, follow_up_required)
                       VALUES (?,?,?,?,?,?)''',
                      (pid, cdate.strftime('%Y-%m-%d %H:%M:%S'), ailment,
                       f"Diagnosed with {ailment.lower()}. Treatment prescribed.", fee,
                       random.choice([True, False])))
            cid = c.lastrowid
            total_c += 1

            # Prescribe
            presc_meds = AILMENT_MEDS.get(ailment, ["Dolo 650"])
            num_m = random.randint(1, min(3, len(presc_meds)))
            for mname in random.sample(presc_meds, min(num_m, len(presc_meds))):
                if mname in med_dict:
                    dosage = random.choice(["1-0-1", "1-1-1", "0-0-1"])
                    duration = random.choice([30, 60] if is_chr else [3, 5, 7, 10])
                    quantity = random.randint(30, 90) if is_chr else random.randint(5, 30)
                    c.execute('''INSERT INTO prescriptions (consultation_id, medicine_id,
                               dosage, duration_days, quantity) VALUES (?,?,?,?,?)''',
                              (cid, med_dict[mname]['id'], dosage, duration, quantity))

            # Purchase
            if random.random() < (0.90 if is_chr else 0.65):
                tdate = cdate + timedelta(hours=random.randint(0, 48))
                c.execute('''SELECT p.medicine_id, p.quantity, m.price
                           FROM prescriptions p JOIN medicines m ON p.medicine_id=m.medicine_id
                           WHERE p.consultation_id=?''', (cid,))
                items = c.fetchall()
                total_amt = sum(i[2] * i[1] for i in items)
                pmode = random.choice(['Cash', 'Card', 'UPI', 'PhonePe', 'Paytm', 'GooglePay'])
                c.execute('''INSERT INTO transactions (patient_id, consultation_id,
                           transaction_date, total_amount, payment_mode, prescription_linked)
                           VALUES (?,?,?,?,?,1)''',
                          (pid, cid, tdate.strftime('%Y-%m-%d %H:%M:%S'), total_amt, pmode))
                tid = c.lastrowid
                total_t += 1
                for mid, qty, price in items:
                    c.execute('''INSERT INTO transaction_items (transaction_id, medicine_id,
                               quantity, price_per_unit, total_price) VALUES (?,?,?,?,?)''',
                              (tid, mid, qty, price, price * qty))
                    c.execute('UPDATE medicines SET stock_quantity=stock_quantity-? WHERE medicine_id=?',
                              (qty, mid))

    # Walk-ins
    num_walk = int(total_t * 0.4)
    otc = [m for m in meds if not m[3]]
    for _ in range(num_walk):
        tdate = datetime.now() - timedelta(days=random.randint(0, 365))
        pid = random.choice([None] + [p[0] for p in patients[:300]])
        items = random.sample(otc, random.randint(1, 4))
        total_amt = sum(m[2] * random.randint(1, 3) for m in items)
        pmode = random.choice(['Cash', 'UPI', 'PhonePe', 'Card'])
        c.execute('''INSERT INTO transactions (patient_id, consultation_id, transaction_date,
                   total_amount, payment_mode, prescription_linked) VALUES (?,?,?,?,?,0)''',
                  (pid, None, tdate.strftime('%Y-%m-%d %H:%M:%S'), total_amt, pmode))
        tid = c.lastrowid
        total_t += 1
        for m in items:
            qty = random.randint(1, 3)
            c.execute('''INSERT INTO transaction_items (transaction_id, medicine_id,
                       quantity, price_per_unit, total_price) VALUES (?,?,?,?,?)''',
                      (tid, m[0], qty, m[2], m[2] * qty))
            c.execute('UPDATE medicines SET stock_quantity=stock_quantity-? WHERE medicine_id=?',
                      (qty, m[0]))

    conn.commit()
    print(f"✓ Generated {total_c} consultations")
    print(f"✓ Generated {total_t} transactions")


def main():
    print("🤖 Creating MediSmart AI - Healthcare Analytics Database...")
    print("=" * 70)
    conn = create_db()
    print("✓ Database schema created")
    populate_meds(conn)
    gen_patients(conn, 1000)
    gen_consults(conn)

    c = conn.cursor()
    print("\n" + "=" * 70)
    print("📊 DATABASE SUMMARY:")
    print("=" * 70)
    c.execute("SELECT COUNT(*) FROM patients")
    print(f"   Patients: {c.fetchone()[0]:,}")
    c.execute("SELECT COUNT(*) FROM consultations")
    print(f"   Consultations: {c.fetchone()[0]:,}")
    c.execute("SELECT COUNT(*) FROM transactions")
    print(f"   Transactions: {c.fetchone()[0]:,}")
    c.execute("SELECT COUNT(*) FROM medicines")
    print(f"   Medicines: {c.fetchone()[0]}")
    c.execute("SELECT SUM(total_amount) FROM transactions")
    print(f"   Total Revenue: ₹{c.fetchone()[0]:,.2f}")
    conn.close()
    print("\n✅ Database created: medical_pharmacy.db")
    print("=" * 70)


if __name__ == "__main__":
    main()
# 🛡️ NetworkSecurity: Phishing Detection with Machine Learning  

A modular, production-ready pipeline for detecting phishing threats using machine learning.  
The project ingests network-related features from URLs and domains, validates them against a schema, detects data drift, and prepares clean datasets for training robust classifiers.  

---

## 📦 Features  

- ✅ MongoDB data ingestion  
- ✅ Schema-based validation using **YAML + Pandera**  
- ✅ Drift detection via **Kolmogorov–Smirnov test**  
- ✅ Train-test splitting & feature store export  
- ✅ Centralized logging & custom exception handling  
- ✅ Modular design for scalability & reuse  

---

## 🗂️ Project Structure  

```
networksecurity/
├── components/              # Core pipeline modules
│   ├── data_ingestion.py
│   ├── data_validation.py
├── entity/                  # Config and artifact definitions
│   ├── config_entity.py
│   ├── artifact_entity.py
├── exception/               # Custom exception class
├── logging/                 # Centralized logging setup
├── utils/                   # Utility functions (e.g., YAML reader)
├── constant/                # Pipeline constants and schema path
├── Artifacts/               # Generated artifacts (CSV, reports)
├── logs/                    # Runtime logs
├── venv/                    # Virtual environment (ignored)
├── .env                     # MongoDB credentials (ignored)
├── schema.yaml              # Column definitions and types
├── test_mongo_db.py         # Standalone MongoDB test script
```

---

## 📊 Dataset Schema  

Defined in **`schema.yaml`**, the dataset includes **30+ numerical features**, such as:  

- `having_IP_Address`, `SSLfinal_State`, `URL_Length`  
- `Domain_registeration_length`, `HTTPS_token`, `Page_Rank`  
- `Result`: Target label (`-1` → phishing, `1` → legitimate)  

Validation checks include:  
- Column count & type matching  
- Null value detection  
- Distribution drift detection (KS test)  

---

## ⚙️ How to Run  

### 1. Clone the Repository  

```bash
git clone https://github.com/sbmshukla/NetworkSecurity.git
cd NetworkSecurity
```

### 2. Set Up Environment  

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure MongoDB Credentials  

Create a `.env` file in the project root:  

```env
MONGO_DB_URL=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
```

### 4. Run the Pipeline  

```bash
python main.py
```

### 5. Drift Detection  

Implemented using `scipy.stats.ks_2samp` to compare distributions between training & test sets.  

Outputs include:  
- Drift status (**True/False**)  
- p-values for each feature  
- Summary CSV report  

---

## 6. Dependencies  

- **pymongo**  
- **pandas, numpy, scipy**  
- **pandera, pyyaml**  
- **scikit-learn**  
- Custom logging & exception modules  

---

## 7. Author  

**Shubham Shukla**  
Expert in ML pipelines, DevOps, and network security tooling  
- GitHub: [@sbmshukla](https://github.com/sbmshukla)  

---

## 8. Contributions  

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you'd like to change.  

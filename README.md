# 🛡️ NetworkSecurity: Phishing Detection with Machine Learning  

A machine learning-powered API for detecting phishing URLs and classifying network threats. Built with FastAPI, containerized with Docker, and deployed via a fully automated CI/CD pipeline to AWS EC2 using GitHub Actions and Amazon ECR. 

---

## 🚀 Features

- 🔍 Predict phishing URLs using trained ML models
- ⚙️ FastAPI backend for scalable API deployment
- 🐳 Dockerized for portability and reproducibility
- 🔄 CI/CD pipeline with GitHub Actions
- ☁️ Deployed to AWS EC2 via self-hosted runner
- 📦 Container image stored in AWS ECR

---

## 🛠️ Tech Stack

- Python 3.10
- FastAPI
- Scikit-learn, Pandas, NumPy
- Docker
- GitHub Actions
- AWS ECR & EC2

---

```
graph TD
A[Push to main branch] --> B[GitHub Actions CI]
B --> C[Build & Push Docker Image to ECR]
C --> D[Trigger EC2 Self-Hosted Runner]
D --> E[Pull Image & Run Container]

Trigger: Push to main

CI: Linting, testing, Docker build

CD: Image pushed to ECR, EC2 pulls and runs container
```

---

## 🗂️ Project Structure  

```
networksecurity/
├── .github/                   # GitHub Actions workflows
│   └── workflows/
│       └── ci-cd.yml
├── src/                       # All source code for the project
│   ├── __init__.py            # Makes `src` a Python package
│   ├── networksecurity/       # Main package directory
│   │   ├── __init__.py        # Makes `networksecurity` a Python package
│   │   ├── components/        # Individual pipeline modules
│   │   │   ├── data_ingestion.py
│   │   │   ├── data_validation.py
│   │   │   └── model_trainer.py
│   │   ├── entity/            # Configuration and artifact definitions
│   │   │   ├── config_entity.py
│   │   │   └── artifact_entity.py
│   │   ├── pipeline/          # End-to-end pipelines
│   │   │   ├── __init__.py
│   │   │   ├── train_pipeline.py
│   │   │   └── predict_pipeline.py
│   │   ├── utils/             # Reusable utility functions
│   │   │   └── common.py
│   │   ├── config/            # Configuration files (YAML, etc.)
│   │   │   └── config.yaml
│   │   ├── constant/          # Project-wide constants
│   │   │   └── training_pipeline.py
│   │   ├── exception.py       # Custom exception class
│   │   └── logger.py          # Centralized logging setup
│   ├── app.py                 # FastAPI application
│   └── main.py                # Main script to run the training pipeline
├── data/                      # Data storage
│   ├── raw/                   # Original, raw data
│   └── processed/             # Cleaned, transformed data
├── models/                    # Saved ML models
├── notebooks/                 # Jupyter notebooks for experimentation
├── tests/                     # Unit and integration tests
│   ├── __init__.py
│   └── test_app.py            # Tests for the FastAPI app
├── artifacts/                 # Generated artifacts from pipeline runs
├── logs/                      # Runtime logs
├── .env                       # Environment variables (ignored by Git)
├── Dockerfile                 # For containerization
├── requirements.txt           # Python dependencies
└── README.md                  # Project README file
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

---
## Run Using Docker
```
git clone https://github.com/sbmshukla/NetworkSecurity.git
cd NetworkSecurity
docker build -t networksecurity .
docker run -d -p 8080:8080 networksecurity
```

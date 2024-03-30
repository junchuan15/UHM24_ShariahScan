import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from company import Company

class Database:
    def __init__(self):
        cred = credentials.Certificate("firebase.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def retrieve_company_data(self, company_name):
        doc_ref = self.db.collection("Company").where("name", "==", company_name)
        docs = doc_ref.get()
        for doc in docs:
            data = doc.to_dict()
            company = Company(
                CBB_current=data.get("CBB_current"),
                CBB_previous=data.get("CBB_previous"),
                Noncurrent_BB_current=data.get("Noncurrent_BB_current"),
                Noncurrent_BB_previous=data.get("Noncurrent_BB_previous"),
                PL_Before_Tax_current=data.get("PL_Before_Tax_current"),
                PL_Before_Tax_previous=data.get("PL_Before_Tax_previous"),
                Revenue_current=data.get("Revenue_current"),
                Revenue_previous=data.get("Revenue_previous"),
                TA_current=data.get("TA_current"),
                TA_previous=data.get("TA_previous"),
                current_BB_current=data.get("current_BB_current"),
                current_BB_previous=data.get("current_BB_previous"),
                name=data.get("name"),
            )

        return company
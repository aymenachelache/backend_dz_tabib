

# src/homepage/utils.py

import random

def format_doctor_data(doctor_row):
    """Format a single doctor's data from the database into a dictionary."""
    return {
        "firstname": doctor_row["firstname"],
        "familyname": doctor_row["familyname"],
        "specialty": doctor_row["specialty"],
        "ville": doctor_row["ville"],
        "wilaya": doctor_row["wilaya"],
        "rue": doctor_row["rue"],
        "photo_url": doctor_row.get("photo_url"),
        "rating": doctor_row.get("rating", round(random.uniform(1, 5), 2)),
    }



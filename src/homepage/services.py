def fetch_doctors(page: int, db):
    """Fetch doctors for the homepage with pagination."""
    page_size = 6
    offset = (page - 1) * page_size
    query = """
        SELECT 
            firstname, 
            familyname, 
            Nom_Specialite AS specialty, 
            ville, 
            wilaya, 
            rue, 
            photo_url, 
            rating 
        FROM doctors 
        LEFT JOIN specialites ON doctors.ID_Specialite = specialites.ID_Specialite 
        LIMIT %s OFFSET %s
    """
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()

def fetch_doctors_by_specialty(category: str, page: int, db):
    """Fetch doctors filtered by category (specialty) with pagination."""
    page_size = 6
    offset = (page - 1) * page_size

    query = """
        SELECT 
            firstname, 
            familyname, 
            Nom_Specialite AS specialty, 
            ville, 
            wilaya, 
            rue, 
            photo_url, 
            rating 
        FROM doctors 
        LEFT JOIN specialites ON doctors.ID_Specialite = specialites.ID_Specialite 
        WHERE Nom_Specialite = %s 
        LIMIT %s OFFSET %s
    """
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, (category, page_size, offset))
        return cursor.fetchall()



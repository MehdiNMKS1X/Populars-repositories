import database

def get_db(db_name: str) -> 'Database':
    from database import Database
    return Database(db_name)

def get_empty_db(db_name: str) -> 'Database':
    db = get_db(db_name)
    for table_name in db.list_tables():
        db.delete_table(table_name)
    return db

def get_programme_db() -> 'Database':
    from database import FieldType
    db = get_empty_db('programme')
    db.create_table(
        'cours',
        ('MNEMONIQUE', FieldType.INTEGER),
        ('NOM', FieldType.STRING),
        ('COORDINATEUR', FieldType.STRING),
        ('CREDITS', FieldType.INTEGER)
    )
    return db
COURSES = [
    {'MNEMONIQUE': 101, 'NOM': 'Programmation',
     'COORDINATEUR': 'Thierry Massart', 'CREDITS': 10},
    {'MNEMONIQUE': 102, 'NOM': 'Fonctionnement des ordinateurs',
     'COORDINATEUR': 'Gilles Geeraerts', 'CREDITS': 5},
    {'MNEMONIQUE': 103, 'NOM': 'Algorithmique I',
     'COORDINATEUR': 'Olivier Markowitch', 'CREDITS': 10},
    {'MNEMONIQUE': 105, 'NOM': 'Langages de programmation I',
     'COORDINATEUR': 'Christophe Petit', 'CREDITS': 5},
    {'MNEMONIQUE': 106, 'NOM': 'Projet d\'informatique I',
     'COORDINATEUR': 'Gwenaël Joret', 'CREDITS': 5},
]

def fill_courses(db: 'Database') -> None:
    for course in COURSES:
        db.add_entry('cours', course)
    return db

db = get_programme_db()
entry = {
        'MNEMONIQUE': 101, 'NOM': 'Programmation',
        'COORDINATEUR': 'Thierry Massart', 'CREDITS': 10
}
fill_courses(db)
data = db.get_complete_table('cours')
print(data)

#retenir l'endroit où tu es dans le fichier et sauvegarder 
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(override=True)


class DataManager:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        #print(db_url)
        self.engine = create_engine(db_url)

    def get_sex(self):
        """
        Return data for sex pie
        """
        query = """
        SELECT person.gender_concept_id, concept.concept_name, count(person.gender_concept_id) as total
        FROM cdm_synthea10.person
        JOIN cdm_synthea10.concept on concept.concept_id = person.gender_concept_id
        GROUP BY person.gender_concept_id, concept.concept_name;
        """
        try:
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
        

    def get_age_at_first_seen(self):
        """
        Return data for age at first seem
        """
        query = """
                SELECT p.person_id, op.observation_period_start_date, p.birth_datetime, EXTRACT(YEAR FROM AGE(p.birth_datetime)) AS age_in_years
                FROM cdm_synthea10.observation_period op
                JOIN cdm_synthea10.person p ON p.person_id = op.person_id
                """
        try:
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
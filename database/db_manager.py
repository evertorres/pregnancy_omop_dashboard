import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno
load_dotenv(override=True)


class DataManager:
    def __init__(self):
        pass

    @staticmethod
    @st.cache_resource
    def get_engine():
        return create_engine(os.getenv("DATABASE_URL"))

    @st.cache_data
    def get_count_patients(_self):
        """
        Return the name of database and the number of patients
        """
    
        engine = _self.get_engine()
        query = """
        SELECT count(*) as total
        FROM cdm_synthea10.person
        """
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
    
    @st.cache_data
    def get_sex(_self):
        """
        Return data for sex pie
        """
        engine = _self.get_engine()
        query = """
        SELECT person.gender_concept_id, concept.concept_name, count(person.gender_concept_id) as total
        FROM cdm_synthea10.person
        JOIN cdm_synthea10.concept on concept.concept_id = person.gender_concept_id
        GROUP BY person.gender_concept_id, concept.concept_name;
        """
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
        

    @st.cache_data
    def get_age_at_first_seen(_self):
        """
        Return data for age at first seem
        """
        engine = _self.get_engine()
        query = """
                SELECT p.person_id, op.observation_period_start_date, p.birth_datetime, EXTRACT(YEAR FROM AGE(p.birth_datetime)) AS age_in_years
                FROM cdm_synthea10.observation_period op
                JOIN cdm_synthea10.person p ON p.person_id = op.person_id
                """
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
        

    @st.cache_data
    def get_conditions_per_person(_self):
        """
        Return data for conditions per person
        """
        engine = _self.get_engine()
        query = """
                SELECT COUNT(DISTINCT co.person_id) AS cnt , co.condition_concept_id, c.concept_name
                FROM cdm_synthea10.condition_occurrence co
                JOIN cdm_synthea10.concept c on c.concept_id = co.condition_concept_id
                GROUP BY co.condition_concept_id, c.concept_name
                ORDER BY cnt DESC
                LIMIT 50;
                """
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
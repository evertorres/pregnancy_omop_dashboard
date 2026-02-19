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
    def get_race(_self):
        """
        Return data for race pie
        """
        engine = _self.get_engine()
        query = """
        SELECT person.race_concept_id, concept.concept_name, count(person.race_concept_id) as total
        FROM cdm_synthea10.person
        LEFT JOIN cdm_synthea10.concept on concept.concept_id = person.race_concept_id
        GROUP BY person.race_concept_id, concept.concept_name;
        """
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
        
    @st.cache_data
    def get_ethnicity(_self):
        """
        Return data for race pie
        """
        engine = _self.get_engine()
        query = """
        SELECT person.ethnicity_concept_id, concept.concept_name, count(person.ethnicity_concept_id) as total
        FROM cdm_synthea10.person
        LEFT JOIN cdm_synthea10.concept on concept.concept_id = person.ethnicity_concept_id
        GROUP BY person.ethnicity_concept_id, concept.concept_name;
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
        
    @st.cache_data
    def get_data_density_total_rows(_self):
        """
        Return data density of some tables in OMOP
        """
        engine = _self.get_engine()
        query = """WITH condition_counts AS (
                    SELECT TO_CHAR(condition_start_date, 'YYYY-MM') AS month_year, COUNT(*) AS count_cond
                    FROM cdm_synthea10.condition_occurrence GROUP BY 1
                ),
                measurement_counts AS (
                    SELECT TO_CHAR(measurement_date, 'YYYY-MM') AS month_year, COUNT(*) AS count_meas
                    FROM cdm_synthea10.measurement GROUP BY 1
                ),
                death_counts AS (
                    SELECT TO_CHAR(death_date, 'YYYY-MM') AS month_year, COUNT(*) AS count_death
                    FROM cdm_synthea10.death GROUP BY 1
                ),
                observation_counts AS (
                    SELECT TO_CHAR(observation_date, 'YYYY-MM') AS month_year, COUNT(*) AS count_obs
                    FROM cdm_synthea10.observation GROUP BY 1
                ),
                visit_counts AS (
                    SELECT TO_CHAR(visit_start_date, 'YYYY-MM') AS month_year, COUNT(*) AS count_visit
                    FROM cdm_synthea10.visit_occurrence GROUP BY 1
                ),
                procedure_counts AS (
                    SELECT TO_CHAR(procedure_date, 'YYYY-MM') AS month_year, COUNT(*) AS count_proc
                    FROM cdm_synthea10.procedure_occurrence GROUP BY 1
                ),
                drug_counts AS (
                    SELECT TO_CHAR(drug_exposure_start_date, 'YYYY-MM') AS month_year, COUNT(*) AS count_drug
                    FROM cdm_synthea10.drug_exposure GROUP BY 1
                ),
                device_counts AS (
                    SELECT TO_CHAR(device_exposure_start_date, 'YYYY-MM') AS month_year, COUNT(*) AS count_device
                    FROM cdm_synthea10.device_exposure GROUP BY 1
                ),
                all_months AS (
                    SELECT month_year FROM condition_counts
                    UNION SELECT month_year FROM measurement_counts
                    UNION SELECT month_year FROM death_counts
                    UNION SELECT month_year FROM observation_counts
                    UNION SELECT month_year FROM visit_counts
                    UNION SELECT month_year FROM procedure_counts
                    UNION SELECT month_year FROM drug_counts
                    UNION SELECT month_year FROM device_counts
                )

                SELECT 
                    am.month_year,
                    COALESCE(c.count_cond, 0) AS condition_total,
                    COALESCE(m.count_meas, 0) AS measurement_total,
                    COALESCE(d.count_death, 0) AS death_total,
                    COALESCE(o.count_obs, 0) AS observation_total,
                    COALESCE(v.count_visit, 0) AS visit_total,
                    COALESCE(p.count_proc, 0) AS procedure_total,
                    COALESCE(dr.count_drug, 0) AS drug_total,
                    COALESCE(dv.count_device, 0) AS device_total
                FROM all_months am
                LEFT JOIN condition_counts c   ON am.month_year = c.month_year
                LEFT JOIN measurement_counts m ON am.month_year = m.month_year
                LEFT JOIN death_counts d       ON am.month_year = d.month_year
                LEFT JOIN observation_counts o ON am.month_year = o.month_year
                LEFT JOIN visit_counts v       ON am.month_year = v.month_year
                LEFT JOIN procedure_counts p   ON am.month_year = p.month_year
                LEFT JOIN drug_counts dr       ON am.month_year = dr.month_year
                LEFT JOIN device_counts dv     ON am.month_year = dv.month_year
                ORDER BY 1 ASC;
                """
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
        
    @st.cache_data
    def get_avg_records_per_person_per_month(_self):
        """
        Return the average of records per person per month
        """
        engine = _self.get_engine()
        query = """WITH metrics_per_table AS (
                    SELECT 
                        DATE_TRUNC('month', condition_start_date)::DATE as month_date,
                        'condition' as domain,
                        COUNT(*) as total_recs,
                        COUNT(DISTINCT person_id) as unique_ppl
                    FROM cdm_synthea10.condition_occurrence GROUP BY 1
                    
                    UNION ALL
                    
                    SELECT DATE_TRUNC('month', measurement_date)::DATE, 'measurement', COUNT(*), COUNT(DISTINCT person_id)
                    FROM cdm_synthea10.measurement GROUP BY 1
                    
                    UNION ALL
                    
                    SELECT DATE_TRUNC('month', death_date)::DATE, 'death', COUNT(*), COUNT(DISTINCT person_id)
                    FROM cdm_synthea10.death GROUP BY 1
                    
                    UNION ALL
                    
                    SELECT DATE_TRUNC('month', observation_date)::DATE, 'observation', COUNT(*), COUNT(DISTINCT person_id)
                    FROM cdm_synthea10.observation GROUP BY 1
                    
                    UNION ALL
                    
                    SELECT DATE_TRUNC('month', visit_start_date)::DATE, 'visit', COUNT(*), COUNT(DISTINCT person_id)
                    FROM cdm_synthea10.visit_occurrence GROUP BY 1
                    
                    UNION ALL
                    
                    SELECT DATE_TRUNC('month', procedure_date)::DATE, 'procedure', COUNT(*), COUNT(DISTINCT person_id)
                    FROM cdm_synthea10.procedure_occurrence GROUP BY 1
                    
                    UNION ALL
                    
                    SELECT DATE_TRUNC('month', drug_exposure_start_date)::DATE, 'drug', COUNT(*), COUNT(DISTINCT person_id)
                    FROM cdm_synthea10.drug_exposure GROUP BY 1
                    
                    UNION ALL
                    
                    SELECT DATE_TRUNC('month', device_exposure_start_date)::DATE, 'device', COUNT(*), COUNT(DISTINCT person_id)
                    FROM cdm_synthea10.device_exposure GROUP BY 1
                )

                SELECT 
                    month_date,
                    ROUND(MAX(CASE WHEN domain = 'condition'   THEN total_recs::numeric / NULLIF(unique_ppl, 0) END), 2) AS avg_conditions,
                    ROUND(MAX(CASE WHEN domain = 'measurement' THEN total_recs::numeric / NULLIF(unique_ppl, 0) END), 2) AS avg_measurements,
                    ROUND(MAX(CASE WHEN domain = 'death'       THEN total_recs::numeric / NULLIF(unique_ppl, 0) END), 2) AS avg_deaths,
                    ROUND(MAX(CASE WHEN domain = 'observation' THEN total_recs::numeric / NULLIF(unique_ppl, 0) END), 2) AS avg_observations,
                    ROUND(MAX(CASE WHEN domain = 'visit'       THEN total_recs::numeric / NULLIF(unique_ppl, 0) END), 2) AS avg_visits,
                    ROUND(MAX(CASE WHEN domain = 'procedure'   THEN total_recs::numeric / NULLIF(unique_ppl, 0) END), 2) AS avg_procedures,
                    ROUND(MAX(CASE WHEN domain = 'drug'        THEN total_recs::numeric / NULLIF(unique_ppl, 0) END), 2) AS avg_drugs,
                    ROUND(MAX(CASE WHEN domain = 'device'      THEN total_recs::numeric / NULLIF(unique_ppl, 0) END), 2) AS avg_devices
                FROM metrics_per_table
                GROUP BY month_date
                ORDER BY month_date;
        """

        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
        
    @st.cache_data
    def get_records_per_person_per_domain(_self):
        """
        Return the number of records per person per domain
        """

        engine = _self.get_engine()
        query = """
                    -- 1. Condition (Diagnósticos)
                    SELECT 
                        person_id, 
                        'Condition' AS domain, 
                        COUNT(DISTINCT condition_concept_id) AS n_concepts
                    FROM cdm_synthea10.condition_occurrence
                    GROUP BY person_id

                    UNION ALL

                    -- 2. Measurement (Laboratorios/Mediciones)
                    -- Nota: En OMOP estándar la tabla suele llamarse 'measurement', no 'measurement_occurrence'
                    SELECT 
                        person_id, 
                        'Measurement' AS domain, 
                        COUNT(DISTINCT measurement_concept_id) AS n_concepts
                    FROM cdm_synthea10.measurement
                    GROUP BY person_id

                    UNION ALL

                    -- 3. Drug (Medicamentos)
                    SELECT 
                        person_id, 
                        'Drug' AS domain, 
                        COUNT(DISTINCT drug_concept_id) AS n_concepts
                    FROM cdm_synthea10.drug_exposure
                    GROUP BY person_id

                    UNION ALL

                    -- 4. Observation (Historia Social/Otros)
                    SELECT 
                        person_id, 
                        'Observation' AS domain, 
                        COUNT(DISTINCT observation_concept_id) AS n_concepts
                    FROM cdm_synthea10.observation
                    GROUP BY person_id

                    UNION ALL

                    -- 5. Procedure (Procedimientos)
                    SELECT 
                        person_id, 
                        'Procedure' AS domain, 
                        COUNT(DISTINCT procedure_concept_id) AS n_concepts
                    FROM cdm_synthea10.procedure_occurrence
                    GROUP BY person_id;
                     """
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error
        
    @st.cache_data
    def get_year_of_birth_patients(_self):
        """
        Return the year of birth of patients
        """
        engine = _self.get_engine()
        query = """SELECT person_id, year_of_birth as age_in_years
                   FROM cdm_synthea10.person"""
        
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return pd.DataFrame() # Retornar vacío en caso de error

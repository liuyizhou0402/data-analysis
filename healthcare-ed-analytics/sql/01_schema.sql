-- =====================================================================
-- Emergency Department & Patient Flow Analytics — Schema (DDL)
-- =====================================================================
-- Dialect: portable ANSI SQL. Tested on SQLite 3.40+ and PostgreSQL 15.
-- A star-schema-style model: two fact tables (presentations, admissions)
-- referencing one dimension table (patients).
-- =====================================================================

DROP TABLE IF EXISTS admissions;
DROP TABLE IF EXISTS ed_presentations;
DROP TABLE IF EXISTS patients;

-- Dimension: patient master
CREATE TABLE patients (
    patient_id          INTEGER PRIMARY KEY,
    age                 INTEGER      NOT NULL,
    sex                 VARCHAR(10)  NOT NULL,
    region              VARCHAR(40)  NOT NULL,   -- catchment / LHD area
    chronic_conditions  INTEGER      NOT NULL,   -- comorbidity count
    insurance_type      VARCHAR(20)  NOT NULL    -- Medicare only / Private health
);

-- Fact: one row per ED presentation
CREATE TABLE ed_presentations (
    presentation_id           INTEGER PRIMARY KEY,
    patient_id                INTEGER      NOT NULL,
    arrival_datetime          TIMESTAMP    NOT NULL,
    triage_category           INTEGER      NOT NULL,  -- ATS 1 (resus) .. 5 (non-urgent)
    presenting_group          VARCHAR(30)  NOT NULL,
    arrival_mode              VARCHAR(15)  NOT NULL,  -- Ambulance / Self
    ed_los_minutes            NUMERIC(8,1) NOT NULL,  -- time in ED
    left_without_being_seen   INTEGER      NOT NULL,  -- 1 = LWBS
    admitted                  INTEGER      NOT NULL,  -- 1 = admitted to ward
    departure_datetime        TIMESTAMP    NOT NULL,
    met_4hr_target            INTEGER      NOT NULL,  -- 1 = LOS <= 240 min (NEAT)
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
);

-- Fact: inpatient admissions arising from an ED presentation
CREATE TABLE admissions (
    admission_id           INTEGER PRIMARY KEY,
    presentation_id        INTEGER      NOT NULL,
    patient_id             INTEGER      NOT NULL,
    admit_datetime         TIMESTAMP    NOT NULL,
    discharge_datetime     TIMESTAMP    NOT NULL,
    los_days               NUMERIC(6,2) NOT NULL,   -- inpatient length of stay
    diagnosis_group        VARCHAR(30)  NOT NULL,
    discharge_destination  VARCHAR(30)  NOT NULL,
    readmitted_28d         INTEGER      NOT NULL,   -- 1 = readmitted within 28 days
    FOREIGN KEY (presentation_id) REFERENCES ed_presentations (presentation_id),
    FOREIGN KEY (patient_id)      REFERENCES patients (patient_id)
);

CREATE INDEX idx_pres_arrival ON ed_presentations (arrival_datetime);
CREATE INDEX idx_pres_triage  ON ed_presentations (triage_category);
CREATE INDEX idx_adm_dx       ON admissions (diagnosis_group);

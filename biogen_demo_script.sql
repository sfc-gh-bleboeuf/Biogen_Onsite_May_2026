-- ============================================================
--  BIOGEN CLINICAL INTELLIGENCE DEMO
--  Snowflake × Biogen | May 13, 2026
--  Presenter: Bob LeBoeuf (bob.leboeuf@snowflake.com)
--
--  AUDIENCE: Clinical/SAS team (Daniel Boisvert, Francis Kendall)
--  PURPOSE : Show Snowflake as a clinical AI platform, not just
--            a warehouse. Bridge from SAS workflows to Snowflake.
--
--  RUN THESE IN ORDER. Each section is a demo "act".
--  Estimated total runtime: ~40 minutes
-- ============================================================


-- ============================================================
-- SETUP: Create demo database and schema
-- ============================================================

USE ROLE SYSADMIN;

CREATE DATABASE IF NOT EXISTS BIOGEN_CLINICAL_DEMO;
CREATE SCHEMA IF NOT EXISTS BIOGEN_CLINICAL_DEMO.SDTM;
CREATE SCHEMA IF NOT EXISTS BIOGEN_CLINICAL_DEMO.ADAM;
CREATE SCHEMA IF NOT EXISTS BIOGEN_CLINICAL_DEMO.DOCS;

USE DATABASE BIOGEN_CLINICAL_DEMO;
USE SCHEMA SDTM;

CREATE WAREHOUSE IF NOT EXISTS CLINICAL_DEMO_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND   = 60
  AUTO_RESUME    = TRUE
  COMMENT        = 'Demo warehouse for Biogen clinical session';

USE WAREHOUSE CLINICAL_DEMO_WH;


-- ============================================================
-- ACT 1: LOAD CLINICAL DATA (SDTM Domains)
-- "Just like loading SAS datasets — but into a governed cloud table"
-- ============================================================

-- 1a. Subject Demographics (DM domain)
CREATE OR REPLACE TABLE SDTM.DM (
    STUDYID   VARCHAR(20)  COMMENT 'Study identifier',
    USUBJID   VARCHAR(50)  COMMENT 'Unique subject identifier',
    SUBJID    VARCHAR(20)  COMMENT 'Subject ID within site',
    SITEID    VARCHAR(10)  COMMENT 'Site identifier',
    ARM       VARCHAR(50)  COMMENT 'Treatment arm description',
    ARMCD     VARCHAR(10)  COMMENT 'Treatment arm code',
    AGE       NUMBER(3)    COMMENT 'Age in years at screening',
    SEX       CHAR(1)      COMMENT 'Sex: M / F',
    RACE      VARCHAR(50)  COMMENT 'Race',
    DMDTC     DATE         COMMENT 'Date of informed consent'
);

-- 1b. Adverse Events (AE domain)
CREATE OR REPLACE TABLE SDTM.AE (
    STUDYID   VARCHAR(20),
    USUBJID   VARCHAR(50),
    AESEQ     NUMBER(4)    COMMENT 'Sequence number within subject',
    AEDECOD   VARCHAR(200) COMMENT 'Dictionary-derived AE term (MedDRA)',
    AEBODSYS  VARCHAR(200) COMMENT 'Body system or organ class',
    AESEV     VARCHAR(20)  COMMENT 'Severity: MILD / MODERATE / SEVERE',
    AESEVN    NUMBER(1)    COMMENT 'Severity numeric grade (1-5)',
    AESER     CHAR(1)      COMMENT 'Serious adverse event: Y / N',
    AEREL     VARCHAR(50)  COMMENT 'Causality: RELATED / NOT RELATED / POSSIBLE',
    AESTDTC   DATE         COMMENT 'Start date',
    AEENDTC   DATE         COMMENT 'End date',
    AEOUT     VARCHAR(50)  COMMENT 'Outcome',
    AENARR    TEXT         COMMENT 'Narrative / verbatim text'
);

-- 1c. Laboratory Results (LB domain)
CREATE OR REPLACE TABLE SDTM.LB (
    STUDYID   VARCHAR(20),
    USUBJID   VARCHAR(50),
    LBSEQ     NUMBER(4),
    LBTEST    VARCHAR(100) COMMENT 'Lab test name',
    LBTESTCD  VARCHAR(20)  COMMENT 'Lab test short name',
    LBCAT     VARCHAR(50)  COMMENT 'Category (HEMATOLOGY, CHEMISTRY, etc.)',
    LBORRES   VARCHAR(50)  COMMENT 'Result (original units)',
    LBORRESU  VARCHAR(20)  COMMENT 'Unit',
    LBSTRESN  FLOAT        COMMENT 'Numeric standardized result',
    LBSTRESU  VARCHAR(20)  COMMENT 'Standardized unit',
    LBNRLO    FLOAT        COMMENT 'Normal range low',
    LBNRHI    FLOAT        COMMENT 'Normal range high',
    LBBLFL    CHAR(1)      COMMENT 'Baseline flag: Y',
    VISITNUM  NUMBER(4)    COMMENT 'Visit number',
    VISIT     VARCHAR(50)  COMMENT 'Visit name',
    LBDTC     DATE         COMMENT 'Date of collection'
);

-- 1d. Protocol Deviations (DV domain)
CREATE OR REPLACE TABLE SDTM.DV (
    STUDYID   VARCHAR(20),
    USUBJID   VARCHAR(50),
    DVSEQ     NUMBER(4),
    DVTERM    VARCHAR(200) COMMENT 'Deviation term',
    DVSCAT    VARCHAR(100) COMMENT 'Sub-category',
    DVSTDTC   DATE,
    DVTEXT    TEXT         COMMENT 'Free-text description of deviation'
);


-- ============================================================
-- Insert synthetic CDISC-format demo data
-- ============================================================

INSERT INTO SDTM.DM VALUES
('STUDY-2024-001','STUDY-001-001-001','001','SITE-001','Placebo','PBO',   52,'M','WHITE',           '2024-01-15'),
('STUDY-2024-001','STUDY-001-001-002','002','SITE-001','Drug A 10mg','A10',47,'F','WHITE',           '2024-01-18'),
('STUDY-2024-001','STUDY-001-001-003','003','SITE-001','Drug A 20mg','A20',61,'M','BLACK OR AFRICAN AMERICAN','2024-01-20'),
('STUDY-2024-001','STUDY-001-002-001','001','SITE-002','Placebo','PBO',   55,'F','ASIAN',            '2024-01-22'),
('STUDY-2024-001','STUDY-001-002-002','002','SITE-002','Drug A 10mg','A10',43,'M','WHITE',           '2024-01-25'),
('STUDY-2024-001','STUDY-001-002-003','003','SITE-002','Drug A 20mg','A20',68,'F','WHITE',           '2024-01-28'),
('STUDY-2024-001','STUDY-001-003-001','001','SITE-003','Placebo','PBO',   39,'M','HISPANIC OR LATINO','2024-02-01'),
('STUDY-2024-001','STUDY-001-003-002','002','SITE-003','Drug A 10mg','A10',58,'F','WHITE',           '2024-02-03'),
('STUDY-2024-001','STUDY-001-003-003','003','SITE-003','Drug A 20mg','A20',72,'M','WHITE',           '2024-02-05'),
('STUDY-2024-001','STUDY-001-003-004','004','SITE-003','Drug A 20mg','A20',50,'F','ASIAN',           '2024-02-08');

INSERT INTO SDTM.AE VALUES
('STUDY-2024-001','STUDY-001-001-002',1,'Nausea','Gastrointestinal disorders','MILD',1,'N','RELATED','2024-02-10','2024-02-14','RECOVERED/RESOLVED','Subject reported mild nausea approximately 2 hours after study drug administration. No antiemetic required. Resolved spontaneously within 4 days.'),
('STUDY-2024-001','STUDY-001-001-002',2,'Headache','Nervous system disorders','MILD',1,'N','POSSIBLE','2024-02-20','2024-02-22','RECOVERED/RESOLVED','Mild frontal headache reported on Day 15. Subject took acetaminophen 500mg PRN with full resolution in 2 days. Investigator assessed as possibly related.'),
('STUDY-2024-001','STUDY-001-001-003',1,'Alanine aminotransferase increased','Investigations','SEVERE',3,'Y','RELATED','2024-03-01',NULL,'NOT RECOVERED/NOT RESOLVED','Subject presented with asymptomatic elevation of ALT to 8.2x ULN on Week 8 laboratory assessment. Study drug was interrupted. Hepatology consult obtained. Subject hospitalized for observation. SAE reported to sponsor within 24 hours per protocol.'),
('STUDY-2024-001','STUDY-001-002-002',1,'Fatigue','General disorders','MODERATE',2,'N','POSSIBLE','2024-02-15','2024-02-28','RECOVERED/RESOLVED','Moderate fatigue reported starting Day 21. Subject able to perform daily activities with some limitation. Resolved without intervention at Day 34.'),
('STUDY-2024-001','STUDY-001-002-003',1,'Dizziness','Nervous system disorders','MILD',1,'N','RELATED','2024-02-12','2024-02-13','RECOVERED/RESOLVED','Brief dizziness reported within 1 hour of first dose. Resolved completely within 24 hours. No dose modification required.'),
('STUDY-2024-001','STUDY-001-002-003',2,'Hypertension','Vascular disorders','SEVERE',3,'Y','POSSIBLE','2024-03-15',NULL,'NOT RECOVERED/NOT RESOLVED','Subject developed blood pressure readings of 168/105 mmHg at Week 10 visit. Cardiology consult initiated. Subject started on antihypertensive therapy. Reported as serious AE due to hospitalization. Causal relationship assessed as possible.'),
('STUDY-2024-001','STUDY-001-003-002',1,'Rash','Skin and subcutaneous tissue disorders','MILD',1,'N','NOT RELATED','2024-02-25','2024-03-05','RECOVERED/RESOLVED','Maculopapular rash on forearm. Considered related to a new detergent used by subject per self-report. Resolved with topical hydrocortisone.'),
('STUDY-2024-001','STUDY-001-003-003',1,'Dyspnea','Respiratory, thoracic and mediastinal disorders','MODERATE',2,'Y','RELATED','2024-03-10',NULL,'RECOVERING/RESOLVING','Subject reported progressive shortness of breath on exertion at Week 9 visit. Pulmonary function tests ordered. SAE declared due to incapacitating nature. Study drug dose reduced. Partial improvement noted at follow-up visit.'),
('STUDY-2024-001','STUDY-001-003-004',1,'Nausea','Gastrointestinal disorders','MILD',1,'N','RELATED','2024-02-18','2024-02-20','RECOVERED/RESOLVED','Mild nausea on Day 10, self-resolving within 48 hours. No treatment required.'),
('STUDY-2024-001','STUDY-001-001-001',1,'Insomnia','Psychiatric disorders','MILD',1,'N','NOT RELATED','2024-02-28','2024-03-10','RECOVERED/RESOLVED','Subject reported difficulty sleeping attributed to personal stress. Investigator assessed as not related to study drug.');

INSERT INTO SDTM.LB VALUES
-- ALT values - Drug A 20mg subjects show elevation
('STUDY-2024-001','STUDY-001-001-003',1,'Alanine Aminotransferase','ALT','CHEMISTRY','22','U/L',22,  'U/L',7,56,'Y',1,'BASELINE','2024-01-20'),
('STUDY-2024-001','STUDY-001-001-003',2,'Alanine Aminotransferase','ALT','CHEMISTRY','412','U/L',412,'U/L',7,56,'N',4,'WEEK 8', '2024-03-18'),
('STUDY-2024-001','STUDY-001-002-002',1,'Alanine Aminotransferase','ALT','CHEMISTRY','18','U/L',18,  'U/L',7,56,'Y',1,'BASELINE','2024-01-25'),
('STUDY-2024-001','STUDY-001-002-002',2,'Alanine Aminotransferase','ALT','CHEMISTRY','28','U/L',28,  'U/L',7,56,'N',4,'WEEK 8', '2024-03-22'),
('STUDY-2024-001','STUDY-001-003-003',1,'Alanine Aminotransferase','ALT','CHEMISTRY','24','U/L',24,  'U/L',7,56,'Y',1,'BASELINE','2024-02-05'),
('STUDY-2024-001','STUDY-001-003-003',2,'Alanine Aminotransferase','ALT','CHEMISTRY','52','U/L',52,  'U/L',7,56,'N',4,'WEEK 8', '2024-04-01'),
-- Hemoglobin
('STUDY-2024-001','STUDY-001-001-001',1,'Hemoglobin','HGB','HEMATOLOGY','14.2','g/dL',14.2,'g/dL',12.0,17.5,'Y',1,'BASELINE','2024-01-15'),
('STUDY-2024-001','STUDY-001-001-002',1,'Hemoglobin','HGB','HEMATOLOGY','13.8','g/dL',13.8,'g/dL',12.0,17.5,'Y',1,'BASELINE','2024-01-18'),
('STUDY-2024-001','STUDY-001-002-001',1,'Hemoglobin','HGB','HEMATOLOGY','12.1','g/dL',12.1,'g/dL',12.0,17.5,'Y',1,'BASELINE','2024-01-22'),
('STUDY-2024-001','STUDY-001-003-002',1,'Hemoglobin','HGB','HEMATOLOGY','15.3','g/dL',15.3,'g/dL',12.0,17.5,'Y',1,'BASELINE','2024-02-03');

INSERT INTO SDTM.DV VALUES
('STUDY-2024-001','STUDY-001-001-002',1,'Study drug taken with food',     'Dosing/Administration','2024-02-10','Subject reported taking study drug with a full meal on Day 25, contrary to protocol instructions requiring fasting administration. Medication log confirmed. No clinical impact observed.'),
('STUDY-2024-001','STUDY-001-002-003',1,'Prohibited concomitant medication','Eligibility Criteria',  '2024-03-05','Subject self-initiated ibuprofen for 3 days (NSAIDs prohibited per protocol Section 5.3). Reported at Week 10 visit. No washout period performed. Protocol deviation filed.'),
('STUDY-2024-001','STUDY-001-003-001',1,'Late informed consent re-signing',  'Informed Consent',    '2024-02-15','Subject''s re-consent for protocol amendment v2.0 obtained 3 days outside the required window due to site scheduling error. Reviewed by IRB and deemed acceptable per deviation committee.'),
('STUDY-2024-001','STUDY-001-003-003',1,'Missed visit window',              'Visit Window',         '2024-03-20','Week 12 visit occurred 11 days outside the allowed ±7 day window due to subject travel. PK sample not collected per missed visit. Statistical implications reviewed with biostatistics team.');


-- ============================================================
-- ACT 2: GOVERNANCE — Column Masking & Row Access Policies
-- "This is your GxP / 21 CFR Part 11 control layer"
-- ============================================================

-- Create roles for the demo
CREATE ROLE IF NOT EXISTS CLINICAL_REVIEWER;
CREATE ROLE IF NOT EXISTS CLINICAL_VIEWER;
GRANT ROLE CLINICAL_REVIEWER TO ROLE SYSADMIN;

-- Column masking: only CLINICAL_REVIEWER sees real subject IDs
CREATE OR REPLACE MASKING POLICY BIOGEN_CLINICAL_DEMO.SDTM.mask_usubjid
  AS (val VARCHAR) RETURNS VARCHAR ->
  CASE
    WHEN CURRENT_ROLE() IN ('SYSADMIN', 'CLINICAL_REVIEWER') THEN val
    ELSE REGEXP_REPLACE(val, '[0-9]{3}$', 'XXX')  -- mask last 3 digits
  END;

-- Apply masking to AE table
ALTER TABLE SDTM.AE MODIFY COLUMN USUBJID
  SET MASKING POLICY BIOGEN_CLINICAL_DEMO.SDTM.mask_usubjid;

-- Tag clinical columns for lineage tracking
ALTER TABLE SDTM.AE MODIFY COLUMN AENARR
  SET TAG SNOWFLAKE.CORE.PRIVACY_CATEGORY = 'SENSITIVE';

-- Verify masking is active (run as CLINICAL_VIEWER to see masked output)
-- SELECT USUBJID, AEDECOD, AESEV FROM SDTM.AE LIMIT 5;


-- ============================================================
-- ACT 3: CLINICAL ANALYTICS — "PROC FREQ / PROC MEANS equivalent"
-- "Same analyses your SAS programs run — now in SQL"
-- ============================================================

-- 3a. AE Frequency Table by System Organ Class (like PROC FREQ)
--     SAS: PROC FREQ DATA=AE; TABLES AEBODSYS * AESEV; RUN;
SELECT
    AEBODSYS                          AS "System Organ Class",
    AESEV                             AS "Severity",
    COUNT(*)                          AS "N",
    COUNT(DISTINCT USUBJID)           AS "Subjects Affected",
    ROUND(COUNT(*) * 100.0 /
          SUM(COUNT(*)) OVER (), 1)   AS "% of All AEs"
FROM SDTM.AE
GROUP BY 1, 2
ORDER BY 3 DESC;


-- 3b. Serious Adverse Events by Treatment Arm
--     (JOIN AE + DM — no SAS MERGE required)
SELECT
    d.ARM                             AS "Treatment Arm",
    COUNT(*)                          AS "Total SAEs",
    COUNT(DISTINCT a.USUBJID)         AS "Subjects with SAE",
    LISTAGG(DISTINCT a.AEDECOD, '; ')
        WITHIN GROUP (ORDER BY a.AEDECOD) AS "SAE Terms"
FROM SDTM.AE  a
JOIN SDTM.DM  d ON a.USUBJID = d.USUBJID
WHERE a.AESER = 'Y'
GROUP BY 1
ORDER BY 2 DESC;


-- 3c. ALT Flag: Subjects with >3x ULN elevation
--     (Hepatotoxicity signal detection — critical for safety monitoring)
WITH baseline AS (
    SELECT USUBJID, LBSTRESN AS BL_ALT
    FROM SDTM.LB
    WHERE LBTESTCD = 'ALT' AND LBBLFL = 'Y'
),
ontreatment AS (
    SELECT USUBJID, VISITNUM, VISIT, LBSTRESN AS OT_ALT, LBNRHI AS ULN
    FROM SDTM.LB
    WHERE LBTESTCD = 'ALT' AND LBBLFL IS NULL
)
SELECT
    o.USUBJID,
    d.ARM,
    b.BL_ALT    AS "Baseline ALT",
    o.OT_ALT    AS "On-Treatment ALT",
    o.ULN       AS "ULN",
    o.VISIT,
    ROUND(o.OT_ALT / o.ULN, 1) AS "Fold Over ULN",
    CASE
        WHEN o.OT_ALT > 3  * o.ULN THEN '⚠️ >3x ULN'
        WHEN o.OT_ALT > 1.5* o.ULN THEN 'Elevated'
        ELSE 'Normal'
    END AS "Flag"
FROM ontreatment o
JOIN baseline    b ON o.USUBJID = b.USUBJID
JOIN SDTM.DM     d ON o.USUBJID = d.USUBJID
ORDER BY 7 DESC;


-- 3d. Subject disposition summary (like PROC FREQ on ENRFL / COMPLFL)
SELECT
    ARM,
    COUNT(DISTINCT USUBJID)    AS "Enrolled",
    COUNT(CASE WHEN SEX='M' THEN 1 END) AS "Male",
    COUNT(CASE WHEN SEX='F' THEN 1 END) AS "Female",
    ROUND(AVG(AGE), 1)         AS "Mean Age",
    MIN(AGE)                   AS "Min Age",
    MAX(AGE)                   AS "Max Age"
FROM SDTM.DM
GROUP BY ARM
ORDER BY ARM;


-- ============================================================
-- ACT 4: CORTEX AI — "Your first AI function call on clinical data"
-- "No API key. No model deployment. Just SQL."
-- ============================================================

-- 4a. Summarize AE narratives using an LLM
--     Replaces manual medical writing / narrative review
SELECT
    USUBJID,
    AEDECOD,
    AESEV,
    AESER,
    AENARR                                    AS "Original Narrative",
    SNOWFLAKE.CORTEX.COMPLETE(
        'llama3.1-70b',
        CONCAT(
            'You are a clinical data reviewer. Summarize this adverse event narrative ',
            'in one concise clinical sentence (max 30 words), using standard medical terminology. ',
            'Narrative: ', AENARR
        )
    )                                         AS "AI Summary"
FROM SDTM.AE
WHERE AESER = 'Y'    -- Serious AEs only
ORDER BY AESTDTC;


-- 4b. Classify protocol deviations by category
--     Replaces manual coding — consistent, scalable, auditable
SELECT
    USUBJID,
    DVTERM,
    DVTEXT,
    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
        DVTEXT,
        ARRAY_CONSTRUCT(
            'Informed Consent',
            'Eligibility Criteria',
            'Dosing and Administration',
            'Visit Window Deviation',
            'Prohibited Concomitant Medication',
            'Protocol Procedure'
        )
    ):'label'::VARCHAR                        AS "AI Classification",
    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
        DVTEXT,
        ARRAY_CONSTRUCT(
            'Informed Consent',
            'Eligibility Criteria',
            'Dosing and Administration',
            'Visit Window Deviation',
            'Prohibited Concomitant Medication',
            'Protocol Procedure'
        )
    ):'score'::FLOAT                          AS "Confidence Score"
FROM SDTM.DV
ORDER BY "Confidence Score" DESC;


-- 4c. Sentiment/urgency scoring on AE narratives
--     Identify AEs that need urgent medical review
SELECT
    USUBJID,
    AEDECOD,
    AENARR,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-7b',
        CONCAT(
            'Rate the clinical urgency of this adverse event report on a scale of 1 (routine) ',
            'to 5 (immediate action required). Respond with only a JSON object like: ',
            '{"urgency": 3, "reason": "brief reason"}. Report: ',
            AENARR
        )
    )                                         AS "Urgency Assessment"
FROM SDTM.AE
WHERE AESEVN >= 2  -- Moderate or higher
ORDER BY AESEVN DESC;


-- ============================================================
-- ACT 5: CORTEX ANALYST SETUP — Semantic Model foundation
-- "Define once, query in plain English forever"
-- ============================================================

-- Cortex Analyst uses a YAML semantic model — here's the SQL
-- that underpins it. The YAML file defines friendly names,
-- metrics, and relationships so Cortex Analyst can generate SQL
-- from questions like "How many SAEs per arm?"

-- Summary view Cortex Analyst will query
CREATE OR REPLACE VIEW BIOGEN_CLINICAL_DEMO.SDTM.V_CLINICAL_SUMMARY AS
SELECT
    d.STUDYID,
    d.USUBJID,
    d.ARM,
    d.ARMCD,
    d.SITEID,
    d.AGE,
    d.SEX,
    d.RACE,
    COUNT(a.AESEQ)                                      AS TOTAL_AES,
    COUNT(CASE WHEN a.AESER = 'Y' THEN 1 END)           AS SERIOUS_AES,
    COUNT(CASE WHEN a.AESEVN >= 3 THEN 1 END)           AS GRADE3_PLUS_AES,
    COUNT(CASE WHEN a.AEREL = 'RELATED' THEN 1 END)     AS RELATED_AES,
    MAX(a.AESEVN)                                       AS MAX_SEVERITY_GRADE,
    COUNT(DISTINCT a.AEBODSYS)                          AS DISTINCT_SOC_COUNT
FROM SDTM.DM d
LEFT JOIN SDTM.AE a ON d.USUBJID = a.USUBJID
GROUP BY 1,2,3,4,5,6,7,8;

-- Sample queries Cortex Analyst will auto-generate from natural language:

-- "Which arm had the most serious adverse events?"
SELECT ARM, SUM(SERIOUS_AES) AS TOTAL_SAES
FROM V_CLINICAL_SUMMARY
GROUP BY ARM ORDER BY 2 DESC;

-- "Show me all subjects with Grade 3+ adverse events"
SELECT USUBJID, ARM, SITEID, GRADE3_PLUS_AES
FROM V_CLINICAL_SUMMARY
WHERE GRADE3_PLUS_AES > 0
ORDER BY GRADE3_PLUS_AES DESC;

-- "What is the mean age by treatment arm?"
SELECT ARM, ROUND(AVG(AGE),1) AS MEAN_AGE, COUNT(*) AS N
FROM V_CLINICAL_SUMMARY
GROUP BY ARM ORDER BY ARM;


-- ============================================================
-- BONUS: DOCUMENT AI — Process the CSR PDF (READY TO RUN ✅)
-- Stage: BIOGEN_CLINICAL_DEMO.DOCS.CLINICAL_DOCS_STAGE (SSE)
-- File:  STUDY-2024-001_CSR_Final.pdf  (already uploaded)
-- All SQL below is production-tested and ready to demo.
-- ============================================================

-- NOTE: Stage uses SNOWFLAKE_SSE encryption (required for PARSE_DOCUMENT).
-- The stage and file are already deployed. Jump straight to Step B.

-- ── STEP A (already done): Stage + upload ───────────────────
-- CREATE OR REPLACE STAGE BIOGEN_CLINICAL_DEMO.DOCS.CLINICAL_DOCS_STAGE
--   DIRECTORY = (ENABLE = TRUE)
--   ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
-- PUT file:///path/to/STUDY-2024-001_CSR_Final.pdf
--   @BIOGEN_CLINICAL_DEMO.DOCS.CLINICAL_DOCS_STAGE AUTO_COMPRESS=FALSE;

-- ── STEP B: Verify the file is on stage ─────────────────────
ALTER STAGE BIOGEN_CLINICAL_DEMO.DOCS.CLINICAL_DOCS_STAGE REFRESH;
SELECT RELATIVE_PATH, SIZE, LAST_MODIFIED
FROM DIRECTORY(@BIOGEN_CLINICAL_DEMO.DOCS.CLINICAL_DOCS_STAGE);

-- ── STEP C: Parse + chunk + vectorize the CSR (already done) ─
-- CSR_CHUNKS table is pre-built with 13 pages + 768-dim vectors.
-- Run this only if you want to rebuild it from scratch:
/*
CREATE OR REPLACE TABLE BIOGEN_CLINICAL_DEMO.DOCS.CSR_CHUNKS AS
SELECT
    'STUDY-2024-001_CSR_Final.pdf'       AS FILE_NAME,
    g.index + 1                          AS PAGE_NUM,
    g.value:content::VARCHAR             AS CHUNK_TEXT,
    SNOWFLAKE.CORTEX.EMBED_TEXT_768(
        'snowflake-arctic-embed-m',
        g.value:content::VARCHAR
    )                                    AS CHUNK_VECTOR
FROM LATERAL FLATTEN(
    input => SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
        '@BIOGEN_CLINICAL_DEMO.DOCS.CLINICAL_DOCS_STAGE',
        'STUDY-2024-001_CSR_Final.pdf',
        {'mode': 'OCR', 'page_split': TRUE}
    )
) f,
LATERAL FLATTEN(input => f.value) g
WHERE TYPEOF(f.value) = 'ARRAY';
*/

-- ── STEP D: Verify chunks and vectors ───────────────────────
SELECT PAGE_NUM,
       LEN(CHUNK_TEXT)          AS text_len,
       CHUNK_VECTOR IS NOT NULL AS has_vector,
       LEFT(CHUNK_TEXT, 80)     AS preview
FROM BIOGEN_CLINICAL_DEMO.DOCS.CSR_CHUNKS
ORDER BY PAGE_NUM;
-- Expected: 13 rows, all has_vector = TRUE

-- ── STEP E: Semantic search — find most relevant pages ───────
-- "Which pages talk about the primary endpoint result?"
SELECT
    PAGE_NUM,
    VECTOR_COSINE_SIMILARITY(
        CHUNK_VECTOR,
        SNOWFLAKE.CORTEX.EMBED_TEXT_768(
            'snowflake-arctic-embed-m',
            'annualized relapse rate ARR reduction Drug A 20mg placebo p-value result'
        )
    )                          AS RELEVANCE_SCORE,
    LEFT(CHUNK_TEXT, 200)      AS EXCERPT
FROM BIOGEN_CLINICAL_DEMO.DOCS.CSR_CHUNKS
ORDER BY RELEVANCE_SCORE DESC
LIMIT 5;

-- ── STEP F: Full RAG — ask the CSR a question ────────────────
-- "What was the primary endpoint result? Did the study succeed?"
-- THIS IS THE MONEY DEMO QUERY.
WITH question AS (
    SELECT 'annualized relapse rate ARR reduction Drug A 20mg placebo p-value result' AS q
),
top_chunks AS (
    SELECT PAGE_NUM, CHUNK_TEXT
    FROM BIOGEN_CLINICAL_DEMO.DOCS.CSR_CHUNKS, question
    ORDER BY VECTOR_COSINE_SIMILARITY(
        CHUNK_VECTOR,
        SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', q)
    ) DESC
    LIMIT 4
),
context AS (
    SELECT LISTAGG(CHUNK_TEXT, '\n\n---\n\n')
           WITHIN GROUP (ORDER BY PAGE_NUM) AS ctx
    FROM top_chunks
)
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'llama3.1-70b',
    CONCAT(
        'You are a clinical data reviewer. Using only the CSR excerpts below, ',
        'answer this question with specific numbers from the text: ',
        'What was the primary endpoint result for Drug A 20mg vs placebo, ',
        'and did the study meet its primary endpoint?\n\nCSR Excerpts:\n', ctx
    )
) AS ANSWER
FROM context;
-- Expected answer: 52.3% ARR reduction, p=0.0008, study MET primary endpoint.


-- ============================================================
-- ACT 6: CORTEX SEARCH SERVICE — Managed RAG (REPLACES manual vectors)
-- "No more manual EMBED + COSINE_SIMILARITY — Snowflake manages the index"
-- ============================================================

-- The CSR_SEARCH service is already created and indexing.
-- It replaces the manual VECTOR_COSINE_SIMILARITY queries above.

-- CREATE OR REPLACE CORTEX SEARCH SERVICE BIOGEN_CLINICAL_DEMO.DOCS.CSR_SEARCH
--   ON CHUNK_TEXT
--   ATTRIBUTES PAGE_NUM, FILE_NAME
--   WAREHOUSE = CLINICAL_DEMO_WH
--   TARGET_LAG = '1 hour'
-- AS (
--   SELECT FILE_NAME, PAGE_NUM, CHUNK_TEXT
--   FROM BIOGEN_CLINICAL_DEMO.DOCS.CSR_CHUNKS
-- );

-- Query the search service (much simpler than manual vector search):
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'BIOGEN_CLINICAL_DEMO.DOCS.CSR_SEARCH',
    '{
      "query": "What was the primary endpoint result for Drug A 20mg?",
      "columns": ["CHUNK_TEXT", "PAGE_NUM"],
      "limit": 3
    }'
  )
)['results'] AS search_results;


-- ============================================================
-- ACT 7: AI_COMPLETE — Persist AI insights to tables
-- "AI_COMPLETE replaces the legacy SNOWFLAKE.CORTEX.COMPLETE"
-- "Results saved permanently — no re-running LLMs during the demo"
-- ============================================================

-- These tables are already built. Here's the DDL for reference:

-- 7a. AE Narrative Summaries + AI Classification (already populated)
-- CREATE OR REPLACE TABLE BIOGEN_CLINICAL_DEMO.SDTM.AE_AI_SUMMARIES AS
-- SELECT *, AI_COMPLETE('llama3.1-70b', ...) AS AI_SUMMARY, ...
-- FROM BIOGEN_CLINICAL_DEMO.SDTM.AE;

-- View the AI-generated summaries:
SELECT USUBJID, AEDECOD, AESEV, AESER,
       LEFT(AENARR, 80)        AS NARRATIVE_PREVIEW,
       AI_SUMMARY,
       AI_CLASSIFICATION
FROM BIOGEN_CLINICAL_DEMO.SDTM.AE_AI_SUMMARIES
ORDER BY AESEVN DESC;

-- 7b. Protocol Deviation AI Classifications (already populated)
SELECT USUBJID, DVTERM, AI_CATEGORY, AI_IMPACT_RATING,
       LEFT(DVTEXT, 100)       AS DEVIATION_PREVIEW
FROM BIOGEN_CLINICAL_DEMO.SDTM.DV_AI_CLASSIFICATIONS;

-- 7c. AE Urgency Scoring (already populated)
SELECT USUBJID, AEDECOD, AESEV, AI_URGENCY_ASSESSMENT
FROM BIOGEN_CLINICAL_DEMO.SDTM.AE_AI_URGENCY;


-- ============================================================
-- ACT 8: SEMANTIC VIEW — Natural language over structured data
-- "Define your data model ONCE. Query with plain English forever."
-- ============================================================

-- The semantic view is already created. Here's the key DDL:

-- CREATE OR REPLACE SEMANTIC VIEW BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_SV
--   TABLES (demographics, adverse_events, lab_results, ai_summaries, deviation_classifications)
--   RELATIONSHIPS (ae_to_dm, lb_to_dm, ai_to_ae, dv_to_dm)
--   FACTS (severity_grade, result_value, age, ...)
--   DIMENSIONS (treatment_arm, site, ae_term, body_system, severity, ai_category, ...)
--   METRICS (subject_count, total_ae_count, serious_ae_count, grade3_plus_count, ...)

-- Verify it exists:
DESCRIBE SEMANTIC VIEW BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_SV;

-- Show all available metrics:
SHOW SEMANTIC METRICS IN SEMANTIC VIEW BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_SV;

-- Show all dimensions:
SHOW SEMANTIC DIMENSIONS IN SEMANTIC VIEW BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_SV;


-- ============================================================
-- ACT 9: SNOWFLAKE INTELLIGENCE AGENT — The unified chatbot
-- "One agent. Two tools. Search + Analytics. Snowflake Intelligence."
-- ============================================================

-- The agent is already created. Here's the DDL for reference:

-- CREATE OR REPLACE AGENT BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_AGENT
--   FROM SPECIFICATION $$
--   models:
--     orchestration: auto
--   tools:
--     - cortex_analyst (clinical_analytics) → Semantic View
--     - cortex_search (csr_document_search) → CSR Search Service
--   $$

-- Verify the agent exists:
SHOW AGENTS IN SCHEMA BIOGEN_CLINICAL_DEMO.SDTM;

-- Test the agent with a structured data question:
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_AGENT',
    'Which treatment arm had the most serious adverse events and what were they?'
) AS AGENT_RESPONSE;

-- Test the agent with a document search question:
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_AGENT',
    'What did the CSR conclude about the benefit-risk profile of Drug A 20mg?'
) AS AGENT_RESPONSE;

-- Test the agent with a combined question:
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_AGENT',
    'How many subjects had ALT elevations above 3x ULN, and what does the CSR say about hepatic safety monitoring?'
) AS AGENT_RESPONSE;

-- ============================================================
-- 🎯 DEMO TIP: Open Snowflake Intelligence in Snowsight
-- Navigate to: snowsight > Intelligence > Clinical Intelligence Agent
-- The agent is now available for natural language interaction.
-- Ask any question about the clinical trial data OR the CSR document.
-- ============================================================


-- ============================================================
-- CLEANUP (run after demo if needed)
-- ============================================================
-- DROP AGENT IF EXISTS BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_AGENT;
-- DROP SEMANTIC VIEW IF EXISTS BIOGEN_CLINICAL_DEMO.SDTM.CLINICAL_INTELLIGENCE_SV;
-- DROP CORTEX SEARCH SERVICE IF EXISTS BIOGEN_CLINICAL_DEMO.DOCS.CSR_SEARCH;
-- DROP DATABASE IF EXISTS BIOGEN_CLINICAL_DEMO;
-- DROP WAREHOUSE IF EXISTS CLINICAL_DEMO_WH;

-- ============================================================
-- END OF DEMO SCRIPT
-- Questions? bob.leboeuf@snowflake.com | kelci.miclaus@snowflake.com
-- ============================================================

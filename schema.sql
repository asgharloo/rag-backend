-- Extensions
-- ========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- ========================================
-- ENUM Types
-- ========================================
CREATE TYPE user_role AS ENUM ('client', 'specialist', 'admin');
CREATE TYPE gender_type AS ENUM ('male', 'female', 'other');
CREATE TYPE marital_status_type AS ENUM ('single', 'married', 'divorced', 'widowed');
CREATE TYPE session_status AS ENUM ('active', 'ended', 'archived');
CREATE TYPE message_sender AS ENUM ('user', 'assistant', 'system');
CREATE TYPE assessment_status AS ENUM ('pending', 'in_progress', 'completed');
CREATE TYPE specialist_status AS ENUM ('available', 'busy', 'offline');
CREATE TYPE appointment_status AS ENUM ('scheduled', 'completed', 'cancelled', 'no_show');
CREATE TYPE test_type AS ENUM ('multiple_choice', 'scale', 'open_ended');
CREATE TYPE prescription_status AS ENUM ('active', 'completed', 'cancelled');
CREATE TYPE recommendation_type AS ENUM ('exercise', 'meditation', 'reading', 'therapy', 'other');

-- ========================================
-- Trigger Function
-- ========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
	    NEW.updated_at = NOW();
	    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ========================================
-- Users
-- ========================================
CREATE TABLE users (
	    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    email        VARCHAR(255) UNIQUE NOT NULL,
	    password_hash VARCHAR(255) NOT NULL,
	    role         user_role NOT NULL DEFAULT 'client',
	    is_active    BOOLEAN DEFAULT TRUE,
	    is_verified  BOOLEAN DEFAULT FALSE,
	    created_at   TIMESTAMPTZ DEFAULT NOW(),
	    updated_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

	-- ========================================
-- Client Profiles
-- ========================================
CREATE TABLE client_profiles (
	    user_id              UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
	    first_name           VARCHAR(100),
	    last_name            VARCHAR(100),
	    date_of_birth        DATE,
	    gender               gender_type,
	    phone                VARCHAR(20),
	    address              TEXT,
	    emergency_contact_name  VARCHAR(100),
	    emergency_contact_phone VARCHAR(20),
	    marital_status       marital_status_type,
	    occupation           VARCHAR(100),
	    education_level      VARCHAR(50),
	    created_at           TIMESTAMPTZ DEFAULT NOW(),
	    updated_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER trg_client_profiles_updated_at
    BEFORE UPDATE ON client_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

	-- ========================================
-- Client Clinical Profiles (AI-managed)
-- ========================================
CREATE TABLE client_clinical_profiles (
	    user_id         UUID PRIMARY KEY REFERENCES client_profiles(user_id) ON DELETE CASCADE,
	    key_events      JSONB DEFAULT '[]',
	    diagnoses       JSONB DEFAULT '[]',
	    medications     JSONB DEFAULT '[]',
	    goals           JSONB DEFAULT '[]',
	    triggers        JSONB DEFAULT '[]',
	    raw_profile     TEXT,
	    last_updated_by VARCHAR(50),
	    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER trg_client_clinical_profiles_updated_at
    BEFORE UPDATE ON client_clinical_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

	-- ========================================
-- Chat Sessions & Messages
-- ========================================
CREATE TABLE chat_sessions (
	    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	    title      VARCHAR(255),
	    status     session_status DEFAULT 'active',
	    started_at TIMESTAMPTZ DEFAULT NOW(),
	    ended_at   TIMESTAMPTZ,
	    created_at TIMESTAMPTZ DEFAULT NOW(),
	    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER trg_chat_sessions_updated_at
    BEFORE UPDATE ON chat_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

	CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id);

	CREATE TABLE chat_messages (
		    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		    session_id  UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
		    sender      message_sender NOT NULL,
		    content     TEXT NOT NULL,
		    token_count INT,
		    metadata    JSONB DEFAULT '{}',
		    created_at  TIMESTAMPTZ DEFAULT NOW()
	);

	CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);

	-- ========================================
-- Memory System
-- ========================================
CREATE TABLE session_summaries (
	    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    session_id      UUID NOT NULL UNIQUE REFERENCES chat_sessions(id) ON DELETE CASCADE,
	    user_id         UUID NOT NULL REFERENCES client_profiles(user_id) ON DELETE CASCADE,
	    summary_text    TEXT NOT NULL,
	    key_topics      JSONB DEFAULT '[]',
	    emotional_state VARCHAR(100),
	    token_count     INT,
	    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_session_summaries_user    ON session_summaries(user_id);
CREATE INDEX idx_session_summaries_session ON session_summaries(session_id);

CREATE TABLE memory_vectors (
	    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    user_id     UUID NOT NULL REFERENCES client_profiles(user_id) ON DELETE CASCADE,
	    session_id  UUID REFERENCES chat_sessions(id) ON DELETE SET NULL,
	    source_type VARCHAR(50) NOT NULL,  -- 'message', 'summary', 'clinical_note'
	    source_id   UUID,
	    content     TEXT NOT NULL,
	    embedding   vector(1536),
	    metadata    JSONB DEFAULT '{}',
	    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_memory_vectors_embedding
    ON memory_vectors
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX idx_memory_vectors_user ON memory_vectors(user_id);

CREATE TABLE memory_retrieval_logs (
	    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    session_id        UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
	    message_id        UUID REFERENCES chat_messages(id) ON DELETE SET NULL,
	    query_text        TEXT,
	    retrieved_ids     UUID[],
	    similarity_scores FLOAT[],
	    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ========================================
-- Assessments
-- ========================================
CREATE TABLE assessment_categories (
	    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    name        VARCHAR(100) UNIQUE NOT NULL,
	    description TEXT,
	    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE client_assessments (
	    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	    category_id     UUID REFERENCES assessment_categories(id) ON DELETE SET NULL,
	    assessment_data JSONB NOT NULL,
	    ai_analysis     TEXT,
	    status          assessment_status DEFAULT 'pending',
	    created_at      TIMESTAMPTZ DEFAULT NOW(),
	    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER trg_client_assessments_updated_at
    BEFORE UPDATE ON client_assessments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

	CREATE TABLE assessment_services (
		    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		    assessment_id  UUID NOT NULL REFERENCES client_assessments(id) ON DELETE CASCADE,
		    service_name   VARCHAR(100) NOT NULL,
		    service_type   VARCHAR(50),
		    api_endpoint   VARCHAR(255),
		    request_data   JSONB,
		    response_data  JSONB,
		    status         VARCHAR(50),
		    created_at     TIMESTAMPTZ DEFAULT NOW()
	);

	-- ========================================
-- Specialists & Appointments
-- ========================================
CREATE TABLE specialist_profiles (
	    user_id          UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
	    first_name       VARCHAR(100) NOT NULL,
	    last_name        VARCHAR(100) NOT NULL,
	    specialization   VARCHAR(100) NOT NULL,
	    license_number   VARCHAR(50) UNIQUE,
	    bio              TEXT,
	    experience_years INT,
	    education        TEXT,
	    certifications   TEXT[],
	    languages        TEXT[],
	    consultation_fee DECIMAL(10,2),
	    status           specialist_status DEFAULT 'available',
	    rating           DECIMAL(3,2) DEFAULT 0.00,
	    total_sessions   INT DEFAULT 0,
	    created_at       TIMESTAMPTZ DEFAULT NOW(),
	    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER trg_specialist_profiles_updated_at
    BEFORE UPDATE ON specialist_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

	CREATE TABLE appointments (
		    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		    client_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
		    specialist_id       UUID NOT NULL REFERENCES specialist_profiles(user_id) ON DELETE CASCADE,
		    scheduled_at        TIMESTAMPTZ NOT NULL,
		    duration_minutes    INT DEFAULT 60,
		    status              appointment_status DEFAULT 'scheduled',
		    notes               TEXT,
		    cancellation_reason TEXT,
		    created_at          TIMESTAMPTZ DEFAULT NOW(),
		    updated_at          TIMESTAMPTZ DEFAULT NOW()
	);

	CREATE TRIGGER trg_appointments_updated_at
	    BEFORE UPDATE ON appointments
	    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

		-- ========================================
-- Tests
-- ========================================
CREATE TABLE tests (
	    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    title            VARCHAR(255) NOT NULL,
	    description      TEXT,
	    category_id      UUID REFERENCES assessment_categories(id) ON DELETE SET NULL,
	    duration_minutes INT,
	    passing_score    INT,
	    is_active        BOOLEAN DEFAULT TRUE,
	    created_at       TIMESTAMPTZ DEFAULT NOW(),
	    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER trg_tests_updated_at
    BEFORE UPDATE ON tests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

	CREATE TABLE test_questions (
		    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		    test_id       UUID NOT NULL REFERENCES tests(id) ON DELETE CASCADE,
		    question_text TEXT NOT NULL,
		    question_type test_type NOT NULL,
		    question_order INT,
		    points        INT DEFAULT 1,
		    created_at    TIMESTAMPTZ DEFAULT NOW()
	);

	CREATE TABLE test_options (
		    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		    question_id  UUID NOT NULL REFERENCES test_questions(id) ON DELETE CASCADE,
		    option_text  TEXT NOT NULL,
		    option_order INT,
		    is_correct   BOOLEAN DEFAULT FALSE,
		    points       INT DEFAULT 0
	);

	CREATE TABLE test_results (
		    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		    user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
		    test_id      UUID NOT NULL REFERENCES tests(id) ON DELETE CASCADE,
		    score        INT,
		    max_score    INT,
		    percentage   DECIMAL(5,2),
		    answers      JSONB,
		    started_at   TIMESTAMPTZ,
		    completed_at TIMESTAMPTZ,
		    created_at   TIMESTAMPTZ DEFAULT NOW()
	);

	-- ========================================
-- Prescriptions & Recommendations
-- ========================================
CREATE TABLE prescriptions (
	    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	    client_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	    specialist_id    UUID REFERENCES specialist_profiles(user_id) ON DELETE SET NULL,
	    medication_name  VARCHAR(255) NOT NULL,
	    dosage           VARCHAR(100),
	    frequency        VARCHAR(100),
	    duration         VARCHAR(100),
	    instructions     TEXT,
	    status           prescription_status DEFAULT 'active',
	    prescribed_at    TIMESTAMPTZ DEFAULT NOW(),
	    created_at       TIMESTAMPTZ DEFAULT NOW(),
	    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER trg_prescriptions_updated_at
    BEFORE UPDATE ON prescriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

	CREATE TABLE recommendations (
		    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
		    recommendation_type recommendation_type NOT NULL,
		    title               VARCHAR(255) NOT NULL,
		    description         TEXT,
		    priority            INT DEFAULT 1,
		    is_completed        BOOLEAN DEFAULT FALSE,
		    created_at          TIMESTAMPTZ DEFAULT NOW(),
		    updated_at          TIMESTAMPTZ DEFAULT NOW()
	);

	CREATE TRIGGER trg_recommendations_updated_at
	    BEFORE UPDATE ON recommendations
	    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


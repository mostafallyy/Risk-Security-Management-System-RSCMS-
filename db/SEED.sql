-- =========================
-- USERS
-- =========================
INSERT INTO users (name, email, role)
VALUES
('Alice Chen', 'alice@company.com', 'Security Analyst'),
('Bob Smith', 'bob@company.com', 'IT Admin'),
('Dana White', 'dana@company.com', 'Auditor')
ON CONFLICT (email) DO NOTHING;

-- =========================
-- RISKS
-- =========================
INSERT INTO risks (title, description, likelihood, impact, owner_id)
VALUES
(
  'Phishing Attacks',
  'Employees may click malicious emails',
  4,
  4,
  (SELECT id FROM users WHERE email = 'alice@company.com')
),
(
  'Weak Passwords',
  'Password reuse across systems',
  3,
  4,
  (SELECT id FROM users WHERE email = 'alice@company.com')
),
(
  'Backup Failure',
  'Backups may fail during ransomware attack',
  2,
  5,
  (SELECT id FROM users WHERE email = 'bob@company.com')
);

-- =========================
-- CONTROLS
-- =========================
INSERT INTO controls (code, title, description, status)
VALUES
(
  'A.9.2.1',
  'Multi-Factor Authentication',
  'Require MFA for all users',
  'Implemented'
),
(
  'A.12.3.1',
  'Password Policy',
  'Enforce strong passwords and rotation',
  'Planned'
),
(
  'A.12.4.1',
  'Centralized Logging',
  'Collect and monitor system logs',
  'Implemented'
)
ON CONFLICT DO NOTHING;

-- =========================
-- RISK ↔ CONTROL
-- =========================
INSERT INTO risk_controls (risk_id, control_id)
SELECT r.id, c.id
FROM risks r, controls c
WHERE r.title = 'Phishing Attacks'
  AND c.code = 'A.9.2.1'
ON CONFLICT DO NOTHING;

INSERT INTO risk_controls (risk_id, control_id)
SELECT r.id, c.id
FROM risks r, controls c
WHERE r.title = 'Weak Passwords'
  AND c.code = 'A.12.3.1'
ON CONFLICT DO NOTHING;

INSERT INTO risk_controls (risk_id, control_id)
SELECT r.id, c.id
FROM risks r, controls c
WHERE r.title = 'Backup Failure'
  AND c.code = 'A.12.4.1'
ON CONFLICT DO NOTHING;

-- =========================
-- INCIDENTS
-- =========================
INSERT INTO incidents (title, description, severity)
VALUES
(
  'Phishing Email Clicked',
  'Employee clicked a malicious email link',
  'High'
),
(
  'Backup Job Failed',
  'Nightly backup job did not complete',
  'Medium'
);

-- =========================
-- INCIDENT ↔ RISK
-- =========================
INSERT INTO incident_risks (incident_id, risk_id)
SELECT i.id, r.id
FROM incidents i, risks r
WHERE i.title = 'Phishing Email Clicked'
  AND r.title = 'Phishing Attacks'
ON CONFLICT DO NOTHING;

INSERT INTO incident_risks (incident_id, risk_id)
SELECT i.id, r.id
FROM incidents i, risks r
WHERE i.title = 'Backup Job Failed'
  AND r.title = 'Backup Failure'
ON CONFLICT DO NOTHING;

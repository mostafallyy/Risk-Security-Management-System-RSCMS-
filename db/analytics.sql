--MTTR BY SEVERITY--
SELECT
  severity,
  ROUND(
    AVG(EXTRACT(EPOCH FROM (closed_at - detected_at)) / 3600),
    2
  ) AS avg_mttr_hours
FROM incidents
WHERE closed_at IS NOT NULL
GROUP BY severity;
--AVERAGE BY MTTR--
SELECT
  ROUND(
    AVG(EXTRACT(EPOCH FROM (closed_at - detected_at)) / 3600),
    2
  ) AS avg_mttr_hours
FROM incidents
WHERE closed_at IS NOT NULL;
-- MTTD by Severity
SELECT
  severity,
  ROUND(
    AVG(EXTRACT(EPOCH FROM (detected_at - occurred_at)) / 3600),
    2
  ) AS avg_mttd_hours
FROM incidents
GROUP BY severity;
-- MTTD (Average)
SELECT
  ROUND(
    AVG(EXTRACT(EPOCH FROM (detected_at - occurred_at)) / 3600),
    2
  ) AS avg_mttd_hours
FROM incidents;

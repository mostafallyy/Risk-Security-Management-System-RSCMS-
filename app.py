from flask import Flask, jsonify
from flask import Flask, jsonify, request

import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="rscms",
        user="postgres",
        password="M.a20005",
        host="localhost",
        port=5432
    )

@app.route("/incidents", methods=["GET"])
def get_incidents():
    severity = request.args.get("severity")
    state = request.args.get("state")

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT id, title, severity, state, occurred_at, detected_at, closed_at
        FROM incidents
        WHERE 1=1
    """
    params = []

    if severity:
        query += " AND severity = %s"
        params.append(severity)

    if state:
        query += " AND state = %s"
        params.append(state)

    cur.execute(query, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    incidents = []
    for row in rows:
        incidents.append({
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "state": row[3],
            "occurred_at": str(row[4]),
            "detected_at": str(row[5]),
            "closed_at": str(row[6]) if row[6] else None
        })

    return jsonify(incidents)

@app.route("/incidents/<int:incident_id>", methods=["GET"])
def get_incident_by_id(incident_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, state, occurred_at, detected_at, closed_at
        FROM incidents
        WHERE id = %s;
    """, (incident_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "Incident not found"}), 404

    incident = {
        "id": row[0],
        "title": row[1],
        "severity": row[2],
        "state": row[3],
        "occurred_at": str(row[4]),
        "detected_at": str(row[5]),
        "closed_at": str(row[6]) if row[6] else None
    }

    return jsonify(incident)
@app.route("/analytics/incidents/count", methods=["GET"])
def get_incident_count():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM incidents;")
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({"total_incidents": count})
@app.route("/analytics/incidents/by-state", methods=["GET"])
def incidents_by_state():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT state, COUNT(*)
        FROM incidents
        GROUP BY state;
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"state": row[0], "count": row[1]}
        for row in rows
    ])
@app.route("/analytics/incidents/trend", methods=["GET"])
def incident_trend():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DATE(detected_at) AS day, COUNT(*)
        FROM incidents
        GROUP BY day
        ORDER BY day;
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"date": str(row[0]), "count": row[1]}
        for row in rows
    ])
@app.route("/analytics/incidents/trend", methods=["GET"])
def incident_trend_daily():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            DATE(detected_at) AS day,
            COUNT(*) AS incident_count
        FROM incidents
        WHERE detected_at IS NOT NULL
        GROUP BY day
        ORDER BY day;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    trend = []
    for row in rows:
        trend.append({
            "date": str(row[0]),
            "count": row[1]
        })

    return jsonify(trend)
@app.route("/analytics/mttd", methods=["GET"])
def get_mttd():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            ROUND(
                AVG(EXTRACT(EPOCH FROM (detected_at - occurred_at)) / 3600),
                2
            )
        FROM incidents
        WHERE detected_at IS NOT NULL
          AND occurred_at IS NOT NULL;
    """)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "avg_mttd_hours": result[0]
    })
@app.route("/analytics/mttr", methods=["GET"])
def get_mttr():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            ROUND(
                AVG(EXTRACT(EPOCH FROM (closed_at - detected_at)) / 3600),
                2
            )
        FROM incidents
        WHERE closed_at IS NOT NULL
          AND detected_at IS NOT NULL;
    """)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "avg_mttr_hours": result[0]
    })

@app.route("/analytics/incidents/by-severity", methods=["GET"])
def incidents_by_severity():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT severity, COUNT(*)
        FROM incidents
        GROUP BY severity;
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"severity": row[0], "count": row[1]}
        for row in rows
    ])

@app.route("/incidents", methods=["POST"])
def create_incident():
    data = request.get_json()

    title = data.get("title")
    severity = data.get("severity")
    occurred_at = data.get("occurred_at")

    if not title or not severity or not occurred_at:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO incidents (title, severity, state, occurred_at, detected_at)
        VALUES (%s, %s, 'Detected', %s, NOW())
        RETURNING id;
    """, (title, severity, occurred_at))

    incident_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Incident created",
        "incident_id": incident_id
    }), 201

@app.route("/")
def health():
    return jsonify({"status": "RSCMS API running"})



if __name__ == "__main__":
    app.run(debug=True)

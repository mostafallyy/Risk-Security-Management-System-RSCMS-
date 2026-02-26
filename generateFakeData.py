import random
from datetime import timedelta
from faker import Faker
import psycopg2

fake = Faker()

SEVERITIES = ["Low", "Medium", "High", "Critical"]
STATES = ["Detected", "Contained", "Recovered", "Closed"]

conn = psycopg2.connect(
    host="localhost",
    database="rscms",
    user="postgres",
    password="M.a20005"
)
conn.autocommit = True
cur = conn.cursor()

NUM_INCIDENTS = 5000

for _ in range(NUM_INCIDENTS):
    occurred_at = fake.date_time_between(start_date="-90d", end_date="-1d")
    detected_at = occurred_at + timedelta(hours=random.randint(1, 48))

    # 70% of incidents are closed
    if random.random() < 0.7:
        closed_at = detected_at + timedelta(hours=random.randint(1, 72))
        state = "Closed"
    else:
        closed_at = None
        state = random.choice(STATES[:-1])

    cur.execute("""
        INSERT INTO incidents (
            title,
            description,
            severity,
            state,
            occurred_at,
            detected_at,
            closed_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        fake.sentence(),
        fake.text(),
        random.choice(SEVERITIES),
        state,
        occurred_at,
        detected_at,
        closed_at
    ))

conn.commit()
cur.close()
conn.close()

print("✅ Fake incidents generated")

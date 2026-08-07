# DB Connection Refused Reproduction

## Goal

Capture a real `DB connection failed` case where the application can resolve the `db` host but PostgreSQL refuses the TCP connection.

This is different from a host resolution failure such as:

```text
could not translate host name "db" to address
```

The target error for this note is:

```text
connection to server at "db" (...), port 5432 failed: Connection refused
```

## Why this matters

For an interview task or operations demo, `Connection refused` communicates a clearer "database connection outage" story than a DNS-style host resolution error.

- Host resolution failure: the app cannot find the `db` host on the network.
- Connection refused: the app finds the host, reaches the IP, and the port is not accepting the connection.

## Reproduction summary

The original `ops-monitor-db` container was already stopped, so the app naturally produced a host lookup failure.

To reproduce `Connection refused` instead:

1. Keep the real database container stopped.
2. Start a temporary dummy container on `ops-monitor_default`.
3. Give the dummy container the network alias `db`.
4. Do not run PostgreSQL inside that dummy container.
5. Wait for the app's next DB health-check cycle.

This leaves the `db` hostname resolvable, but no process is listening on port `5432`.

## Command used for the repro

```text
docker run -d --rm --name ops-monitor-db-dummy --network ops-monitor_default --network-alias db --entrypoint sh postgres:16 -c "sleep 300"
```

After the real log was captured, the temporary container was removed:

```text
docker stop ops-monitor-db-dummy
```

## Captured result

The application produced the expected real log lines:

```text
ERROR:    Database connection failed
psycopg2.OperationalError: connection to server at "db" (172.18.0.2), port 5432 failed: Connection refused
Is the server running on that host and accepting TCP/IP connections?
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "db" (172.18.0.2), port 5432 failed: Connection refused
```

Artifacts saved in `docs/`:

- `db-error-log-capture-refused.png`
- `db-error-log-capture-refused.txt`

## Practical takeaway

If the goal is to demonstrate a "DB connection outage" in a dashboard, report, or interview task:

- Use host resolution errors when you want to show Docker/network naming problems.
- Use `Connection refused` when you want to show that the DB endpoint exists but is not accepting connections.

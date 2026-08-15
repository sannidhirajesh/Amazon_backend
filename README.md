# amazon_backend_fixed

A ready-to-run educational Amazon-inspired FastAPI backend.

## Start
From this folder run:

```powershell
docker compose down -v
docker compose up --build
```

Then open **http://localhost:8000/docs**

The database and demo data initialize automatically. No Alembic command or manual seed command is required for this Docker version.

Demo seller:
`seller@example.com` / `Seller@12345`

Demo admin:
`admin@example.com` / `Admin@12345`

Customer registration is available at `POST /api/v1/auth/register`.

The `userrole`, `orderstatus`, and `paymentstatus` PostgreSQL ENUM types are created safely and are not recreated by SQLAlchemy, preventing the previous `DuplicateObject` error.

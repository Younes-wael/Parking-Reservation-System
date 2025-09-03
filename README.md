# Parking Reservation System

This repository contains a minimal example of a LAN-only parking reservation system. It includes a .NET 8 backend and a React 18 frontend.

## Backend

The backend is a .NET 8 Minimal API located in `backend/`. It uses EF Core with an in-memory database for demo purposes. To run:

```bash
cd backend
# restore packages
# dotnet restore
# run the API
# dotnet run
```

It exposes the following minimal endpoints:

- `GET /api/availability?start=YYYY-MM-DD&end=YYYY-MM-DD` – returns per-day availability
- `POST /api/reservations` – creates a reservation when capacity is available

Unit tests are located under `backend/Tests` and can be executed with `dotnet test`.

## Frontend

The frontend resides in `frontend/` and was bootstrapped with Vite + React + TypeScript. To develop:

```bash
cd frontend
npm install
npm run dev
```

Run frontend unit tests with:

```bash
npm test
```

## Database backup

For SQL Server Express deployments, a simple PowerShell snippet can be used to perform nightly backups:

```powershell
$timestamp = Get-Date -Format yyyyMMdd_HHmm
Backup-SqlDatabase -ServerInstance .\SQLEXPRESS -Database Parking -BackupFile "C:\Backups\Parking_$timestamp.bak"
```

This example repository is meant as a starting point and does not implement all production features.

# Database Migration Guide

## Setup

1. **Install dependencies** (jika belum):
```bash
pip install alembic sqlalchemy-utils
```

2. **Setup environment**:
```bash
cp .env.example .env
# Edit .env file dengan konfigurasi database PostgreSQL Anda
```

## Commands

### Menggunakan Makefile (Recommended)

```bash
# Lihat semua command yang tersedia
make help

# Generate migration baru
make generate-migration MESSAGE="add new table"

# Generate dan run migration sekaligus
make generate-and-run MESSAGE="add new table"

# Run migration yang sudah ada
make migrate

# Fresh migration (drop semua tabel dan recreate)
make migrate-fresh

# Cek status migration
make status

# Rollback ke migration sebelumnya
make rollback

# Rollback ke revision tertentu
make rollback-to REVISION="abc123"
```

### Menggunakan Script Langsung

```bash
# Generate migration
python generate_migration.py --message "add new table"

# Generate dan run sekaligus
python generate_migration.py --message "add new table" --run

# Run migration saja
python generate_migration.py --run

# Fresh migration
python migrate_fresh.py
```

### Menggunakan Alembic Langsung

```bash
# Generate migration
alembic revision --autogenerate -m "add new table"

# Run migration
alembic upgrade head

# Cek status
alembic current
alembic history

# Rollback
alembic downgrade -1
```

## Environment Variables

Pastikan file `.env` Anda berisi:

```env
URL_DATABASE=postgresql://username:password@localhost:5432/database_name
```

## Models

Migration akan otomatis mendeteksi perubahan pada model-model berikut:

- `ApiKey` - untuk manajemen API key
- `PersonDuration` - untuk data durasi person
- `DetailPersonDuration` - untuk detail durasi person

## Troubleshooting

1. **Error "No such file or directory"**: Pastikan semua dependencies terinstall
2. **Error database connection**: Cek konfigurasi `URL_DATABASE` di file `.env`
3. **Error import models**: Pastikan struktur folder dan import path sudah benar

## Tips

- Selalu backup database sebelum melakukan `migrate-fresh`
- Gunakan message yang deskriptif saat generate migration
- Test migration di environment development dulu sebelum production 
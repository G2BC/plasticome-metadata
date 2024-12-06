#!/bin/bash
set -e

echo "Esperando o PostgreSQL iniciar..."
sleep 5

apt-get update && apt-get install -y lzop

if [ -f /dump/plasticome-psql-v1.sql.lzo ]; then
    echo "Descompactando o dump..."
    lzop -d /dump/plasticome-psql-v1.sql.lzo -c > /dump/plasticome-psql-v1.sql
    echo "Restaurando o banco de dados a partir do dump..."
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /dump/plasticome-psql-v1.sql
    echo "Restauração do banco de dados concluída!"
    python create_user.py

else
    echo "Dump não encontrado em /dump/plasticome-psql-v1.sql.lzo"
fi

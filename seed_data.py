import os
import random
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import sql
from faker import Faker
from dotenv import load_dotenv

# ==========================================
# Configurações
# ==========================================
load_dotenv()
fake = Faker('pt_BR')

DB = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS")
}

N = 50  # registros por tabela


def connect():
    return psycopg2.connect(**DB)


# ==========================================
# Funções auxiliares para gerar dados fake
# ==========================================
def gen_coords():
    return round(random.uniform(-30.0, -2.0), 6), round(random.uniform(-60.0, -35.0), 6)

def gen_time_range():
    inicio = datetime.now() - timedelta(days=random.randint(0, 365))
    fim = inicio + timedelta(hours=random.randint(1, 6))
    return inicio, fim


# ==========================================
# Populando tabelas
# ==========================================
def seed_database():
    conn = connect()
    cur = conn.cursor()

    print("🧩 Limpando dados anteriores (truncate cascade)...")
    cur.execute("""
        DO $$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'middleware_oab') LOOP
                EXECUTE 'TRUNCATE TABLE middleware_oab.' || quote_ident(r.tablename) || ' CASCADE;';
            END LOOP;
        END$$;
    """)
    conn.commit()

    inserted = {}

    # 1️⃣ Cadastro
    print("Inserindo Cadastro...")
    cur.execute("SET search_path TO middleware_oab;")
    cur.execute("TRUNCATE TABLE cadastro RESTART IDENTITY CASCADE;")
    for _ in range(N):
        cur.execute("""
            INSERT INTO Cadastro (nome, email, telefone, cpf, rg, endereco, data_cadastro)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING cadastro_id;
        """, (
            fake.name(),
            fake.unique.email(),
            fake.phone_number(),
            fake.unique.cpf(),
            fake.rg(),
            fake.address(),
            fake.date_time_this_year()
        ))
        inserted.setdefault("Cadastro", []).append(cur.fetchone()[0])
    conn.commit()

    # 2️⃣ Usuario_advogado
    print("Inserindo Usuario_advogado...")
    for _ in range(N):
        cur.execute("""
            INSERT INTO Usuario_advogado (registro_oab, codigo_de_seguranca, adimplencia_oab, cadastro_id)
            VALUES (%s,%s,%s,%s)
            RETURNING usuario_id;
        """, (
            f"OAB-{random.randint(10000, 99999)}",
            fake.password(length=10),
            random.choice([True, False]),
            random.choice(inserted["Cadastro"])
        ))
        inserted.setdefault("Usuario_advogado", []).append(cur.fetchone()[0])
    conn.commit()

    # 3️⃣ Analista_de_ti
    print("Inserindo Analista_de_ti...")
    for _ in range(N):
        cur.execute("""
            INSERT INTO Analista_de_ti (usuario, senha, cadastro_id)
            VALUES (%s,%s,%s)
            RETURNING analista_id;
        """, (
            fake.unique.user_name(),
            fake.password(length=12),
            random.choice(inserted["Cadastro"])
        ))
        inserted.setdefault("Analista_de_ti", []).append(cur.fetchone()[0])
    conn.commit()

    # 4️⃣ Administrador_sala_coworking
    print("Inserindo Administrador_sala_coworking...")
    for _ in range(N):
        cur.execute("""
            INSERT INTO Administrador_sala_coworking (usuario, senha, adm_local, admin_central, cadastro_id)
            VALUES (%s,%s,%s,%s,%s)
            RETURNING admin_id;
        """, (
            fake.unique.user_name(),
            fake.password(length=12),
            random.choice([True, False]),
            random.choice([True, False]),
            random.choice(inserted["Cadastro"])
        ))
        inserted.setdefault("Administrador_sala_coworking", []).append(cur.fetchone()[0])
    conn.commit()

    # 5️⃣ Subsecional
    print("Inserindo Subsecional...")
    for _ in range(N):
        cur.execute("""
            INSERT INTO Subsecional (nome)
            VALUES (%s)
            RETURNING subsecional_id;
        """, (f"Subsecional {fake.city()}",))
        inserted.setdefault("Subsecional", []).append(cur.fetchone()[0])
    conn.commit()

    # 6️⃣ Unidade
    print("Inserindo Unidade...")
    for _ in range(N):
        lat, lon = gen_coords()
        cur.execute("""
            INSERT INTO Unidade (nome, hierarquia, endereco, latitude, longitude, subsecional_id)
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING unidade_id;
        """, (
            f"Unidade {fake.city()}",
            random.choice(["SEDE", "FILIAL"]),
            fake.address(),
            lat, lon,
            random.choice(inserted["Subsecional"])
        ))
        inserted.setdefault("Unidade", []).append(cur.fetchone()[0])
    conn.commit()

    # 7️⃣ Sala_coworking
    print("Inserindo Sala_coworking...")
    for _ in range(N):
        cur.execute("""
            INSERT INTO Sala_coworking (nome_da_sala, subsecional_id, unidade_id, administrador_id)
            VALUES (%s,%s,%s,%s)
            RETURNING coworking_id;
        """, (
            f"Sala {fake.word()}",
            random.choice(inserted["Subsecional"]),
            random.choice(inserted["Unidade"]),
            random.choice(inserted["Administrador_sala_coworking"])
        ))
        inserted.setdefault("Sala_coworking", []).append(cur.fetchone()[0])
    conn.commit()

    # 8️⃣ Computador
    print("Inserindo Computador...")
    for _ in range(N):
        cur.execute("""
            INSERT INTO Computador (ip_da_maquina, numero_de_tombamento, coworking_id)
            VALUES (%s,%s,%s)
            RETURNING computador_id;
        """, (
            fake.unique.ipv4(),
            f"TOMB-{random.randint(1000,9999)}",
            random.choice(inserted["Sala_coworking"])
        ))
        inserted.setdefault("Computador", []).append(cur.fetchone()[0])
    conn.commit()

    # 9️⃣ Sessao
    print("Inserindo Sessao...")
    for _ in range(N):
        inicio, fim = gen_time_range()
        cur.execute("""
            INSERT INTO Sessao (data, inicio_de_sessao, final_de_sessao, ativado, computador_id, usuario_id, administrador_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING sessao_id;
        """, (
            inicio.date(),
            inicio,
            fim,
            random.choice([True, False]),
            random.choice(inserted["Computador"]),
            random.choice(inserted["Usuario_advogado"]),
            random.choice(inserted["Administrador_sala_coworking"])
        ))
        inserted.setdefault("Sessao", []).append(cur.fetchone()[0])
    conn.commit()

    # 🔟 Sessoes_analistas
    print("Inserindo Sessoes_analistas...")
    for _ in range(N):
        cur.execute("""
            INSERT INTO Sessoes_analistas (analista_id, sessao_id)
            VALUES (%s,%s)
            ON CONFLICT DO NOTHING;
        """, (
            random.choice(inserted["Analista_de_ti"]),
            random.choice(inserted["Sessao"])
        ))
    conn.commit()

    print("✅ Banco populado com sucesso!")
    cur.close()
    conn.close()


if __name__ == "__main__":
    seed_database()

import os
import random
import psycopg2
from faker import Faker
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

print("🔍 Variáveis carregadas:")
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))


# Configuração de conexão com o banco
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()
fake = Faker("pt_BR")

print("Setting search_path to middleware_oab and truncating tables...")

cursor.execute("SET search_path TO middleware_oab;")

# Limpa tabelas antes de popular
tables = [
    "Sessoes_analistas", "Sessao", "Computador", "Sala_coworking",
    "Unidade", "Subsecional", "Administrador_sala_coworking",
    "Analista_de_ti", "Usuario_advogado", "Cadastro"
]
for table in tables:
    cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")

conn.commit()

# Função auxiliar para gerar telefone válido
def gerar_telefone():
    tel = fake.phone_number()
    return tel[:15]  # garante que não passa de 15 caracteres

# Popula Cadastro
print("Populando tabela Cadastro...")
cadastros = []
for _ in range(50):
    nome = fake.name()
    email = fake.unique.email()
    telefone = gerar_telefone()
    cpf = fake.cpf()
    rg = fake.rg()
    endereco = fake.address().replace("\n", ", ")
    cursor.execute("""
        INSERT INTO Cadastro (nome, email, telefone, cpf, rg, endereco)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING cadastro_id;
    """, (nome, email, telefone, cpf, rg, endereco))
    cadastro_id = cursor.fetchone()[0]
    cadastros.append(cadastro_id)

conn.commit()

# Popula Usuario_advogado
print("Populando tabela Usuario_advogado...")

# Garante unicidade nos registros OAB
registro_oabs = set()
while len(registro_oabs) < 50:
    registro_oabs.add(f"OAB-{fake.random_int(min=1000, max=9999)}")

for registro_oab in registro_oabs:
    codigo_de_seguranca = fake.random_int(min=10000, max=99999)
    cadastro_id = random.randint(1, 50)
    cursor.execute("""
        INSERT INTO Usuario_advogado (registro_oab, codigo_de_seguranca, adimplencia_oab, cadastro_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (registro_oab) DO NOTHING;
    """, (registro_oab, codigo_de_seguranca, True, cadastro_id))

# Popula Analista_de_ti
print("Populando tabela Analista_de_ti...")
for i in range(50):
    usuario = fake.user_name()
    senha = fake.password(length=10)
    cadastro_id = random.choice(cadastros)
    cursor.execute("""
        INSERT INTO Analista_de_ti (usuario, senha, cadastro_id)
        VALUES (%s, %s, %s);
    """, (usuario, senha, cadastro_id))

# Popula Administrador_sala_coworking
print("Populando tabela Administrador_sala_coworking...")
admins = []
for i in range(50):
    usuario = fake.user_name()
    senha = fake.password(length=10)
    adm_local = fake.boolean()
    admin_central = fake.boolean()
    cadastro_id = random.choice(cadastros)
    cursor.execute("""
        INSERT INTO Administrador_sala_coworking (usuario, senha, adm_local, admin_central, cadastro_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING admin_id;
    """, (usuario, senha, adm_local, admin_central, cadastro_id))
    admins.append(cursor.fetchone()[0])

# Popula Subsecional
print("Populando tabela Subsecional...")
subsecoes = []  # lista para guardar os IDs, não os nomes
for _ in range(10):
    nome = f"Subseção {fake.last_name()}"
    cursor.execute("""
        INSERT INTO Subsecional (nome)
        VALUES (%s)
        RETURNING subsecional_id;
    """, (nome,))
    subsecional_id = cursor.fetchone()[0]
    subsecoes.append(subsecional_id)

# ==============================
# 6️⃣ Populando Unidade
# ==============================
print("Populando tabela Unidade...")
for _ in range(50):
    nome = f"Unidade {fake.city()}"
    hierarquia = random.choice(["SEDE", "FILIAL"])
    endereco = fake.address().replace("\n", ", ")
    latitude = round(random.uniform(-33.0, 5.0), 6)
    longitude = round(random.uniform(-74.0, -34.0), 6)
    subsecional_id = random.choice(subsecoes)  # agora é inteiro ✅
    
    cursor.execute("""
        INSERT INTO Unidade (nome, hierarquia, endereco, latitude, longitude, subsecional_id)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (nome, hierarquia, endereco[:150], latitude, longitude, subsecional_id))
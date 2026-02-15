import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# ======================================
# CARREGA .env
# ======================================
load_dotenv()

# ======================================
# VARIÁVEIS DE AMBIENTE
# ======================================
NOME_PLANILHA = os.getenv("NOME_PLANILHA")
ABA = os.getenv("ABA_PLANILHA")
CAMINHO_CREDENCIAIS = os.getenv("CAMINHO_CREDENCIAIS")

print("🔎 Variáveis carregadas:")
print("Planilha:", NOME_PLANILHA)
print("Aba:", ABA)
print("Credenciais:", CAMINHO_CREDENCIAIS)
print("-" * 40)

# ======================================
# AUTENTICAÇÃO GOOGLE
# ======================================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CAMINHO_CREDENCIAIS, scope
)

client = gspread.authorize(creds)

# ======================================
# ABRIR PLANILHA
# ======================================
planilha = client.open(NOME_PLANILHA)

print("📄 Abas encontradas na planilha:")
for aba in planilha.worksheets():
    print(f"- '{aba.title}'")

print("-" * 40)

sheet = planilha.worksheet(ABA)
dados = sheet.get_all_records()

# ======================================
# TESTE FINAL
# ======================================
print("✅ Conexão OK!")
print(f"📊 Total de registros: {len(dados)}\n")

for i, linha in enumerate(dados, start=1):
    print(f"Linha {i}: {linha}")

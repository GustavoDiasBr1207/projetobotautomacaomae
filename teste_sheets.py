import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ======================================
# CONFIGURAÇÕES
# ======================================

NOME_PLANILHA = "Planilha Moradores"
ABA = "Página1"
CAMINHO_CREDENCIAIS = "credenciais.json"

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

sheet = client.open(NOME_PLANILHA).worksheet(ABA)

dados = sheet.get_all_records()

# ======================================
# TESTE
# ======================================

print("✅ Conexão OK!")
print("📄 Dados encontrados na planilha:\n")

for linha in dados:
    print(linha)

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

# ==================================================
# CARREGA VARIÁVEIS DE AMBIENTE
# ==================================================

load_dotenv()

# ==================================================
# CONFIGURAÇÕES (ENV)
# ==================================================

# Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
NUMERO_DESTINO_FIXO = os.getenv("NUMERO_DESTINO_FIXO")

# Google Sheets
NOME_PLANILHA = os.getenv("NOME_PLANILHA")
ABA = os.getenv("ABA_PLANILHA")
CAMINHO_CREDENCIAIS = os.getenv("CAMINHO_CREDENCIAIS")

# ==================================================
# GOOGLE SHEETS
# ==================================================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CAMINHO_CREDENCIAIS, scope
)

client_gs = gspread.authorize(creds)
sheet = client_gs.open(NOME_PLANILHA).worksheet(ABA)
dados = sheet.get_all_records()

# ==================================================
# TWILIO
# ==================================================

client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ==================================================
# DATA
# ==================================================

hoje = datetime.today().date()
dia_semana = hoje.weekday()  # 0=seg, 6=dom

# ==================================================
# PROCESSAMENTO
# ==================================================

if dia_semana <= 5:  # Segunda a sexta
    for i, linha in enumerate(dados, start=2):

        nome = linha.get("Nome", "").strip()
        status = linha.get("Status", "").strip().lower()
        data_ultima = linha.get("Data da última entrevista", "").strip()

        # Só processa pendentes
        if status != "pendente":
            continue

        # Se houver data, valida e calcula
        if data_ultima:
            try:
                data_ultima_date = datetime.strptime(
                    data_ultima, "%d/%m/%Y"
                ).date()
            except ValueError:
                print(f"Data inválida na linha {i}")
                continue

            proxima_data = data_ultima_date + relativedelta(months=2)

            if proxima_data > hoje:
                continue
        else:
            # Se não existir data, pula (ou ajusta se quiser outro comportamento)
            continue

        # ==================================================
        # ENVIO DA MENSAGEM
        # ==================================================

        mensagem = (
            f"Olá Aliene 👋\n\n"
            f"A última entrevista da família {nome} aconteceu em "
            f"{data_ultima_date.strftime('%d/%m/%Y')}.\n\n"
            f"Lembre-se de realizar uma nova entrevista dentro de uma semana.\n\n"
            f"Até mais!"
        )

        client_twilio.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=NUMERO_DESTINO_FIXO,
            body=mensagem
        )

        # Atualiza planilha
        sheet.update_cell(i, 6, "realizada")  # Status
        sheet.update_cell(i, 7, hoje.strftime("%d/%m/%Y"))  # Data da última entrevista

        print(f"Mensagem enviada para: {nome}")

else:
    print("Fim de semana — nenhuma mensagem enviada.")

print("Processo finalizado.")

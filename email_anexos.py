import imaplib
import email
import os
from datetime import datetime

EMAIL = "seu_e-mail" # !!! Inserir seu endereço de e-mail
SENHA = "sua_senha"  # !!! Gere uma senha de aplicativo no Google Account Security e insira nessa linha.
IMAP_SERVER = "imap.gmail.com"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, SENHA)
mail.select("inbox") 

# Buscar os e-mails não lidos
status, messages = mail.search(None, 'UNSEEN')

# Verificar se há e-mails
emails_ids = messages[0].split()
if not emails_ids:
    print("Nenhum e-mail não lido encontrado.")

pasta_anexos = "anexos"
if not os.path.exists(pasta_anexos):
    os.makedirs(pasta_anexos)

# Processar os e-mails
for num in emails_ids:
    status, msg_data = mail.fetch(num, "(RFC822)")
    raw_email = msg_data[0][1]
    
    # Converter para objeto email
    msg = email.message_from_bytes(raw_email)

    # Pegar a data do e-mail
    data_email = msg["Date"]
    data_formatada = datetime.strptime(data_email[:16].strip(), "%a, %d %b %Y").strftime("%Y-%m-%d")
    
    pasta_data = os.path.join(pasta_anexos, data_formatada)
    if not os.path.exists(pasta_data):
        os.makedirs(pasta_data)

    # Verificar se há anexos
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = part.get_filename()
            if filename:
                filepath = os.path.join(pasta_data, filename)
                
                # Evitar sobrescrever arquivos com o mesmo nome
                contador = 1
                while os.path.exists(filepath):
                    nome, ext = os.path.splitext(filename)
                    filepath = os.path.join(pasta_data, f"{nome}_{contador}{ext}")
                    contador += 1
                
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                print(f"Anexo {filename} salvo em {pasta_data}/")

print("Processo concluído!")
mail.logout()

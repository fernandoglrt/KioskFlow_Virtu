from celery import shared_task
from redmail import gmail
import csv
import io


@shared_task
def enviar_email_task(data):
    # Configurações
    gmail.username = 'fernandoglrt@gmail.com'
    gmail.password = 'xypz vucv npsn liwl'

    # CSV
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(['Campo', 'Resposta'])

    html_body = "<h3>Nova Pesquisa Recebida</h3><table border='1'>"
    for k, v in data.items():
        writer.writerow([k, v])
        html_body += f"<tr><td>{k}</td><td>{v}</td></tr>"
    html_body += "</table>"

    csv_str = csv_buffer.getvalue()

    try:
        gmail.send(
            subject=f"Pesquisa: {data.get('nome')}",
            receivers=["fernandoglrt@gmail.com"],
            html=html_body,
            attachments={"respostas.csv": csv_str}
        )
        return "Email enviado"
    except Exception as e:
        return f"Erro: {e}"
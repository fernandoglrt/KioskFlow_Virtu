# 🗳️ KioskFlow - Pesquisa Gravataí 2026

**Powered by Virtu Intelligence**

Aplicação web otimizada para Totens (Kiosks) e Tablets destinada à coleta de intenção de votos.
O sistema possui interface "Touch-First" animada e processamento assíncrono de envio de resultados por e-mail.

## 📋 Pré-requisitos

Para rodar este projeto, você **não** precisa instalar Python ou Redis na sua máquina. Você precisa apenas de:

* **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** instalado e rodando.

---

## 🚀 Como Rodar (Passo a Passo)

1.  **Extraia o projeto** em uma pasta de sua preferência.
2.  Abra o terminal (CMD ou PowerShell) **dentro da pasta do projeto**.
3.  Execute o comando abaixo para construir e iniciar os containers:

    ```bash
    docker-compose up --build
    ```

    > *Nota: A primeira execução pode demorar alguns minutos pois o Docker baixará as imagens necessárias.*

4.  Aguarde até ver logs indicando que o servidor está rodando (ex: `Starting development server at http://0.0.0.0:8000/`).

---

## 📱 Acessando a Aplicação

Abra seu navegador (Chrome, Edge, Firefox) e acesse:

* **Pesquisa (Kiosk):** [http://localhost:8000](http://localhost:8000)
* **Painel Administrativo:** [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🛠️ Tecnologias e Arquitetura

O projeto roda em containers Docker isolados:

1.  **Web (Django):** Interface do usuário e lógica de validação.
2.  **Worker (Celery):** Processo em segundo plano que gera os CSVs e envia e-mails sem travar a tela do usuário.
3.  **Redis:** Banco de dados em memória para gerenciar a fila de tarefas do Celery.

---

## 🛑 Como Parar

Para encerrar a execução, vá no terminal onde o comando está rodando e pressione:
`Ctrl + C`

Ou, abra um novo terminal na pasta e rode:
```bash
docker-compose down
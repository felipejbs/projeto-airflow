# projeto-airflow
![image](https://github.com/user-attachments/assets/7f0f7c3d-a3d1-4fdf-8d50-c2f015785dfe)

# 🌬️ Wind Turbine Data Pipeline com Apache Airflow

Este projeto é um pipeline de dados orquestrado com **Apache Airflow**, responsável por monitorar arquivos gerados por turbinas eólicas, processá-los, tomar decisões baseadas em temperatura, e então armazenar os dados em um banco de dados PostgreSQL ou enviar alertas por e-mail.

---

## 🗂️ Visão Geral

O fluxo de trabalho se baseia na seguinte sequência de tarefas:

1. **Monitoramento de Arquivos**: Verifica a presença de novos arquivos gerados por turbinas eólicas.
2. **Processamento com Python**: Executa uma lógica de extração e pré-processamento.
3. **Decisão Ramificada**:
   - Verifica condições de temperatura.
   - Decide entre armazenar no banco de dados ou enviar um alerta por e-mail.

---

## 📌 Estrutura do Pipeline

```text
windturbine 
   ↓
📁 Criação de Arquivo
   ↓
📁 File_sensor_task (FileSensor)
   ↓
⚙️ PythonOperator
   ↓
├── 📤 BranchPythonOperator (Group_check_temp)
│     ├── 📧 EmailOperator (alerta)
│     └── 📧 EmailOperator (confirmação)
│
└── 🛢️ PostgresOperator → PostgresOperator (Group_database)
```

---

## 🧩 Tarefas e Componentes

| Tarefa                  | Tipo                  | Descrição |
|------------------------|-----------------------|-----------|
| `File_sensor_task`     | `FileSensor`          | Espera um novo arquivo gerado pela turbina eólica. |
| `PythonOperator`       | `PythonOperator`      | Executa a leitura do arquivo e o pré-processamento dos dados. |
| `BranchPythonOperator` | `BranchPythonOperator`| Avalia a temperatura e decide a próxima ação. |
| `EmailOperator`        | `EmailOperator`       | Envia e-mail se a temperatura estiver fora do intervalo esperado. |
| `PostgresOperator`     | `PostgresOperator`    | Insere os dados tratados no banco de dados PostgreSQL. |

---

## 🔀 Ramificação Condicional

O `BranchPythonOperator` executa uma função que verifica a temperatura presente nos dados e retorna uma das seguintes tarefas:

- `'send_alert_email'`: se a temperatura estiver anormal.
- `'store_in_db'`: se a temperatura estiver dentro do intervalo esperado.

---

## 📁 Organização dos Grupos

- **Group_check_temp**: Responsável pelas ações relacionadas à verificação da temperatura e envio de e-mails.
- **Group_database**: Responsável pelas tarefas de inserção de dados no banco PostgreSQL.

---

## ⚙️ Requisitos

- Python >= 3.8
- Apache Airflow >= 2.6
- PostgreSQL
- Bibliotecas:
  - `psycopg2`
  - `apache-airflow-providers-postgres`
  - `apache-airflow-providers-email`

---

## ▶️ Como Executar

1. Clone este repositório:
```bash
git clone https://github.com/seuusuario/windturbine-airflow.git
cd windturbine-airflow
```

2. Crie um ambiente virtual e instale os requisitos:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Inicialize o Airflow:
```bash
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

4. Inicie o Airflow:
```bash
airflow scheduler
airflow webserver --port 8080
```

5. Acesse o painel em: [http://localhost:8080](http://localhost:8080)

---

## 📬 Contato

Para dúvidas ou sugestões, entre em contato com [seu-email@dominio.com].

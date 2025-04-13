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

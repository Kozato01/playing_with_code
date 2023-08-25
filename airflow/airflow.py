from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'padrao',
    'start_date': datetime(2023, 8, 24),
    'retries': 1,
}

dag = DAG(
    'meu_workflow',
    default_args=default_args,
    schedule_interval=None,
    catchup=False  
)

def execute_py_file(file_name):
    with open(file_name, 'r') as file:
        exec(file.read())

bronze_task = PythonOperator(
    task_id='bronze_task',
    python_callable=execute_py_file,
    op_args=['etl\raw.py'], 
    dag=dag
)

silver_task = PythonOperator(
    task_id='silver_task',
    python_callable=execute_py_file,
    op_args=['etl\silver.py'], 
    dag=dag
)

gold_task = PythonOperator(
    task_id='gold_task',
    python_callable=execute_py_file,
    op_args=['etl\gold.py'], 
    dag=dag
)

# Defina a ordem das tarefas
bronze_task >> silver_task >> gold_task


final_task = PythonOperator(
    task_id='final_task',
    python_callable=lambda: print("O fluxo de trabalho foi concluído com sucesso."),
    dag=dag
)


gold_task >> final_task

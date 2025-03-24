from celery import shared_task
import pandas as pd

@shared_task
def process_file_celery(file_path, temp_columns, min_temp, max_temp):
    df = pd.read_excel(file_path)

    # Aplicar la lógica de filtrado correctamente
    df[temp_columns] = df[temp_columns].apply(lambda x: x if min_temp <= x <= max_temp else None)

    output_path = file_path.replace(".xlsx", "_processed.xlsx")
    df.to_excel(output_path, index=False)

    return output_path

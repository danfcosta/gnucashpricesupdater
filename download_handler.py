import os
import requests
from requests.exceptions import RequestException
import time

def download_file(url, download_dir, max_retries=3):
    # Extrai o nome do arquivo da URL e cria o caminho completo de salvamento.
    file_name = url.split("/")[-1]
    save_path = os.path.join(download_dir, file_name)

    print(f"Downloading [{url}]")

    for _ in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança uma exceção se houver erro na resposta HTTP
            with open(save_path, 'wb') as file:
                file.write(response.content)
            return save_path  # Retorna o caminho do arquivo após o download bem-sucedido
        except RequestException as e:
            print(f"Erro no download: {e}")
            time.sleep(5)  # Espera um segundo antes de tentar novamente

    # Se todas as tentativas falharem, lança uma exceção.
    raise Exception(f"Não foi possível fazer o download após {max_retries} tentativas")
    
    return save_path
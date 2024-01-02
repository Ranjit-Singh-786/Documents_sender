import os ,logging
from datetime import datetime


LOG_DIRECTORY_NAME = "App logs"
os.makedirs(LOG_DIRECTORY_NAME,exist_ok=True)
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
FILE_NAME =f"log_{CURRENT_TIME_STAMP}.log"
FILE_PATH = os.path.join(LOG_DIRECTORY_NAME,FILE_NAME)

logging.basicConfig(filename=FILE_PATH,
                    filemode="w",
                    level=logging.DEBUG,
                    format="[%(asctime)s]  - %(levelname)s - %(message)s")

if __name__=="__main__":
    logging.info('Successfully tested !')
FROM image_base_for_telegram:v1.0
WORKDIR /home/telegram
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

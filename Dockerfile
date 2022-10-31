FROM python

RUN ["pip", "install", "wave"]

RUN ["pip", "install", "numpy"]

RUN ["pip", "install", "matplotlib"]

COPY . /home

WORKDIR /home

ENTRYPOINT [ "python", "main.py"]
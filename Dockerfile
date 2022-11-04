FROM python

RUN ["pip", "install", "wave"]

RUN ["pip", "install", "numpy"]

RUN ["pip", "install", "matplotlib"]

RUN ["pip", "install", "scipy"]

COPY . /home

WORKDIR /home

ENTRYPOINT [ "python", "main.py"]
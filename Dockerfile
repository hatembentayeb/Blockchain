FROM python:3
RUN pip install Flask_Cors==3.0.7
RUN pip install requests==2.21.0
RUN pip install Flask==1.0.2
RUN pip install pycrypto==2.6.1
COPY . /app
WORKDIR /app
EXPOSE 2000
ENTRYPOINT ["python3"]
CMD ["node.py"]

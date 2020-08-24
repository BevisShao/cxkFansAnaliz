FROM cxk_coms:1.1
COPY . /code
WORKDIR /code
#ENV ISDOCKER 1
ENV  PATH "${PATH}:/code"
#RUN pip3 install -r requirements.txt
CMD python3 /code/entryfile.py
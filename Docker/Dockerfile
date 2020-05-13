FROM python
COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt
EXPOSE 5006
CMD ["bokeh", "serve", "/opt/app/ressources/test1.py", "--dev"]
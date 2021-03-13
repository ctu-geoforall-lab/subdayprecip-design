FROM sphinxdoc/sphinx:3.5.2
WORKDIR /docs
ADD requirements.txt /docs
RUN pip3 install -r requirements.txt

CMD ["/docs/build.sh"]
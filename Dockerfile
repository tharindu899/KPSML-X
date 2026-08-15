FROM nanthakps/kpsmlx:heroku_v2

WORKDIR /usr/src/app

RUN chmod 777 /usr/src/app
RUN pip3 install --upgrade setuptools pip
RUN pip3 install --use-pep517 pymediainfo pyaes

# Remove any pre-baked pyrogram fork from the base image first — pyrofork
# and pyrotgfork both install into the same "pyrogram" package namespace,
# so leaving the old one in place can leave a corrupted mixed install.
RUN pip3 uninstall -y pyrofork pyrogram pyrotgfork tgcrypto || true

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "start.sh"]

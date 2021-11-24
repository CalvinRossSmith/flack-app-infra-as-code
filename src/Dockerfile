FROM python

RUN mkdir /home/appuser && \
    groupadd -r appuser && \
    useradd -r -g appuser -d /home/appuser -s /sbin/nologin -c "App User" appuser && \
    chown appuser:appuser /home/appuser && \
    install -d -o appuser -g appuser -m 740 /home/appuser/helloworld

WORKDIR /home/appuser/helloworld

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

COPY --chown=appuser:appuser ./python /home/appuser/helloworld

USER appuser
EXPOSE 5000

CMD ["python", "./hello.py"]
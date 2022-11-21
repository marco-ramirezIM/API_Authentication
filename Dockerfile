FROM python:3.9
COPY ./ /api-authentication
RUN pip install --no-cache-dir --upgrade -r /api-authentication/requirements.txt
COPY ./ /api-authentication
WORKDIR /api-authentication
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
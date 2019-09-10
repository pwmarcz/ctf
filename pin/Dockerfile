FROM python:3
RUN useradd --create-home --shell /bin/bash user
USER user
WORKDIR /home/user
RUN python -m venv env/
ENV PATH="/home/user/env/bin:$PATH"
RUN pip install flask gunicorn

EXPOSE 8000

ADD . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]

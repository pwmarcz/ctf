FROM python:3
RUN useradd --create-home --shell /bin/bash user
USER user
WORKDIR /home/user
RUN python -m venv env/
ENV PATH="/home/user/env/bin:$PATH"
RUN pip install flask gunicorn pyyaml==3.13

COPY flag.txt /home/user/flag.txt

EXPOSE 8000
WORKDIR /home/user/app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]

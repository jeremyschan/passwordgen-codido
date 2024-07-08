# choose an appropriate base image for your algorithm.
FROM python:latest

# docker files start running from the point that got changed. since our code files will tend to change alot,
# we don't want things like pulling the base docker image and downloading the requirements.txt file to happen everytime.
# hence we keep these things at the top
COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . .

ENTRYPOINT ["python", "app.py"]

CMD ["--codido", "False"]
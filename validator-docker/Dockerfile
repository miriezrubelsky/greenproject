# Use the official Python image from the Docker Hub
FROM python:3.9 

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip 
    #copy to code directory
COPY . /code    

RUN chmod +x /code/src
RUN pip install --no-cache-dir --upgrade -r code/src/greenproject/requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx


WORKDIR /code

# Declare the directory as a volume
VOLUME /code/src/greenproject/trained_model
# Declare the directory as a volume
VOLUME /code/src/greenproject/logs



# Create the input-files directory
#RUN mkdir -p /downloaded_files


VOLUME /downloaded_files


EXPOSE 8000



ENV PYTHONPATH "${PYTHONPATH}:/code/src"


ENTRYPOINT ["python", "/code/src/greenproject/validator_file_watcher.py"]


#CMD ["pytest"]

# Default command to provide flexibility if no arguments are passed
CMD ["--help"]

#CMD ["--host", "0.0.0.0", "--port", "8000"]





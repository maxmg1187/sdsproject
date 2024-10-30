FROM python:3.9-slim
WORKDIR /final-project-kem-entertainment
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "trendingbuzz/❤️_Moodmatch.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]

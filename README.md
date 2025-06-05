
## Prerequisites
- Python 3.12+
- Docker & Docker Compose

## Setup

### 1. Clone the repository
```
git clone <your-repo-url>
cd liora-dev
```

### 2. Start MongoDB with Docker Compose
```
docker-compose up -d
```
This will start MongoDB on `localhost:27018` with username `root` and password `example`.

### 3. Install Python dependencies
```
pip install -r requirements.txt
```
Required packages include:
- pymongo
- python-dotenv
- requests
- PyPDF2
- sentence-transformers
- numpy

### 4. Set environment variables
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=mongodb://root:example@localhost:27017/
```

### 5. Process PDF files into MongoDB
Place your PDF files in the project directory. Then run:
```
python mongo_vector.py
```
Edit the `pdf_path` in `mongo_vector.py` if needed.

### 6. Run the main assistant script
```
python main_with_context.py
```
This will:
- Retrieve related context from MongoDB for each user message
- Send the message and context to the OpenAI API
- Print the assistant's response


```
python main.py
```
This will do the same, but without context retrieval

## File Descriptions
- `main.py`: Main script withour context retrieval
- `main_with_context.py`: Main script, retrieves context and interacts with the AI model
- `mongo_vector.py`: Handles PDF processing, embedding, and MongoDB vector search
- `docker-compose.yml`: Sets up MongoDB with Docker

## Notes
- Ensure MongoDB is running before processing PDFs or running the main script.
- You can add more PDFs and re-run `mongo_vector.py` to expand the context database.

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import openai
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configuração do log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar o aplicativo FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Substitua pela sua chave de API real da OpenAI
openai.api_key = ''

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask(request: QuestionRequest):
    question = request.question
    if not question:
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

    try:
        logger.info(f"Pergunta recebida: {question}")
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=question,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
        logger.info(f"Resposta gerada: {answer}")
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Erro ao processar a pergunta: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar a pergunta.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from supabase import create_client
from pydantic import BaseModel
import os
from dotenv import load_dotenv

app = FastAPI()

# Configuração do Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuração de templates e arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class SearchQuery(BaseModel):
    search: str = ""

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/items")
async def get_items(search: str = ""):
    try:
        query = supabase.table('licencas').select("item, desc_catmas, valor_un_mensal, qtde_minima")  # Adicionei qtde_minima
        if search:
            query = query.ilike('desc_catmas', f'%{search}%')
        
        response = query.execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from supabase import create_client

# Configuração do Supabase
SUPABASE_URL = "https://elzufyyqepwysxaacauv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVsenVmeXlxZXB3eXN4YWFjYXV2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA1MjM4MDUsImV4cCI6MjA1NjA5OTgwNX0.DiPGsHsM7edsF-tINpKYA1qQo0z9f7S7lUhFHtgEPmI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuração do FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/debug")
async def debug():
    response = supabase.table("licencas").select("*").execute()
    return response.data  # Retorna os dados diretamente para testar



@app.get("/")
async def listar_produtos(request: Request):
    # Buscar produtos no Supabase
    response = supabase.table("licencas").select("*").execute()
    produtos = response.data
    return templates.TemplateResponse("index.html", {"request": request, "produtos": produtos})

@app.post("/salvar/")
async def salvar_quantidade(item: int = Form(...), qtde_mensal: int = Form(...)):
    # Buscar o valor unitário mensal do produto
    produto = supabase.table("licencas").select("valor_un_mensal").eq("item", item).execute()
    
    if not produto.data:
        return {"error": "Produto não encontrado"}

    valor_un_mensal = produto.data[0]["valor_un_mensal"]

    # Cálculo dos campos automáticos
    valor_un_total = valor_un_mensal * 36

    # Atualizar os dados no Supabase
    supabase.table("licencas").update({
        "qtde_mensal": qtde_mensal,
        "valor_un_total": valor_un_total
    }).eq("item", item).execute()

    return {"message": "Dados salvos com sucesso!", "item": item}

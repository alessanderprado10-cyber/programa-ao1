from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

# ===================== DADOS =====================
pedidos = {}

# ===================== PRODUTOS =====================
produtos_cadastrados = []

# ===================== DADOS EM MEMÓRIA =====================
dados_maquinas = {
    i: {
        "produzido": 0,
        "meta": 1000,
        "status": "PARADA"
    } for i in range(1, 7)
}

# ===================== LOGO =====================
@app.get("/logo")
def logo():
    return FileResponse("logo.png")


# ===================== TELA PRINCIPAL =====================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="
        background:linear-gradient(180deg,#0b2d1f,#06351f);
        color:white;
        font-family:Arial;
        margin:0;
    ">

        <div style="
            position:fixed;
            top:0;
            width:100%;
            background:#06281c;
            padding:12px 20px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            box-shadow:0 4px 15px rgba(0,0,0,0.5);
        ">
            <div style="display:flex; align-items:center; gap:10px;">
                <img src="/logo" style="width:40px;">
                <b>INDUPACK</b>
            </div>
        </div>

        <div style="margin-top:100px; text-align:center;">

            <img src="/logo" class="logo">

            <div class="menu">
                <a href="/producao"><button class="btn">🏭 Produção</button></a>
                <a href="/serigrafia"><button class="btn">🎨 Serigrafia</button></a>
                <a href="/impressao"><button class="btn">🖨 Impressão</button></a>
                <a href="/expedicao"><button class="btn">📦 Expedição</button></a>
            </div>

        </div>

        <style>
        .logo {
            width:150px;
            margin-top:20px;
            border-radius:15px;
            opacity:0;
            transform: translateY(-30px);
            animation: aparecer 0.8s ease forwards;
        }

        @keyframes aparecer {
            to {
                opacity:1;
                transform: translateY(0);
            }
        }

        .menu {
            display:flex;
            flex-direction:column;
            gap:15px;
            max-width:300px;
            margin:40px auto;
        }

        .btn {
            padding:18px;
            font-size:18px;
            width:100%;
            border-radius:12px;
            border:none;
            background:#16a34a;
            color:white;
            cursor:pointer;
            transition:0.25s;
        }

        .btn:hover {
            background:#22c55e;
            transform: scale(1.05);
        }
        </style>

    </body>
    </html>
    """
# ===================== PRODUÇÃO =====================
@app.get("/producao", response_class=HTMLResponse)
def producao():
    maquinas = ""

    for i in range(1, 7):

        # STATUS
        if i % 3 == 0:
            status = "RODANDO"
            cor = "#16a34a"
        elif i % 2 == 0:
            status = "MANUTENÇÃO"
            cor = "#f59e0b"
        else:
            status = "PARADA"
            cor = "#dc2626"

        # FILA (pega último pedido)
        lista = pedidos.get(i, [])

        if lista:
            pedido = lista[-1]
        else:
            pedido = {}

        cliente = pedido.get("cliente", "---")
        produto = pedido.get("produto", "---")
        fardos = pedido.get("fardos", 0)
        descricao = pedido.get("descricao", "---")

        try:
            quantidade = int(pedido.get("quantidade", 1000))
        except:
            quantidade = 1000

        maquinas += f"""
        <div class="card" onclick="window.location.href='/programacao/{i}'">

            <div class="topo">
                <div class="numero">{i:02}</div>
                <div class="status" style="background:{cor};">{status}</div>
            </div>

            <div class="barra">
                <div class="progresso" style="background:{cor};"></div>
            </div>

            <p class="info">0 / {quantidade}</p>

            <div class="info_box">
                <div><span>👤 Cliente:</span> {cliente}</div>
                <div><span>📦 Produto:</span> {produto}</div>
                <div><span>📊 Fardos:</span> {fardos}</div>
                <div><span>📝 Obs:</span> {descricao}</div>
            </div>

        </div>
        """

    return f"""
    <html>
    <body style="background:#0b2d1f; color:white; font-family:Arial; margin:0;">

        <div class="topbar">
            <div style="display:flex; align-items:center; gap:10px;">
                <img src="/logo" style="width:35px;">
                <b>INDUPACK</b>
            </div>
        </div>

        <div style="margin-top:90px; padding:20px;">

            <h1 style="text-align:center;">🏭 PRODUÇÃO</h1>

            <div class="grid">
                {maquinas}
            </div>

        </div>

        <style>

        .topbar {{
            position:fixed;
            top:0;
            width:100%;
            background:#06281c;
            padding:12px 20px;
            display:flex;
            align-items:center;
            box-shadow:0 4px 15px rgba(0,0,0,0.5);
        }}

        .grid {{
            display:grid;
            grid-template-columns: repeat(3, 1fr);
            gap:20px;
        }}

        .card {{
            background:#e5e7eb;
            color:black;
            padding:15px;
            border-radius:15px;
            box-shadow:0 8px 20px rgba(0,0,0,0.4);
            cursor:pointer;
            transition:0.2s;
        }}

        .card:hover {{
            transform: scale(1.03);
        }}

        .topo {{
            display:flex;
            justify-content:space-between;
            align-items:center;
        }}

        .numero {{
            background:#065f46;
            color:white;
            padding:8px 12px;
            border-radius:8px;
            font-weight:bold;
        }}

        .status {{
            color:white;
            padding:5px 10px;
            border-radius:10px;
            font-size:12px;
            font-weight:bold;
        }}

        .barra {{
            background:#9ca3af;
            height:8px;
            border-radius:10px;
            margin:10px 0;
        }}

        .progresso {{
            width:65%;
            height:100%;
            border-radius:10px;
        }}

        .info {{
            text-align:center;
            font-weight:bold;
        }}

        .info_box {{
            margin-top:10px;
            display:flex;
            flex-direction:column;
            gap:6px;
            font-size:14px;
        }}

        .info_box div {{
            background:white;
            padding:6px 10px;
            border-radius:8px;
            box-shadow:0 2px 5px rgba(0,0,0,0.1);
        }}

        .info_box span {{
            font-weight:bold;
            color:#065f46;
        }}

        </style>

    </body>
    </html>
    """

# ===================== PROGRAMAÇÃO MAQUINA =====================
@app.get("/programacao/{id}", response_class=HTMLResponse)
def programacao_maquina(id: int):

    lista = pedidos.get(id, [])

    opcoes_produtos = "".join([f"<option>{p}</option>" for p in produtos_cadastrados])

    linhas = ""

    for idx, p in enumerate(lista):

        ordem = f"{idx+1}º"

        linhas += f"""
        <div class="linha">

            <div class="ordem">{ordem}</div>

            <input value="{p.get("data","")}" data-i="{idx}" data-campo="data">
            <input value="{p.get("cod","")}" data-i="{idx}" data-campo="cod">
            <input value="{p.get("produto","")}" data-i="{idx}" data-campo="produto">
            <input value="{p.get("quantidade","")}" data-i="{idx}" data-campo="quantidade">
            <input value="{p.get("fardos","")}" data-i="{idx}" data-campo="fardos">
            <input value="{p.get("etiqueta","X")}" data-i="{idx}" data-campo="etiqueta">
            <input value="{p.get("descricao","")}" data-i="{idx}" data-campo="descricao">
            <input value="{p.get("finalizado","")}" data-i="{idx}" data-campo="finalizado">

            <button class="delete" onclick="deletar({idx})">🗑</button>

        </div>
        """

    return f"""
    <html>
    <body style="background:#0b2d1f; color:white; font-family:Arial; margin:0;">

        <h1 style="text-align:center; padding:20px;">
        📋 PROGRAMAÇÃO MÁQUINA {id}
        </h1>

        <div class="container">

            <button class="btn_pedido" onclick="abrirPedido()">+ Pedido</button>

            <div class="tabela">

                <div class="linha cabecalho">
                    <div>ORDEM</div>
                    <div>DATA</div>
                    <div>CÓD</div>
                    <div>MEDIDA</div>
                    <div>QUANTIDADE</div>
                    <div>EMBALAGEM</div>
                    <div>ETIQUETA</div>
                    <div>OBSERVAÇÃO</div>
                    <div>FINALIZADO</div>
                    <div>AÇÃO</div>
                </div>

                {linhas}

            </div>

            <button class="salvar" onclick="salvarTabela()">💾 Salvar</button>

        </div>

        <!-- MODAL -->
        <div id="modal" class="modal">
            <div class="box">

                <h3>📦 Novo Pedido</h3>

                <input id="cliente" placeholder="Cliente">

                <div class="linha_produto">
                    <select id="produto">
                        <option value="">Selecione produto</option>
                        {opcoes_produtos}
                    </select>

                    <button onclick="limparProduto()">🗑</button>
                </div>

                <button class="novo_produto" onclick="novoProduto()">+ Novo Produto</button>

                <input id="quantidade" value="1000">

                <select id="fardos">
                    <option>50</option>
                    <option selected>100</option>
                    <option>200</option>
                    <option>250</option>
                </select>

                <input id="descricao" placeholder="Descrição">

                <button class="salvar_btn" onclick="salvarPedido()">Salvar Pedido</button>
                <button class="fechar_btn" onclick="fechar()">Fechar</button>

            </div>
        </div>

        <style>

        .container {{
            display:flex;
            flex-direction:column;
            align-items:center;
            padding:20px;
        }}

        .tabela {{
            width:95%;
        }}

        .linha {{
            display:grid;
            grid-template-columns: 70px repeat(8, 1fr) 70px;
            gap:5px;
            margin-bottom:5px;
        }}

        .linha input {{
            padding:8px;
            border-radius:6px;
            border:none;
            text-align:center;
        }}

        .ordem {{
            background:#1f2937;
            color:white;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:6px;
            font-weight:bold;
        }}

        .cabecalho div {{
            background:#1f2937;
            padding:10px;
            text-align:center;
            font-weight:bold;
        }}

        .delete {{
            background:#ef4444;
            border:none;
            border-radius:6px;
            color:white;
            cursor:pointer;
        }}

        .btn_pedido {{
            background:#f59e0b;
            padding:10px;
            border:none;
            border-radius:8px;
            margin-bottom:10px;
            cursor:pointer;
        }}

        .salvar {{
            margin-top:20px;
            background:#22c55e;
            padding:10px;
            border:none;
            border-radius:10px;
        }}

        .modal {{
            display:none;
            position:fixed;
            top:0;
            left:0;
            width:100%;
            height:100%;
            background:rgba(0,0,0,0.7);
            justify-content:center;
            align-items:center;
            z-index:9999;
        }}

        .box {{
            background:#1f2937;
            padding:25px;
            border-radius:15px;
            display:flex;
            flex-direction:column;
            gap:12px;
            width:320px;
        }}

        .box input, .box select {{
            padding:12px;
            border-radius:10px;
            border:none;
            background:#111827;
            color:white;
        }}

        .linha_produto {{
            display:flex;
            gap:8px;
        }}

        .linha_produto select {{
            flex:1;
        }}

        .linha_produto button {{
            background:#ef4444;
            border:none;
            border-radius:8px;
            color:white;
            padding:10px;
        }}

        .novo_produto {{
            background:#3b82f6;
            border:none;
            border-radius:8px;
            padding:10px;
            color:white;
        }}

        .salvar_btn {{
            background:#22c55e;
        }}

        .fechar_btn {{
            background:#ef4444;
        }}

        </style>

        <script>

        function abrirPedido(){{
            document.getElementById("modal").style.display = "flex";
        }}

        function fechar(){{
            document.getElementById("modal").style.display = "none";
        }}

        function limparProduto(){{
            document.getElementById("produto").value = "";
        }}

        function novoProduto(){{
            let nome = prompt("Nome do produto:");
            if(nome){{
                fetch(`/add_produto?nome=${{nome}}`)
                .then(()=>location.reload())
            }}
        }}

        function salvarPedido(){{

            let cliente = document.getElementById("cliente").value;
            let produto = document.getElementById("produto").value;
            let quantidade = document.getElementById("quantidade").value;
            let fardos = document.getElementById("fardos").value;
            let descricao = document.getElementById("descricao").value;

            if(!produto){{
                alert("Selecione um produto!");
                return;
            }}

            fetch(`/salvar_pedido/{id}?cliente=${{cliente}}&produto=${{produto}}&quantidade=${{quantidade}}&fardos=${{fardos}}&descricao=${{descricao}}`)
            .then(res => res.json())
            .then(data => {{
                if(data.ok){{
                    location.reload();
                }} else {{
                    alert("Erro ao salvar");
                }}
            }})
            .catch(() => {{
                alert("Erro no servidor");
            }});

        }}

        function deletar(i){{
            fetch(`/deletar/{id}?index=${{i}}`)
            .then(()=>location.reload())
        }}

        function salvarTabela(){{

            let inputs = document.querySelectorAll("input[data-i]");
            let dados = [];

            inputs.forEach(input => {{
                let i = input.dataset.i;
                let campo = input.dataset.campo;

                if(!dados[i]) dados[i] = {{}};

                dados[i][campo] = input.value;
            }});

            fetch("/salvar_programacao/{id}", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify(dados)
            }});

        }}

        </script>

    </body>
    </html>
    """

# ===================== PEDIDO =====================
@app.get("/pedido/{id}", response_class=HTMLResponse)
def pedido(id: int):

    opcoes = "".join([f"<option>{p}</option>" for p in produtos_cadastrados])

    return f"""
    <html>
    <body style="background:#0b2d1f; color:white; font-family:Arial; margin:0;">

        <!-- 🔝 TOPO -->
        <div class="topo">
            <h1>MÁQUINA {id}</h1>
        </div>

        <div class="container">

            <div class="form">

                <label>Cliente</label>
                <input id="cliente" placeholder="---">

                <label>Produto</label>

                <div class="linha">
                    <select id="produto">
                        <option value="">---</option>
                        {opcoes}
                    </select>

                    <button class="lixeira" onclick="limparProduto()">🗑</button>
                </div>

                <button class="novo" onclick="novoProduto()">+ Novo Produto</button>

                <label>Quantidade</label>
                <input id="quantidade" value="1000">

                <label>Fardos</label>
                <div class="linha">
                    <select id="fardos">
                        <option value="50">50</option>
                        <option value="100" selected>100</option>
                        <option value="200">200</option>
                        <option value="250">250</option>
                    </select>
                </div>

                <label>Descrição</label>
                <input id="descricao" placeholder="---">

                <button class="salvar" onclick="salvar()">Salvar Pedido</button>

            </div>

        </div>

        <style>

        body {{
            margin:0;
        }}

        .topo {{
            text-align:center;
            padding:20px;
            background:linear-gradient(to right,#063d2b,#0b2d1f);
        }}

        .container {{
            display:flex;
            justify-content:center;
            margin-top:20px;
        }}

        .form {{
            width:350px;
            background:#d1d5db;
            padding:20px;
            border-radius:20px;
            display:flex;
            flex-direction:column;
            gap:10px;
        }}

        label {{
            font-weight:bold;
            color:black;
        }}

        input, select {{
            padding:10px;
            border-radius:10px;
            border:none;
            background:#1f2937;
            color:white;
        }}

        .linha {{
            display:flex;
            gap:10px;
        }}

        .linha select {{
            flex:1;
        }}

        .lixeira {{
            background:#ef4444;
            color:white;
            border:none;
            border-radius:8px;
            padding:10px;
        }}

        .novo {{
            background:#3b82f6;
            color:white;
            border:none;
            border-radius:8px;
            padding:10px;
        }}

        .salvar {{
            background:#22c55e;
            color:white;
            border:none;
            border-radius:10px;
            padding:12px;
            margin-top:10px;
            font-size:16px;
        }}

        </style>

        <script>

        function limparProduto() {{
            document.getElementById("produto").value = "";
        }}

        function novoProduto() {{
            let nome = prompt("Nome do produto:");

            if(nome) {{
                fetch(`/add_produto?nome=${{nome}}`)
                .then(() => location.reload());
            }}
        }}

        function salvar() {{

            let cliente = document.getElementById("cliente").value;
            let produto = document.getElementById("produto").value;
            let quantidade = document.getElementById("quantidade").value;
            let fardos = document.getElementById("fardos").value;
            let descricao = document.getElementById("descricao").value;

            fetch(`/salvar_pedido/{id}?cliente=${{cliente}}&produto=${{produto}}&quantidade=${{quantidade}}&fardos=${{fardos}}&descricao=${{descricao}}`)
            .then(() => {{
                alert("Salvo!");
                window.location.href = "/producao";
            }});

        }}

        </script>

    </body>
    </html>
    """

# ===================== SERIGRAFIA =====================
@app.get("/serigrafia", response_class=HTMLResponse)
def serigrafia():
    return "<h1>Serigrafia</h1>"


# ===================== IMPRESSÃO =====================
@app.get("/impressao", response_class=HTMLResponse)
def impressao():
    return "<h1>Impressão</h1>"


# ===================== EXPEDIÇÃO =====================
@app.get("/expedicao", response_class=HTMLResponse)
def expedicao():
    return "<h1>Expedição</h1>"

# ===================== SOMAR PRODUÇÃO =====================
@app.get("/add/{id}/{valor}")
def add(id: int, valor: int):
    dados_maquinas[id]["produzido"] += valor
    return {"ok": True}


# ===================== ALTERAR STATUS =====================
@app.get("/status/{id}/{novo}")
def status(id: int, novo: str):
    dados_maquinas[id]["status"] = novo
    return {"ok": True}



# ===================== CADASTRAR PRODUTO =====================
@app.get("/add_produto")
def add_produto(nome: str):
    if nome not in produtos_cadastrados:
        produtos_cadastrados.append(nome)
    return {"ok": True}

# ===================== SALVAR PEDIDO =====================
@app.get("/salvar_pedido/{id}")
def salvar_pedido(id: int, cliente: str = "", produto: str = "", quantidade: int = 0, fardos: int = 0, descricao: str = ""):

    from datetime import datetime

    data_hoje = datetime.now().strftime("%d/%m")

    if id not in pedidos:
        pedidos[id] = []

    # 🔥 evita erro se não selecionar produto
    if produto:
        partes = produto.split(" ")
        cod = partes[0] if len(partes) > 0 else ""
        medida = " ".join(partes[1:-1]) if len(partes) > 2 else produto
        peso = partes[-1] if len(partes) > 1 else ""
        medida_final = f"{medida} - {peso}"
    else:
        cod = ""
        medida_final = ""

    pedidos[id].append({
        "data": data_hoje,
        "cliente": cliente,
        "cod": cod,
        "produto": medida_final,
        "quantidade": int(quantidade),
        "fardos": int(fardos),
        "descricao": descricao
    })

    return {"ok": True}
# ===================== NOVO PEDIDO =====================
@app.get("/novo_pedido/{id}")
def novo_pedido(id: int):

    if id not in pedidos:
        pedidos[id] = []

    pedidos[id].append({
        "cliente": "",
        "produto": "",
        "quantidade": 0,
        "fardos": 0,
        "descricao": ""
    })

    return {"ok": True}

# ===================== tablet 01 =====================
@app.get("/tablet/{id}", response_class=HTMLResponse)
def tablet(id: int):

    lista = pedidos.get(id, [])

    linhas = ""

    for p in lista:
        linhas += f"""
        <div class="card">
            <div><b>Produto:</b> {p.get("produto","")}</div>
            <div><b>Qtd:</b> {p.get("quantidade","")}</div>
            <div><b>Fardos:</b> {p.get("fardos","")}</div>
            <div><b>Obs:</b> {p.get("descricao","")}</div>
        </div>
        """

    return f"""
    <html>
    <body style="background:#0b2d1f; color:white; font-family:Arial; text-align:center;">

        <h1>📱 MÁQUINA {id}</h1>

        <input id="operador" placeholder="Nome do operador" style="padding:10px; width:80%; margin-bottom:10px;">

        <button onclick="iniciar()" style="background:#22c55e; padding:15px; width:80%; margin:5px;">INICIAR</button>
        <button onclick="parar()" style="background:#ef4444; padding:15px; width:80%; margin:5px;">PARAR</button>

        <hr>

        {linhas}

        <script>

        function iniciar(){
            alert("Produção iniciada");
        }

        function parar(){
            alert("Máquina parada");
        }

        </script>

    </body>
    </html>
    """


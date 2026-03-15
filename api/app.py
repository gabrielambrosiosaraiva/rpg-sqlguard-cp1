from fastapi import FastAPI
import oracledb, os

app = FastAPI()

pool = oracledb.create_pool(
    user=DB_USER,
    password=DB_PASSWORD,
    dsn=DB_DSN,
    min=1,
    max=5,
    increment=1
)

def get_connection():
    return pool.acquire()

@app.get("/listar-herois", response_class=HTMLResponse)
def listar_herois():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT nome, classe, hp_atual, hp_max, status FROM TB_HEROIS")
        dados = cur.fetchall()
        cur.close()
        conn.close()

        # Montar tabela HTML
        html = """
        <html>
        <head>
            <style>
                table {border-collapse: collapse; width: 80%; margin: 20px auto;}
                th, td {border: 1px solid #ccc; padding: 8px; text-align: center;}
                th {background-color: #f2f2f2;}
            </style>
        </head>
        <body>
            <h2 style="text-align:center;">Tabela de Heróis</h2>
            <table>
                <tr>
                    <th>Nome</th>
                    <th>Classe</th>
                    <th>HP Atual</th>
                    <th>HP Máx</th>
                    <th>Status</th>
                </tr>
        """
        for nome, classe, hp_atual, hp_max, status in dados:
            html += f"""
                <tr>
                    <td>{nome}</td>
                    <td>{classe}</td>
                    <td>{hp_atual}</td>
                    <td>{hp_max}</td>
                    <td>{status}</td>
                </tr>
            """
        html += """
            </table>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"<p>Erro: {str(e)}</p>"

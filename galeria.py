from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)
CARPETA_SALIDAS = "salidas"
os.makedirs(CARPETA_SALIDAS, exist_ok=True)

@app.route('/')
def galeria():
    imagenes = [f for f in os.listdir(CARPETA_SALIDAS) if f.endswith('.png')]
    html = """
    <html>
    <head>
        <title>Galería de Imágenes</title>
        <style>
            body { margin: 0; font-family: 'Segoe UI', sans-serif; background: #fdfdfd; }
            .banner {
                background-color: #F26522;
                color: white;
                padding: 15px 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .banner img {
                height: 50px;
                margin-right: 15px;
            }
            .grid {
                padding: 30px;
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
            }
            .item {
                background: white;
                padding: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border-radius: 10px;
                text-align: center;
                max-width: 320px;
                cursor: pointer;
            }
            img.grafico {
                max-width: 100%;
                height: auto;
                border-radius: 6px;
                transition: transform 0.2s;
            }
            img.grafico:hover {
                transform: scale(1.05);
            }
            h2 { font-size: 0.9rem; margin: 0.5em 0 0; color: #333; }

            /* Modal */
            .modal {
                display: none;
                position: fixed;
                z-index: 999;
                left: 0; top: 0;
                width: 100%; height: 100%;
                background-color: rgba(0,0,0,0.8);
            }
            .modal-content {
                display: block;
                margin: 50px auto;
                max-width: 90%;
                max-height: 80%;
                border-radius: 10px;
                box-shadow: 0 0 10px white;
            }
            .modal-close {
                position: absolute;
                top: 20px;
                right: 30px;
                color: white;
                font-size: 2rem;
                font-weight: bold;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="banner">
            <div style="display: flex; align-items: center;">
                <img src="/static/logo_ulima.png" alt="Universidad de Lima Logo">
                <div>
                    <strong>Redes de Computadoras</strong><br>
                    Universidad de Lima · Proyecto 2025
                </div>
            </div>
        </div>

        <div class="grid">
            {% for img in imagenes %}
            <div class="item" onclick="mostrarModal('{{ img }}')">
                <img class="grafico" src="/img/{{ img }}" alt="{{ img }}">
                <h2>{{ img }}</h2>
            </div>
            {% endfor %}
        </div>

        <div id="modal" class="modal" onclick="cerrarModal()">
            <span class="modal-close">&times;</span>
            <img id="modal-img" class="modal-content">
        </div>

        <script>
            function mostrarModal(src) {
                var modal = document.getElementById("modal");
                var modalImg = document.getElementById("modal-img");
                modal.style.display = "block";
                modalImg.src = "/img/" + src;
            }
            function cerrarModal() {
                document.getElementById("modal").style.display = "none";
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, imagenes=imagenes)

@app.route('/img/<path:nombre>')
def imagen(nombre):
    return send_from_directory(CARPETA_SALIDAS, nombre)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

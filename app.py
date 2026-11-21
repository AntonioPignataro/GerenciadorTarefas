"""Gerenciador de Tarefas - Projeto de Desenvolvimento de Software I e II.

Aplicação web simples (Flask + SQLite) com CRUD de Tarefas e Categorias.
"""
import os
import sqlite3

from flask import Flask, flash, g, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-projeto-faculdade"  # usado apenas para flash()
app.config["DATABASE"] = os.path.join(BASE_DIR, "tarefas.db")


# ---------------------------------------------------------------- Banco de dados
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas caso ainda não existam."""
    with open(os.path.join(BASE_DIR, "schema.sql"), encoding="utf-8") as f:
        script = f.read()
    db = sqlite3.connect(app.config["DATABASE"])
    db.executescript(script)
    db.commit()
    db.close()


# ---------------------------------------------------------------- Tarefas (CRUD)
@app.route("/")
def listar_tarefas():
    """READ - lista as tarefas, com filtros opcionais por categoria e status."""
    categoria_id = request.args.get("categoria", "")
    status = request.args.get("status", "")

    sql = (
        "SELECT t.*, c.nome AS categoria_nome FROM tarefa t "
        "LEFT JOIN categoria c ON c.id = t.categoria_id WHERE 1=1"
    )
    params = []
    if categoria_id.isdigit():
        sql += " AND t.categoria_id = ?"
        params.append(int(categoria_id))
    if status == "pendentes":
        sql += " AND t.concluida = 0"
    elif status == "concluidas":
        sql += " AND t.concluida = 1"
    sql += " ORDER BY t.concluida, t.prazo IS NULL, t.prazo, t.id"

    db = get_db()
    tarefas = db.execute(sql, params).fetchall()
    categorias = db.execute("SELECT * FROM categoria ORDER BY nome").fetchall()
    return render_template(
        "index.html",
        tarefas=tarefas,
        categorias=categorias,
        filtro_categoria=categoria_id,
        filtro_status=status,
    )


def _dados_tarefa_do_form():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip() or None
    prazo = request.form.get("prazo", "").strip() or None
    categoria_id = request.form.get("categoria_id", "")
    categoria_id = int(categoria_id) if categoria_id.isdigit() else None
    return titulo, descricao, prazo, categoria_id


@app.route("/tarefas/nova", methods=["GET", "POST"])
def criar_tarefa():
    """CREATE - cadastra uma nova tarefa."""
    db = get_db()
    categorias = db.execute("SELECT * FROM categoria ORDER BY nome").fetchall()
    if request.method == "POST":
        titulo, descricao, prazo, categoria_id = _dados_tarefa_do_form()
        if not titulo:
            flash("O título é obrigatório.", "erro")
            return render_template("tarefa_form.html", tarefa=request.form, categorias=categorias, novo=True)
        db.execute(
            "INSERT INTO tarefa (titulo, descricao, prazo, categoria_id) VALUES (?, ?, ?, ?)",
            (titulo, descricao, prazo, categoria_id),
        )
        db.commit()
        flash("Tarefa cadastrada com sucesso!", "ok")
        return redirect(url_for("listar_tarefas"))
    return render_template("tarefa_form.html", tarefa={}, categorias=categorias, novo=True)


@app.route("/tarefas/<int:tarefa_id>/editar", methods=["GET", "POST"])
def editar_tarefa(tarefa_id):
    """UPDATE - altera os dados de uma tarefa."""
    db = get_db()
    tarefa = db.execute("SELECT * FROM tarefa WHERE id = ?", (tarefa_id,)).fetchone()
    if tarefa is None:
        flash("Tarefa não encontrada.", "erro")
        return redirect(url_for("listar_tarefas"))
    categorias = db.execute("SELECT * FROM categoria ORDER BY nome").fetchall()

    if request.method == "POST":
        titulo, descricao, prazo, categoria_id = _dados_tarefa_do_form()
        if not titulo:
            flash("O título é obrigatório.", "erro")
            return render_template("tarefa_form.html", tarefa=request.form, categorias=categorias, novo=False, tarefa_id=tarefa_id)
        db.execute(
            "UPDATE tarefa SET titulo = ?, descricao = ?, prazo = ?, categoria_id = ? WHERE id = ?",
            (titulo, descricao, prazo, categoria_id, tarefa_id),
        )
        db.commit()
        flash("Tarefa atualizada com sucesso!", "ok")
        return redirect(url_for("listar_tarefas"))
    return render_template("tarefa_form.html", tarefa=tarefa, categorias=categorias, novo=False, tarefa_id=tarefa_id)


@app.route("/tarefas/<int:tarefa_id>/concluir", methods=["POST"])
def alternar_conclusao(tarefa_id):
    """UPDATE - marca como concluída (ou volta para pendente)."""
    db = get_db()
    db.execute("UPDATE tarefa SET concluida = 1 - concluida WHERE id = ?", (tarefa_id,))
    db.commit()
    return redirect(request.referrer or url_for("listar_tarefas"))


@app.route("/tarefas/<int:tarefa_id>/excluir", methods=["POST"])
def excluir_tarefa(tarefa_id):
    """DELETE - remove uma tarefa."""
    db = get_db()
    db.execute("DELETE FROM tarefa WHERE id = ?", (tarefa_id,))
    db.commit()
    flash("Tarefa excluída.", "ok")
    return redirect(url_for("listar_tarefas"))


# ---------------------------------------------------------------- Categorias (CRUD)
@app.route("/categorias", methods=["GET", "POST"])
def categorias():
    """CREATE + READ de categorias."""
    db = get_db()
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if not nome:
            flash("O nome da categoria é obrigatório.", "erro")
        else:
            try:
                db.execute("INSERT INTO categoria (nome) VALUES (?)", (nome,))
                db.commit()
                flash("Categoria cadastrada!", "ok")
            except sqlite3.IntegrityError:
                flash("Já existe uma categoria com esse nome.", "erro")
        return redirect(url_for("categorias"))

    lista = db.execute(
        "SELECT c.*, COUNT(t.id) AS total FROM categoria c "
        "LEFT JOIN tarefa t ON t.categoria_id = c.id GROUP BY c.id ORDER BY c.nome"
    ).fetchall()
    return render_template("categorias.html", categorias=lista)


@app.route("/categorias/<int:categoria_id>/editar", methods=["POST"])
def editar_categoria(categoria_id):
    """UPDATE - renomeia uma categoria."""
    nome = request.form.get("nome", "").strip()
    if not nome:
        flash("O nome da categoria é obrigatório.", "erro")
    else:
        db = get_db()
        try:
            db.execute("UPDATE categoria SET nome = ? WHERE id = ?", (nome, categoria_id))
            db.commit()
            flash("Categoria atualizada!", "ok")
        except sqlite3.IntegrityError:
            flash("Já existe uma categoria com esse nome.", "erro")
    return redirect(url_for("categorias"))


@app.route("/categorias/<int:categoria_id>/excluir", methods=["POST"])
def excluir_categoria(categoria_id):
    """DELETE - remove uma categoria (as tarefas ficam sem categoria)."""
    db = get_db()
    db.execute("DELETE FROM categoria WHERE id = ?", (categoria_id,))
    db.commit()
    flash("Categoria excluída.", "ok")
    return redirect(url_for("categorias"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

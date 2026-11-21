"""Testes automatizados do CRUD (rodar com: python -m unittest discover tests)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app as modulo_app  # noqa: E402


class CrudTest(unittest.TestCase):
    def setUp(self):
        fd, self.caminho = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        modulo_app.app.config["DATABASE"] = self.caminho
        modulo_app.app.config["TESTING"] = True
        modulo_app.init_db()
        self.client = modulo_app.app.test_client()

    def tearDown(self):
        os.remove(self.caminho)

    def test_crud_categoria(self):
        self.client.post("/categorias", data={"nome": "Estudos"})
        self.assertIn(b"Estudos", self.client.get("/categorias").data)
        self.client.post("/categorias/1/editar", data={"nome": "Faculdade"})
        pagina = self.client.get("/categorias").data
        self.assertIn(b"Faculdade", pagina)
        self.assertNotIn(b"Estudos", pagina)
        self.client.post("/categorias/1/excluir")
        self.assertNotIn(b"Faculdade", self.client.get("/categorias").data)

    def test_crud_tarefa(self):
        self.client.post("/categorias", data={"nome": "Casa"})
        # Create
        self.client.post("/tarefas/nova", data={"titulo": "Lavar louça", "categoria_id": "1", "prazo": "2026-12-01"})
        pagina = self.client.get("/").data
        self.assertIn("Lavar louça".encode(), pagina)
        self.assertIn(b"Casa", pagina)
        # Update
        self.client.post("/tarefas/1/editar", data={"titulo": "Lavar roupa", "categoria_id": "1"})
        pagina = self.client.get("/").data
        self.assertIn(b"Lavar roupa", pagina)
        self.assertNotIn("Lavar louça".encode(), pagina)
        # Concluir + filtro
        self.client.post("/tarefas/1/concluir")
        self.assertNotIn(b"Lavar roupa", self.client.get("/?status=pendentes").data)
        self.assertIn(b"Lavar roupa", self.client.get("/?status=concluidas").data)
        # Delete
        self.client.post("/tarefas/1/excluir")
        self.assertIn(b"Nenhuma tarefa", self.client.get("/").data)

    def test_titulo_obrigatorio(self):
        resposta = self.client.post("/tarefas/nova", data={"titulo": "  "})
        self.assertIn("título é obrigatório".encode(), resposta.data)

    def test_excluir_categoria_mantem_tarefa(self):
        self.client.post("/categorias", data={"nome": "Temp"})
        self.client.post("/tarefas/nova", data={"titulo": "Sobrevive", "categoria_id": "1"})
        self.client.post("/categorias/1/excluir")
        self.assertIn(b"Sobrevive", self.client.get("/").data)


if __name__ == "__main__":
    unittest.main()

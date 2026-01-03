# main.py
import sys
import threading

# IMPORTANTE: Criar QApplication ANTES de importar módulos que usam Qt
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

from gui.app import app as dash_app  # noqa: E402
from gui.main_gui import MainWindow  # noqa: E402


def _start_dash():
    # use_reloader=False evita que o Dash crie processos extras
    dash_app.run(host="127.0.0.1", port=8050, debug=False)


if __name__ == "__main__":
    # Inicia Dash em thread separada
    dash_thread = threading.Thread(target=_start_dash, daemon=True)
    dash_thread.start()

    # Inicia GUI PyQt5 no thread principal
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

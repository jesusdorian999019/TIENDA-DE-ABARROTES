"""
Módulo de actualizaciones automáticas.
Verifica y descarga actualizaciones desde GitHub.
"""
import os
import sys
import json
import ssl
import urllib.request
import urllib.error
from pathlib import Path
from config.settings import (
    APP_VERSION, GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH
)


class UpdateChecker:
    """Verificador de actualizaciones desde GitHub."""

    def __init__(self):
        self.version = APP_VERSION
        self.owner = GITHUB_OWNER
        self.repo = GITHUB_REPO
        self.branch = GITHUB_BRANCH

    def get_latest_version(self):
        """Obtiene la última versión desde GitHub."""
        try:
            # URL del archivo de versión en GitHub
            url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}/ferreteria_app/config/settings.py"

            # Crear contexto SSL que no verificafic certificados (para compatibilidad)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # Hacer request
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                content = response.read().decode('utf-8')

            # Buscar APP_VERSION en el contenido
            for line in content.split('\n'):
                if 'APP_VERSION' in line and '=' in line:
                    # Extraer versión
                    version = line.split('=')[1].strip().strip('"').strip("'")
                    return version

            return None
        except Exception as e:
            print(f"Error al verificar versión: {e}")
            return None

    def check_for_updates(self):
        """Verifica si hay actualizaciones disponibles."""
        latest = self.get_latest_version()

        if latest is None:
            return {
                'available': False,
                'message': 'No se pudo verificar actualizaciones',
                'latest_version': None
            }

        # Comparar versiones
        current = self._parse_version(self.version)
        new = self._parse_version(latest)

        if new > current:
            return {
                'available': True,
                'current_version': self.version,
                'latest_version': latest,
                'message': f'Nueva versión disponible: {latest}'
            }
        else:
            return {
                'available': False,
                'current_version': self.version,
                'latest_version': latest,
                'message': 'Ya tienes la última versión'
            }

    def _parse_version(self, version_str):
        """Convierte string de versión a tuple para comparar."""
        try:
            parts = version_str.split('.')
            return tuple(int(p) for p in parts)
        except:
            return (0, 0, 0)

    def download_update(self, callback=None):
        """Descarga la actualización desde GitHub."""
        try:
            # URL base del repo
            base_url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}"

            # Archivos a descargar
            files_to_update = [
                'ferreteria_app/config/settings.py',
                'ferreteria_app/main.py',
                'ferreteria_app/ui/main_window.py',
                'ferreteria_app/ui/inventory_tab.py',
                'ferreteria_app/ui/sales_tab.py',
                'ferreteria_app/ui/reports_tab.py',
            ]

            # Determinar carpeta destino
            if getattr(sys, 'frozen', False):
                base_dir = Path(sys.executable).parent
            else:
                base_dir = Path(__file__).parent.parent

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            downloaded = []

            for file_path in files_to_update:
                url = f"{base_url}/{file_path}"

                try:
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
                        content = response.read().decode('utf-8')

                    # Guardar archivo
                    dest_path = base_dir / file_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    dest_path.write_text(content, encoding='utf-8')

                    downloaded.append(file_path)

                    if callback:
                        callback(f"Descargado: {file_path}")

                except Exception as e:
                    print(f"Error descargando {file_path}: {e}")

            return {
                'success': True,
                'downloaded': downloaded,
                'message': f'Actualizados {len(downloaded)} archivos'
            }

        except Exception as e:
            return {
                'success': False,
                'downloaded': [],
                'message': f'Error: {str(e)}'
            }
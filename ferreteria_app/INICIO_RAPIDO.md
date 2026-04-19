# Guía de Inicio Rápido

## 🚀 Instalación en 3 Pasos

### Paso 1: Instalar Dependencias

Abra una terminal en la carpeta `ferreteria_app` y ejecute:

```bash
pip install -r requirements.txt
```

**¿Qué instala?**
- `openpyxl` - Para exportar a Excel
- `bcrypt` - Para seguridad de contraseñas

**Tiempo estimado:** 1-2 minutos

---

### Paso 2: Ejecutar la Aplicación

```bash
python main.py
```

**¿Qué pasa?**
- Se crea la carpeta `data_storage/` con los archivos JSON
- Se crea el usuario administrador
- Se abre la ventana de login

**Usuario de prueba:** `admin` / `admin123`

---

### Paso 3: (Opcional) Cargar Datos de Demostración

Si quiere ver la aplicación con datos de ejemplo:

```bash
python load_demo_data.py
```

Luego reinicie la aplicación con `python main.py`

---

## 📋 Estructura Rápida

```
ferreteria_app/
├── main.py                  ← EJECUTE ESTO
├── requirements.txt         ← Dependencias
├── README.md               ← Documentación completa
├── ARQUITECTURA.md         ← Detalles técnicos
├── ui/                     ← Interfaz gráfica
├── business/               ← Lógica de negocio
├── data/                   ← Acceso a datos
├── utils/                  ← Herramientas
├── config/                 ← Configuración
└── data_storage/           ← Datos (se crea automáticamente)
```

---

## 🎯 Primera Vez Usando la Aplicación

1. **Inicie sesión:** admin / admin123
2. **Vaya a Inventario:** Haga clic en "📦 Inventario"
3. **Añada un producto:** Haga clic en "➕ Nuevo"
4. **Registre una venta:** Vaya a "💳 Ventas"
5. **Vea reportes:** Haga clic en "📊 Reportes"
6. **Exporte a Excel:** Botón "📥 Exportar a Excel"

---

## 🛠️ Generar Ejecutable para Windows

### Requisito Previo
```bash
pip install pyinstaller
```

### Generar .exe
```bash
python build_exe.py
```

El archivo `Ferreteria.exe` se creará en la carpeta `dist/`

**Distribución:**
- Copie solo el archivo `Ferreteria.exe`
- No necesita Python instalado
- No necesita `data_storage/` (se crea automáticamente)

---

## ❓ Preguntas Frecuentes

### P: ¿Dónde se guardan los datos?
**R:** En `data_storage/` como archivos JSON

### P: ¿Es seguro para producción?
**R:** Es un prototipo. Para producción, migre a SQLite (ver `ARQUITECTURA.md`)

### P: ¿Puedo cambiar la contraseña de admin?
**R:** 
1. Inicie con admin / admin123
2. Vaya a "Registrarse" para crear otro usuario
3. Delete el usuario admin manualmente del archivo `data_storage/users.json`

### P: ¿Qué pasa si pierdo mis datos?
**R:** Copie `data_storage/` regularmente como backup

### P: ¿Funciona en Mac/Linux?
**R:** Sí, pero primero instale Tkinter:
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **Mac:** `brew install python-tk`

### P: El programa es lento
**R:**
- Tiene demasiados datos (JSON es lento con > 10000 registros)
- Considere migrar a SQLite (ver `ARQUITECTURA.md`)

---

## 📞 Soporte

Si tiene problemas:

1. **Error: ModuleNotFoundError** → `pip install -r requirements.txt`
2. **Error: Tkinter not found** → Instale python3-tk (ver arriba)
3. **Los datos no se guardan** → Verifique permisos de carpeta
4. **El .exe no funciona** → Reinstale Python y regenere con `build_exe.py`

---

## 🎓 Próximos Pasos

- Lea `README.md` para documentación completa
- Revise `ARQUITECTURA.md` para entender el código
- Consulte `tests.py` para ver ejemplos de uso
- Personalice los colores en `config/settings.py`

---

**¿Listo?** Execute `python main.py` ¡Ahora!

---

**Última actualización:** 18 de Abril de 2026

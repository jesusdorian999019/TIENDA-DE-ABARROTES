import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from config.settings import (
    APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, PRIMARY_COLOR, 
    SECONDARY_COLOR, LIGHT_BG, TEXT_COLOR, SUCCESS_COLOR, WARNING_COLOR
)
from business.user_service import UserService


class LoginWindow:
    """Ventana de login de la aplicación."""
    
    def __init__(self, root):
        """Inicializa la ventana de login."""
        self.root = root
        self.root.title(f"{APP_TITLE} - Login")
        
        # Configurar tamaño
        window_width = 400
        window_height = 300
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular posición central
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Configurar geometría (centrada)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        
        # Hacer la ventana siempre visible
        self.root.deiconify()  # Asegurar que se muestre
        self.root.lift()       # Traer al frente
        self.root.focus()      # Dar foco
        
        self.user_service = UserService()
        self.current_user = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de login."""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = ttk.Label(
            main_frame,
            text=APP_TITLE,
            font=("Helvetica", 18, "bold")
        )
        title.pack(pady=20)
        
        # Username
        ttk.Label(main_frame, text="Usuario:").pack(anchor=tk.W, pady=(10, 0))
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        username_entry.pack(pady=(0, 10), fill=tk.X)
        username_entry.focus()
        
        # Password
        ttk.Label(main_frame, text="Contraseña:").pack(anchor=tk.W)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, width=30, show="*")
        password_entry.pack(pady=(0, 20), fill=tk.X)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        login_btn = ttk.Button(button_frame, text="Ingresar", command=self._login)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        register_btn = ttk.Button(button_frame, text="Registrarse", command=self._register)
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        password_entry.bind('<Return>', lambda e: self._login())
        
        # Nota
        note = ttk.Label(
            main_frame,
            text="Demo: admin / admin123",
            font=("Helvetica", 9),
            foreground="gray"
        )
        note.pack(pady=10)
    
    def _login(self):
        """Intenta hacer login."""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        success, message = self.user_service.authenticate(username, password)
        
        if success:
            self.current_user = username
            self.root.destroy()  # Cerrar login window
        else:
            messagebox.showerror("Error", message)
    
    def _register(self):
        """Registra un nuevo usuario."""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        success, message = self.user_service.create_user(username, password)
        
        if success:
            messagebox.showinfo("Éxito", message + "\nAhora puede ingresar con sus credenciales")
            self.username_var.set("")
            self.password_var.set("")
        else:
            messagebox.showerror("Error", message)
    
    def show(self):
        """Muestra la ventana de login."""
        self.root.mainloop()
        return self.current_user

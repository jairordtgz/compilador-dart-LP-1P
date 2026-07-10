import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from lexer.lexer import analizar as analizar_lexico
from parser.parser import analizar_sintactico, errores_sintacticos
from parser.parser import analizar_semantico, errores_semanticos


COLORES_TOKEN = {
    'PALABRA_RESERVADA': '#6A4C93',
    'TIPO':               '#3B8BD4',
    'LITERAL':             '#1D9E75',
    'OPERADOR':            '#B8860B',
    'IDENTIFICADOR':       '#222222',
}

PALABRAS_RESERVADAS = {
    'VAR','INT','DOUBLE','STRING_TYPE','BOOL','DYNAMIC','FINAL','CONST',
    'VOID','RETURN','IF','ELSE','WHILE','FOR','IN','BREAK','CONTINUE',
    'PRINT','NULL','TRUE','FALSE','IMPORT','LIST_TYPE','MAP_TYPE','SET_TYPE',
}
TIPOS = {'INT','DOUBLE','STRING_TYPE','BOOL','LIST_TYPE','MAP_TYPE','SET_TYPE','VAR','DYNAMIC'}
LITERALES = {'ENTERO','FLOTANTE','CADENA','TRUE','FALSE'}
OPERADORES = {
    'MAS','MENOS','PRODUCTO','DIVISION','DIVISION_ENTERA','MODULO',
    'IGUAL_IGUAL','DIFERENTE','MENOR','MAYOR','MENOR_IGUAL','MAYOR_IGUAL',
    'ASIGNACION','MAS_IGUAL','MENOS_IGUAL','PRODUCTO_IGUAL','DIVISION_IGUAL',
    'AND','OR','NOT',
}


def clasificar_token(tipo_token):
    if tipo_token in TIPOS:
        return 'TIPO'
    if tipo_token in PALABRAS_RESERVADAS:
        return 'PALABRA_RESERVADA'
    if tipo_token in LITERALES:
        return 'LITERAL'
    if tipo_token in OPERADORES:
        return 'OPERADOR'
    return 'IDENTIFICADOR'


class DartAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Dart — Léxico, Sintáctico y Semántico (PLY)")
        self.geometry("1150x680")

        self._build_toolbar()
        self._build_panels()
        self._build_statusbar()
        self._cargar_algoritmo_por_defecto()

    # ------------------------------------------------------------
    # TOOLBAR
    # ------------------------------------------------------------
    def _build_toolbar(self):
        barra = ttk.Frame(self, padding=6)
        barra.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(barra, text="Analizar Léxico",
                   command=self.accion_lexico).pack(side=tk.LEFT, padx=3)

        ttk.Button(barra, text="Analizar Sintáctico",
                   command=self.accion_sintactico).pack(side=tk.LEFT, padx=3)

        ttk.Button(barra, text="Analizar Semántico",
                   command=self.accion_semantico).pack(side=tk.LEFT, padx=3)

        ttk.Separator(barra, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)

        ttk.Button(barra, text="Limpiar",
                   command=self.accion_limpiar).pack(side=tk.LEFT, padx=3)

        ttk.Button(barra, text="Exportar log",
                   command=self.accion_exportar).pack(side=tk.LEFT, padx=3)

    # ------------------------------------------------------------
    # PANELES (editor izquierda / resultados derecha)
    # ------------------------------------------------------------
    def _build_panels(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # --- Panel izquierdo: editor con numeros de linea ---
        panel_izq = ttk.Frame(contenedor)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        ttk.Label(panel_izq, text="Código fuente (Dart)").pack(anchor=tk.W)

        frame_editor = tk.Frame(panel_izq)
        frame_editor.pack(fill=tk.BOTH, expand=True)

        self.lineas = tk.Text(frame_editor, width=4, padx=4, takefocus=0,
                               border=0, background='#f0f0f0',
                               state='disabled', wrap='none')
        self.lineas.pack(side=tk.LEFT, fill=tk.Y)

        self.editor = tk.Text(frame_editor, wrap='none', undo=True,
                               font=('Consolas', 11))
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(frame_editor, orient=tk.VERTICAL,
                                  command=self._on_scroll)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor.config(yscrollcommand=scroll_y.set)

        self.editor.bind('<KeyRelease>', lambda e: self._actualizar_lineas())
        self.editor.bind('<MouseWheel>', lambda e: self.after(10, self._actualizar_lineas))

        # --- Panel derecho: pestañas de resultados ---
        panel_der = ttk.Frame(contenedor)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tabs = ttk.Notebook(panel_der)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # Pestaña Tokens (Jairo)
        self.tab_tokens = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_tokens, text="Tokens")
        self._build_tab_tokens()

        # Pestaña Sintáctico
        self.tab_sintactico = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_sintactico, text="Sintáctico")
        self._build_tab_sintactico()

        # Pestaña Semántico — TODO Benjamin
        self.tab_semantico = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_semantico, text="Semántico")
        ttk.Label(self.tab_semantico, text="Resultado del análisis semántico").pack(
            anchor=tk.W, padx=4, pady=(4, 0))
        self.texto_semantico = tk.Text(self.tab_semantico, wrap='word',
                                        font=('Consolas', 10))
        self.texto_semantico.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.texto_semantico.tag_configure('OK', foreground='#1D9E75')
        self.texto_semantico.tag_configure('ERR', foreground='#B00020')

        # Pestaña Errores — TODO Benjamin (consolidado de los 3 análisis)
        self.tab_errores = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_errores, text="Errores")
        ttk.Label(self.tab_errores, text="Errores semánticos").pack(
            anchor=tk.W, padx=4, pady=(4, 0))
        self.texto_errores = tk.Text(self.tab_errores, wrap='word',
                                      font=('Consolas', 10),
                                      foreground='#B00020',
                                      background='#FCEBEB')
        self.texto_errores.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    def _build_tab_tokens(self):
        columnas = ('linea', 'tipo', 'valor')
        self.tabla_tokens = ttk.Treeview(self.tab_tokens, columns=columnas,
                                          show='headings', height=18)
        self.tabla_tokens.heading('linea', text='Línea')
        self.tabla_tokens.heading('tipo', text='Tipo')
        self.tabla_tokens.heading('valor', text='Valor')
        self.tabla_tokens.column('linea', width=60, anchor=tk.CENTER)
        self.tabla_tokens.column('tipo', width=160)
        self.tabla_tokens.column('valor', width=200)
        self.tabla_tokens.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        for categoria, color in COLORES_TOKEN.items():
            self.tabla_tokens.tag_configure(categoria, foreground=color)

        ttk.Label(self.tab_tokens, text="Errores léxicos",
                  foreground='#B00020').pack(anchor=tk.W, padx=4)
        self.texto_errores_lexicos = tk.Text(self.tab_tokens, height=6,
                                              foreground='#B00020',
                                              background='#FCEBEB')
        self.texto_errores_lexicos.pack(fill=tk.X, padx=4, pady=(0, 4))

    def _build_tab_sintactico(self):
        ttk.Label(self.tab_sintactico, text="Resultado del análisis sintáctico").pack(
            anchor=tk.W, padx=4, pady=(4, 0))
        self.texto_sintactico = tk.Text(self.tab_sintactico, wrap='word',
                                         font=('Consolas', 10))
        self.texto_sintactico.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.texto_sintactico.tag_configure('OK', foreground='#1D9E75')
        self.texto_sintactico.tag_configure('ERR', foreground='#B00020')

    def _build_statusbar(self):
        self.status = tk.StringVar(value="Listo.")
        barra = ttk.Label(self, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W)
        barra.pack(side=tk.BOTTOM, fill=tk.X)

    # ------------------------------------------------------------
    # Editor: numeros de linea sincronizados
    # ------------------------------------------------------------
    def _on_scroll(self, *args):
        self.editor.yview(*args)
        self.lineas.yview(*args)

    def _actualizar_lineas(self):
        total = int(self.editor.index('end-1c').split('.')[0])
        contenido = '\n'.join(str(n) for n in range(1, total + 1))
        self.lineas.config(state='normal')
        self.lineas.delete('1.0', tk.END)
        self.lineas.insert('1.0', contenido)
        self.lineas.config(state='disabled')
        self.lineas.yview_moveto(self.editor.yview()[0])

    def _cargar_algoritmo_por_defecto(self):
        ruta = os.path.join(PROJECT_ROOT, 'algoritmos', 'algoritmo_jairo.dart')
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                self.editor.insert('1.0', f.read())
        self._actualizar_lineas()

    # ------------------------------------------------------------
    # ACCIONES
    # ------------------------------------------------------------
    def accion_lexico(self):
        codigo = self.editor.get('1.0', tk.END)
        tokens_encontrados, errores = analizar_lexico(codigo, 'GUI-jairordtgz', 'editor.dart')

        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        for tok in tokens_encontrados:
            categoria = clasificar_token(tok['tipo'])
            self.tabla_tokens.insert('', tk.END,
                                      values=(tok['linea'], tok['tipo'], tok['valor']),
                                      tags=(categoria,))

        self.texto_errores_lexicos.delete('1.0', tk.END)
        if errores:
            self.texto_errores_lexicos.insert('1.0', '\n'.join(errores))
        else:
            self.texto_errores_lexicos.insert('1.0', 'Sin errores léxicos.')

        self.tabs.select(self.tab_tokens)
        self.status.set(
            f"Léxico: {len(tokens_encontrados)} tokens, {len(errores)} errores. Log guardado en /logs."
        )

    def accion_sintactico(self):
        codigo = self.editor.get('1.0', tk.END)
        analizar_sintactico(codigo, 'GUI-caluloper')

        self.texto_sintactico.delete('1.0', tk.END)
        if errores_sintacticos:
            self.texto_sintactico.insert(
                '1.0',
                f"Errores sintácticos ({len(errores_sintacticos)}):\n\n"
                + '\n'.join(errores_sintacticos),
                'ERR',
            )
        else:
            self.texto_sintactico.insert(
                '1.0', 'Análisis sintáctico completado sin errores.', 'OK')

        self.tabs.select(self.tab_sintactico)
        self.status.set(
            f"Sintáctico: {len(errores_sintacticos)} error(es). Log guardado en /logs."
        )

    def accion_semantico(self):
        codigo = self.editor.get('1.0', tk.END)
        analizar_semantico(codigo, 'GUI-ibcg04')

        self.texto_semantico.delete('1.0', tk.END)
        self.texto_errores.delete('1.0', tk.END)

        if errores_semanticos:
            resultado = (
                f"Errores semánticos ({len(errores_semanticos)}):\n\n"
                + '\n'.join(errores_semanticos)
            )
            self.texto_semantico.insert('1.0', resultado, 'ERR')
            self.texto_errores.insert('1.0', resultado)
        else:
            self.texto_semantico.insert(
                '1.0', 'Análisis semántico completado sin errores.', 'OK')
            self.texto_errores.insert('1.0', 'Sin errores semánticos.')

        self.tabs.select(self.tab_semantico)
        self.status.set(
            f"Semántico: {len(errores_semanticos)} error(es). Log guardado en /logs."
        )

    def accion_limpiar(self):
        self.editor.delete('1.0', tk.END)
        self._actualizar_lineas()
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        self.texto_errores_lexicos.delete('1.0', tk.END)
        self.status.set("Editor limpiado.")

    def accion_exportar(self):
        carpeta_logs = os.path.join(PROJECT_ROOT, 'logs')
        messagebox.showinfo("Logs", f"Los logs se guardan automáticamente en:\n{carpeta_logs}")


if __name__ == '__main__':
    app = DartAnalyzerApp()
    app.mainloop()

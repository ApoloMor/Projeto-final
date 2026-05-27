from customtkinter import *
from tkinter import ttk

# =====================================
# CONFIGURAÇÃO DA JANELA
# =====================================

app = CTk()
app.title("Game Store - Produtos")
app.geometry("1400x800")
app.configure(fg_color="#F3F4F6")

# =====================================
# SIDEBAR
# =====================================

sidebar = CTkFrame(
    app,
    width=240,
    fg_color="#081120",
    corner_radius=0
)
sidebar.pack(side="left", fill="y")

# LOGO

logo = CTkLabel(
    sidebar,
    text="GAME STORE",
    font=("Poppins", 28, "bold"),
    text_color="white"
)
logo.pack(pady=(40, 5))

subtitle = CTkLabel(
    sidebar,
    text="BOARD GAMES & CARD GAMES",
    font=("Poppins", 11),
    text_color="#FACC15"
)
subtitle.pack(pady=(0, 40))

# MENU

menus = [
    "🏠 Início",
    "📦 Produtos",
    "👥 Clientes",
    "🚚 Fornecedores",
    "🏆 Eventos",
    "🛒 Vendas",
    "📊 Relatórios",
    "⚙️ Configurações"
]

for menu in menus:

    color = "#6D4AFF" if "Produtos" in menu else "transparent"

    btn = CTkButton(
        sidebar,
        text=menu,
        height=45,
        fg_color=color,
        hover_color="#7C5CFF",
        anchor="w",
        font=("Poppins", 15)
    )

    btn.pack(fill="x", padx=15, pady=5)

# =====================================
# ÁREA PRINCIPAL
# =====================================

main = CTkFrame(app, fg_color="#F3F4F6")
main.pack(side="left", fill="both", expand=True)

# =====================================
# TOPO
# =====================================

top_frame = CTkFrame(main, fg_color="transparent")
top_frame.pack(fill="x", padx=30, pady=20)

title_frame = CTkFrame(top_frame, fg_color="transparent")
title_frame.pack(side="left")

title = CTkLabel(
    title_frame,
    text="Produtos",
    font=("Poppins", 34, "bold"),
    text_color="#111827"
)
title.pack(anchor="w")

subtitle = CTkLabel(
    title_frame,
    text="Gerencie os produtos cadastrados na loja.",
    font=("Poppins", 14),
    text_color="#6B7280"
)
subtitle.pack(anchor="w")

# BOTÕES

buttons_frame = CTkFrame(top_frame, fg_color="transparent")
buttons_frame.pack(side="right")

novo_btn = CTkButton(
    buttons_frame,
    text="+ Novo Produto",
    width=180,
    height=45,
    fg_color="#6D4AFF",
    hover_color="#7C5CFF",
    font=("Poppins", 14, "bold")
)
novo_btn.pack(side="left", padx=10)

exportar_btn = CTkButton(
    buttons_frame,
    text="Exportar",
    width=120,
    height=45,
    fg_color="white",
    text_color="#111827",
    border_width=1,
    border_color="#D1D5DB",
    hover_color="#F3F4F6",
    font=("Poppins", 14)
)
exportar_btn.pack(side="left")

# =====================================
# BUSCA
# =====================================

search_frame = CTkFrame(main, fg_color="transparent")
search_frame.pack(fill="x", padx=30)

search = CTkEntry(
    search_frame,
    placeholder_text="Buscar produto...",
    height=45,
    font=("Poppins", 14)
)
search.pack(fill="x")

# =====================================
# CONTEÚDO
# =====================================

content = CTkFrame(main, fg_color="transparent")
content.pack(fill="both", expand=True, padx=30, pady=20)

# =====================================
# TABELA
# =====================================

table_frame = CTkFrame(
    content,
    fg_color="white",
    corner_radius=15
)
table_frame.pack(side="left", fill="both", expand=True)

columns = (
    "ID",
    "Produto",
    "Categoria",
    "Preço",
    "Estoque",
    "Status"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=15
)

# CABEÇALHOS

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

# DADOS

produtos = [
    ("001", "Magic Booster Box", "Card Game", "R$ 349,90", "25", "Disponível"),
    ("002", "Catan", "Board Game", "R$ 219,90", "4", "Estoque Baixo"),
    ("003", "Deck Box Pokémon", "Acessório", "R$ 49,90", "0", "Esgotado"),
    ("004", "Yu-Gi-Oh Structure Deck", "Card Game", "R$ 89,90", "12", "Disponível"),
]

for produto in produtos:
    tree.insert("", "end", values=produto)

tree.pack(fill="both", expand=True, padx=20, pady=20)

# =====================================
# PAINEL DIREITO
# =====================================

right_panel = CTkFrame(
    content,
    width=300,
    fg_color="transparent"
)
right_panel.pack(side="right", fill="y", padx=(20, 0))

# =====================================
# RESUMO
# =====================================

summary_card = CTkFrame(
    right_panel,
    fg_color="white",
    corner_radius=15
)
summary_card.pack(fill="x", pady=(0, 20))

summary_title = CTkLabel(
    summary_card,
    text="Resumo do estoque",
    font=("Poppins", 20, "bold"),
    text_color="#111827"
)
summary_title.pack(anchor="w", padx=20, pady=20)

infos = [
    ("Total de produtos", "132"),
    ("Board Games", "48"),
    ("Card Games", "63"),
    ("Acessórios", "21")
]

for texto, valor in infos:

    frame = CTkFrame(summary_card, fg_color="transparent")
    frame.pack(fill="x", padx=20, pady=8)

    label_text = CTkLabel(
        frame,
        text=texto,
        font=("Poppins", 14),
        text_color="#6B7280"
    )
    label_text.pack(side="left")

    label_value = CTkLabel(
        frame,
        text=valor,
        font=("Poppins", 15, "bold"),
        text_color="#6D4AFF"
    )
    label_value.pack(side="right")

# =====================================
# FILTROS
# =====================================

filter_card = CTkFrame(
    right_panel,
    fg_color="white",
    corner_radius=15
)
filter_card.pack(fill="x")

filter_title = CTkLabel(
    filter_card,
    text="Filtros",
    font=("Poppins", 20, "bold"),
    text_color="#111827"
)
filter_title.pack(anchor="w", padx=20, pady=20)

# CATEGORIA

categoria = CTkLabel(
    filter_card,
    text="Categoria",
    font=("Poppins", 14)
)
categoria.pack(anchor="w", padx=20)

categoria_combo = CTkComboBox(
    filter_card,
    values=["Todas", "Board Game", "Card Game", "Acessório"],
    height=40
)
categoria_combo.pack(fill="x", padx=20, pady=(5, 15))

# STATUS

status = CTkLabel(
    filter_card,
    text="Status",
    font=("Poppins", 14)
)
status.pack(anchor="w", padx=20)

status_combo = CTkComboBox(
    filter_card,
    values=["Todos", "Disponível", "Estoque Baixo", "Esgotado"],
    height=40
)
status_combo.pack(fill="x", padx=20, pady=(5, 15))

# PREÇO

preco = CTkLabel(
    filter_card,
    text="Preço máximo",
    font=("Poppins", 14)
)
preco.pack(anchor="w", padx=20)

preco_entry = CTkEntry(
    filter_card,
    placeholder_text="R$",
    height=40
)
preco_entry.pack(fill="x", padx=20, pady=(5, 20))

# BOTÃO

filter_btn = CTkButton(
    filter_card,
    text="Aplicar filtros",
    height=45,
    fg_color="#6D4AFF",
    hover_color="#7C5CFF",
    font=("Poppins", 14, "bold")
)
filter_btn.pack(fill="x", padx=20, pady=(0, 20))

# =====================================
# EXECUTAR
# =====================================

app.mainloop()
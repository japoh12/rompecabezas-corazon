import streamlit as st
import random
from PIL import Image, ImageDraw
import io
import base64
import os

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="💖 Rompecabezas del Corazón",
    page_icon="💖",
    layout="centered",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Quicksand:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #ffe0ec 0%, #ffd6e7 30%, #ffb3d1 60%, #ff85b3 100%);
    min-height: 100vh;
}

h1 {
    font-family: 'Pacifico', cursive !important;
    color: #c0005a !important;
    text-shadow: 2px 2px 8px rgba(192,0,90,0.25);
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #e0006a;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.ref-box {
    background: rgba(255,255,255,0.65);
    border: 2px solid #ffb3d1;
    border-radius: 18px;
    padding: 0.8rem 1rem;
    text-align: center;
    margin-bottom: 1rem;
}

.ref-title {
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
    color: #c0005a;
    font-size: 0.95rem;
    margin-bottom: 0.4rem;
}

.instructions {
    background: rgba(255,255,255,0.55);
    border-radius: 16px;
    padding: 0.8rem 1.2rem;
    color: #7a0040;
    font-size: 0.9rem;
    line-height: 1.7;
    margin-bottom: 1rem;
    border: 1.5px solid #ffb3d1;
}

.moves-badge {
    display: inline-block;
    background: #ff69b4;
    color: white;
    padding: 3px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.9rem;
    margin: 0.2rem;
}

.win-box {
    background: linear-gradient(135deg, #fff0f7, #ffe0ef);
    border: 3px solid #ff69b4;
    border-radius: 24px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 8px 40px rgba(255,105,180,0.25);
    animation: pop 0.6s ease;
}

@keyframes pop {
    0%   { transform: scale(0.7); opacity: 0; }
    70%  { transform: scale(1.07); }
    100% { transform: scale(1); opacity: 1; }
}

.win-title {
    font-family: 'Pacifico', cursive;
    font-size: 2rem;
    color: #c0005a;
    margin-bottom: 0.5rem;
}

.win-msg {
    font-size: 1.1rem;
    color: #7a0040;
    font-weight: 600;
    line-height: 1.8;
}

.stButton > button {
    background: linear-gradient(135deg, #ff69b4, #c0005a) !important;
    color: white !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.5rem 1.4rem !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(192,0,90,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.04) !important;
    box-shadow: 0 8px 20px rgba(192,0,90,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Heart mask ───────────────────────────────────────────────────────────────
HEART_MASK = [
    [0, 1, 1, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
ROWS = len(HEART_MASK)
COLS = len(HEART_MASK[0])

PIECE_EMOJIS = [
    "🌸","💕","🌷","✨","🦋","🍓","🌺","💐",
    "🎀","💫","🌼","🍒","💝","🌻","🌈","🍰",
    "🦄","🎶","🌙","💎","🍭","🎠","🌟","🍯",
    "🐝","🌿","🎁","🧁","🦢","🕊️","💖","🫶",
    "🥂","🌮","🎊","🎉","💌","🌊","🦩","🌴",
]

COLORS = [
    "#ff9eb5","#ffb3c6","#ffc8d7","#ffd6e4","#ffe0ec",
    "#ff85a1","#ff6b8a","#ff4d73","#e63965","#cc2255",
    "#ff99bb","#ffadc8","#ffc1d5","#ffd5e2","#f9a8c0",
]


def get_heart_cells():
    return [(r, c) for r in range(ROWS) for c in range(COLS) if HEART_MASK[r][c] == 1]


def make_solved_board():
    cells = get_heart_cells()
    board = [[None] * COLS for _ in range(ROWS)]
    for idx, (r, c) in enumerate(cells):
        board[r][c] = idx + 1
    return board


def shuffle_board(solved):
    cells = get_heart_cells()
    ids = [solved[r][c] for r, c in cells]
    random.shuffle(ids)
    board = [[None] * COLS for _ in range(ROWS)]
    for (r, c), pid in zip(cells, ids):
        board[r][c] = pid
    return board


def is_solved(board, solved):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != solved[r][c]:
                return False
    return True


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def build_reference_image(color_map, cell_size=40, gap=3):
    """Generate a small PIL image showing the solved heart with colors + numbers."""
    w = COLS * (cell_size + gap) + gap
    h = ROWS * (cell_size + gap) + gap
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    solved = make_solved_board()

    for r in range(ROWS):
        for c in range(COLS):
            if HEART_MASK[r][c] == 0:
                continue
            pid = solved[r][c]
            color = color_map.get(pid, "#ffb3c6")
            rgb = hex_to_rgb(color)
            x0 = gap + c * (cell_size + gap)
            y0 = gap + r * (cell_size + gap)
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            draw.rounded_rectangle([x0, y0, x1, y1], radius=8,
                                    fill=rgb + (230,), outline=(192, 0, 90, 180), width=2)
            num = str(pid)
            # center the number
            tx = x0 + cell_size // 2 - len(num) * 4
            ty = y0 + cell_size // 2 - 7
            draw.text((tx, ty), num, fill=(90, 0, 40, 255))

    return img


def pil_to_b64(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


# ─── Session state ────────────────────────────────────────────────────────────
if "solved" not in st.session_state:
    st.session_state.solved = make_solved_board()
if "board" not in st.session_state:
    st.session_state.board = shuffle_board(st.session_state.solved)
if "selected" not in st.session_state:
    st.session_state.selected = None
if "moves" not in st.session_state:
    st.session_state.moves = 0
if "won" not in st.session_state:
    st.session_state.won = False

cells = get_heart_cells()
if "emoji_map" not in st.session_state:
    st.session_state.emoji_map = {idx + 1: PIECE_EMOJIS[idx % len(PIECE_EMOJIS)]
                                   for idx, _ in enumerate(cells)}
if "color_map" not in st.session_state:
    st.session_state.color_map = {idx + 1: COLORS[idx % len(COLORS)]
                                   for idx, _ in enumerate(cells)}


def swap_pieces(r1, c1, r2, c2):
    b = st.session_state.board
    b[r1][c1], b[r2][c2] = b[r2][c2], b[r1][c1]
    st.session_state.moves += 1
    st.session_state.selected = None
    if is_solved(st.session_state.board, st.session_state.solved):
        st.session_state.won = True


def reset_game():
    st.session_state.board = shuffle_board(st.session_state.solved)
    st.session_state.selected = None
    st.session_state.moves = 0
    st.session_state.won = False


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 💖 Rompecabezas del Corazón 💖")
st.markdown('<p class="subtitle">🌸 Ordena las piezas y descubre el mensaje especial 🌸</p>',
            unsafe_allow_html=True)

# ─── WIN SCREEN ───────────────────────────────────────────────────────────────
if st.session_state.won:
    st.markdown(f"""
    <div class="win-box">
        <div class="win-title">🎉 ¡Felicitaciones! 🎉</div>
        <div class="win-msg">
            💖 <b>Feliz día Mamita</b> 💖<br><br>
            🍽️ Te has ganado una invitación a almorzar<br>
            🤞 ...cuando pase la recesión económica 😄<br><br>
            🌸🌷🌺🌻🌼🌸🌷🌺🌻🌼<br><br>
            ✨ Resolviste el rompecabezas en
            <span class="moves-badge">🔄 {st.session_state.moves} movimientos</span><br>
            ¡Eres increíble! 🦋💕
        </div>
    </div>
    """, unsafe_allow_html=True)

    for p in ["foto.jpg", "foto.jpeg", "foto.png"]:
        if os.path.exists(p):
            st.markdown("<br>", unsafe_allow_html=True)
            st.image(Image.open(p), caption="💖 ¡Para la mejor mamá del mundo! 💖",
                     use_container_width=True)
            break
    else:
        st.info("💡 Coloca una imagen llamada **foto.jpg** en la misma carpeta para verla al ganar. 🌸")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🔄 Jugar de Nuevo"):
            reset_game()
            st.rerun()

# ─── GAME SCREEN ──────────────────────────────────────────────────────────────
else:
    board  = st.session_state.board
    solved = st.session_state.solved
    sel    = st.session_state.selected
    em     = st.session_state.emoji_map
    cm     = st.session_state.color_map

    # ── Reference image ──────────────────────────────────────────────────────
    ref_img = build_reference_image(cm, cell_size=40, gap=3)
    ref_b64 = pil_to_b64(ref_img)

    st.markdown(f"""
    <div class="ref-box">
        <div class="ref-title">🗺️ Imagen de referencia — así debe quedar el corazón ✅</div>
        <img src="data:image/png;base64,{ref_b64}"
             style="max-width:340px; width:100%; border-radius:12px;
                    box-shadow:0 4px 16px rgba(192,0,90,0.2);" />
        <div style="font-size:0.8rem;color:#c0005a;margin-top:0.4rem;">
            💡 El número en cada pieza te dice cuál es su posición correcta
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Instructions ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="instructions">
        🎮 <b>Cómo jugar:</b> Haz clic en una pieza para <b>seleccionarla</b> (botón ↕),
        luego haz clic en <b>otra pieza</b> para intercambiarlas de lugar.<br>
        🎯 <b>Objetivo:</b> Que cada número quede en la posición que muestra la referencia.<br>
        ✅ Las piezas bien ubicadas muestran una marca verde.<br>
        👆 <b>Movimientos:</b> <span class="moves-badge">🔄 {st.session_state.moves}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Board ─────────────────────────────────────────────────────────────────
    for r in range(ROWS):
        if not any(HEART_MASK[r][c] for c in range(COLS)):
            continue

        cols = st.columns(COLS)
        for c in range(COLS):
            with cols[c]:
                if HEART_MASK[r][c] == 0:
                    st.markdown("<div style='height:72px'></div>", unsafe_allow_html=True)
                else:
                    pid        = board[r][c]
                    emoji      = em.get(pid, "❓")
                    color      = cm.get(pid, "#ffb3c6")
                    is_sel     = sel == (r, c)
                    is_correct = (pid == solved[r][c])

                    border = ("3px solid #c0005a" if is_sel
                              else "2px solid #44cc44" if is_correct
                              else "2px solid rgba(255,255,255,0.7)")
                    shadow = ("0 0 0 3px #c0005a, 0 4px 16px rgba(192,0,90,0.4)" if is_sel
                              else "0 3px 8px rgba(0,0,0,0.1)")
                    scale      = "1.12" if is_sel else "1"
                    check      = "✅" if is_correct else ""
                    num_color  = "#fff" if is_sel else "#7a0040"

                    st.markdown(f"""
                    <div style="
                        width:72px; height:72px;
                        background:{color};
                        border:{border};
                        border-radius:12px;
                        display:flex; flex-direction:column;
                        align-items:center; justify-content:center;
                        font-size:1.5rem;
                        box-shadow:{shadow};
                        transform:scale({scale});
                        transition:all 0.2s;
                        margin:2px auto;
                    ">
                        {emoji}
                        <span style="font-size:0.6rem;font-weight:700;color:{num_color};line-height:1">
                            #{pid} {check}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button("↕", key=f"p_{r}_{c}", help=f"Pieza #{pid} — {emoji}"):
                        if sel is None:
                            st.session_state.selected = (r, c)
                        elif sel == (r, c):
                            st.session_state.selected = None
                        else:
                            swap_pieces(sel[0], sel[1], r, c)
                        st.rerun()

    # ── Reset ─────────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🔀 Mezclar de Nuevo"):
            reset_game()
            st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#c0005a;font-family:Quicksand,sans-serif;font-size:0.85rem'>"
    "💖 Hecho con amor para el Día de la Madre 💖</p>",
    unsafe_allow_html=True,
)
import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk

BG = '#050812'
CARD = '#10182b'
BLUE = '#0b8dff'
CYAN = '#00ebff'
RED = '#ff294f'
WHITE = '#eff6ff'
MUTED = '#9dafcb'
SAVE = Path.home() / '.roma_bob_settings.json'


class FFMaxApp:
    def __init__(self, root):
        self.root = root
        self.root.title('ROMA + BOB')
        self.root.geometry('420x840')
        self.root.configure(bg=BG)

        self.assist = tk.BooleanVar(value=True)
        self.head = tk.IntVar(value=50)
        self.size = tk.IntVar(value=60)
        self.opacity = tk.IntVar(value=85)
        self.crosssize = tk.IntVar(value=60)
        self.crossop = tk.IntVar(value=100)
        self.general = tk.IntVar(value=55)
        self.red_dot = tk.IntVar(value=62)
        self.scope2 = tk.IntVar(value=48)
        self.scope4 = tk.IntVar(value=58)
        self.sniper = tk.IntVar(value=52)
        self.free_look = tk.IntVar(value=66)
        self.color = '#00dfff'
        self.active_profile = 'headshot'
        self.bubble = None
        self.control = None
        self.bubble_frozen = False
        self.dragging = False
        self.drag_offset = (0, 0)
        self.drag_start = (0, 0)

        self.load_settings()
        self.build_ui()
        self.root.protocol('WM_DELETE_WINDOW', self.close_app)
        self.sync_float_state()

    def build_ui(self):
        title = tk.Label(self.root, text='ROMA + BOB', fg=CYAN, bg=BG, font=('Arial', 24, 'bold'))
        title.pack(pady=(12, 0))

        subtitle = tk.Label(self.root, text='HEADSHOT • DRAG • MAX', fg=MUTED, bg=BG, font=('Arial', 9, 'bold'))
        subtitle.pack(pady=(0, 10))

        launch = self.card(self.root)
        tk.Label(launch, text='FREE FIRE MAX | Панель настроек', bg=CARD, fg=WHITE, font=('Arial', 11, 'bold')).pack(anchor='w', padx=10, pady=10)

        row = tk.Frame(launch, bg=CARD)
        row.pack(fill='x', padx=8, pady=6)
        self.btn(row, 'FREE FIRE MAX', lambda: self.notice('Прямой запуск Free Fire на этой платформе недоступен. Откройте игру вручную.'), '#0a6ae8').pack(side='left', expand=True, fill='x', padx=4)
        self.btn(row, 'FREE FIRE', lambda: self.notice('Прямой запуск Free Fire на этой платформе недоступен. Откройте игру вручную.'), '#1a2a4d').pack(side='left', expand=True, fill='x', padx=4)

        aim = self.card(self.root)
        tk.Label(aim, text='НАСТРОЙКИ ПРИЦЕЛА', bg=CARD, fg=CYAN, font=('Arial', 11, 'bold')).pack(anchor='w', padx=10, pady=(8, 4))
        self.canvas = tk.Canvas(aim, width=180, height=110, bg='#080d1a', highlightthickness=0)
        self.canvas.pack()
        self.draw_crosshair()
        self.slider(aim, 'Размер прицела', self.crosssize, 10, 100)
        self.slider(aim, 'Прозрачность', self.crossop, 10, 100)

        colors = tk.Frame(aim, bg=CARD)
        colors.pack(fill='x', padx=8, pady=8)
        swatches = ['#ff244e','#ffe000','#00e66b','#00dfff','#a500ff','#ffffff','#ff28a8','#ff9638']
        for c in swatches:
            tk.Button(colors, bg=c, width=2, relief='flat', bd=0, command=lambda x=c: self.set_color(x)).pack(side='left', expand=True, padx=2)

        mini = tk.Frame(aim, bg=CARD)
        mini.pack(fill='x', padx=8, pady=(2, 8))
        self.btn(mini, '−', lambda: self.adjust_cross_size(-5), '#1b2c46').pack(side='left', expand=True, fill='x', padx=3)
        self.btn(mini, '+', lambda: self.adjust_cross_size(5), '#1b2c46').pack(side='left', expand=True, fill='x', padx=3)
        self.btn(mini, 'ЗАМОРОЗИТЬ ПРИЦЕЛ', self.toggle_bubble_freeze, '#0c5dc9').pack(side='left', expand=True, fill='x', padx=3)
        self.btn(mini, 'СКРЫТЬ ПРИЦЕЛ', self.toggle_crosshair_visibility, '#3b475a').pack(side='left', expand=True, fill='x', padx=3)

        prof = self.card(self.root)
        tk.Label(prof, text='ПРОФИЛИ ЧУВСТВИТЕЛЬНОСТИ', bg=CARD, fg=CYAN, font=('Arial', 11, 'bold')).pack(anchor='w', padx=10, pady=(8, 5))
        grid = tk.Frame(prof, bg=CARD)
        grid.pack(fill='x', padx=6, pady=4)
        names = ['HEADSHOT', 'ONE TAP', 'DRAG SHOT', 'RUSH', 'PRO PLAYER', 'MAX DRAG']
        for idx, name in enumerate(names):
            btn = self.btn(grid, name, lambda n=name: self.set_profile(n), '#172e4d' if n != 'MAX DRAG' else '#3d2a07', '#ffe06d' if n == 'MAX DRAG' else WHITE)
            btn.grid(row=idx // 3, column=idx % 3, sticky='ew', padx=3, pady=3)
        for i in range(3):
            grid.columnconfigure(i, weight=1)

        rcard = self.card(self.root)
        tk.Label(rcard, text='КРАСНАЯ КНОПКА R', bg=CARD, fg=CYAN, font=('Arial', 11, 'bold')).pack(anchor='w', padx=10, pady=(8, 4))
        self.slider(rcard, 'HEADSHOT', self.head, 10, 100)
        self.slider(rcard, 'Размер круглой кнопки', self.size, 20, 100)
        self.slider(rcard, 'Прозрачность кнопки', self.opacity, 10, 100)

        toggle = tk.Frame(rcard, bg=CARD)
        toggle.pack(fill='x', padx=10, pady=(6, 8))
        tk.Checkbutton(toggle, text='AssistiveTouch / плавающая кнопка', variable=self.assist, command=self.sync_float_state, bg=CARD, fg=WHITE, selectcolor='#172b4b', activebackground=CARD, activeforeground=CYAN, font=('Arial', 10, 'bold')).pack(anchor='w')
        tk.Label(toggle, text='Выключи переключатель — появится круглая красная R-кнопка.', bg=CARD, fg=MUTED, font=('Arial', 8)).pack(anchor='w', pady=(3, 0))

        sens = self.card(self.root)
        tk.Label(sens, text='ОБЩАЯ ЧУВСТВИТЕЛЬНОСТЬ', bg=CARD, fg=CYAN, font=('Arial', 11, 'bold')).pack(anchor='w', padx=10, pady=(8, 4))
        self.slider(sens, 'Общая чувствительность', self.general, 10, 100)
        self.slider(sens, 'Красная точка', self.red_dot, 10, 100)
        self.slider(sens, 'Прицел 2X', self.scope2, 10, 100)
        self.slider(sens, 'Прицел 4X', self.scope4, 10, 100)
        self.slider(sens, 'Снайперский прицел', self.sniper, 10, 100)
        self.slider(sens, 'Свободный обзор', self.free_look, 10, 100)

        actions = tk.Frame(self.root, bg=BG)
        actions.pack(fill='x', padx=12, pady=10)
        self.btn(actions, 'СБРОС', self.reset_app, '#34205e').pack(side='left', expand=True, fill='x', padx=3)
        self.btn(actions, 'СОХРАНИТЬ', lambda: self.save_settings(True), '#075bd5').pack(side='left', expand=True, fill='x', padx=3)

        self.status = tk.Label(self.root, text='Готово', bg=BG, fg=MUTED, font=('Arial', 8))
        self.status.pack(pady=(0, 6))

    def card(self, parent):
        frame = tk.Frame(parent, bg=CARD, highlightbackground='#183b71', highlightthickness=1)
        frame.pack(fill='x', padx=12, pady=6)
        return frame

    def btn(self, parent, text, command, bg='#102a56', fg=WHITE):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg, activebackground='#0d4db4', activeforeground='white', relief='flat', bd=0, highlightthickness=0, font=('Arial', 9, 'bold'), cursor='hand2', padx=7, pady=7)

    def slider(self, parent, title, var, lo, hi):
        frame = tk.Frame(parent, bg=CARD)
        frame.pack(fill='x', padx=12, pady=3)
        label = tk.Label(frame, text=f'{title}: {var.get()}%', bg=CARD, fg=WHITE, font=('Arial', 9, 'bold'))
        label.pack(anchor='w')
        ttk.Scale(frame, from_=lo, to=hi, variable=var, style='Blue.Horizontal.TScale', command=lambda val: label.config(text=f'{title}: {int(float(val))}%')).pack(fill='x', pady=3)

    def draw_crosshair(self):
        if not hasattr(self, 'canvas'):
            return
        canvas = self.canvas
        canvas.delete('all')
        cx, cy = 90, 55
        r = max(12, self.crosssize.get() * 0.45)
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=self.color, width=3, stipple='gray50')
        canvas.create_line(cx, cy-r-10, cx, cy-r+8, fill=RED, width=3)
        canvas.create_line(cx, cy+r-8, cx, cy+r+10, fill='#ffe500', width=3)
        canvas.create_line(cx-r-10, cy, cx-r+8, cy, fill='#ff315a', width=3)
        canvas.create_line(cx+r-8, cy, cx+r+10, cy, fill=CYAN, width=3)
        canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill='white', outline='')

    def set_color(self, color):
        self.color = color
        self.draw_crosshair()

    def adjust_cross_size(self, delta):
        self.crosssize.set(max(10, min(100, self.crosssize.get() + delta)))
        self.draw_crosshair()

    def set_profile(self, name):
        self.active_profile = name.lower().replace(' ', '_')
        self.head.set(100)
        self.notice(f'Профиль: {name}')
        self.save_settings(False)

    def notice(self, text):
        self.status.config(text=text)

    def toggle_bubble_freeze(self):
        if self.bubble and self.bubble.winfo_exists():
            self.bubble_frozen = not self.bubble_frozen
            self.notice('Положение зафиксировано' if self.bubble_frozen else 'Перемещение снова доступно')
            return
        self.notice('Кнопка R не активна')

    def toggle_crosshair_visibility(self):
        if hasattr(self, 'canvas'):
            current = self.canvas.cget('state')
            self.canvas.configure(state='hidden' if current != 'hidden' else 'normal')
            self.notice('Прицел скрыт' if current != 'hidden' else 'Прицел показан')

    def sync_float_state(self):
        if self.assist.get():
            self.hide_bubble()
            self.notice('AssistiveTouch активен')
        else:
            self.show_bubble()
            self.notice('Круглая красная кнопка активна')
        self.save_settings(False)

    def show_bubble(self):
        if self.bubble and self.bubble.winfo_exists():
            self.bubble.deiconify();
            return
        self.bubble = tk.Toplevel(self.root)
        self.bubble.overrideredirect(True)
        self.bubble.attributes('-topmost', True)
        d = max(44, min(80, int(self.size.get()) + 12))
        self.bubble.geometry(f'{d}x{d}+40+220')
        self.bubble.configure(bg=BG)
        self.bubble_canvas = tk.Canvas(self.bubble, width=d, height=d, bg=BG, highlightthickness=0)
        self.bubble_canvas.pack(fill='both', expand=True)
        self.draw_bubble()
        self.bubble.bind('<ButtonPress-1>', self.drag_start_bubble)
        self.bubble.bind('<B1-Motion>', self.drag_move_bubble)
        self.bubble.bind('<ButtonRelease-1>', self.click_bubble)

    def draw_bubble(self):
        if not self.bubble or not self.bubble.winfo_exists():
            return
        d = max(44, min(80, int(self.size.get()) + 12))
        c = self.bubble_canvas
        c.delete('all')
        cx = d / 2
        cy = d / 2
        r = d * 0.42
        c.create_oval(cx-r, cy-r, cx+r, cy+r, fill='#ff2b5d', outline='#ff9ab1', width=max(2, int(d * 0.12)))
        c.create_text(cx, cy, text='R', fill='white', font=('Arial', max(18, int(d * 0.42)), 'bold'))

    def drag_start_bubble(self, event):
        self.drag_start = (event.x_root - self.bubble.winfo_x(), event.y_root - self.bubble.winfo_y())
        self.dragging = False

    def drag_move_bubble(self, event):
        if self.bubble_frozen or self.assist.get():
            return
        x = event.x_root - self.drag_start[0]
        y = event.y_root - self.drag_start[1]
        self.bubble.geometry(f'+{x}+{y}')
        self.dragging = True

    def click_bubble(self, event):
        if not self.dragging:
            self.open_control_panel()

    def hide_bubble(self):
        if self.bubble and self.bubble.winfo_exists():
            self.bubble.destroy()
        self.bubble = None
        self.bubble_canvas = None

    def open_control_panel(self):
        if self.control and self.control.winfo_exists():
            self.control.lift();
            return
        self.control = tk.Toplevel(self.root)
        self.control.title('ROMA + BOB')
        self.control.geometry('360x380')
        self.control.attributes('-topmost', True)
        self.control.configure(bg=BG)
        tk.Label(self.control, text='ROMA + BOB', bg=BG, fg=CYAN, font=('Arial', 18, 'bold')).pack(pady=(12, 6))
        tk.Frame(self.control, bg=BLUE, height=2).pack(fill='x', padx=16)
        preview = tk.Canvas(self.control, width=170, height=170, bg=BG, highlightthickness=0)
        preview.pack(pady=8)
        cx = 85; cy = 85; r = max(28, min(72, int(self.size.get()) * 0.7))
        preview.create_oval(cx-r, cy-r, cx+r, cy+r, outline='#168cff', width=4)
        preview.create_arc(cx-r, cy-r, cx+r, cy+r, start=110, extent=160, style='arc', outline=RED, width=5)
        preview.create_line(cx, cy-r-12, cx, cy-r+8, fill='white', width=3)
        preview.create_line(cx, cy+r-8, cx, cy+r+12, fill='white', width=3)
        preview.create_line(cx-r-12, cy, cx-r+8, cy, fill=RED, width=3)
        preview.create_line(cx+r-8, cy, cx+r+12, cy, fill=CYAN, width=3)
        preview.create_oval(cx-6, cy-6, cx+6, cy+6, fill=RED, outline='white')

        box = tk.Frame(self.control, bg=CARD)
        box.pack(fill='x', padx=15, pady=5)
        tk.Label(box, text=f'Headshot: {self.head.get()}% (10–100%)', bg=CARD, fg=WHITE, font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=(9, 2))
        ttk.Scale(box, from_=10, to=100, variable=self.head, style='Blue.Horizontal.TScale').pack(fill='x', padx=10, pady=(0, 9))
        tk.Label(box, text=f'Размер круглой кнопки: {self.size.get()}%', bg=CARD, fg=WHITE, font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=(3, 2))
        ttk.Scale(box, from_=20, to=100, variable=self.size, style='Blue.Horizontal.TScale').pack(fill='x', padx=10, pady=(0, 10))
        freeze_btn = self.btn(self.control, 'ЗАМОРОЗИТЬ ПОЗИЦИЮ' if not self.bubble_frozen else 'РАЗМОРОЗИТЬ ПОЗИЦИЮ', self.toggle_bubble_freeze, '#9b2442' if self.bubble_frozen else '#075bd5')
        freeze_btn.pack(fill='x', padx=18, pady=(8, 5))
        self.btn(self.control, 'ЗАКРЫТЬ', self.control.destroy, '#26324d').pack(fill='x', padx=18, pady=5)

    def reset_app(self):
        self.head.set(50)
        self.size.set(60)
        self.opacity.set(85)
        self.crosssize.set(60)
        self.crossop.set(100)
        self.general.set(55)
        self.red_dot.set(62)
        self.scope2.set(48)
        self.scope4.set(58)
        self.sniper.set(52)
        self.free_look.set(66)
        self.color = '#00dfff'
        self.active_profile = 'headshot'
        self.notice('Сброшено')
        self.save_settings(False)

    def save_settings(self, announce=False):
        data = {
            'assist': self.assist.get(),
            'headshot': self.head.get(),
            'size': self.size.get(),
            'opacity': self.opacity.get(),
            'crosssize': self.crosssize.get(),
            'crossop': self.crossop.get(),
            'general': self.general.get(),
            'red_dot': self.red_dot.get(),
            'scope2': self.scope2.get(),
            'scope4': self.scope4.get(),
            'sniper': self.sniper.get(),
            'free_look': self.free_look.get(),
            'color': self.color,
            'bubble_frozen': self.bubble_frozen,
            'active_profile': self.active_profile,
        }
        try:
            SAVE.write_text(json.dumps(data), encoding='utf-8')
        except OSError:
            pass
        if announce:
            self.notice('Настройки сохранены')

    def load_settings(self):
        try:
            payload = json.loads(SAVE.read_text(encoding='utf-8'))
            self.assist.set(payload.get('assist', True))
            self.head.set(payload.get('headshot', 50))
            self.size.set(payload.get('size', 60))
            self.opacity.set(payload.get('opacity', 85))
            self.crosssize.set(payload.get('crosssize', 60))
            self.crossop.set(payload.get('crossop', 100))
            self.general.set(payload.get('general', 55))
            self.red_dot.set(payload.get('red_dot', 62))
            self.scope2.set(payload.get('scope2', 48))
            self.scope4.set(payload.get('scope4', 58))
            self.sniper.set(payload.get('sniper', 52))
            self.free_look.set(payload.get('free_look', 66))
            self.color = payload.get('color', '#00dfff')
            self.bubble_frozen = bool(payload.get('bubble_frozen', False))
            self.active_profile = payload.get('active_profile', 'headshot')
        except (OSError, ValueError, TypeError):
            pass

    def close_app(self):
        self.save_settings(False)
        self.hide_bubble()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    FFMaxApp(root)
    root.mainloop()

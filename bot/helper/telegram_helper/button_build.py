from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

try:
    from pyrogram.enums import ButtonStyle
    _STYLE_SUPPORTED = True
except ImportError:
    ButtonStyle = None
    _STYLE_SUPPORTED = False

STYLE_MAP = {
    'red': 'DANGER',
    'danger': 'DANGER',
    'green': 'SUCCESS',
    'success': 'SUCCESS',
    'blue': 'PRIMARY',
    'primary': 'PRIMARY',
    'default': 'DEFAULT',
}


def _resolve_style(style):
    """Return a ButtonStyle if the installed pyrogram/pyrofork build supports
    it, otherwise None (older pyrofork builds have no style/color param at
    all on InlineKeyboardButton, so we must not pass one)."""
    if not _STYLE_SUPPORTED or style is None:
        return None
    if isinstance(style, ButtonStyle):
        return style
    name = STYLE_MAP.get(str(style).lower())
    return getattr(ButtonStyle, name, None) if name else None


class ButtonMaker:
    def __init__(self):
        self.__button = []
        self.__header_button = []
        self.__first_body_button = []
        self.__last_body_button = []
        self.__footer_button = []

    def ubutton(self, key, link, position=None, style=None):
        kwargs = {'text': key, 'url': link}
        resolved = _resolve_style(style)
        if resolved is not None:
            kwargs['style'] = resolved
        if not position:
            self.__button.append(InlineKeyboardButton(**kwargs))
        elif position == 'header':
            self.__header_button.append(InlineKeyboardButton(**kwargs))
        elif position == 'f_body':
            self.__first_body_button.append(InlineKeyboardButton(**kwargs))
        elif position == 'l_body':
            self.__last_body_button.append(InlineKeyboardButton(**kwargs))
        elif position == 'footer':
            self.__footer_button.append(InlineKeyboardButton(**kwargs))

    def ibutton(self, key, data, position=None, style=None):
        kwargs = {'text': key, 'callback_data': data}
        resolved = _resolve_style(style)
        if resolved is not None:
            kwargs['style'] = resolved
        if not position:
            self.__button.append(InlineKeyboardButton(**kwargs))
        elif position == 'header':
            self.__header_button.append(InlineKeyboardButton(**kwargs))
        elif position == 'f_body':
            self.__first_body_button.append(InlineKeyboardButton(**kwargs))
        elif position == 'l_body':
            self.__last_body_button.append(InlineKeyboardButton(**kwargs))
        elif position == 'footer':
            self.__footer_button.append(InlineKeyboardButton(**kwargs))

    def build_menu(self, b_cols=1, h_cols=8, fb_cols=2, lb_cols=2, f_cols=8):
        menu = [self.__button[i:i+b_cols]
                for i in range(0, len(self.__button), b_cols)]
        if self.__header_button:
            if len(self.__header_button) > h_cols:
                header_buttons = [self.__header_button[i:i+h_cols]
                                  for i in range(0, len(self.__header_button), h_cols)]
                menu = header_buttons + menu
            else:
                menu.insert(0, self.__header_button)
        if self.__first_body_button:
            if len(self.__first_body_button) > fb_cols:
                [menu.append(self.__first_body_button[i:i+fb_cols])
                 for i in range(0, len(self.__first_body_button), fb_cols)]
            else:
                menu.append(self.__first_body_button)
        if self.__last_body_button:
            if len(self.__last_body_button) > lb_cols:
                [menu.append(self.__last_body_button[i:i+lb_cols])
                 for i in range(0, len(self.__last_body_button), lb_cols)]
            else:
                menu.append(self.__last_body_button)
        if self.__footer_button:
            if len(self.__footer_button) > f_cols:
                [menu.append(self.__footer_button[i:i+f_cols])
                 for i in range(0, len(self.__footer_button), f_cols)]
            else:
                menu.append(self.__footer_button)
        return InlineKeyboardMarkup(menu)

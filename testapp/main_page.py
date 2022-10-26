from vkbottle import KeyboardButtonColor

from src.button.button_data import ButtonData, ButtonCallback
from src.button.button_function import ButtonFunction
from src.communication.api import ApiType
from src.page.page import Page


class MainPage(Page):
    async def handle_contact(self, user, phone):
        await self._send_message(user, f"Номер {phone} получен")

    def _initialize(self, markup_factory):
        super()._initialize(markup_factory)
        self.bot_events.subscribe_contact_share(self.handle_contact)

    async def make_render_content(self, user):
        useless_button = ButtonData("User ID", ButtonCallback(self._send_message,
                                                              message=f"User {user.id} has pressed an useless button!"))
        native_args_button = ButtonData("Native Args", ButtonCallback(self.navigator.change_page, path='/nargs'))

        if self.api.api_type == ApiType.Vk:
            info_button = ButtonData("Info", ButtonCallback(self.navigator.change_page, path='/info'), color=KeyboardButtonColor.PRIMARY)
            # TODO: add navigate to input page button
            bottom_button = None
        else:
            info_button = ButtonData("Info", ButtonCallback(self.navigator.change_page, path='/info'))
            bottom_button = ButtonData("Phone", None,
                                       ButtonFunction.request_phone)

        self.markup.add_row([
            useless_button,
            native_args_button,
            info_button
        ])
        if bottom_button:
            self.markup.add_row([bottom_button])
        await self._send_keyboard_message(user, self.markup, 'Main')

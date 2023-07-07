from nicegui import ui
import asyncio

# internal imports
from backends.sqlite_backend import search_async
from backends.backend import ResultList
from settings import images
from helpers import CreateHtml


class EasyDict:
    def __init__(self):
        self.title = "EasyDict-GUI"
        self.lang = "eng"
        self.results = ResultList()
        self.task = None
        self.search_limit = 1

    def create_header(self):
        with ui.header().classes(add="column", replace="row") as header:
            ui.button(on_click=lambda: left_drawer.toggle()).props(
                "flat color=white icon=menu"
            )
            self.search_entry = ui.input(
                placeholder="start typing",
                on_change=self.search_in_db,
                validation={"Input too short": lambda value: len(value) >= self.search_limit},
            ).style("width: 100%; margin-right: 10px; margin-left: 10px;").props('clearable')
            self.search_type = ui.toggle(
                options={
                    "first_chars": "First chars",
                    "fulltext": "Fulltext",
                    "whole_word": "Whole word",
                },
                value="first_chars",
                on_change=self.search_in_db,
            ).style("width: 100%;")

        with ui.left_drawer() as left_drawer:
            ui.label("Side menu")

    @ui.refreshable
    def create_body(self):
        with ui.column().style(
            "justify-content: center; margin: auto; display: flex;"
        ) as self.main_column:
            if not self.results.items:
                ui.label("Welcome to EasyDict").style(
                    "text-align: center; font-weight: bold; font-size: 140%; justify-content: center; margin: auto; display: flex;"
                )
                ui.image(images["ed_icon.png"]).style("justify-content: center;")

                ui.label(
                    "The first open source translator which is completely open with dictionary data too."
                ).style(
                    "text-align: center; font-weight: bold; font-size: 120%; justify-content: center; margin: auto; display: flex;"
                )
                return
            with ui.column():
                create_html = CreateHtml(self.results.items, self.lang)
                ui.html(create_html())

    def __call__(self):
        ui_args = {
            "native": True,
            "title": self.title,
            "window_size": (700, 1500),
            "show": True,
            "dark": True,
        }
        self.create_header()
        self.create_body()
        ui.run(**ui_args)

    async def search_task(self, word: str):
        results = search_async(
            word=word, lang=self.lang, search_type=self.search_type.value
        )
        self.results = await results
        # print(self.results)
        if self.results:
            self.create_body.refresh()

    async def search_in_db(self, *args):
        if self.search_type.value == "fulltext":
            self.search_limit = 3
            self.search_type.update()
        else:
            self.search_limit = 1
            self.search_type.update()
        if self.search_entry.value and len(self.search_entry.value) >= self.search_limit:
            print(f"poustim tasky a man {self.search_limit}")
            async with asyncio.TaskGroup() as tg:
                if self.task:
                    self.task.cancel()
                    try:
                        await self.task
                    except asyncio.CancelledError:
                        pass
                    print(f'canceled: {self.task.cancelled()} or done: {self.task.done()}')
                self.task = tg.create_task(self.search_task(word=self.search_entry.value))
                # count = len(self.results.items)

    def search_setter(self, value):
        print(self.toggle.value)
        print(value.value)
        self.search_type = value.value


if __name__ in {"__main__", "__mp_main__"}:  # __mp_main__ to allow multiprocessing
    easydict = EasyDict()
    easydict()

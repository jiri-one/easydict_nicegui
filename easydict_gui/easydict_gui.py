from nicegui import ui

# internal imports
from backends import sqlite_backend
from backends.backend import ResultList
from settings import images
from time import sleep


class EasyDict:
    def __init__(self):
        self.title = "EasyDict-GUI"
        self.db = sqlite_backend.SQLiteBackend()
        self.lang = "eng"
        self.results = ResultList()
        self.search_in_progress = False


    def create_header(self):
        with ui.header().classes(replace="row items-center") as header:
            ui.button(on_click=lambda: left_drawer.toggle()).props(
                "flat color=white icon=menu"
            )
            ui.input(
                    placeholder="start typing",
                    on_change=self.search_in_db,
                    validation={"Input too short": lambda value: len(value) > 3},
                )
             # ui.label("EasyDict").style(
            #     "font-weight: bold; font-size: 150%; justify-content: center; margin: auto; display: flex;"
            # )

        with ui.left_drawer() as left_drawer:
            ui.label("Side menu")
    
    
    @ui.refreshable
    def create_body(self):
        with ui.column().style("justify-content: center; margin: auto; display: flex;") as self.main_column:
            if not self.results.items:
                # ui.label("Welcome to EasyDict").style("font-weight: bold; font-size: 150%; justify-content: center; margin: auto; display: flex;")
                ui.image(images["ed_icon.png"]).style("justify-content: center;")

                ui.label(
                    "The first open source translator which is completely open with dictionary data too."
                ).style(
                    "text-align: center; font-weight: bold; font-size: 120%; justify-content: center; margin: auto; display: flex;"
                )
                return
            with ui.column():
                for item in self.results.items:
                    ui.label(f"{item.cze}")


    def __call__(self):
        ui_args = {
            "native": True,
            "title": self.title,
            "window_size": (280, 550),
            "show": True,
            "dark": True,
        }
        self.create_header()
        self.create_body()
        ui.run(**ui_args)

    def search_in_db(self, word):
        print(word.value)
        if not self.search_in_progress:
            self.search_in_progress = True
            fulltext = False
            #if self.fulltext.get() == "Fulltext":
            fulltext = True
            self.results = self.db.search_sorted(word=word.value, lang=self.lang, fulltext=fulltext)
            self.create_body.refresh()
            #count = len(self.results.items)
            self.search_in_progress = False


            


if __name__ in {"__main__", "__mp_main__"}:  # __mp_main__ to allow multiprocessing
    easydict = EasyDict()
    easydict()

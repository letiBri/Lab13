import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        anni = self._model.getYears()
        for anno in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(anno))
        self._view.update_page()

    def handleDDYearSelection(self, e):
        pass

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        if self._view._ddAnno.value is None or self._view._ddAnno.value == "":
            self._view.txt_result.controls.append(ft.Text("Attenzione: selezionare un anno!", color="red"))
            self._view.update_page()
            return
        anno = int(self._view._ddAnno.value)
        self._model.buildGraph(anno)
        nodi, archi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {archi}"))

        bestDriver = self._model.getBestDriver()
        self._view.txt_result.controls.append(ft.Text(f"Best driver: {bestDriver[0]}, with score {bestDriver[1]}"))

        self._view._txtIntK.disabled = False
        self._view._btnCerca.disabled = False
        self._view.update_page()

    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        if self._view._txtIntK.value is None or self._view._txtIntK.value == "":
            self._view.txt_result.controls.append(ft.Text("Attenzione: inserire la dimensione del DreamTeam!", color="red"))
            self._view.update_page()
            return
        try:
            kInt = int(self._view._txtIntK.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Attenzione: inserire un intero positivo come dimensione del DreamTeam!", color="red"))
            self._view.update_page()
            return
        if kInt <= 0:
            self._view.txt_result.controls.append(ft.Text("Attenzione: inserire un intero positivo come dimensione del DreamTeam!", color="red"))
            self._view.update_page()
            return

        team, tasso = self._model.getDreamTeam(kInt)
        self._view.txt_result.controls.append(ft.Text(f"Dream team composto da {kInt} piloti trovato con tasso di sconfitta={tasso}:"))
        for p in team:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()

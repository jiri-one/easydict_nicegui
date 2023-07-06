class CreateHtml:
    def __init__(self, results, language):
        self.lng1 = language
        self.lng2 = [lang for lang in ["cze", "eng"] if lang != language][0]
        self.html_string = ""
        for item in results:
            self.html_string += self.create_html(item)
    
    def __call__(self):
        return self.html_string
            
    def create_html(self, item):
        if item.notes:
            notes =  " | " + item.notes
        else:
            notes = ""
        if item.special:
            special =  " | " + item.special
        else:
            special = ""        
    
        html = f"""
        <p>{getattr(item, self.lng1)}</b>
        <br>&emsp;{getattr(item, self.lng2)}{notes}{special}<hr />
        </p>
        """
        return html
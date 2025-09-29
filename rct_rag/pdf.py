import pdfplumber
from config import *


class Pdf:
    """
    TODO : implement a class for summary extraction from pdfs
    """

    def __init__(self, path) -> None:
        self.path = path
        pass

    def retrieve_text(self):
        with pdfplumber.open(self.path) as pdf:
            for page in pdf.pages:
                # print(page.page_number)
                try:
                    tables = page.extract_tables()
                    print(tables)
                    # if len(page.images) > 0 :
                    #     print(page.page_number)
                    #     for img in page.images :
                    #         img.save(img_data_path / f"{page.page_number}.png", format="PNG", quantize=True, colors=256, bits=8)
                except Exception as e:
                    print(e)
        return


if __name__ == "__main__":
    # print(img_data_path / f"img.png")
    print((type(img_data_path)))
    # pdf = Pdf(list(pdf_data_path.glob("*.pdf"))[0])
    # pdf.retrieve_text()

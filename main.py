from pdf_util import PDFUtility

input_file = "TestBookMarks.pdf"
# input_file = "Full Progress Set.pdf"
output_file = "output.pdf"

search_texts = [" O.C. ", " Shear Wall ", " On-center ", " Panel ", " Roof ", " Low Eave ", " Parapet " , " Bump-out "]
# search_texts = [" O.C. "]

pdf_bookmark_adder = PDFUtility(input_file, output_file,(0,0,1))
for text in search_texts:
    # print(text)
    pdf_bookmark_adder.add_bookmarks_from_text(text)
pdf_bookmark_adder.save_pdf_file()
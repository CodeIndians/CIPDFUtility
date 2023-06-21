from pdf_util import PDFUtility

input_file = "Full Progress Set.pdf"
output_file = "output.pdf"

pdf_bookmark_adder = PDFUtility(input_file, output_file,(0,0,1))
pdf_bookmark_adder.add_bookmarks_from_text("Finished Opening")
pdf_bookmark_adder.save_pdf_file()
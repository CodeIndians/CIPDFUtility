from pdf_util import PDFUtility

input_file = "Full Progress Set.pdf"
output_file = "output.pdf"

pdf_bookmark_adder = PDFUtility(input_file, output_file)
pdf_bookmark_adder.add_bookmarks_from_text("Finished Opening", "On Center")

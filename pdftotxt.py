import fitz  # PyMuPDF
import os

def pdf_to_text(pdf_path, txt_path):
    """
    Convert a PDF file to a text file.
    
    :param pdf_path: Path to the input PDF file.
    :param txt_path: Path to the output text file.
    """
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        text = ""
        
        # Extract text from each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        
        # Write text to the output file
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        
        print(f"Successfully converted '{pdf_path}' to '{txt_path}'")
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

def process_pdfs(input_folder, output_folder):
    """
    Convert all PDF files in the input folder to text files in the output folder.
    
    :param input_folder: Folder containing input PDF files.
    :param output_folder: Folder to save output text files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(output_folder, txt_filename)
            pdf_to_text(pdf_path, txt_path)

if __name__ == "__main__":
    import argparse
    
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Convert PDF files to text files.")
    parser.add_argument('input_folder', type=str, help="Folder containing PDF files.")
    parser.add_argument('output_folder', type=str, help="Folder to save text files.")
    
    args = parser.parse_args()
    
    # Process the folder of PDFs
    process_pdfs(args.input_folder, args.output_folder)

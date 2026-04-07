# Importar las bibliotecas necesarias
import os
import shutil
from pdf2image import convert_from_path, pdfinfo_from_path
from ebooklib import epub

def sanitize_filename(filename):
    """
    Limpia el nombre del archivo para evitar problemas con caracteres especiales.

    Args:
        filename (str): Nombre del archivo original.

    Returns:
        str: Nombre del archivo limpio.
    """
    return "".join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in filename)

def rename_files_to_simple_names(pdf_files):
    """
    Renombra los archivos PDF a nombres más simples y manejables.

    Args:
        pdf_files (list): Lista de nombres de archivos PDF.

    Returns:
        list: Lista de nuevos nombres de archivos PDF.
    """
    renamed_files = []
    for index, pdf_file in enumerate(pdf_files, start=1):
        new_name = f"archivo_{index}.pdf"
        print(f"Renombrando archivo: {pdf_file} -> {new_name}")
        shutil.move(pdf_file, new_name)
        renamed_files.append(new_name)
    return renamed_files

def pdf_to_epub():
    """
    Convierte todos los archivos PDF en el directorio actual a formato EPUB.
    """
    # Obtener la lista de archivos PDF en el directorio actual
    current_dir = os.getcwd()
    pdf_files = [f for f in os.listdir(current_dir) if f.endswith('.pdf')]

    if not pdf_files:
        print("No se encontraron archivos PDF en el directorio actual.")
        return

    # Renombrar los archivos a nombres simples
    pdf_files = rename_files_to_simple_names(pdf_files)

    for pdf_file in pdf_files:
        # Verificar si el archivo existe
        if not os.path.exists(pdf_file):
            print(f"El archivo '{pdf_file}' no se encuentra en el directorio.")
            continue

        # Generar el nombre del archivo EPUB de salida
        output_file = os.path.splitext(pdf_file)[0] + ".epub"

        # Verificar si el archivo PDF es válido
        try:
            pdfinfo_from_path(pdf_file)
        except Exception as e:
            print(f"El archivo '{pdf_file}' no es un PDF válido o está dañado: {e}")
            continue

        # Crear un libro EPUB
        book = epub.EpubBook()
        book.set_identifier("id123456")
        book.set_title(f"Convertido: {pdf_file}")
        book.set_language("es")
        book.add_author("Autor Desconocido")

        # Convertir las páginas del PDF a imágenes
        print(f"Convirtiendo páginas del PDF '{pdf_file}' a imágenes...")
        try:
            pages = convert_from_path(pdf_file)
        except Exception as e:
            print(f"Error al convertir el archivo '{pdf_file}': {e}")
            continue

        # Agregar cada página como un capítulo al EPUB
        for i, page in enumerate(pages):
            # Guardar la imagen temporalmente
            image_path = f"page_{i + 1}.jpg"
            page.save(image_path, "JPEG")

            # Crear un capítulo para la página
            chapter = epub.EpubHtml(title=f"Página {i + 1}", file_name=f"page_{i + 1}.xhtml")
            chapter.content = f'<img src="{image_path}" alt="Página {i + 1}" />'
            book.add_item(chapter)

            # Agregar la imagen al libro
            book.add_item(epub.EpubItem(uid=f"image_{i + 1}", file_name=image_path, media_type="image/jpeg"))

        # Definir la tabla de contenido y el flujo de lectura
        book.toc = tuple(book.items)
        book.spine = [item for item in book.items]

        # Guardar el archivo EPUB
        print(f"Guardando el archivo EPUB '{output_file}'...")
        epub.write_epub(output_file, book)
        print(f"Archivo EPUB guardado en: {output_file}")

if __name__ == "__main__":
    # Cambiar al directorio deseado
    os.chdir("D:\\resources_psycho\\resources_github\\repos_publicos\\matematicas\\pdf_to_epub")

    # Llamar a la función para convertir los PDFs
    pdf_to_epub()
import logging
import os

from py_toolkit.exceptions import MissingOptionalDependencyError, PdfError

logger = logging.getLogger(__name__)

try:
    from pdf2image import convert_from_path  # type: ignore[import-untyped]
except ModuleNotFoundError:  # pragma: no cover
    convert_from_path = None  # type: ignore[assignment]


def convert_pdf_to_img(
    src_filename: str, parent_folder: str, prefix: str, dpi: int = 500
) -> list[str]:
    """Convert each page of a PDF to a JPEG image.

    Args:
        src_filename: Path to the source PDF file.
        parent_folder: Directory to save images into.
        prefix: Filename prefix for each generated image.
        dpi: Resolution in dots per inch (default 500).

    Returns:
        List of paths to the generated image files.

    Raises:
        MissingOptionalDependencyError: If pdf2image is not installed.
        PdfError: If the conversion fails.

    Example:
        >>> convert_pdf_to_img("doc.pdf", "/tmp/output/", "page_")
        ['/tmp/output/page_1.jpg', '/tmp/output/page_2.jpg']
    """
    if convert_from_path is None:
        raise MissingOptionalDependencyError(
            "pdf2image is not installed. Install it with: pip install py-toolkit[pdf]"
        )
    try:
        pages = convert_from_path(src_filename, dpi)
        output_paths: list[str] = []
        for count, page in enumerate(pages, start=1):
            output_path = os.path.join(parent_folder, f"{prefix}{count}.jpg")
            page.save(output_path, "JPEG")
            output_paths.append(output_path)
        logger.debug("Converted %d pages from %s", len(pages), src_filename)
        return output_paths
    except Exception as e:
        msg = f"Failed to convert PDF {src_filename} to images: {e}"
        logger.error(msg)
        raise PdfError(msg) from e

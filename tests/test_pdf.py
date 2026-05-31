from unittest import mock

import pytest

from py_toolkit.exceptions import MissingOptionalDependencyError, PdfError
from py_toolkit.pdf.pdf_to_image import convert_pdf_to_img


class TestPdf:
    @mock.patch("py_toolkit.pdf.pdf_to_image.convert_from_path")
    def test_convert_pdf_to_img_returns_paths(self, mock_convert, temp_dir):
        mock_page = mock.MagicMock()
        mock_convert.return_value = [mock_page, mock_page]

        result = convert_pdf_to_img("test.pdf", temp_dir + "/", "page_")
        assert len(result) == 2
        assert all(p.endswith(".jpg") for p in result)

    @mock.patch("py_toolkit.pdf.pdf_to_image.convert_from_path")
    def test_convert_pdf_to_img_calls_save(self, mock_convert, temp_dir):
        mock_page = mock.MagicMock()
        mock_convert.return_value = [mock_page]

        convert_pdf_to_img("test.pdf", temp_dir + "/", "img_", dpi=300)
        mock_convert.assert_called_once_with("test.pdf", 300)
        mock_page.save.assert_called_once()

    @mock.patch("py_toolkit.pdf.pdf_to_image.convert_from_path")
    def test_convert_pdf_to_img_handles_error(self, mock_convert):
        mock_convert.side_effect = Exception("corrupt PDF")
        with pytest.raises(PdfError, match="corrupt PDF"):
            convert_pdf_to_img("bad.pdf", "/tmp/", "x_")

    @mock.patch("py_toolkit.pdf.pdf_to_image.convert_from_path", None)
    def test_convert_raises_when_pdf2image_missing(self):
        with pytest.raises(MissingOptionalDependencyError, match="pdf2image"):
            convert_pdf_to_img("test.pdf", "/tmp/", "x_")

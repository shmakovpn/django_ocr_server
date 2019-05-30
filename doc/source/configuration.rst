Configuration
=============
 For changing your django_ocr_server behavior you can use
 several parameters in the settings.py of your django project.

  | OCR_STORE_FILES Set it to True (default) to enable storing uploaded files on the server
  | OCR_FILE_PREVIEW  Set it to True (default) to enable showing uploaded images preview in admin interface
  | OCR_TESSERACT_LANG Sets priority of using languages, default to 'rus+eng'
  | OCR_STORE_PDF Set it to True (default) to enable storing created searchable PDFs on the server
  | OCR_FILES_UPLOAD_TO Sets path for uploaded files
  | OCR_PDF_UPLOAD_TO Sets path for created searchable PDFs
  | OCR_FILES_TTL Sets time to live for uploaded files, uploaded files older this interval will be removed. Use python datetime.timedelta to set it or 0 (default) to disable.
  | OCR_PDF_TTL Sets time to live for created searchable PDFs, PDFs older this interval will be removed. Use python datetime.timedelta to set it or 0 (default) to disable.
  | OCR_TTL Sets time to live for created models of OCRedFile, models older this interval will be removed. Use python datetime.timedelta to set it or 0 (default) to disable.

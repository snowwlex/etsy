"""
The standard CSVItemExporter class does not pass the kwargs through to the
CSV writer, resulting in EXPORT_FIELDS and EXPORT_ENCODING being ignored
(EXPORT_EMPTY is not used by CSV).
"""

from scrapy.utils.project import get_project_settings
from scrapy.exporters import CsvItemExporter

class CSVkwItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        settings = get_project_settings()
        kwargs['fields_to_export'] = settings.getlist('EXPORT_FIELDS') or None
        kwargs['encoding'] = settings.get('EXPORT_ENCODING', 'utf-8')

        super(CSVkwItemExporter, self).__init__(*args, **kwargs)

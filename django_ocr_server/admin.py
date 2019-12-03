"""
django_ocr_server/admin.py
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-04-16'


from django.core.exceptions import PermissionDenied
from django.contrib import admin
from django.contrib.admin.actions import delete_selected as delete_selected_
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import path, reverse
from .forms import *


def remove_selected(modeladmin, request, queryset):
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied
    for obj in queryset:
        obj.delete()


remove_selected.short_description = "Delete selected objects"


def remove_file_selected(modeladmin, request, queryset):
    if not modeladmin.has_change_permission(request):
        raise PermissionDenied
    for obj in queryset:
        obj.remove_file()


remove_file_selected.short_description = "Delete files from selected objects"


def remove_pdf_selected(modeladmin, request, queryset):
    if not modeladmin.has_change_permission(request):
        raise PermissionDenied
    for obj in queryset:
        obj.remove_pdf()


remove_pdf_selected.short_description = "Delete PDFs from selected objects"


def create_pdf_selected(modeladmin, request, queryset):
    """
    This function creates pdf for selected models if creation is possible
    :param modeladmin: a modeladmin instance
    :param request: a current request
    :param queryset: a selected models query set
    :return: None
    """
    if not modeladmin.has_change_permission(request):
        raise PermissionDenied
    for obj in queryset:
        obj.create_pdf(modeladmin, request)


create_pdf_selected.short_description = "Create PDFs in selected objects"


def filefield_to_listdisplay(obj):
    if 'store_files_disabled' in obj.file.name:
        return 'NO FILE'
    elif 'file_removed' in obj.file.name:
        return 'REMOVED'
    filename = os.path.basename(obj.file.name)
    return format_html('<a href="{}" target="_blank">{}</a><a class="button" href="{}">Remove</a>',
                       reverse(f"{__package__}:download", kwargs={
                           'download_target': 'file', 'filename': filename
                       }),
                       filename,
                       reverse('admin:ocredfile-file-remove', args=[obj.pk])
                       )


filefield_to_listdisplay.short_description = "File"


def pdffield_to_listdisplay(obj):
    """
    Formats pdffield to show in the listdisplay of admin interface
    :param obj: a model instance
    :return: pdffield html
    """
    out = ''
    if not obj.ocred_pdf:
        out = ''
    elif 'store_pdf_disabled' in obj.ocred_pdf.name:
        out = 'NO PDF'
    elif 'pdf_removed' in obj.ocred_pdf.name:
        out = 'REMOVED'
    else:
        filename = os.path.basename(obj.ocred_pdf.name)
        return format_html('<a href="{}" target="_blank">{}</a><a class="button" href="{}">Remove</a>',
                           reverse(f"{__package__}:download", kwargs={
                               'download_target': 'pdf', 'filename': filename
                           }),
                           filename,
                           reverse('admin:ocredfile-ocred_pdf-remove', args=[obj.pk])
                           )
    if obj.can_create_pdf:
        return format_html('{}<a class="button" href="{}">Create</a>',
                           out,
                           reverse('admin:ocredfile-ocred_pdf-create', args=[obj.pk]))
    return out


pdffield_to_listdisplay.short_description = "PDF"


def pdfinfo_to_listdisplay(obj):
    html = ''
    if obj.pdf_num_pages:
        html += '<div>nPages: '+str(obj.pdf_num_pages)+'</div>'
    if obj.pdf_author:
        html += '<div>Author: '+str(obj.pdf_author)+'</div>'
    if obj.pdf_creation_date:
        html += '<div>Created: '+str(obj.pdf_creation_date)+'</div>'
    if obj.pdf_creator:
        html += '<div>Creator: '+str(obj.pdf_creator)+'</div>'
    if obj.pdf_mod_date:
        html += '<div>Modified: '+str(obj.pdf_mod_date)+'</div>'
    if obj.pdf_producer:
        html += '<div>Producer: '+str(obj.pdf_producer)+'</div>'
    if obj.pdf_title:
        html += '<div>Title: '+str(obj.pdf_title)+'</div>'
    return format_html(html)


# Register your models here.
class OCRedFileAdmin(admin.ModelAdmin):
    """
    The ModelAdmin for the model OCRedFile
    """
    actions = [remove_selected, remove_file_selected, remove_pdf_selected, create_pdf_selected]
    list_display = ('md5', 'uploaded', 'ocred', filefield_to_listdisplay, pdffield_to_listdisplay, pdfinfo_to_listdisplay, 'ocred_pdf_md5')

    def get_actions(self, request):
        """
        Remove 'delete_selected' from actions. Returns the list of available actions 2019-04-22
        :param request: not used
        :return: the list of available actions
        """
        actions = super(OCRedFileAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_fieldsets(self, request, obj=None):
        """
        This function returns fieldsets for the OCRFileForm,
        excludes 'uploaded' and 'ocred' fields from OCRedFileAdmin.fieldsets 2019-03-18
        :param request: does not use
        :param obj: the current instance of the OCRedFile model
        :return: fieldsets for the OCRFileForm,
        """
        if not obj:
            return (
                (None, {
                    'fields': ('file', 'file_type',)
                }),
            )
        return (
            (None, {
                'fields': ('file', 'ocred_pdf',)
            }),
            (None, {
                'fields': ('file_type', )
            }),
            (None, {
                'fields': (('md5', 'ocred_pdf_md5'), )
            }),
            (None, {
                'fields': (('uploaded', 'ocred',), 'pdf_info', )
            }),
            (None, {
                'fields': ('text', )
            })
        )

    def get_readonly_fields(self, request, obj=None):
        """
        This function tuple of readonly fields,
         excludes 'uploaded' and 'ocred' from readonly fields when adding 2019-03-18
        :param request: a current request
        :param obj: a model instance
        :return: a tuple of 'readonly_fields'
        """
        if not obj:
            return ()
        return ('uploaded', 'ocred', )

    def process_file_remove(self, request, ocredfile_id, *args, **kwargs):
        try:
            ocredfile = OCRedFile.objects.get(pk=ocredfile_id)
            ocredfile.remove_file()
            self.message_user(request, 'File removed "'+ocredfile.file.name+'" ')
        except Exception as e:
            self.message_user(request, 'An error has occurred: '+str(e))
        return HttpResponseRedirect(reverse('admin:{package}_ocredfile_changelist'.format(package=__package__)))

    def process_pdf_remove(self, request, ocredfile_id, *args, **kwargs):
        try:
            ocredfile = OCRedFile.objects.get(pk=ocredfile_id)
            filename = ocredfile.ocred_pdf.name
            ocredfile.remove_pdf()
            self.message_user(request, 'PDF removed "'+filename+'" ')
        except Exception as e:
            self.message_user(request, 'An error has occurred: '+str(e))
        return HttpResponseRedirect(reverse('admin:{package}_ocredfile_changelist'.format(package=__package__)))

    def process_pdf_create(self, request, ocredfile_id, *args, **kwargs):
        """
        Creates a searchable pdf if it does not exits and creation is possible
        :param request:
        :param ocredfile_id: a primary key of a model instance
        :param args:
        :param kwargs:
        :return: HttpResponseRedirect to 'admin:ocr_ocredfile_changelist'
        """
        try:
            ocredfile = OCRedFile.objects.get(pk=ocredfile_id)
            ocredfile.create_pdf(self, request)
        except Exception as e:
            self.message_user(request, 'An error has occurred:'+str(e))
        return HttpResponseRedirect(reverse('admin:{package}_ocredfile_changelist'.format(package=__package__)))

    def get_urls(self):
        """
        Creates urls for OCRedFile admin_view
        :return: list of urls
        """
        urls = super(OCRedFileAdmin, self).get_urls()
        custom_urls = [
            path(
                 '<int:ocredfile_id>/file_remove/',
                 self.admin_site.admin_view(self.process_file_remove),
                 name='ocredfile-file-remove',
                 ),
            path(
                '<int:ocredfile_id>/pdf_remove/',
                self.admin_site.admin_view(self.process_pdf_remove),
                name='ocredfile-ocred_pdf-remove',
            ),
            path(
                '<int:ocredfile_id>/pdf_create/',
                self.admin_site.admin_view(self.process_pdf_create),
                name='ocredfile-ocred_pdf-create',
            ),
        ]
        return custom_urls+urls

    def response_change(self, request, obj):
        if '_removefile' in request.POST:
            self.message_user(request, 'File removed')
            obj.remove_file()  # remove file from filesystem and rename filefield to 'file_removed'
            return HttpResponseRedirect('.')
        if '_removepdf' in request.POST:
            self.message_user(request, 'PDF removed')
            obj.remove_pdf()  # remove ocred_pdf from filesystem and rename filefield to 'pdf_removed'
            return HttpResponseRedirect('.')
        if '_createpdf' in request.POST:
            obj.create_pdf(self, request)  # create ocred pdf (if it is possible)
            return HttpResponseRedirect('.')
        return super(OCRedFileAdmin, self).response_change(request, obj)

    def add_view(self, request, form_url='', extra_context=None):
        self.form = OCRedFileAddForm
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['ocr_show_save_and_add_another'] = True
        extra_context['ocr_show_save_and_view'] = True
        return super(OCRedFileAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.form = OCRedFileViewForm
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['ocr_show_save_and_add_another'] = False
        return super(OCRedFileAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        return super(OCRedFileAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        return super(OCRedFileAdmin, self).delete_model(request, obj)


admin.site.register(OCRedFile, OCRedFileAdmin)
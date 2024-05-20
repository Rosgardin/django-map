from django import forms
from django.http import QueryDict


class RouteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        arg_len = kwargs.get('len')
        if not arg_len is None:
            del kwargs['len']
        super(RouteForm, self).__init__(*args, **kwargs)

        if len(args) > 0:
            req_arg: QueryDict = args[0]
            for k, v in req_arg.dict().items():
                self.fields[f"{k}"] = forms.CharField(label='', required=False, initial=f"{v}", help_text=f"Точка {k}")
            self.fields[f"{0}"].help_text = "Начало"
            self.fields[f"{len(req_arg.dict().keys()) - 1}"].help_text = "Конец"
        if arg_len != None:
            for i in range(int(arg_len) - 2):
                self.fields[f"{i}"] = forms.CharField(label='', required=False, help_text=f"Точка {i}")
            self.fields[f"{0}"].help_text = "Начало"
            self.fields[f"{arg_len - 1}"].help_text = "Конец"


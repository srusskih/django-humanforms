from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings


class Removeable(forms.TextInput):
    """
    Field will appeare only when JS is turned on
    """
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        html = """
        <div style="display: none;" id="%(id)s_holder"></div>
        <script type="text/javascript">
        (function(){
            var holder = document.getElementById("%(id)s_holder");
            var input = document.createElement('input');
            input.type="text";
            input.name="%(name)s";
            holder.appendChild(input);
        })();
        </script>
        """ % final_attrs
        return mark_safe(html)


class HumanMixin(object):
    """
    Human form should contains "human_question" in resquest data
    to pass validation
    """

    def __init__(self, *args, **kwargs):
        super(HumanMixin, self).__init__(*args, **kwargs)

        if getattr(settings, "ROBOT_PROTECTION", True):
            self.fields['human_question'] = forms.CharField(widget=Removeable,
                                                            required=False)

    def clean(self):
        data = super(HumanMixin, self).clean()

        if getattr(settings, "ROBOT_PROTECTION", True):
            if 'human_question' not in self.data:
                raise forms.ValidationError("try again")
        return data

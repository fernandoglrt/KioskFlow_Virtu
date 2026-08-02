from django import forms

from .models import Question


def build_survey_form(data=None):
    """Monta um forms.Form em runtime a partir das Questions ativas no banco,
    na ordem definida em cada Question.order. Adicionar/editar/reordenar
    perguntas no admin muda o formulário do totem sem precisar mexer em código.
    """
    fields = {}
    questions = (
        Question.objects.filter(is_active=True)
        .prefetch_related('options')
        .order_by('order', 'id')
    )
    for question in questions:
        required = question.is_required
        error_messages = {
            'required': f'Por favor, responda "{question.label}" antes de continuar.',
        }

        if question.question_type == Question.TEXT:
            field = forms.CharField(
                label=question.label, required=required, max_length=255,
                error_messages=error_messages,
            )
        elif question.question_type == Question.NUMBER:
            field = forms.CharField(
                label=question.label, required=required, max_length=50,
                widget=forms.NumberInput, error_messages=error_messages,
            )
        elif question.question_type == Question.CHECKBOX_MULTI:
            choices = [(opt.effective_value, opt.label) for opt in question.options.all()]
            field = forms.MultipleChoiceField(
                label=question.label, required=required, choices=choices,
                widget=forms.CheckboxSelectMultiple, error_messages=error_messages,
            )
        else:  # radio
            choices = [(opt.effective_value, opt.label) for opt in question.options.all()]
            field = forms.ChoiceField(
                label=question.label, required=required, choices=choices,
                widget=forms.RadioSelect, error_messages=error_messages,
            )
        fields[question.key] = field

    form_class = type('DynamicSurveyForm', (forms.Form,), fields)
    return form_class(data=data)


def build_skip_rules():
    """Regras de 'pular pergunta se...' pro JS do totem, geradas a partir de
    Question.depends_on — ver templates/survey.html."""
    rules = {}
    for question in Question.objects.filter(is_active=True, depends_on__isnull=False):
        rules[question.key] = {
            'parent': question.depends_on.key,
            'expected': question.depends_on_value,
        }
    return rules

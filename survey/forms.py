from django import forms
from .models import PesquisaGravatai

class PesquisaForm(forms.ModelForm):
    CANDIDATOS_OPTS = [
        ('Bombeiro Batista – REP', 'Bombeiro Batista – REP'),
        ('Thiago De Leon – PDT', 'Thiago De Leon – PDT'),
        ('Dimas Costa – PSD', 'Dimas Costa – PSD'),
        ('Marco Alba – MDB', 'Marco Alba – MDB'),
        ('Branco/nulo', 'Branco/nulo'),
        ('Outro', 'Outro'),
        ('Não sei', 'Não sei'),
    ]
    GOV_OPTS = [
        ('Edegar Pretto – PT', 'Edegar Pretto – PT'),
        ('Gabriel Souza – MDB', 'Gabriel Souza – MDB'),
        ('Luciano Zucco – PL', 'Luciano Zucco – PL'),
        ('Juliana Brizola – PDT', 'Juliana Brizola – PDT'),
        ('Branco/Nulo/Outro', 'Branco/Nulo/Outro'),
        ('Não sei', 'Não sei'),
    ]

    candidatos_poderia_votar = forms.MultipleChoiceField(
        label='Entre estes, em quais você PODERIA votar para Deputado?',
        choices=CANDIDATOS_OPTS,
        widget=forms.CheckboxSelectMultiple
    )

    candidatos_rejeicao = forms.MultipleChoiceField(
        label='Em quais destes você NÃO VOTARIA de jeito nenhum?',
        choices=CANDIDATOS_OPTS,
        widget=forms.CheckboxSelectMultiple
    )

    candidato_voto_hoje = forms.ChoiceField(
        label='Se a eleição fosse hoje, em quem você votaria?',
        choices=CANDIDATOS_OPTS,
        widget=forms.RadioSelect
    )
    candidato_governador = forms.ChoiceField(
        label='Para Governador do RS, em quem você vota?',
        choices=GOV_OPTS,
        widget=forms.RadioSelect
    )

    class Meta:
        model = PesquisaGravatai
        fields = '__all__'
        labels = {
            'sexo': 'Qual seu sexo biológico?',
            'sexo_outro': 'Por favor, especifique:',
            'faixa_etaria': 'Qual a sua faixa etária?',
            'escolaridade': 'Qual seu grau de escolaridade?',
            'ocupacao': 'Qual sua ocupação principal atual?',
            'renda_familiar': 'Somando tudo, qual a renda média da sua família?',
            'candidatos_poderia_votar': 'Entre estes, em quais você PODERIA votar para Deputado?',
            'candidato_voto_hoje': 'Se a eleição fosse hoje, em quem você votaria?',
            'candidatos_rejeicao': 'Em quais destes você NÃO VOTARIA de jeito nenhum?',
            'candidato_governador': 'Para Governador do RS, em quem você vota?',
            'nome': 'Para finalizar, qual seu primeiro nome?',
            'whatsapp': 'Digite seu WhatsApp para receber o resultado:'
        }
        widgets = {
            'sexo': forms.RadioSelect,
            'faixa_etaria': forms.RadioSelect,
            'escolaridade': forms.RadioSelect,
            'ocupacao': forms.RadioSelect,
            'renda_familiar': forms.RadioSelect,
            'nome': forms.TextInput(attrs={'placeholder': 'Seu Nome'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '(XX) XXXXX-XXXX'}),
        }

    def clean_candidatos_poderia_votar(self):
        return ", ".join(self.cleaned_data['candidatos_poderia_votar'])

    def clean_candidatos_rejeicao(self):
        return ", ".join(self.cleaned_data['candidatos_rejeicao'])
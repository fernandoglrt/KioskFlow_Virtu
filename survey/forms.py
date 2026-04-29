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
    REGIOES_OPTS = [
        ('Central', 'CENTRAL (Centro, Dom Feliciano, Flamboyant, Timbaúva, Salgado Filho, São Vicente)'),
        ('Moradas', 'DAS MORADAS (Águas Claras, Morada I, II e III, Pq. Ipiranga)'),
        ('Bonsucesso',
         'BONSUCESSO (Barnabé, Bonsucesso, Garibaldina, Pq. Eucaliptos, Planaltina, São Geraldo, Vl. Branca)'),
        ('Morungava', 'MORUNGAVA (Cadiz, Itacolomi, Morungava, Santa Tecla)'),
        ('Rincao', 'DO RINCÃO (Auxiliadora, Nova Conquista, Rincão)'),
        ('Parque Florido', 'PARQUE FLORIDO (Pq. Florido, Pq. Olinda, São Vicente)'),
        ('Cohabs', 'DAS COHABS (Cohab A e C, Monte Belo, São Jerônimo)'),
        ('Parque',
         'DO PARQUE (Caça e Pesca, Itatiaia, Mato Alto, Morada Gaúcha, Pq. Anjos, Passo dos Ferreiros, Sítio Gaúcho)'),
        ('Breno Garcia', 'DO BRENO GARCIA (Jd. Cedro, Padre Réus, Passo da Caveira, Sagrada Família, Vila Neiva)'),
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
    regiao_residencia = forms.ChoiceField(
        label='Qual das regiões você atualmente reside? De forma aproximada:',
        choices=REGIOES_OPTS,
        widget=forms.RadioSelect
    )
    PRESIDENTE_OPTS = [
        ('Flávio Bolsonaro - PL', 'Flávio Bolsonaro - PL'),
        ('Luis Inácio Lula da Silva - PT', 'Luis Inácio Lula da Silva - PT'),
        ('Romeu Zema - NOVO', 'Romeu Zema - NOVO'),
        ('Ronaldo Caiado', 'Ronaldo Caiado'),
        ('Branco/Nulo', 'Branco/Nulo'),
        ('Não sei', 'Não sei'),
    ]

    RUMO_ESTADO_OPTS = [
        ('Deve continuar como está', 'Deve continuar como está'),
        ('Mudar apenas o que está ruim', 'Mudar apenas o que está ruim'),
        ('Mudar totalmente', 'Mudar totalmente'),
        ('Não sei', 'Não sei'),
    ]

    AVALIACAO_ZAFFALLON_OPTS = [
        ('Ótima', 'Ótima'),
        ('Boa', 'Boa'),
        ('Regular', 'Regular'),
        ('Ruim', 'Ruim'),
        ('Péssima', 'Péssima'),
        ('Não sei', 'Não sei'),
    ]

    # --- CAMPOS MAPEADOS ---
    voto_presidente = forms.ChoiceField(
        label='Se as eleições fossem hoje, e os candidatos a presidência fossem estes, você votaria em:',
        choices=PRESIDENTE_OPTS,
        widget=forms.RadioSelect
    )

    rumo_governo_estado = forms.ChoiceField(
        label='Na sua opinião, em relação ao rumo do Governo do Estado, você acredita que:',
        choices=RUMO_ESTADO_OPTS,
        widget=forms.RadioSelect
    )

    avaliacao_zaffallon = forms.ChoiceField(
        label='De maneira geral, como você avalia a gestão do Governo Zaffallon?',
        choices=AVALIACAO_ZAFFALLON_OPTS,
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
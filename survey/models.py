from django.db import models


class PesquisaGravatai(models.Model):
    """Identidade do respondente. As respostas às perguntas em si ficam em Answer —
    ver Question/QuestionOption/Answer abaixo."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Enviada em')
    nome = models.CharField(max_length=150)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    is_duplicate = models.BooleanField(
        default=False, db_index=True, verbose_name='Duplicata',
        help_text='Marcada automaticamente: respostas idênticas enviadas em sequência rápida (flood/toque duplo no totem).',
    )

    class Meta:
        verbose_name = 'Pesquisa respondida'
        verbose_name_plural = 'Pesquisas respondidas'

    def __str__(self):
        return self.nome


class Question(models.Model):
    RADIO = 'radio'
    CHECKBOX_MULTI = 'checkbox_multi'
    TEXT = 'text'
    NUMBER = 'number'
    QUESTION_TYPES = [
        (RADIO, 'Escolha única'),
        (CHECKBOX_MULTI, 'Múltipla escolha'),
        (TEXT, 'Texto curto'),
        (NUMBER, 'Número'),
    ]

    key = models.SlugField(
        max_length=60, unique=True,
        help_text="Identificador interno estável — não mude depois que a pergunta já tiver respostas.",
    )
    label = models.CharField(max_length=255, verbose_name='Pergunta')
    category = models.CharField(
        max_length=100, blank=True, verbose_name='Categoria (agrupa no dashboard)',
        help_text='Ex: "Intenção de voto", "Perfil demográfico". Deixe em branco pra cair em "Outras perguntas".',
    )
    help_text = models.CharField(max_length=255, blank=True, verbose_name='Texto de apoio (opcional)')
    question_type = models.CharField(
        max_length=20, choices=QUESTION_TYPES, default=RADIO, verbose_name='Tipo de resposta',
    )
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True, verbose_name='Obrigatória')
    is_active = models.BooleanField(default=True, verbose_name='Ativa no totem')
    is_system = models.BooleanField(
        default=False, editable=False,
        help_text='Campo de identificação do respondente (nome/whatsapp) — não pode ser excluído.',
    )
    depends_on = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='dependents',
        verbose_name='Só exibir se a pergunta',
    )
    depends_on_value = models.CharField(
        max_length=255, blank=True, verbose_name='...tiver a resposta',
        help_text="Preencha junto com 'Só exibir se a pergunta' para pular esta pergunta condicionalmente.",
    )

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Pergunta'
        verbose_name_plural = 'Perguntas'

    def __str__(self):
        return self.label


class QuestionOption(models.Model):
    STATUS_CHOICES = [
        ('', '— nenhum —'),
        ('good', 'Ótimo (verde)'),
        ('warning', 'Neutro (amarelo)'),
        ('serious', 'Ruim (laranja)'),
        ('critical', 'Péssimo (vermelho)'),
        ('neutral', 'Sem opinião (cinza)'),
    ]

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    label = models.CharField(max_length=255, verbose_name='Texto exibido')
    value = models.CharField(
        max_length=255, blank=True, verbose_name='Valor salvo (opcional)',
        help_text='Se vazio, usa o próprio texto exibido. Só mude se souber o que está fazendo — respostas antigas usam o valor salvo pra contar certo no dashboard.',
    )
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, blank=True, default='',
        verbose_name='Status (opcional)',
        help_text='Preenchendo o status em todas as opções, a pergunta vira um gráfico de avaliação no dashboard.',
    )

    class Meta:
        ordering = ['order', 'id']
        unique_together = [('question', 'label')]
        verbose_name = 'Opção de resposta'
        verbose_name_plural = 'Opções de resposta'

    def __str__(self):
        return f'{self.label} ({self.question.key})'

    @property
    def effective_value(self):
        return self.value or self.label


class Answer(models.Model):
    response = models.ForeignKey(PesquisaGravatai, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    value = models.TextField(blank=True)

    class Meta:
        unique_together = [('response', 'question')]

    def __str__(self):
        return f'{self.question.key} = {self.value!r}'
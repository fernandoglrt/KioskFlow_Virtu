from django.db import migrations


CAT_VOTO = 'Intenção de voto'
CAT_PERFIL = 'Perfil demográfico'
CAT_CANDIDATOS = 'Candidatos a Deputado'

# (key, label, category, question_type, required, options[(value, label, status)], depends_on_key, depends_on_value)
QUESTIONS = [
    ('sexo', 'Qual seu sexo biológico?', CAT_PERFIL, 'radio', True, [
        ('Masculino', 'Masculino', ''), ('Feminino', 'Feminino', ''), ('Outro', 'Outro', ''),
    ], None, ''),
    ('sexo_outro', 'Por favor, especifique:', CAT_PERFIL, 'text', False, [], 'sexo', 'Outro'),
    ('faixa_etaria', 'Qual a sua faixa etária?', CAT_PERFIL, 'radio', True, [
        ('16-24', '16 a 24 anos', ''), ('25-34', '25 a 34 anos', ''), ('35-44', '35 a 44 anos', ''),
        ('45-59', '45 a 59 anos', ''), ('60+', '60 anos ou mais', ''),
    ], None, ''),
    ('escolaridade', 'Qual seu grau de escolaridade?', CAT_PERFIL, 'radio', True, [
        ('Analfabeto', 'Analfabeto', ''), ('Fundamental', 'Fundamental', ''), ('Medio', 'Ensino Médio', ''),
        ('Superior', 'Superior', ''), ('Pos', 'Pós-graduação', ''),
    ], None, ''),
    ('ocupacao', 'Qual sua ocupação principal atual?', CAT_PERFIL, 'radio', True, [
        ('CLT', 'CLT', ''), ('Autonomo', 'Autônomo', ''), ('Empresario', 'Empresário', ''),
        ('Servidor', 'Servidor Público', ''), ('Estudante', 'Estudante', ''),
        ('Desempregado', 'Desempregado/Aposentado', ''),
    ], None, ''),
    ('regiao_residencia', 'Qual das regiões você atualmente reside? De forma aproximada:', CAT_PERFIL, 'radio', True, [
        ('Central', 'CENTRAL (Centro, Dom Feliciano, Flamboyant, Timbaúva, Salgado Filho, São Vicente)', ''),
        ('Moradas', 'DAS MORADAS (Águas Claras, Morada I, II e III, Pq. Ipiranga)', ''),
        ('Bonsucesso', 'BONSUCESSO (Barnabé, Bonsucesso, Garibaldina, Pq. Eucaliptos, Planaltina, São Geraldo, Vl. Branca)', ''),
        ('Morungava', 'MORUNGAVA (Cadiz, Itacolomi, Morungava, Santa Tecla)', ''),
        ('Rincao', 'DO RINCÃO (Auxiliadora, Nova Conquista, Rincão)', ''),
        ('Parque Florido', 'PARQUE FLORIDO (Pq. Florido, Pq. Olinda, São Vicente)', ''),
        ('Cohabs', 'DAS COHABS (Cohab A e C, Monte Belo, São Jerônimo)', ''),
        ('Parque', 'DO PARQUE (Caça e Pesca, Itatiaia, Mato Alto, Morada Gaúcha, Pq. Anjos, Passo dos Ferreiros, Sítio Gaúcho)', ''),
        ('Breno Garcia', 'DO BRENO GARCIA (Jd. Cedro, Padre Réus, Passo da Caveira, Sagrada Família, Vila Neiva)', ''),
    ], None, ''),
    ('candidatos_poderia_votar', 'Entre estes, em quais você PODERIA votar para Deputado?', CAT_CANDIDATOS, 'checkbox_multi', True, [
        ('Bombeiro Batista – REP', 'Bombeiro Batista – REP', ''), ('Thiago De Leon – PDT', 'Thiago De Leon – PDT', ''),
        ('Dimas Costa – PSD', 'Dimas Costa – PSD', ''), ('Marco Alba – MDB', 'Marco Alba – MDB', ''),
        ('Branco/nulo', 'Branco/nulo', ''), ('Outro', 'Outro', ''), ('Não sei', 'Não sei', ''),
    ], None, ''),
    ('candidato_voto_hoje', 'Se a eleição fosse hoje, em quem você votaria?', CAT_VOTO, 'radio', True, [
        ('Bombeiro Batista – REP', 'Bombeiro Batista – REP', ''), ('Thiago De Leon – PDT', 'Thiago De Leon – PDT', ''),
        ('Dimas Costa – PSD', 'Dimas Costa – PSD', ''), ('Marco Alba – MDB', 'Marco Alba – MDB', ''),
        ('Branco/nulo', 'Branco/nulo', ''), ('Outro', 'Outro', ''), ('Não sei', 'Não sei', ''),
    ], None, ''),
    ('candidatos_rejeicao', 'Em quais destes você NÃO VOTARIA de jeito nenhum?', CAT_CANDIDATOS, 'checkbox_multi', True, [
        ('Bombeiro Batista – REP', 'Bombeiro Batista – REP', ''), ('Thiago De Leon – PDT', 'Thiago De Leon – PDT', ''),
        ('Dimas Costa – PSD', 'Dimas Costa – PSD', ''), ('Marco Alba – MDB', 'Marco Alba – MDB', ''),
        ('Branco/nulo', 'Branco/nulo', ''), ('Outro', 'Outro', ''), ('Não sei', 'Não sei', ''),
    ], None, ''),
    ('rumo_governo_estado', 'Na sua opinião, em relação ao rumo do Governo do Estado, você acredita que:', CAT_VOTO, 'radio', True, [
        ('Deve continuar como está', 'Deve continuar como está', ''),
        ('Mudar apenas o que está ruim', 'Mudar apenas o que está ruim', ''),
        ('Mudar totalmente', 'Mudar totalmente', ''), ('Não sei', 'Não sei', ''),
    ], None, ''),
    ('candidato_governador', 'Para Governador do RS, em quem você vota?', CAT_VOTO, 'radio', True, [
        ('Gabriel Souza – MDB', 'Gabriel Souza – MDB', ''), ('Luciano Zucco – PL', 'Luciano Zucco – PL', ''),
        ('Juliana Brizola – PDT', 'Juliana Brizola – PDT', ''), ('Branco/Nulo/Outro', 'Branco/Nulo/Outro', ''),
        ('Não sei', 'Não sei', ''),
    ], None, ''),
    ('voto_presidente', 'Se as eleições fossem hoje, e os candidatos a presidência fossem estes, você votaria em:', CAT_VOTO, 'radio', True, [
        ('Flávio Bolsonaro - PL', 'Flávio Bolsonaro - PL', ''), ('Luis Inácio Lula da Silva - PT', 'Luis Inácio Lula da Silva - PT', ''),
        ('Romeu Zema - NOVO', 'Romeu Zema - NOVO', ''), ('Ronaldo Caiado', 'Ronaldo Caiado', ''),
        ('Branco/Nulo', 'Branco/Nulo', ''), ('Não sei', 'Não sei', ''),
    ], None, ''),
    ('voto_senador', 'Se a eleição fosse hoje e os candidatos fossem estes, quem você votaria para ser Senador?', CAT_VOTO, 'radio', True, [
        ('Paulo Pimenta - PT', 'Paulo Pimenta - PT', ''), ('Manuela Davila - PSOL', 'Manuela Davila - PSOL', ''),
        ('Germano Rigotto - MDB', 'Germano Rigotto - MDB', ''), ('Marcel Van Hatten - NOVO', 'Marcel Van Hatten - NOVO', ''),
        ('Ubiratan Sanderson - PL', 'Ubiratan Sanderson - PL', ''), ('Branco/Nulo', 'Branco/Nulo', ''),
        ('Não sei', 'Não sei', ''),
    ], None, ''),
    ('avaliacao_zaffallon', 'De maneira geral, como você avalia a gestão do Governo Zaffallon?', 'Avaliação de governo', 'radio', True, [
        ('Ótima', 'Ótima', 'good'), ('Boa', 'Boa', 'good'), ('Regular', 'Regular', 'warning'),
        ('Ruim', 'Ruim', 'serious'), ('Péssima', 'Péssima', 'critical'), ('Não sei', 'Não sei', 'neutral'),
    ], None, ''),
    ('renda_familiar', 'Somando tudo, qual a renda média da sua família?', CAT_PERFIL, 'radio', True, [
        ('Ate 1', 'Até 1 SM', ''), ('1 a 2', '1 a 2 SM', ''), ('2 a 5', '2 a 5 SM', ''),
        ('5 a 10', '5 a 10 SM', ''), ('Mais 10', 'Mais de 10 SM', ''), ('NaoResponder', 'Não responder', ''),
    ], None, ''),
    ('nome', 'Para finalizar, qual seu primeiro nome?', '', 'text', True, [], None, ''),
    ('whatsapp', 'Digite seu WhatsApp para receber o resultado:', '', 'text', False, [], None, ''),
]

SYSTEM_KEYS = {'nome', 'whatsapp'}


def create_questions(apps, schema_editor):
    Question = apps.get_model('survey', 'Question')
    QuestionOption = apps.get_model('survey', 'QuestionOption')

    by_key = {}
    for order, (key, label, category, qtype, required, options, dep_key, dep_value) in enumerate(QUESTIONS, start=10):
        q = Question.objects.create(
            key=key, label=label, category=category, question_type=qtype, order=order * 10,
            is_required=required, is_active=True, is_system=key in SYSTEM_KEYS,
        )
        by_key[key] = q
        for opt_order, (value, opt_label, status) in enumerate(options, start=1):
            QuestionOption.objects.create(
                question=q, label=opt_label,
                value='' if value == opt_label else value,
                order=opt_order, status=status,
            )

    for key, label, category, qtype, required, options, dep_key, dep_value in QUESTIONS:
        if dep_key:
            q = by_key[key]
            q.depends_on = by_key[dep_key]
            q.depends_on_value = dep_value
            q.save(update_fields=['depends_on', 'depends_on_value'])

    PesquisaGravatai = apps.get_model('survey', 'PesquisaGravatai')
    Answer = apps.get_model('survey', 'Answer')

    field_questions = [q for q in QUESTIONS if q[0] not in SYSTEM_KEYS]
    answers_to_create = []
    for resp in PesquisaGravatai.objects.all().iterator():
        for key, *_ in field_questions:
            value = getattr(resp, key, None)
            if value:
                answers_to_create.append(Answer(response_id=resp.id, question_id=by_key[key].id, value=value))
        if len(answers_to_create) >= 2000:
            Answer.objects.bulk_create(answers_to_create)
            answers_to_create = []
    if answers_to_create:
        Answer.objects.bulk_create(answers_to_create)


def remove_questions(apps, schema_editor):
    Question = apps.get_model('survey', 'Question')
    Question.objects.filter(key__in=[q[0] for q in QUESTIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_remove_pesquisagravatai_avaliacao_zaffallon_and_more'),
    ]

    operations = [
        migrations.RunPython(create_questions, remove_questions),
    ]

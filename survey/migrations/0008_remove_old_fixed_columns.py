from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_backfill_questions_and_answers'),
    ]

    operations = [
        migrations.RemoveField(model_name='pesquisagravatai', name='avaliacao_zaffallon'),
        migrations.RemoveField(model_name='pesquisagravatai', name='candidato_governador'),
        migrations.RemoveField(model_name='pesquisagravatai', name='candidato_voto_hoje'),
        migrations.RemoveField(model_name='pesquisagravatai', name='candidatos_poderia_votar'),
        migrations.RemoveField(model_name='pesquisagravatai', name='candidatos_rejeicao'),
        migrations.RemoveField(model_name='pesquisagravatai', name='escolaridade'),
        migrations.RemoveField(model_name='pesquisagravatai', name='faixa_etaria'),
        migrations.RemoveField(model_name='pesquisagravatai', name='ocupacao'),
        migrations.RemoveField(model_name='pesquisagravatai', name='regiao_residencia'),
        migrations.RemoveField(model_name='pesquisagravatai', name='renda_familiar'),
        migrations.RemoveField(model_name='pesquisagravatai', name='rumo_governo_estado'),
        migrations.RemoveField(model_name='pesquisagravatai', name='sexo'),
        migrations.RemoveField(model_name='pesquisagravatai', name='sexo_outro'),
        migrations.RemoveField(model_name='pesquisagravatai', name='voto_presidente'),
        migrations.RemoveField(model_name='pesquisagravatai', name='voto_senador'),
    ]

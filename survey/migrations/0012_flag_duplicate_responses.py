from collections import defaultdict

from django.db import migrations

THRESHOLD_SECONDS = 120


def flag_duplicates(apps, schema_editor):
    PesquisaGravatai = apps.get_model('survey', 'PesquisaGravatai')
    Answer = apps.get_model('survey', 'Answer')

    responses = list(PesquisaGravatai.objects.order_by('created_at').values('id', 'created_at'))
    answers_by_response = defaultdict(list)
    for question_id, response_id, value in Answer.objects.values_list('question_id', 'response_id', 'value'):
        answers_by_response[response_id].append((question_id, value))

    by_signature = defaultdict(list)
    for r in responses:
        sig = tuple(sorted(answers_by_response.get(r['id'], [])))
        if sig:
            by_signature[sig].append(r)

    duplicate_ids = set()
    for rows in by_signature.values():
        if len(rows) < 2:
            continue
        rows.sort(key=lambda r: r['created_at'])
        prev_time = rows[0]['created_at']
        for r in rows[1:]:
            if (r['created_at'] - prev_time).total_seconds() <= THRESHOLD_SECONDS:
                duplicate_ids.add(r['id'])
            prev_time = r['created_at']

    if duplicate_ids:
        PesquisaGravatai.objects.filter(id__in=duplicate_ids).update(is_duplicate=True)


def unflag_duplicates(apps, schema_editor):
    PesquisaGravatai = apps.get_model('survey', 'PesquisaGravatai')
    PesquisaGravatai.objects.update(is_duplicate=False)


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0011_pesquisagravatai_is_duplicate'),
    ]

    operations = [
        migrations.RunPython(flag_duplicates, unflag_duplicates),
    ]

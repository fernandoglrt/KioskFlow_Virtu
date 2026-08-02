"""Deteccao de respostas duplicadas (flood / toque duplo no totem).

Regra: duas respostas contam como duplicata quando tem o mesmo conjunto de
respostas em TODAS as perguntas e foram enviadas a poucos minutos uma da
outra. Na pratica isso so acontece quando alguem manda a mesma resposta
varias vezes seguidas (tela travada, dedo grudado no botao Finalizar) — duas
pessoas diferentes acertarem a mesma combinacao de ~15 respostas por acaso,
no mesmo minuto, e estatisticamente irrelevante.
"""
from collections import defaultdict
from datetime import timedelta

DUPLICATE_WINDOW_SECONDS = 120


def _signature(response):
    return tuple(sorted((a.question_id, a.value) for a in response.answers.all()))


def compute_duplicate_ids(queryset=None, threshold_seconds=DUPLICATE_WINDOW_SECONDS):
    """Retorna o set de ids que devem ser marcados como duplicata (mantem
    sempre a primeira resposta de cada sequencia, marca o resto)."""
    from .models import PesquisaGravatai

    qs = queryset if queryset is not None else PesquisaGravatai.objects.all()
    responses = list(qs.order_by('created_at').prefetch_related('answers'))

    by_signature = defaultdict(list)
    for r in responses:
        sig = _signature(r)
        if sig:
            by_signature[sig].append(r)

    duplicate_ids = set()
    for rows in by_signature.values():
        if len(rows) < 2:
            continue
        rows.sort(key=lambda r: r.created_at)
        prev_time = rows[0].created_at
        for r in rows[1:]:
            if (r.created_at - prev_time).total_seconds() <= threshold_seconds:
                duplicate_ids.add(r.id)
            prev_time = r.created_at
    return duplicate_ids


def is_recent_duplicate(response, threshold_seconds=DUPLICATE_WINDOW_SECONDS):
    """Checa se `response` (ja salva, com Answers ja criadas) repete uma
    resposta enviada nos ultimos `threshold_seconds`."""
    from .models import PesquisaGravatai

    sig = _signature(response)
    if not sig:
        return False

    cutoff = response.created_at - timedelta(seconds=threshold_seconds)
    candidates = (
        PesquisaGravatai.objects.filter(created_at__gte=cutoff, created_at__lt=response.created_at)
        .exclude(id=response.id)
        .prefetch_related('answers')
    )
    return any(_signature(cand) == sig for cand in candidates)

import json
from otree.api import *

doc = """
Cuestionario inicial del Juego CPR-Bosque (survey_ini).
Recoge: identificación académica, consentimiento informado, escala de
identidad grupal (GIS), confianza interpersonal y dificultad percibida
para cooperar. Los demás grupos se identifican con el logo de su
universidad (coloreado según la relación con el participante).
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey_ini'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


# Logo de cada universidad: el color depende de la relación (misma U / misma
# carrera, etc.). El avatar final de cada participante combina este logo con
# un ícono de carrera elegido en AvatarSelection (ver participant.vars['career_icons']).
UNI_LOGO_CLASS = {
    'UDD': 'logo-udd',
    'UTalca': 'logo-utalca',
    'UAndes': 'logo-uandes',
    'USACH': 'logo-usach',
}


def _icon_for_degree(career_icons, degree):
    """Ícono (figura '1'-'9') asignado por el participante a `degree`.

    La asignación de íconos se hace por carrera únicamente (sin distinguir
    universidad, ver AvatarSelection), por lo que el mismo ícono se usa para
    una carrera sin importar en qué universidad la estudie cada compañero.
    Si la carrera no tiene ícono propio (p.ej. compañero anónimo) se usa el
    ícono reservado para '__anon__'.
    """
    if degree:
        return career_icons.get(degree, '') or career_icons.get('__anon__', '')
    return career_icons.get('__anon__', '')


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # ── Identification ────────────────────────────────────────────────────────
    university = models.StringField(
        choices=[
            ['UDD',    'Universidad del Desarrollo (UDD)'],
            ['UTalca', 'Universidad de Talca (UTalca)'],
            ['UAndes', 'Universidad de los Andes (UAndes)'],
            ['USACH',  'Universidad de Santiago de Chile (USACH)'],
        ],
        label='Universidad',
    )
    faculty = models.StringField(
        label='Facultad',
        blank=True,
    )
    degree = models.StringField(
        label='Carrera',
        blank=True,
    )

    # ── AvatarSelection ──────────────────────────────────────────────────────
    # JSON: { "carrera": "icon_id", ..., "__anon__": "icon_id" }
    avatar_assignments_json = models.LongStringField(blank=True)


    # ── Wellcome ──────────────────────────────────────────────────────────────
    consent_confirmed = models.BooleanField(
        widget=widgets.CheckboxInput,
        label=(
            'Confirmo que he leído, comprendido y firmado el documento de '
            'consentimiento informado, y acepto participar voluntariamente '
            'en este estudio.'
        ),
    )

    # ── GIS – Group Identity Scale (escala 1–9, 9 ítems) ─────────────────────
    gis_1 = models.IntegerField(
        min=1, max=9,
        label='Me siento identificado/a con los/as estudiantes de mi carrera.',
    )
    gis_2 = models.IntegerField(
        min=1, max=9,
        label='Me alegra pertenecer a mi carrera.',
    )
    gis_3 = models.IntegerField(
        min=1, max=9,
        label='Siento que pertenecer a mi carrera me frena o limita.',
    )
    gis_4 = models.IntegerField(
        min=1, max=9,
        label='Creo que los estudiantes de mi carrera funcionamos bien juntos.',
    )
    gis_5 = models.IntegerField(
        min=1, max=9,
        label='Me considero una parte importante de mi carrera.',
    )
    gis_6 = models.IntegerField(
        min=1, max=9,
        label='No encajo bien con los demás estudiantes de mi carrera.',
    )
    gis_7 = models.IntegerField(
        min=1, max=9,
        label='No considero que mi grupo de mi carrera sea importante.',
    )
    gis_8 = models.IntegerField(
        min=1, max=9,
        label='Me siento incómodo/a con los estudiantes de mi carrera.',
    )
    gis_9 = models.IntegerField(
        min=1, max=9,
        label='Siento fuertes lazos con los estudiantes de mi carrera.',
    ) 
    # ── Trust ─────────────────────────────────────────────────────────────────
    # JSON: { "profile_key": rating_int, ... }
    trust_ratings_json = models.LongStringField(
        blank=True,
        label='',
    )

    # ── Conflict ──────────────────────────────────────────────────────────────
    # JSON: { "profile_key": rating_int, ... }
    conflict_ratings_json = models.LongStringField(
        blank=True,
        label='',
    )


# ─────────────────────────────────────────────────────────────────────────────
# Páginas
# ─────────────────────────────────────────────────────────────────────────────

class Identification(Page):
    form_model = 'player'
    form_fields = ['university', 'faculty', 'degree']

    def error_message(player, values):
        if not values.get('faculty'):
            return 'Por favor seleccione una facultad.'
        if not values.get('degree'):
            return 'Por favor seleccione una carrera.'

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vars['university'] = player.university or ''
        player.participant.vars['degree'] = player.degree or ''


class Wellcome(Page):
    form_model = 'player'
    form_fields = ['consent_confirmed']

    def consent_confirmed_error_message(player, value):
        if not value:
            return 'Debe aceptar el consentimiento informado para continuar.'


def _session_profiles(player):
    """Perfiles distintos (universidad × carrera) del resto de la sesión."""
    my_uni = player.university or ''
    my_deg = player.degree or ''
    career_icons = player.participant.vars.get('career_icons', {}) or {}
    profiles = {}
    for other in player.subsession.get_players():
        if other.id_in_subsession == player.id_in_subsession:
            continue
        u = other.university or ''
        d = other.degree or ''
        if not u or not d:
            continue
        key = f"{u}__{d}"
        if key not in profiles:
            same_uni = (u == my_uni)
            same_deg = (d == my_deg)
            if same_uni and same_deg:
                relation = 'you'
            elif same_uni:
                relation = 'nearClose'
            elif same_deg:
                relation = 'nearFar'
            else:
                relation = 'far'
            profiles[key] = {
                'key': key,
                'university': u,
                'degree': d,
                'count': 0,
                'relation': relation,
                'icon': _icon_for_degree(career_icons, d),
            }
        profiles[key]['count'] += 1
    return list(profiles.values())


def _session_careers(player):
    """Carreras distintas presentes en la sesión (sin distinguir universidad).

    Cada carrera recibirá un único ícono, elegido por el participante en
    AvatarSelection, independientemente de en qué universidad se estudie.
    """
    my_deg = player.degree or ''
    careers = {}
    for p in player.subsession.get_players():
        d = p.degree or ''
        if not d:
            continue
        if d not in careers:
            careers[d] = {
                'key': d,
                'degree': d,
                'count': 0,
                'relation': 'you' if d == my_deg else 'far',
            }
        careers[d]['count'] += 1
    result = list(careers.values())
    result.sort(key=lambda c: (c['relation'] != 'you', c['degree']))
    return result


class WaitForIdentification(WaitPage):
    body_text = 'Espera mientras los demás participantes completan sus datos...'


class AvatarSelection(Page):
    """El participante elige un ícono distinto para cada carrera presente en
    la sesión (sin distinguir universidad) y otro para 'Estudiante Anónimo'.
    El avatar final de cada compañero combina el logo de SU universidad con
    el ícono que el participante asignó a SU carrera (ver _icon_for_degree)."""
    form_model = 'player'
    form_fields = ['avatar_assignments_json']

    @staticmethod
    def vars_for_template(player):
        return dict(careers_json=json.dumps(_session_careers(player)))

    @staticmethod
    def error_message(player, values):
        raw = values.get('avatar_assignments_json') or '{}'
        try:
            assignments = json.loads(raw)
        except (ValueError, TypeError):
            return 'Selección de avatares inválida.'
        expected_keys = {c['key'] for c in _session_careers(player)} | {'__anon__'}
        if not expected_keys.issubset(assignments.keys()):
            return 'Por favor, elige un ícono para cada carrera y para el estudiante anónimo.'
        icon_ids = list(assignments.values())
        if len(set(icon_ids)) != len(icon_ids):
            return 'Por favor, elige un ícono distinto para cada grupo.'

    @staticmethod
    def before_next_page(player, timeout_happened):
        raw = player.avatar_assignments_json or '{}'
        try:
            assignments = json.loads(raw)
        except (ValueError, TypeError):
            assignments = {}
        player.participant.vars['career_icons'] = assignments


class GisDegree(Page):
    form_model = 'player'
    form_fields = [
        'gis_1', 'gis_2', 'gis_3', 'gis_4', 'gis_5',
        'gis_6', 'gis_7', 'gis_8', 'gis_9',
    ]

    @staticmethod
    def vars_for_template(player):
        my_uni = player.university or ''
        my_deg = player.degree     or ''
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        return dict(
            my_university=my_uni,
            my_degree=my_deg,
            my_logo_class=UNI_LOGO_CLASS.get(my_uni, ''),
            my_icon_id=_icon_for_degree(career_icons, my_deg),
        )


def _profiles_with_self(player):
    """Perfiles de la sesión garantizando que el propio aparece primero."""
    my_uni   = player.university or ''
    my_deg   = player.degree     or ''
    my_key   = f"{my_uni}__{my_deg}"
    profiles = _session_profiles(player)
    if my_uni and my_deg and not any(p['key'] == my_key for p in profiles):
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        profiles.insert(0, {
            'key': my_key, 'university': my_uni, 'degree': my_deg,
            'count': 0, 'relation': 'you',
            'icon': _icon_for_degree(career_icons, my_deg),
        })
    return profiles


class Trust(Page):
    form_model = 'player'
    form_fields = ['trust_ratings_json']

    def vars_for_template(player):
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        return dict(
            groups_json=json.dumps(_profiles_with_self(player)),
            anon_icon=career_icons.get('__anon__', ''),
        )


class Conflict(Page):
    form_model = 'player'
    form_fields = ['conflict_ratings_json']

    def vars_for_template(player):
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        return dict(
            groups_json=json.dumps(_profiles_with_self(player)),
            anon_icon=career_icons.get('__anon__', ''),
        )


class EtapasInstructions(Page):
    pass


class CPRInstructionsFrame(Page):
    pass


class CPRInstructionsExpectations(Page):
    pass


class CPRInstructionsStrategy(Page):
    pass


class CPRInstructionsPayments(Page):
    pass


page_sequence = [
    Identification,
    WaitForIdentification,    
    Wellcome, 
    AvatarSelection,   
    GisDegree,
    Trust,
    Conflict,
    EtapasInstructions,
    CPRInstructionsFrame,
    CPRInstructionsExpectations,
    CPRInstructionsStrategy,
    CPRInstructionsPayments,
]

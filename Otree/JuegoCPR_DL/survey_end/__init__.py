import json
from otree.api import *

doc = """
Cuestionario de cierre del Juego CPR-Bosque (survey_end).
Recoge: expectativas post-juego, identidad grupal (in-group y out-group),
experiencia previa con otras carreras, descripciones de estrategia y
datos sociodemográficos.
"""


# Logo de cada universidad: el color depende de la relación (misma U / misma
# carrera, etc.). El avatar final de cada compañero combina este logo con el
# ícono de carrera que el participante eligió en survey_ini/AvatarSelection.
UNI_LOGO_CLASS = {
    'UDD': 'logo-udd',
    'UTalca': 'logo-utalca',
    'UAndes': 'logo-uandes',
    'USACH': 'logo-usach',
}


def _icon_for_degree(career_icons, degree):
    """Ícono ('1'-'9') que el participante asignó a `degree` en AvatarSelection
    (survey_ini), sin distinguir universidad. Usa el ícono '__anon__' si la
    carrera no tiene ícono propio (p.ej. compañero anónimo)."""
    if degree:
        return career_icons.get(degree, '') or career_icons.get('__anon__', '')
    return career_icons.get('__anon__', '')


class C(BaseConstants):
    NAME_IN_URL = 'survey_end'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # ── ExpectationsScreenEnd ────────────────────────────────────────────────
    expectation_end_json = models.LongStringField(blank=True, label='')

    # ── GIS in-group (cierre) ────────────────────────────────────────────────
    gis_end_1 = models.IntegerField(
        min=1, max=9,
        label='Me siento identificado/a con los/as estudiantes de mi carrera.',
    )
    gis_end_2 = models.IntegerField(
        min=1, max=9,
        label='Me alegra pertenecer a mi carrera.',
    )
    gis_end_3 = models.IntegerField(
        min=1, max=9,
        label='Siento que pertenecer a mi carrera me frena o limita.',
    )
    gis_end_4 = models.IntegerField(
        min=1, max=9,
        label='Creo que los estudiantes de mi carrera funcionamos bien juntos.',
    )
    gis_end_5 = models.IntegerField(
        min=1, max=9,
        label='Me considero una parte importante de mi carrera.',
    )
    gis_end_6 = models.IntegerField(
        min=1, max=9,
        label='No encajo bien con los demás estudiantes de mi carrera.',
    )
    gis_end_7 = models.IntegerField(
        min=1, max=9,
        label='No considero que mi grupo de mi carrera sea importante.',
    )
    gis_end_8 = models.IntegerField(
        min=1, max=9,
        label='Me siento incómodo/a con los estudiantes de mi carrera.',
    )
    gis_end_9 = models.IntegerField(
        min=1, max=9,
        label='Siento fuertes lazos con los estudiantes de mi carrera.',
    )

    
    # ── Experiencia con otras carreras ────────────────────────────────────────
    # JSON: list of profile keys selected
    experience_careers_json = models.LongStringField(blank=True, label='')

    # ── Descripción de estrategia ────────────────────────────────────────────
    experience_strategy_self   = models.LongStringField(blank=True, label='')
    experience_strategy_others = models.LongStringField(blank=True, label='')

    # ── Sociodemografía ──────────────────────────────────────────────────────
    gender      = models.StringField(blank=True, label='')
    gender_text = models.StringField(blank=True, label='')
    year_study  = models.StringField(blank=True, label='')
    age         = models.StringField(blank=True, label='')


# ─────────────────────────────────────────────────────────────────────────────
# Funciones auxiliares
# ─────────────────────────────────────────────────────────────────────────────

def _get_profiles_for_player(player: 'Player') -> list:
    """Perfiles distintos (universidad × carrera) del resto de la sesión."""
    my_uni = player.participant.vars.get('university', '')
    my_deg = player.participant.vars.get('degree', '')
    career_icons = player.participant.vars.get('career_icons', {}) or {}
    profiles = {}
    for p in player.subsession.get_players():
        if p.id_in_subsession == player.id_in_subsession:
            continue
        u = p.participant.vars.get('university', '')
        d = p.participant.vars.get('degree', '')
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
            profiles[key] = dict(
                key=key, university=u, degree=d,
                count=0, relation=relation,
                icon=_icon_for_degree(career_icons, d),
            )
        profiles[key]['count'] += 1
    return list(profiles.values())


def _profiles_with_self(player: 'Player') -> list:
    """Perfiles de la sesión garantizando que el propio aparece primero."""
    my_uni = player.participant.vars.get('university', '')
    my_deg = player.participant.vars.get('degree', '')
    my_key = f"{my_uni}__{my_deg}"
    profiles = _get_profiles_for_player(player)
    if my_uni and my_deg and not any(p['key'] == my_key for p in profiles):
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        profiles.insert(0, {
            'key': my_key, 'university': my_uni, 'degree': my_deg,
            'count': 0, 'relation': 'you',
            'icon': _icon_for_degree(career_icons, my_deg),
        })
    return profiles


def _profile_vars(player: 'Player') -> dict:
    career_icons = player.participant.vars.get('career_icons', {}) or {}
    return dict(
        groups_json=json.dumps(_profiles_with_self(player)),
        my_university=player.participant.vars.get('university', ''),
        my_degree=player.participant.vars.get('degree', ''),
        anon_icon=_icon_for_degree(career_icons, ''),
    )


def _outgroup_targets_for_player(player: 'Player') -> list:
    """Compañeros reales del equipo de cpr_game sobre quienes se pregunta la
    escala de identidad de out-group.

    - Grupo homogéneo o anónimo: una sola caja genérica "Estudiante Anónimo"
      (en el grupo homogéneo los 2 compañeros comparten el propio perfil, por
      lo que no hay un verdadero out-group al que preguntar).
    - Si uno de los 2 compañeros comparte universidad y carrera con el
      participante, se omite (no es out-group) y solo se pregunta por el otro.
    - En caso contrario, se pregunta por ambos compañeros, identificados.
    """
    career_icons = player.participant.vars.get('career_icons', {}) or {}
    is_anon = player.participant.vars.get('is_anon_group', False)
    is_homo = player.participant.vars.get('is_homo_group', 0)
    if is_anon or is_homo:
        return [{
            'key': '__anon__', 'university': '', 'degree': '', 'relation': 'anon',
            'icon': _icon_for_degree(career_icons, ''),
        }]

    my_uni = player.participant.vars.get('university', '')
    my_deg = player.participant.vars.get('degree', '')
    teammates = player.participant.vars.get('teammates', []) or []

    targets = []
    for t in teammates:
        u = t.get('university', '')
        d = t.get('degree', '')
        if u == my_uni and d == my_deg:
            continue
        same_uni = (u == my_uni)
        same_deg = (d == my_deg)
        if same_uni:
            relation = 'nearClose'
        elif same_deg:
            relation = 'nearFar'
        else:
            relation = 'far'
        targets.append({
            'key': f"{u}__{d}", 'university': u, 'degree': d, 'relation': relation,
            'icon': _icon_for_degree(career_icons, d),
        })

    if not targets:
        return [{
            'key': '__anon__', 'university': '', 'degree': '', 'relation': 'anon',
            'icon': _icon_for_degree(career_icons, ''),
        }]
    return targets


# Bono "expectativas acertadas": hectáreas por expectativa correcta y tarifa
# por hectárea (debe coincidir con cpr_game.C.TOKEN_VALUE_CLP) usados en el
# pago final.
BONUS_HECTARES = 5
TOKEN_VALUE_CLP = 60


def _expectation_bonus_hectares(player: 'Player', prediction_field: str, actual_key: str) -> int:
    """Hectáreas de bono por una ronda de expectativas (ronda 1: predictions
    en 'expectation_ini_json' / actuals en 'round1_extraction'; ronda 4:
    'expectation_rg_json' / 'round4_extraction'). Ambos JSON de predicciones
    están guardados con la misma forma {perfil_o_'__anon__': valor}.

    - Grupo homogéneo o anónimo: los 2 compañeros comparten una sola
      predicción (mismo perfil, o "Anónimo"), así que se compara contra el
      promedio real de ambos, redondeado hacia abajo. Si acierta: 10 ha.
    - Grupo mixto: se compara cada compañero por separado contra la
      predicción hecha para su propio perfil. 5 ha por cada acierto (hasta 10
      si ambos aciertan).
    """
    teammates = player.participant.vars.get('teammates') or []
    if len(teammates) < 2 or any(actual_key not in t for t in teammates):
        return 0

    predictions = json.loads(player.participant.vars.get(prediction_field, '{}') or '{}')
    is_anon = player.participant.vars.get('is_anon_group', False)
    is_homo = player.participant.vars.get('is_homo_group', 0)

    if is_anon or is_homo:
        my_uni = player.participant.vars.get('university', '')
        my_deg = player.participant.vars.get('degree', '')
        key = '__anon__' if is_anon else f"{my_uni}__{my_deg}"
        predicted = predictions.get(key)
        if predicted is None:
            return 0
        actual_avg = (int(teammates[0][actual_key]) + int(teammates[1][actual_key])) // 2
        return BONUS_HECTARES * 2 if int(predicted) == actual_avg else 0

    bonus = 0
    for t in teammates:
        key = f"{t.get('university', '')}__{t.get('degree', '')}"
        predicted = predictions.get(key)
        if predicted is not None and int(predicted) == int(t[actual_key]):
            bonus += BONUS_HECTARES
    return bonus


def _total_expectation_bonus_hectares(player: 'Player') -> int:
    return (
        _expectation_bonus_hectares(player, 'expectation_ini_json', 'round1_extraction')
        + _expectation_bonus_hectares(player, 'expectation_rg_json', 'round4_extraction')
    )


# ─────────────────────────────────────────────────────────────────────────────
# Páginas
# ─────────────────────────────────────────────────────────────────────────────

class ExpectationsScreenEnd(Page):
    form_model = 'player'
    form_fields = ['expectation_end_json']

    @staticmethod
    def vars_for_template(player: Player):
        return _profile_vars(player)


class gisDegreeEnd(Page):
    form_model = 'player'
    form_fields = [
        'gis_end_1', 'gis_end_2', 'gis_end_3', 'gis_end_4', 'gis_end_5',
        'gis_end_6', 'gis_end_7', 'gis_end_8', 'gis_end_9',
    ]

    @staticmethod
    def vars_for_template(player: Player):
        my_uni = player.participant.vars.get('university', '')
        my_deg = player.participant.vars.get('degree', '')
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        return dict(
            my_university=my_uni,
            my_degree=my_deg,
            my_logo_class=UNI_LOGO_CLASS.get(my_uni, ''),
            my_icon_id=_icon_for_degree(career_icons, my_deg),
        )


class postExptQuestionsExperienciaCarrera(Page):
    form_model = 'player'
    form_fields = ['experience_careers_json']

    @staticmethod
    def vars_for_template(player: Player):
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        return dict(
            groups_json=json.dumps(_profiles_with_self(player)),
            anon_icon=_icon_for_degree(career_icons, ''),
        )


class postExptQuestionsDescription(Page):
    form_model = 'player'
    form_fields = ['experience_strategy_self', 'experience_strategy_others']

    @staticmethod
    def error_message(player: Player, values):
        if not (values.get('experience_strategy_self') or '').strip():
            return 'Por favor escribe tu respuesta a la primera pregunta.'
        if not (values.get('experience_strategy_others') or '').strip():
            return 'Por favor escribe tu respuesta a la segunda pregunta.'


class postExptSocioDem(Page):
    form_model = 'player'
    form_fields = ['gender', 'gender_text', 'year_study', 'age']

    @staticmethod
    def error_message(player: Player, values):
        if not (values.get('gender') or '').strip():
            return 'Por favor indica cómo te describes.'
        if not (values.get('year_study') or '').strip():
            return 'Por favor indica en qué año de carrera estás.'
        if not (values.get('age') or '').strip():
            return 'Por favor indica tu edad.'


class finalPayment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        game_hectares = player.participant.vars.get('cpr_total_hectares', 0)
        bonus_hectares = _total_expectation_bonus_hectares(player)
        total_hectares = game_hectares + bonus_hectares
        bonus_payment = bonus_hectares * TOKEN_VALUE_CLP
        # Idempotente: cada carga de la página fija (no acumula) el bono en el
        # payoff de este jugador. Las 15 rondas del juego ya fueron pagadas
        # por cpr_game a la misma tarifa (TOKEN_VALUE_CLP), así que sumando
        # solo el bono acá, participant.payoff termina siendo exactamente
        # total_hectares * TOKEN_VALUE_CLP.
        player.payoff = bonus_payment
        return dict(
            game_hectares=game_hectares,
            bonus_hectares=bonus_hectares,
            total_hectares=total_hectares,
            token_value=TOKEN_VALUE_CLP,
            total_payment=total_hectares * TOKEN_VALUE_CLP,
        )


page_sequence = [
    ExpectationsScreenEnd,
    gisDegreeEnd,
    postExptQuestionsExperienciaCarrera,
    postExptQuestionsDescription,
    postExptSocioDem,
    finalPayment,
]

import json
import random
from collections import defaultdict
from otree.api import *

doc = """
Juego de Recursos Comunes (CPR) – Fondo Estudiantil
3 jugadores aleatorizados por orden de llegada, 15 rondas.

Mecánica:
- Fondo inicial: 100 tokens
- Cada jugador cosecha 0–10 tokens por ronda (simultáneo y privado)
- Regeneración: tokens_restantes × 1.18, tope 100
- Si fondo < 30: nadie puede cosechar hasta que el fondo se regenere de vuelta a 30 o más
- Pago: $60 CLP por token cosechado
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
    NAME_IN_URL = 'cpr'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 15
    INITIAL_POOL = 100
    MAX_EXTRACTION = 10
    REGEN_RATE = 0.18
    POOL_COLLAPSE_THRESHOLD = 30
    # Debe coincidir con survey_end.TOKEN_VALUE_CLP: es la misma tarifa que se
    # usa para el bono de expectativas y el desglose de la pantalla de pago final.
    TOKEN_VALUE_CLP = 60
    SUSTAINABILITY_THRESHOLD = 16
    # 4 versions of the Strategy table (columns_rows): each participant is
    # randomly assigned exactly one, used for all 3 of their StrategySlot pages.
    STRATEGY_TABLE_VERSIONS = ['3_4', '3_11', '4_4', '4_11']


# Bosque disponible (columnas) y cosecha promedio de los demás (filas) que
# ofrece cada versión de la tabla de Estrategia. Debe reflejar exactamente los
# arrays STOCKS/SCENARIOS de cpr_game/StrategySlot_<version>.html.
STRATEGY_TABLE_DEFS = {
    '3_4':  {'stocks': [100, 75, 50],     'scenarios': [5, 7, 9, 10]},
    '3_11': {'stocks': [100, 75, 50],     'scenarios': list(range(11))},
    '4_4':  {'stocks': [100, 75, 50, 30], 'scenarios': [5, 7, 9, 10]},
    '4_11': {'stocks': [100, 75, 50, 30], 'scenarios': list(range(11))},
}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pool_before = models.IntegerField(initial=100)
    pool_after = models.IntegerField(initial=100)
    total_extracted = models.IntegerField(initial=0)


class Player(BasePlayer):
    extraction = models.IntegerField(min=0, max=10, blank=True, initial=0)
    earnings_round = models.IntegerField(initial=0)
    expectation_ini_json = models.LongStringField(blank=True)
    expectation_rg_json = models.LongStringField(blank=True)
    strategy_noinfo_json = models.LongStringField(blank=True)
    strategy_info_json = models.LongStringField(blank=True)
    strategy_homo_json = models.LongStringField(blank=True)
    is_anon_group = models.BooleanField(initial=False)
    is_homo_group = models.IntegerField(initial=0)
    strategy_table_version = models.StringField(blank=True)
    # Ronda (1-15), sorteada una vez por participante, cuyo pago/resultado se
    # reemplaza por la respuesta de Estrategia en vez de la decisión real.
    strategy_payment_round = models.IntegerField(blank=True)
    # True solo en esa ronda si efectivamente se pudo aplicar el reemplazo.
    paid_by_strategy = models.BooleanField(initial=False)
    # Hectáreas provenientes de la respuesta de Estrategia usadas ese round.
    strategy_extraction = models.IntegerField(blank=True)


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for group in subsession.get_groups():
            group.pool_before = C.INITIAL_POOL


def _form_groups(subsession: Subsession) -> list:
    """
    Three-step group formation (runs once, round 1):

    1. For each (university × degree) with > 4 players: pick 3 at random
       → homogeneous group (players see each other's identity).
    2. From all remaining ungrouped players: pick 3 at random
       → anonymous group (is_anon_group = True; they never see teammates'
       university/degree in the game pages). Skipped entirely if the session
       has only 3 participants in total.
    3. Remaining ungrouped players: random groups of 3.
       If a leftover < 3 exists it is appended to the last group.

    Sets participant.vars['is_anon_group'] for every player.
    Returns the group matrix (list of lists of Player objects).
    """
    players = subsession.get_players()

    # Bucket players by (university, degree) using participant.vars
    by_profile: dict = defaultdict(list)
    for p in players:
        key = (
            p.participant.vars.get('university', '') or '',
            p.participant.vars.get('degree', '') or '',
        )
        by_profile[key].append(p)

    # Initialise flags for all players
    for p in players:
        p.participant.vars['is_anon_group'] = False
        p.participant.vars['is_homo_group'] = 0
        order = ['noinfo', 'info', 'homo']
        random.shuffle(order)
        p.participant.vars['strategy_order'] = order
        p.participant.vars['strategy_table_version'] = random.choice(C.STRATEGY_TABLE_VERSIONS)
        p.participant.vars['strategy_payment_round'] = random.randint(1, C.NUM_ROUNDS)

    ungrouped = list(players)
    matrix = []

    # Step 1 — ONE homogeneous group from the largest qualifying profile (> 4 students)
    # If multiple profiles tie on count, the one that sorts first alphabetically wins.
    eligible = [
        (key, bucket)
        for key, bucket in by_profile.items()
        if len(bucket) > 4
    ]
    if eligible:
        eligible.sort(key=lambda x: (-len(x[1]), x[0]))
        _, bucket = eligible[0]
        bucket = list(bucket)
        random.shuffle(bucket)
        selected = bucket[:3]
        matrix.append(selected)
        for p in selected:
            ungrouped.remove(p)
            p.participant.vars['is_homo_group'] = 1

    # Step 2 — one anonymous group (skipped if the whole session only has 3
    # participants, since then there'd be nothing left but the anon group).
    random.shuffle(ungrouped)
    if len(players) > 3 and len(ungrouped) >= 3:
        anon_group = ungrouped[:3]
        matrix.append(anon_group)
        for p in anon_group:
            p.participant.vars['is_anon_group'] = True
        ungrouped = ungrouped[3:]

    # Step 3 — random groups of 3 from the rest
    random.shuffle(ungrouped)
    i = 0
    while i + 3 <= len(ungrouped):
        matrix.append(ungrouped[i:i + 3])
        i += 3

    # Attach any leftover (< 3) to the last group
    leftover = ungrouped[i:]
    if leftover:
        if matrix:
            matrix[-1].extend(leftover)
        else:
            matrix.append(leftover)

    return matrix


def get_pool_before(group: Group) -> int:
    if group.round_number == 1:
        return C.INITIAL_POOL
    return group.pool_before


def get_max_extraction(group: Group) -> int:
    pool = get_pool_before(group)
    if pool < C.POOL_COLLAPSE_THRESHOLD:
        return 0
    return C.MAX_EXTRACTION


def get_sustainability_threshold(group: Group) -> int:
    """Cosecha total del equipo (3 personas) que mantiene el bosque estable."""
    pool = get_pool_before(group)
    return int(pool - pool / 1.18)


def get_sustainability_individual_threshold(group: Group) -> int:
    """Cuota individual sustentable: la cosecha total dividida entre 3, hacia
    abajo, para garantizar que si los 3 la respetan el total siga siendo
    sustentable (redondear hacia arriba podría superar el umbral total)."""
    return get_sustainability_threshold(group) // 3


def _official_extraction(player: 'Player') -> int:
    """La jugada 'oficial' de este jugador para esta ronda.

    En la ronda sorteada como su ronda de pago por Estrategia, la jugada
    oficial (la que ve el resto del grupo, la que se usa para el total del
    equipo y para el bosque disponible de la siguiente ronda) es su respuesta
    de Estrategia, no lo que efectivamente escribió esa ronda. Lo que escribió
    queda guardado en player.extraction, pero deja de usarse para todo lo
    demás una vez reemplazado.
    """
    if player.paid_by_strategy:
        return player.strategy_extraction or 0
    return player.extraction or 0


def set_payoffs(group: Group):
    players = group.get_players()
    pool = get_pool_before(group)
    group.pool_before = pool

    # Paso 1: si a algún jugador le tocó esta ronda como su ronda de pago por
    # Estrategia, resolvemos su respuesta ahora (usando el promedio real de
    # sus compañeros) y la dejamos marcada como su jugada oficial.
    for p in players:
        if p.strategy_payment_round == group.round_number:
            others = [q for q in players if q.id_in_subsession != p.id_in_subsession]
            mean_others = sum((q.extraction or 0) for q in others) / len(others) if others else 0
            strategy_value = _strategy_value_for_payment(p, pool, mean_others)
            if strategy_value is not None:
                p.paid_by_strategy = True
                p.strategy_extraction = strategy_value

    # Paso 2: el total del grupo y el bosque de la ronda siguiente se calculan
    # con las jugadas oficiales (reemplazadas cuando corresponde), no con lo
    # que cada uno escribió.
    total = sum(_official_extraction(p) for p in players)
    group.total_extracted = total

    remaining = pool - total
    if remaining <= 0:
        group.pool_after = 0
    else:
        regenerated = int(remaining * (1 + C.REGEN_RATE))
        group.pool_after = min(C.INITIAL_POOL, regenerated)

    if group.round_number < C.NUM_ROUNDS:
        next_group = group.in_round(group.round_number + 1)
        next_group.pool_before = group.pool_after

    for p in players:
        official = _official_extraction(p)
        p.earnings_round = official * C.TOKEN_VALUE_CLP
        p.payoff += p.earnings_round
        # Total cosechado (oficial) a lo largo de las 15 rondas; survey_end lo
        # usa para el desglose de la pantalla de pago final.
        p.participant.vars['cpr_total_hectares'] = p.participant.vars.get('cpr_total_hectares', 0) + official

    # Rondas 1 y 4: estampar en 'teammates' la jugada oficial de cada
    # compañero real (ver _official_extraction), para que survey_end pueda
    # calcular el bono de expectativas de ExpectationsScreenIni/RG1.
    if group.round_number in (1, 4):
        field_name = 'round1_extraction' if group.round_number == 1 else 'round4_extraction'
        extraction_by_code = {p.participant.code: _official_extraction(p) for p in players}
        for p in players:
            teammates = p.participant.vars.get('teammates') or []
            for t in teammates:
                code = t.get('participant_code')
                if code in extraction_by_code:
                    t[field_name] = extraction_by_code[code]
            p.participant.vars['teammates'] = teammates


def _get_profiles_for_player(player: 'Player'):
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
            profiles[key] = {
                'key': key, 'university': u, 'degree': d,
                'count': 0, 'relation': relation,
                'icon': _icon_for_degree(career_icons, d),
            }
        profiles[key]['count'] += 1
    return list(profiles.values())


def _profiles_with_self(player: 'Player') -> list:
    """Perfiles de la sesión garantizando que el propio perfil aparece primero."""
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


def _group_opponents(player: 'Player') -> list:
    is_anon = player.participant.vars.get('is_anon_group', False)
    my_uni = player.participant.vars.get('university', '')
    my_deg = player.participant.vars.get('degree', '')
    career_icons = player.participant.vars.get('career_icons', {}) or {}
    opponents = []
    for p in player.group.get_players():
        if p.id_in_subsession == player.id_in_subsession:
            continue
        if is_anon:
            # Anonymous group: hide teammate identity
            u, d, relation = '', '', 'anon'
        else:
            u = p.participant.vars.get('university', '')
            d = p.participant.vars.get('degree', '')
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
        opponents.append({
            'university': u, 'degree': d,
            'relation': relation,
            'icon': _icon_for_degree(career_icons, d),
            'extraction': _official_extraction(p),
        })
    return opponents


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------

class WaitForGroup(WaitPage):
    wait_for_all_groups = True
    title_text = "Esperando a los demás participantes..."
    body_text = (
        "Estamos formando los equipos. "
        "Por favor espera mientras los demás participantes completan su registro."
    )

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        if subsession.round_number != 1:
            return

        matrix = _form_groups(subsession)
        subsession.set_group_matrix(matrix)

        # Propagate the same groups to rounds 2–15
        for rnd in range(2, C.NUM_ROUNDS + 1):
            future = [[p.in_round(rnd) for p in grp] for grp in matrix]
            subsession.in_round(rnd).set_group_matrix(future)

        # Initialise pool for the newly-assigned round-1 groups
        for group in subsession.get_groups():
            group.pool_before = C.INITIAL_POOL

        # Write group-type flags to the Player field in every round
        for grp in matrix:
            for p in grp:
                is_anon = p.participant.vars.get('is_anon_group', False)
                is_homo = p.participant.vars.get('is_homo_group', 0)
                table_version = p.participant.vars.get('strategy_table_version') or C.STRATEGY_TABLE_VERSIONS[0]
                payment_round = p.participant.vars.get('strategy_payment_round') or 1
                for rnd in range(1, C.NUM_ROUNDS + 1):
                    p.in_round(rnd).is_anon_group = is_anon
                    p.in_round(rnd).is_homo_group = is_homo
                    p.in_round(rnd).strategy_table_version = table_version
                    p.in_round(rnd).strategy_payment_round = payment_round

        # Store each player's real teammates' profile (university/degree) so
        # later apps (e.g. survey_end) can reference the actual game group
        # without needing access to cpr_game's app-specific Group model.
        for grp in matrix:
            for p in grp:
                p.participant.vars['teammates'] = [
                    {
                        'university': q.participant.vars.get('university', ''),
                        'degree': q.participant.vars.get('degree', ''),
                        'participant_code': q.participant.code,
                    }
                    for q in grp if q.id_in_subsession != p.id_in_subsession
                ]


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ExpectationsScreenIni(Page):
    form_model = 'player'
    form_fields = ['expectation_ini_json']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        return dict(
            groups_json=json.dumps(_profiles_with_self(player)),
            anon_icon=_icon_for_degree(career_icons, ''),
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Copia las predicciones de la ronda 1 a participant.vars para que
        # survey_end pueda calcular el bono de expectativas acertadas.
        player.participant.vars['expectation_ini_json'] = player.expectation_ini_json or '{}'


_STRATEGY_FIELD_BY_VARIANT = {
    'noinfo': 'strategy_noinfo_json',
    'info': 'strategy_info_json',
    'homo': 'strategy_homo_json',
}


def _strategy_variant_for_slot(player: 'Player', slot_index: int) -> str:
    order = player.participant.vars.get('strategy_order') or ['noinfo', 'info', 'homo']
    return order[slot_index]


def _strategy_groups_for_variant(player: 'Player', variant: str) -> list:
    career_icons = player.participant.vars.get('career_icons', {}) or {}
    if variant == 'noinfo':
        anon_icon = _icon_for_degree(career_icons, '')
        return [
            {'key': '__anon__', 'university': '', 'degree': '', 'relation': 'anon', 'icon': anon_icon},
            {'key': '__anon__', 'university': '', 'degree': '', 'relation': 'anon', 'icon': anon_icon},
        ]
    if variant == 'homo':
        my_uni = player.participant.vars.get('university', '')
        my_deg = player.participant.vars.get('degree', '')
        my_key = f"{my_uni}__{my_deg}"
        my_icon = _icon_for_degree(career_icons, my_deg)
        return [
            {'key': my_key, 'university': my_uni, 'degree': my_deg, 'relation': 'you', 'icon': my_icon},
            {'key': my_key, 'university': my_uni, 'degree': my_deg, 'relation': 'you', 'icon': my_icon},
        ]
    return _get_profiles_for_player(player)[:2]


def _strategy_vars_for_slot(player: 'Player', slot_index: int) -> dict:
    variant = _strategy_variant_for_slot(player, slot_index)
    return dict(
        variant=variant,
        field_name=_STRATEGY_FIELD_BY_VARIANT[variant],
        groups_json=json.dumps(_strategy_groups_for_variant(player, variant)),
    )


def _strategy_variant_for_actual_group(player: 'Player') -> str:
    """Variante de Estrategia que corresponde al grupo real que le tocó al
    jugador en el juego (no al orden aleatorio de los slots)."""
    if player.is_homo_group:
        return 'homo'
    if player.is_anon_group:
        return 'noinfo'
    return 'info'


def _strategy_value_for_payment(player: 'Player', pool_before: int, mean_others: float):
    """Busca, en la respuesta de Estrategia de la variante que corresponde al
    grupo real del jugador, el valor cuya combinación (bosque disponible,
    cosecha promedio de los demás) es más cercana a lo ocurrido esta ronda.
    Devuelve None si el jugador no alcanzó a responder esa Estrategia."""
    variant = _strategy_variant_for_actual_group(player)
    field_name = _STRATEGY_FIELD_BY_VARIANT[variant]
    # Las respuestas de Estrategia solo se guardan en la ronda 1.
    raw = getattr(player.in_round(1), field_name)
    if not raw:
        return None
    try:
        answers = json.loads(raw)
    except ValueError:
        return None
    if not answers:
        return None

    table_def = STRATEGY_TABLE_DEFS.get(player.strategy_table_version) \
        or STRATEGY_TABLE_DEFS[C.STRATEGY_TABLE_VERSIONS[0]]
    closest_stock = min(table_def['stocks'], key=lambda s: abs(s - pool_before))
    closest_scenario = min(table_def['scenarios'], key=lambda sc: abs(sc - mean_others))
    key = f"scen{closest_scenario}_st{closest_stock}"
    return answers.get(key)


def _strategy_template_name(player: 'Player') -> str:
    version = player.strategy_table_version or C.STRATEGY_TABLE_VERSIONS[0]
    return f'cpr_game/StrategySlot_{version}.html'


class StrategySlot1(Page):
    """Fase II – Estrategia. Cada 'slot' (1, 2 y 3) muestra una de las 3
    variantes (sin información, con información, homogénea); el orden se
    aleatoriza por participante en WaitForGroup.after_all_players_arrive.
    La tabla (columnas de bosque x filas de cosecha) también se sortea por
    participante entre las 4 versiones disponibles (StrategySlot_<version>.html)."""
    form_model = 'player'

    def get_template_name(self):
        return _strategy_template_name(self.player)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def get_form_fields(player: Player):
        return [_STRATEGY_FIELD_BY_VARIANT[_strategy_variant_for_slot(player, 0)]]

    @staticmethod
    def vars_for_template(player: Player):
        return _strategy_vars_for_slot(player, 0)


class StrategySlot2(Page):
    form_model = 'player'

    def get_template_name(self):
        return _strategy_template_name(self.player)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def get_form_fields(player: Player):
        return [_STRATEGY_FIELD_BY_VARIANT[_strategy_variant_for_slot(player, 1)]]

    @staticmethod
    def vars_for_template(player: Player):
        return _strategy_vars_for_slot(player, 1)


class StrategySlot3(Page):
    form_model = 'player'

    def get_template_name(self):
        return _strategy_template_name(self.player)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def get_form_fields(player: Player):
        return [_STRATEGY_FIELD_BY_VARIANT[_strategy_variant_for_slot(player, 2)]]

    @staticmethod
    def vars_for_template(player: Player):
        return _strategy_vars_for_slot(player, 2)


class ExpectationsScreenRG1(Page):
    form_model = 'player'
    form_fields = ['expectation_rg_json']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        pool = get_pool_before(group)
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        if player.is_anon_group:
            # Compañeros indistinguibles: una sola fila para ambos.
            opponents = [{
                'university': '', 'degree': '',
                'relation': 'anon',
                'icon': _icon_for_degree(career_icons, ''),
                'extraction': 0,
            }]
        elif player.is_homo_group:
            # Mismo perfil que el propio participante: una sola fila también.
            my_uni = player.participant.vars.get('university', '')
            my_deg = player.participant.vars.get('degree', '')
            opponents = [{
                'university': my_uni, 'degree': my_deg,
                'relation': 'you',
                'icon': _icon_for_degree(career_icons, my_deg),
                'extraction': 0,
            }]
        else:
            opponents = _group_opponents(player)
        return dict(
            opponents=json.dumps(opponents),
            bosque_disponible=pool,
            cuota_sustentable=get_sustainability_individual_threshold(group),
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Las respuestas llegan indexadas por fila (member_0, member_1). Las
        # normalizamos a {perfil: valor} -- el mismo formato que
        # expectation_ini_json -- para que survey_end pueda reusar la misma
        # lógica de comparación en ambas rondas de expectativas.
        raw = json.loads(player.expectation_rg_json or '{}')
        if player.is_anon_group:
            predictions = {'__anon__': raw.get('member_0')}
        elif player.is_homo_group:
            my_uni = player.participant.vars.get('university', '')
            my_deg = player.participant.vars.get('degree', '')
            predictions = {f"{my_uni}__{my_deg}": raw.get('member_0')}
        else:
            mates = [q for q in player.group.get_players() if q.id_in_subsession != player.id_in_subsession]
            predictions = {}
            for idx, mate in enumerate(mates):
                u = mate.participant.vars.get('university', '')
                d = mate.participant.vars.get('degree', '')
                predictions[f"{u}__{d}"] = raw.get(f'member_{idx}')
        player.participant.vars['expectation_rg_json'] = json.dumps(predictions)


class Decision1to15_game1(Page):
    form_model = 'player'
    form_fields = ['extraction']

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        pool = get_pool_before(group)
        max_ext = get_max_extraction(group)
        pct = round(pool / C.INITIAL_POOL * 100)
        if pool > 75:
            bar_color = '#5E8C61'
        elif pool >= 51:
            bar_color = '#C9963A'
        else:
            bar_color = '#B5564B'
        my_uni = player.participant.vars.get('university', '')
        my_deg = player.participant.vars.get('degree', '')
        career_icons = player.participant.vars.get('career_icons', {}) or {}
        return dict(
            round_number=player.round_number,
            pool_before=pool,
            max_extraction=max_ext,
            is_constrained=pool < C.POOL_COLLAPSE_THRESHOLD,
            token_value=C.TOKEN_VALUE_CLP,
            sustainability_threshold=int(pool - pool / 1.18),
            sustainability_individual_threshold=int((pool - pool / 1.18)/3),
            total_rounds=C.NUM_ROUNDS,
            pool_pct=pct,
            bar_color=bar_color,
            my_university=my_uni,
            my_degree=my_deg,
            my_logo_class=UNI_LOGO_CLASS.get(my_uni, ''),
            my_icon_id=_icon_for_degree(career_icons, my_deg),
            opponents=json.dumps(_group_opponents(player)),
        )

    @staticmethod
    def error_message(player: Player, values):
        max_ext = get_max_extraction(player.group)
        ext = values.get('extraction', 0)
        if ext is None or ext < 0:
            return "Debes ingresar un número entre 0 y el máximo permitido."
        if ext > max_ext:
            pool = get_pool_before(player.group)
            return (
                f"El fondo actual es de {pool} tokens. "
                f"El máximo que puedes usar esta ronda es {max_ext}."
            )


class Feedback_game1_wait(WaitPage):
    after_all_players_arrive = 'set_payoffs'
    title_text = "Procesando resultados..."
    body_text = "Esperando que los otros integrantes de tu equipo envíen su decisión."


class Feedback_game1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        pool_b = group.pool_before
        pool_a = group.pool_after
        total = group.total_extracted
        remaining = pool_b - total
        regen = pool_a - remaining if remaining > 0 else 0
        my_extraction = _official_extraction(player)
        others = [p for p in group.get_players() if p.id_in_subsession != player.id_in_subsession]
        mean_others = sum(_official_extraction(p) for p in others) / len(others) if others else 0
        my_uni = player.participant.vars.get('university', '')
        my_deg = player.participant.vars.get('degree', '')
        career_icons = player.participant.vars.get('career_icons', {}) or {}

        sustainability_threshold = int(pool_b - pool_b / 1.18)
        if total <= sustainability_threshold:
            groupsum_color, groupsum_bg = '#5E8C61', '#EFF5EF'
        else:
            groupsum_color, groupsum_bg = '#B5564B', '#F7EBE9'

        if player.earnings_round > 0:
            ganancia_color, ganancia_bg = '#5E8C61', '#EFF5EF'
        else:
            ganancia_color, ganancia_bg = '#B5564B', '#F7EBE9'

        if pool_a > 75:
            newres_color, newres_bg = '#5E8C61', '#EFF5EF'
        elif pool_a >= 51:
            newres_color, newres_bg = '#C9963A', '#FAF1E3'
        else:
            newres_color, newres_bg = '#B5564B', '#F7EBE9'

        return dict(
            round_number=player.round_number,
            total_rounds=C.NUM_ROUNDS,
            pool_before=pool_b,
            pool_after=pool_a,
            total_extracted=total,
            my_extraction=my_extraction,
            paid_by_strategy=player.paid_by_strategy,
            mean_others=round(mean_others, 1),
            earnings_round=player.earnings_round,
            token_value=C.TOKEN_VALUE_CLP,
            regeneration=regen,
            my_university=my_uni,
            my_degree=my_deg,
            my_logo_class=UNI_LOGO_CLASS.get(my_uni, ''),
            my_icon_id=_icon_for_degree(career_icons, my_deg),
            opponents=json.dumps(_group_opponents(player)),
            groupsum_color=groupsum_color, groupsum_bg=groupsum_bg,
            ganancia_color=ganancia_color, ganancia_bg=ganancia_bg,
            newres_color=newres_color, newres_bg=newres_bg,
        )


page_sequence = [
    WaitForGroup,
    Instructions,    
    StrategySlot1,
    StrategySlot2,
    StrategySlot3,
    ExpectationsScreenIni,
    ExpectationsScreenRG1,
    Decision1to15_game1,
    Feedback_game1_wait,
    Feedback_game1,
]

# cards/models.py

from django.db import models

# ----------------------------
# MODELOS PARA YU-GI-OH! (yugioh.db)
# ----------------------------

class YuGiOhCard(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    attribute = models.TextField(blank=True)
    effect = models.TextField(blank=True)
    specie_and_others = models.TextField(blank=True)
    link = models.TextField(blank=True)
    atk = models.TextField(blank=True)
    defs = models.TextField(blank=True)
    url = models.TextField(blank=True)
    level = models.TextField(blank=True)
    p_scale = models.TextField(blank=True)
    p_scale_effect = models.TextField(blank=True)
    img_url = models.URLField(max_length=500, blank=True)

    class Meta:
        db_table = 'cards'
        managed = False
        app_label = 'cards'
        verbose_name = 'Yu-Gi-Oh! Card'
        verbose_name_plural = 'Yu-Gi-Oh! Cards'

    def __str__(self):
        return self.name


class YuGiOhSet(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True)

    class Meta:
        db_table = 'sets'
        managed = False
        app_label = 'cards'
        verbose_name = 'Yu-Gi-Oh! Set'
        verbose_name_plural = 'Yu-Gi-Oh! Sets'

    def __str__(self):
        return self.name


class YuGiOhCardSet(models.Model):
    card_id = models.ForeignKey(YuGiOhCard, on_delete=models.DO_NOTHING, db_constraint=False)
    set_id = models.ForeignKey(YuGiOhSet, on_delete=models.DO_NOTHING, db_constraint=False)
    date = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    rarity = models.CharField(max_length=200)
    card_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'card_set'
        managed = False
        app_label = 'cards'
        verbose_name = 'Yu-Gi-Oh! Card-Set Link'
        verbose_name_plural = 'Yu-Gi-Oh! Card-Set Links'

    def __str__(self):
        return f"{self.card.name} in {self.set.name}"


# ----------------------------
# MODELOS PARA POKÉMON (pokemon.db)
# ----------------------------

class PokemonSet(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True)
    generation = models.TextField(blank=True)
    annotation = models.TextField(blank=True)
    url = models.TextField(blank=True)

    class Meta:
        db_table = 'sets'
        managed = False
        app_label = 'cards'
        verbose_name = 'Pokémon Set'
        verbose_name_plural = 'Pokémon Sets'

    def __str__(self):
        return self.name
    
class PokemonCard(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True)
    type = models.TextField(blank=True)
    ability_info = models.TextField(blank=True)
    ability_effect = models.TextField(blank=True)
    attack_1_info = models.TextField(blank=True)
    attack_1_effect = models.TextField(blank=True)
    attack_2_info = models.TextField(blank=True)
    attack_2_effect = models.TextField(blank=True)
    effect = models.TextField(blank=True)
    number_rarity = models.TextField(blank=True)
    weakness_ressistance_retreat = models.TextField(blank=True)
    extracted_from = models.TextField(blank=True)
    set_id = models.ForeignKey(
        PokemonSet,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column='set_id'
    )
    image = models.URLField(max_length=500)

    class Meta:
        db_table = 'cards'
        managed = False
        app_label = 'cards'
        verbose_name = 'Pokémon Card'
        verbose_name_plural = 'Pokémon Cards'

    def __str__(self):
        return self.name
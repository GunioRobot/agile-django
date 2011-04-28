# -*- coding: utf-8 -*-
from lettuce import step, world
from sure import that

@step(u'Dado el numero "(.*)"')
def dado_el_numero_group1(step, group1):
    world.numero1 = int(group1)

@step(u'Y dado el numero "(.*)"')
def y_dado_el_numero_group1(step, group1):
    world.numero2 = int(group1)

@step(u'Los sumo')
def los_sumo(step):
    world.resultado = world.numero1 + world.numero2

@step(u'Y veo el resultado "(.*)"')
def y_veo_el_resultado_group1(step, group1):
    assert that(world.resultado).equals(int(group1))
    
@step(u'see the page for (.+) seconds')
def see_the_page_for_n_seconds(step, n):
    import time
    time.sleep(float(n))
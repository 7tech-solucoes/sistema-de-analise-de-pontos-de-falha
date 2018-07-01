import json
from django.shortcuts import render
from django.http import HttpResponse
from ijapp.models import Juncao
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def get_juncao(request, juncao):
    j = Juncao.objects.filter(
        vsatname__contains='{}'.format(juncao.zfill(4))).first()
    if j is None:
        return HttpResponse(json.dumps({
            'error': 'Nao pertence a Primisys'
        }))
    d = {
        'vsatname': j.vsatname,
        'nmd': j.nmd,
        'ender': j.ender,
        'municipio': j.municipio,
        'UF': j.UF,
        'junserviço': j.junserviço,
        'compart': j.compart,
        'desc': j.desc,
        'nomeserv': j.nomeserv,
        'fone': j.fone,
        'primeid': j.primeid,
        'category': j.category,
        'serial': j.serial,
        'softprof': j.softprof,
        'devicetype': j.devicetype,
        'ipmgmt': j.ipmgmt,
        'iplan1': j.iplan1,
        'mask': j.mask,
        'servplan': j.servplan,
        'AIS': j.AIS,
        'OutrouteGroup': j.OutrouteGroup,
        'FAP': j.FAP,
        'IPGW': j.IPGW,
        'Ipipgw': j.Ipipgw,
        'IQoS': j.IQoS,
        'IQoSnum': j.IQoSnum,
        'Enable': j.Enable,
        'vadb': j.vadb,
        'vadb1': j.vadb1,
        'vadb2': j.vadb2,
        'Enable': j.Enable,
        'DDR': j.DDR,
    }
    return HttpResponse(json.dumps(d))


@csrf_exempt
def get_pontos_uf(request):

    def f(juncoes):
        dist = {}
        for j in juncoes:
            if j.UF in dist.keys():
                dist[j.UF] += 1
            else:
                dist[j.UF] = 1
        return dist

    return filtra_juncao(request, f)


@csrf_exempt
def get_pontos_ipgw(request):

    def f(juncoes):
        dist = {}
        for j in juncoes:
            if j.IPGW in dist.keys():
                dist[j.IPGW] += 1
            else:
                dist[j.IPGW] = 1
        return dist

    return filtra_juncao(request, f)


def filtra_juncao(request, funcao):
    if request.method == 'POST':
        n_juncoes = json.loads(request.body.decode('utf-8'))
        juncoes = []
        for j in n_juncoes:
            jun = Juncao.objects.filter(vsatname__contains='{}'.format(
                str(j).zfill(4))).first()
            if not jun is None:
                juncoes.append(jun)

        dist = funcao(juncoes)

        d = {
            'total': len(juncoes),
            'dados': dist
        }
    return HttpResponse(json.dumps(d))
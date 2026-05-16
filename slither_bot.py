import requests
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1505020954638553179/MA5J5g4DDBVlQuOylUeZX1qeroTpzU4G5E3LcmyeOUTnE-0KjlcaW6uEQWEsXuf35cNa"
API_URL = "https://slithermania.com.br/api/public/ranking-live"
SCORE_LIMITE = 45000
INTERVALO_VERIFICACAO = 30

def formatar_score(score):
            return f"{score:,}".replace(",", ".")

def enviar_alerta(nick, clan, score, lugar, slot_id, server_key):
            clan_texto = f" [{clan}]" if clan else ""
            embed = {
                "title": "Slither ALERTA - Ranker acima de 45.000!",
                "color": 0x00FF88,
                "fields": [
                    {"name": "Jogador", "value": f"**{nick}**{clan_texto}", "inline": True},
                    {"name": "Score Atual", "value": f"**{formatar_score(score)} pontos**", "inline": True},
                    {"name": "Posicao", "value": f"#{lugar}", "inline": True},
                    {"name": "Servidor", "value": f"Slot {slot_id} - {server_key}", "inline": False},
                ],
                "footer": {"text": "Slither Monitor - slithermania.com.br"},
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            payload = {
                "content": "@everyone",
                "username": "Slither Monitor",
                "embeds": [embed],
                "allowed_mentions": {"parse": ["everyone"]}
            }
            try:
                            r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                            if r.status_code in (200, 204):
                                                print(f"  Alerta enviado: {nick} - {formatar_score(score)} pts")
            else:
                                print(f"  Webhook retornou {r.status_code}: {r.text}")
except Exception as e:
        print(f"  Erro: {e}")

def verificar_ranking():
            try:
                            r = requests.get(API_URL, timeout=10)
                            r.raise_for_status()
                            dados = r.json()
except Exception as e:
        print(f"Erro ao buscar API: {e}")
        return
    slots = dados.get("slots", [])
    for slot in slots:
                    slot_id = slot.get("slotId")
                    server_key = slot.get("serverKey", "?")
                    top10 = slot.get("top10", [])
                    for jogador in top10:
                                        nick = jogador.get("nick", "?")
                                        clan = jogador.get("clan", "")
                                        score = jogador.get("score", 0)
                                        lugar = jogador.get("place", 0)
                                        if score > SCORE_LIMITE:
                                                                enviar_alerta(nick, clan, score, lugar, slot_id, server_key)

                            if __name__ == "__main__":
                                        print(f"Slither Monitor iniciado! Limite: {formatar_score(SCORE_LIMITE)} pts | Verificando a cada {INTERVALO_VERIFICACAO}s...")
                                        while True:
                                                        print(f"Verificando... {time.strftime('%H:%M:%S')}")
                                                        verificar_ranking()
                                                        time.sleep(INTERVALO_VERIFICACAO)

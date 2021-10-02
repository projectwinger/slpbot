from discord_webhook import DiscordWebhook, DiscordEmbed
from utils.vars import *

WEBHOOK_URL="https://discord.com/api/webhooks/893548724066857080/hL2qkIQrqi3hd5MD2RSYPXRIB2oCKqkvM3ZC0soo_5tp0lJ-AE-Wswxb2sdAD5ZjjUbe"


def send_notification(value, transfer_type, tx_hash=None, desc=None, failed=False):
    color = '228B22' if not failed else 'FF0000'

    webhook = DiscordWebhook(url=WEBHOOK_URL)
    embed = DiscordEmbed(title='Transfer ' + ("Successful" if not failed else "Failed"),
                         color=color)

    # set footer
    embed.set_footer(text='LolWhut?!!')
    if failed:
        embed.add_embed_field(name='Error', value=desc, inline=False)

    if tx_hash:
        embed.add_embed_field(name='View on explorer', url='https://explorer.roninchain.com/tx/' + tx_hash,
                              value='https://explorer.roninchain.com/tx/{}'.format(tx_hash), inline=False)

    embed.set_timestamp()

    embed.add_embed_field(name='Type', value=transfer_type, inline=True)
    embed.add_embed_field(name='Value', value=value, inline=True)
    embed.add_embed_field(name='From', value=FROM_ADDR.replace("0x", "ronin:"), inline=False)
    embed.add_embed_field(name='To', value=TO_ADDR.replace("0x", "ronin:"), inline=False)

    webhook.add_embed(embed)

    response = webhook.execute()

import discord
import json
import logging
import requests
from config import *

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()


@client.event
async def on_ready():
    print('{} Logged In!'.format(client.user.name))


@client.event
async def on_message(message):
    if message.content.startswith('!stockx '):
        headers = {
            'User-Agent': user_agent
        }

        params = {
            'x-algolia-agent': 'Algolia for vanilla JavaScript 3.22.1',
            'x-algolia-api-key': '6bfb5abee4dcd8cea8f0ca1ca085c2b3',
            'x-algolia-application-id': 'XW7SBCT9V6',
        }

        data = {
            "params": "query={}&hitsPerPage=20&facets=*".format(message.content.split('!stockx ')[1])
        }

        response = requests.post(url=api_url, headers=headers, params=params, json=data)
        output = json.loads(response.text)

        deadstock_sold = output['hits'][0]['deadstock_sold']
        highest_ask = output['facets_stats']['lowest_ask']['max']
        highest_bid = output['hits'][0]['highest_bid']
        image = output['hits'][0]['media']['imageUrl']
        last_sale = output['hits'][0]['last_sale']
        lowest_ask = output['hits'][0]['lowest_ask']
        name = output['hits'][0]['name']
        # retail = output['hits'][0]['traits'][2]['value']
        sales_last_72 = output['hits'][0]['sales_last_72']
        # style = output['hits'][0]['style_id']
        url = 'https://stockx.com/' + output['hits'][0]['url']

        embed = discord.Embed(color=4500277)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Product Name", value="[{}]({})".format(name, url), inline=False)
        # embed.add_field(name="Product Style ID", value="{}".format(style), inline=False)
        # embed.add_field(name="Retail", value="${}".format(retail), inline=False)
        embed.add_field(name="Last Sale", value="${}".format(last_sale), inline=True)
        embed.add_field(name="Highest Bid", value="${}".format(highest_bid), inline=True)
        embed.add_field(name="Lowest Ask", value="${}".format(lowest_ask), inline=True)
        embed.add_field(name="Highest Ask", value="${}".format(highest_ask), inline=True)
        embed.add_field(name="Units Sold in Last 72 Hrs", value="{}".format(sales_last_72), inline=True)
        embed.add_field(name="Total Units Sold", value="{}".format(deadstock_sold), inline=True)

        await client.send_message(message.channel, embed=embed)


client.run(token)

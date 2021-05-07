import discord
from discord.ext import commands
import requests
import random
import json

client = commands.Bot(command_prefix = '!')


@client.event
async def on_ready():
    print('Bot is ready.')

@client.command(name='guide')
async def displayembed(ctx):
    embed=discord.Embed(title="Foots Stock Checker", description="Guide to Check Stock for Footlocker & EU", color=0xff0a0a)
    embed.set_author(name="{name/whatever} - Stock Checker", url="{twitter/whatever}", icon_url="https://cdn.discordapp.com/icons/781719579859746836/a5bdb7cd356631a16bddd4f96a151b70.webp?size=128")
    embed.add_field(name="How To Check Stock", value="Get the sku for your product and use the command !stock [url]", inline=False)
    embed.set_footer(text="Made by {name/whatever}")
    await ctx.send(embed=embed)


@client.command(name='stock')
async def local(ctx, url):
    sizes_to_checkEU = ['40','40.5', '41' , '42', '42.5', '43', '44', '44.5', '45', '45.5']
    sizes_to_checkUS = ['3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0', '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0', '16.5', '17.0', '17.5', '18.0']
    new_regions = ['BE','GR','PT','ES','LU','CZ','HU','DK','DE','IT','AT','SE','IE','PL']
    
    #proxies = {
    #    "http": ""
    #}

    s = requests.session()
    #s.proxies.update(proxies)

    #proxytest = s.get("http://httpbin.org/ip")#, proxies=proxies, verify=False)
    #print(proxytest.content)

    
    print(url)

    sku = url.split("/")[-1].split(".html")[0]
    region = url.split('footlocker.')[-1].split("/")[0]
    print(region)
    print(region in new_regions)
    stockendpoint = f"https://www.footlocker.{region}/api/products/pdp/{sku}"

    stock = s.get(stockendpoint)#, proxies=proxies, verify=False)
    print(stock.status_code)
    if stock.status_code == 429 or stock.status_code == 403:
        embed=discord.Embed(title="Foots Stock Checker", description="Guide to Check Stock for Footlocker & EU", color=0xff0a0a)
        embed.set_author(name="name/whatever - Stock Checker", url="twitter/whatever", icon_url="https://cdn.discordapp.com/icons/781719579859746836/a5bdb7cd356631a16bddd4f96a151b70.webp?size=128")
        embed.add_field(name="Error", value=f"Cannot connect to site **{stock.status_code}**", inline=False)
        embed.set_footer(text="Made by name/whatever")
        await ctx.send(embed=embed)
    else:
        prodinfo1 = json.loads(stock.text)
        print(prodinfo1)
        for line in prodinfo1['variantAttributes']:
            if sku == line['sku']:
                productcode = line['code']
                break
    
        global availsizes, availids
        availsizes = []
        availids = []
        stock_str = ''
        size_in_stock = {}
        for line in prodinfo1['sellableUnits']:
            if productcode == str(line['attributes'][1]['id']):
                if line['stockLevelStatus'] == 'inStock':
                    #print(f'Test: {line}')
                    size = line['attributes'][0]['value']
                    print(type(size))
                    producttitle = prodinfo1['name']
                    availsizes = (str(line['attributes'][0]['value']))
                    availids = (str(line['attributes'][0]['id']))
                    if region.upper() in new_regions:
                        if size in sizes_to_checkEU:
                            stock_str = stock_str + f":green_circle: {size}\n" 
                        else:
                            stock_str = stock_str + f":red_circle: {size}\n"  
                    elif region == 'com':
                        if size in sizes_to_checkUS:
                            stock_str = stock_str + f":green_circle: {size}\n"  
                        else:
                            stock_str = stock_str + f":red_circle: {size}\n" 
        print(size_in_stock)
        for line in prodinfo1['sellableUnits']:
            price = str([line['price']['formattedOriginalPrice']])

        print(producttitle)
        print(price)



        print(stock_str)
        ###### END ######
        embed=discord.Embed(title=producttitle, url=url, description="Guide to Check Stock for Footlocker & EU", color=0xff0a0a)
        embed.set_author(name="name/whatever - Stock Checker", url="twitter/whatever", icon_url="https://cdn.discordapp.com/icons/781719579859746836/a5bdb7cd356631a16bddd4f96a151b70.webp?size=128")
        embed.add_field(name="Stock Level", value=stock_str, inline=False)
        embed.set_footer(text="Made by name/whatever")
        await ctx.send(embed=embed)

client.run("")

#314213592604

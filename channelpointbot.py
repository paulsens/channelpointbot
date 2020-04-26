from twitchio.ext import commands
import json

#oauth token with channel:read:redemptions scope, DO NOT pad with 'oauth:' like you do with the irc_token below
oauth = '<your redemption scoped oauth token>'

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='oauth:<your irc oauth token>', client_id='<your client id>', nick='<your bot name>', prefix='!',
                         initial_channels=['<your channel name>'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        print("Subscribing to channel points...\n\n")

        #to obtain your channel id, use Postman to send a GET to https://api.twitch.tv/helix/users?login=<your channel name>
            #with a header whose key is "client-id" and the corresponding value is your app's client id on the dev console
        await self.pubsub_subscribe(oauth, "channel-points-channel-v1.<your_channel_id>")

    async def event_message(self, message):
        print(message.content)
        if(message.content[0]=="!"):
            await self.handle_commands(message)

    async def event_raw_pubsub(self,  data):
        #data is given to us as a dictionary
        if data['type'] == 'MESSAGE':
            payload = data['data']['message']
            #but this payload is a json string
            payload = json.loads(payload)
            #now the payload is a dictionary, but it's nested as hell, so getting to the name of the reward is clunky

            title = payload['data']['redemption']['reward']['title']
            print("title is "+str(title))
            #title will exactly match the name of the reward that was redeemed
            #Now you can easily write if-statements to handle your different rewards. Enjoy!



    # Commands use a decorator...
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()
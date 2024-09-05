import discord
from redbot.core import commands
import datetime
import asyncio

class WeeklyMessage(commands.Cog):
    """A cog that sends a weekly message on a certain weekday at a specified time"""

    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1234567890  # Replace with your channel ID
        self.target_weekday = 1  # Default is Tuesday (0=Monday, 6=Sunday)
        self.target_hour = 12  # Default is 12:00 (24-hour format)
        self.target_minute = 0  # Default is 00 minutes
        self.message = "This is your weekly message!"  # Default message
        self.message_task = self.bot.loop.create_task(self.weekly_message())

    def cog_unload(self):
        self.message_task.cancel()

    async def weekly_message(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            now = datetime.datetime.now()
            current_weekday = now.weekday()
            current_hour = now.hour
            current_minute = now.minute

            # If it's the target day and time
            if current_weekday == self.target_weekday and current_hour == self.target_hour and current_minute == self.target_minute:
                channel = self.bot.get_channel(self.channel_id)
                if channel:
                    await channel.send(self.message)

                # Wait until the next week
                await asyncio.sleep(7 * 24 * 60 * 60)
            else:
                # Wait 1 minute before checking again
                await asyncio.sleep(60)

    @commands.command()
    async def set_weekly_message(self, ctx, channel_id: int, weekday: int, hour: int, minute: int, *, new_message: str):
        """Set the weekly message, day, and time (24-hour format)"""
        if weekday < 0 or weekday > 6:
            await ctx.send("Invalid weekday! Use 0 for Monday and 6 for Sunday.")
            return
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            await ctx.send("Invalid time! Use 24-hour format for hours (0-23) and minutes (0-59).")
            return

        self.channel_id = channel_id
        self.target_weekday = weekday
        self.target_hour = hour
        self.target_minute = minute
        self.message = new_message

        await ctx.send(f"Weekly message set! It will send on weekday {weekday} at {hour:02d}:{minute:02d} in <#{channel_id}>.")

    @commands.command()
    async def current_time(self, ctx):
        """Print the current time and weekday"""
        now = datetime.datetime.now()
        weekday = now.weekday()
        hour = now.hour
        minute = now.minute

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        current_day = days[weekday]

        await ctx.send(f"Current time is {hour:02d}:{minute:02d} and today is {current_day} (weekday {weekday}).")

def setup(bot):
    bot.add_cog(WeeklyMessage(bot))

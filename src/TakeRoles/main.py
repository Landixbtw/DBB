        
class take_roles():
    async def date_handler():
        cur.execute("SELECT REDEEMED_AT FROM CodeRedeemLogs")
        date = cur.fetchone()[0]
        print(date)
            
        if role_Onlyfans in user.roles and date == now: 
            # wenn user rolle hat und date == now entspricht rolle weg.            
        user.remove_roles(role_Onlyfans)
        DM = await bot.fetch_user(interaction.user.id)
        print(f"DAS IST DIE USER ID" ,{DM})
        await DM.send("1 Month is over, and your Bestfans or Onlyfans role has been taken away, if you want the role again and can prove that you have a **valid subscription** of either, open a Ticket on the 'I have a question' Ticket and send a screenshot of privatebunnys respective profile so that we can see you are subscribed. ")        
        
        await date_handler()
        
        else:
        await interaction.response.send_message(
            f"*{interaction.user.name}* du hast den falschen Code eingegeben")
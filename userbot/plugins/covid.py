# corona virus stats for catuserbot
from covid import Covid

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP, covidindia


@bot.on(admin_cmd(pattern="covid(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="covid(?: |$)(.*)", allow_sudo=True))
async def corona(event):
    if event.pattern_match.group(1):
        country = (event.pattern_match.group(1)).title()
    else:
        country = "World"
    catevent = await edit_or_reply(event, "`collecting data...........`")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n🥺 الحالات اليوم   :   <code>{country_data['new_cases']}</code>"
        data += f"\n😟 الوفيات اليوم   :   <code>{country_data['new_deaths']}</code>"
        data += f"\n\n⚠️ الحالات الإجمالية  :   <code>{hmm1}</code>"
        data += f"\n⚰️ إجمالي الوفيات     :   <code>{hmm2}</code>"
        data += f"\n😔 الحالات النشطة     :   <code>{country_data['active']}</code>"
        data += f"\n🤕 الحالات الحرجة     :   <code>{country_data['critical']}</code>"
        data += f"\n😊     المتعافين          :   <code>{country_data['recovered']}</code>"
#        data += f"\n💉 إجمالي الاختبارات   :   <code>{country_data['total_tests']}</code>"
        await catevent.edit(
            "<b>🦠 إحصائيات كورونا 👈🏼 {} :\n{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            cat1 = int(data["new_positive"]) - int(data["positive"])
            cat2 = int(data["new_death"]) - int(data["death"])
            cat3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n\n⚠️Confirmed   : <code>{data['new_positive']}</code>\
                \n😔Active           : <code>{data['new_active']}</code>\
                \n⚰️Deaths         : <code>{data['new_death']}</code>\
                \n😊Recovered   : <code>{data['new_cured']}</code>\
                \n🥺New Cases   : <code>{cat1}</code>\
                \n😟New Deaths : <code>{cat2}</code>\
                \n😃New cured  : <code>{cat3}</code> </b>"
            await catevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                catevent,
                "`Corona Virus Info of {} is not avaiable or unable to fetch`".format(
                    country
                ),
                5,
            )


CMD_HELP.update(
    {
        "covid": "**Plugin : **`covid`\
        \n\n**Syntax : **`.covid <country name>`\
        \n**Function :** __Get an information about covid-19 data in the given country.__\
        \n\n**Syntax : **`.covid <state name>`\
        \n**Function :** __Get an information about covid-19 data in the given state of India only.__\
        "
    }
)

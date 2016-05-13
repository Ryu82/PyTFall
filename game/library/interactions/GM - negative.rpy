label interactions_escalation:
    $ gm.set_img("battle", "confident", "angry")
    call interactions_fight_begins
    hide screen girl_interactions
    if "park" in gm.label_cache:
        $ n = randint(1,4)
        $ back = "content/gfx/bg/be/b_park_" + str(n) + ".jpg"
    elif "beach" in gm.label_cache:
        $ n = randint(1,3)
        $ back = "content/gfx/bg/be/b_beach_" + str(n) + ".jpg"
    elif "forest" in gm.label_cache or "mage" in gm.label_cache:
        $ n = randint(1,8)
        $ back = "content/gfx/bg/be/b_forest_" + str(n) + ".jpg"
    elif "village" in gm.label_cache:
        $ back = "content/gfx/bg/be/b_village_1.jpg"
    elif "grave" in gm.label_cache:
        $ back = "content/gfx/bg/be/b_grave_1.jpg"
    elif "academy" in gm.label_cache:
        $ back = "content/gfx/bg/be/b_academy_1.jpg"
    elif "arena" in gm.label_cache:
        $ back = "content/gfx/bg/be/battle_arena_1.jpg"
    elif "tavern" in gm.label_cache:
        $ back = "content/gfx/bg/be/b_tavern_1.jpg"
    else:
        $ n = randint(1,6)
        $ back = "content/gfx/bg/be/b_city_" + str(n) + ".jpg"
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        your_team = Team(name="Your Team", max_size=3)
        enemy_team.add(char)
        for member in enemy_team:
            member.controller = BE_AI(member)

        battle = BE_Core(Image(back), start_sfx=get_random_image_dissolve(1.5), music="random", end_sfx=dissolve)
        for member in hero.team:
            if member <> hero:
                if member.status <> "slave":
                    if (member.disposition >= 700) or (check_lovers(member, hero)) or (("Yandere" in member.traits) and (member.disposition >= 200)): # girls usually don't support MC when he harasses other girls, unless they are close enough to him or are yandere with at least some disposition
                        your_team.add(member)
                else:
                    if "Yandere" in member.traits and member.disposition >= 100: # and yandere slaves can serve as cannon fodder
                         your_team.add(member)
            else:
                your_team.add(member)
        for member in your_team:
            if member <> hero and member.status == "slave":
                member.controller = Slave_BE_AI(member)
        battle.teams.append(your_team)
        battle.teams.append(enemy_team)
        battle.start_battle()
        your_team.reset_controller()
        enemy_team.reset_controller()
        for member in your_team:
            if member in battle.corpses:
                member.health = 1
            else:
                member.exp += char.level*10
        for member in enemy_team:
            if member in battle.corpses:
                member.health = 1
            else:
                member.exp += hero.level*10
    if battle.winner != your_team:
        show expression gm.bg_cache
        call interactions_fight_won
        
    else:
        show expression gm.bg_cache
        python:
            for member in hero.team:
                if (member.status <> "slave") and not("Yandere" in member.traits) and member<>hero:
                    member.disposition -= randint(5, 10) # and even if they help, they don't like it
        $ char.disposition -= randint(30, 60)
        call interactions_fight_lost
    jump girl_interactions_end

label interactions_fight_begins:
    $ char.override_portrait("portrait", "angry")
    if ct("Impersonal"):
        $ rc("I now regard you as my enemy, and I will put you down by force.", "Understood... Let us discuss this matter with our fists.", "I don't want this to be a big deal. So let's just do it as quickly as possible.", "I will erase you.")
    elif ct("Imouto"):
        $ rc("I have to hit you, or I won't be able calm myself!", "I'm toootally gonna make you cry!", "Ahaha, time to pound your face in!", "I-I'm going to make you accept your punishment!") 
    elif ct("Dandere"):
        $ rc("I'll make you regret to have angered me.", "You're ugly on the inside... Let's end this quickly.", "Seems like I have no choice but to restrain you physically.", "I'm selling a fist to the face. Please purchase one.")
    elif ct("Tsundere"):
        $ rc("You insolent prick... I'll beat you here and now!", "Fufhn! I challenge you!", "Today's the day you stop getting away with this!", "Looks like I have no choice but... to do this!"),
    elif ct("Kuudere"):
        $ rc("Feel my anger with every bone in your body!", "You've got guts, but it won't keep you in one piece!", "I'll accept your challenge... And I'll acknowledge that you have some courage.", "Hmph. It's too late for regrets... Nothing's going to stop me now!")
    elif ct("Kamidere"):
        $ rc("Aah, I'm pissed off now! Get ready!", "I'll teach you the meaning of pain!", "Come on... Hurry up and bring it.", "Kuh, don't come crying when you get hurt...!", "It seems like I need to teach you some manners.")
    elif ct("Bokukko"):
        $ rc("So, I'm seriously angry now!", "Ok, I'm gonna hit you now. Just once. Well, I guess I'll smack you two or three more times after that. We clear?", "Hey, can I hit you? It's okay, right? Hey, hey!", "Lemme borrow that mug of yours real quick. 'Cause I'm gonna turn it into my personal punching bag.", "I kinda wanna deck you one. Don't move, 'kay?")
    elif ct("Ane"):
        $ rc("Looks like you're never going to shape up unless I punish you...", "Just give me a moment please, it'll all end soon.", "I don't usually approve of this sort of thing, but I can't take it anymore!", "Please choose. Sit quietly and get hit, or struggle and get hit.")
    elif ct("Yandere"):
        $ rc("You... have a shadow of death hanging over you...", "I'll pay you back in pain!", "Very well. I'll make it so you won't even be able to stand!", "You're at the end of your rope I'll wager.")
    else:
        $ rc("Geez, now I'm pissed!", "Geez, I will never forgive you!", "I can't deal with this. I want to hit you so bad I can't stop myself!", "Since it's come down to this, I'll have to use force!", "I didn't want to have to fight... but it seems like there's no other choice.")
    $ char.restore_portrait()
    return
    
label interactions_fight_won:
    $ char.override_portrait("portrait", "confident")
    if ct("Impersonal"):
        $ rc("It would be better for you if you stayed obedient for a while.", "Now do you understand your own powerlessness?")
    elif ct("Imouto"):
        $ rc("Flawless victory! ♪", "Th-this is all your fault, you made me so mad!", "Are you okay? Are you still alive?", "Loooooooser!") 
    elif ct("Dandere"):
        $ rc("Don't make me dirty my hands next time.", "Huu... I suppose we can leave it at this.", "Please learn from this.", "Hmph, is that it.")
    elif ct("Tsundere"):
        $ rc("Haaa... Feels so good.", "Hah! Big mouth and little muscles!", "...Hmph! Did you really think you could win against me?", "Hmph, of course it was going to end this way."),
    elif ct("Kuudere"):
        $ rc("Hmph. You're out of your league.", "Well, how was that! Don't forget it!", "Phew, what a waste of time...", "And stay down.", "Tch, what a stupid waste of time.")
    elif ct("Kamidere"):
        $ rc("Hmph, not even worth talking about...", "Hmph, charging in without knowing your opponent's strength... You're nothing but a stupid, weak animal.", "This is what you deserve.")
    elif ct("Bokukko"):
        $ rc("What's this? You're a loser, after all.",  "Well? Now do you get it?", "Ahaha ♪ I'm so strong ♪", "Jeez, now I'm tired after all that.", "Huh, so that's all you got?")
    elif ct("Ane"):
        $ rc("Do you understand how I feel now?", "Phew, I wonder if you'll still stand up to me after that?", "Oh my, I think I may have overdone it a little.", "Have you come to your senses?")
    elif ct("Yandere"):
        $ rc("Lie on the floor... as you are...", "Hah, just a small fry.", "Good lord, look at this. You even got my clothes all dirty.")
    else:
        $ rc("Phew... I feel so much better now... ♪", "So? Do you give up?", "Now that you know the difference between you and I, would you like to try again?")
    $ char.restore_portrait()
    return
 
label interactions_fight_lost:
    $ char.override_portrait("portrait", "angry")
    if ct("Impersonal"):
        $ rc("Ugh... I underestimated you...", "I've failed...", "So I was defeated...")
    elif ct("Imouto"):
        $ rc("Oh, it hurts...", "Ugh, this wasn't supposed to happen...", "Ah...ahaha... I lost...", "I-I haven't...lost...yet...uu...")
    elif ct("Dandere"):
        $ rc("Kuh...", "This... this isn't the way it's supposed to be...", "How mean...", "Ugh... No way...")
    elif ct("Tsundere"):
        $ rc("Auu... This is terrible...", "Oww... Why'd you do that..?", "Kyuu... you..."),
    elif ct("Kuudere"):
        $ rc("Uuu... You'll regret...", "Kuh... I lost...", "Buha! ...I-impossible...I have been...", "Kuh... That's all I can...", "Tch... Damn it...!")
    elif ct("Kamidere"):
        $ rc("Ugh... Frustrating...", "Kuh, I'm so pissed...", "Guh... How did I...", "...Really, just... not my day...")
    elif ct("Bokukko"):
        $ rc("Why... did this happen...", "Damn... this loser beat me...?", "Uuh... I'm so uncool...", "Owie... This sucks...")
    elif ct("Ane"):
        $ rc("Kuu... Why, like this...", "Ugh... How could this happened...", "Kuh, I misread you...", "Tch... to think that I'd...")
    elif ct("Yandere"):
        $ rc("You little... I won't forget this...", "Da... mn...", "Shit... This is... nothing...", "...")
    else:
        $ rc("Kuh, damn, you got me...", "Ugh, what the hell... geez...", "Kuh... You're... pretty good...")
    $ char.restore_portrait()
    return
    
label interactions_character_apology:
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $ rc("Sorry. My bad.", "I am very sorry.")
    elif ct("Shy") and dice(50):
        $ rc("Um... I-I... I-I'm s-sor...ry...", "I-I'm so sorry... How could I...")
    elif ct("Imouto"):
        $ rc("I'm sowweeeeee, forgive meeeeee...", "I'm sorry, I'm sorry, I'm sorry!") 
    elif ct("Dandere"):
        $ rc("...My bad. Forgive me.", "...Sorry about that.")
    elif ct("Tsundere"):
        $ rc("I-I'm sorry... I said I was sorry, alright?", "「I'm honestly really sorry!"),
    elif ct("Kuudere"):
        $ rc("I was wrong... It's as you see, forgive me...", "I'm sorry... Forgive me.", "Sorry, I guess that was a bit thoughtless...")
    elif ct("Kamidere"):
        $ rc("It is my fault, isn't it... Forgive me.", "I suppose I could offer you an apology. I'm sorry.")
    elif ct("Bokukko"):
        $ rc("I'm sorry. I did something terrible...", "Um, so, ...'m sorry.", "Well, y'know... Sorry.")
    elif ct("Ane"):
        $ rc("Please find it in your heart to forgive me.", "I really need to apologize.")
    elif ct("Yandere"):
        $ rc("I'm very sorry, I just...", "I'm sorry, if you could somehow forgive me...", "I'm responsible for all of this! I am so, so sorry!")
    else:
        $ rc("Um... I'm sorry...", "Sorry, please forgive me...")
    $ char.restore_portrait()
    return

label interactions_got_insulted:
    $ char.override_portrait("portrait", "angry")
    if ct("Impersonal"):
        $ rc("...I see that you have a hostility problem.", "I can't believe you can look me in the eyes and say those things.", "...Are you talking about me? I see, so that's what you think of me.")
    elif ct("Shy") and dice(50):
        $ rc("Th-That's terrible! It's way too much!", "Th-that's... so cruel of you to say...", "N-no way... you're horrible...", "T-That's not true!")
    elif ct("Imouto"):
        $ rc("Hah! Y-You think that kind of abuse will have any effect on m-me?", "I'm so pissed off!", "I-I... I'm not like that!", "LA LA I CAN'T HEAR YOU!") 
    elif ct("Dandere"):
        $ rc("...Are you trying to make me angry?", "...Are you teasing me?", "Do you want me to hate you that much?", "All bark and no bite. As they say.", "Was that meant to be an insult just now? How rude.")
    elif ct("Tsundere"):
        $ rc("You... you insolent swine!", "I-I will not forgive you!", "What was that?! Try saying that one more time!", "Hmph, I don't want to hear that from you!", "E-even if you say that, it doesn't mean anything to me, you know!"),
    elif ct("Kuudere"):
        $ rc("...What did you say? Who do you think you are?", "Oooh, it's ok for me to accept this as a challenge, right...?", "Shut your mouth. Or do you want me to shut it for you?", "Oh, do you want to get hurt that badly?")
    elif ct("Kamidere"):
        $ rc("Huhn? It seem you want to make me your enemy.", "Oh? Is your mouth all you know how to use?", "Bring your face over here so I can slap it!", "You're really trash, aren't you...")
    elif ct("Bokukko"):
        $ rc("What's that? Are you picking a fight with me?", "...Hey, you. You're ready for a pounding, yeah?", "Hey fucker, you trying to start a fight?!", "Oh, so talkin's all you're good at, huh...")
    elif ct("Ane"):
        $ rc("You shouldn't say things like that.", "Hmm, I didn't know you were the type to say things like that...", "My, you have some nerve.", "Good grief... Your parents did a terrible job raising you.")
    elif ct("Yandere"):
        $ rc("Hey, it would be better if you didn't talk like that.", "...You should... be careful, when walking at night.", "Please die and come back as a better person, for everyone's sake.")
    else:
        $ rc("Th-that's a terrible thing to say!", "Wh-why would you say that, that's so cruel...", "All talk and nothing to back it up. What are you even trying to do?", "What's your problem? Saying that out of nowhere.")
    $ char.restore_portrait()
    return
    
label interactions_demand_apology:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("Apologize. Then we'll talk.", "I won't forgive you unless you apologize.")
    elif ct("Shy") and dice(50):
        $ rc("Please apologize...", "Isn't there... something you want to apologize about first?")
    elif ct("Imouto"):
        $ rc("Umm, if you grovel in the dirt for me, I'll forgive you...", "I might consider forgiving you if you grovel pitifully.") 
    elif ct("Dandere"):
        $ rc("I'll forgive you if you apologize.", "Is it impossible for you to give an apology?", "...You should know that I haven't forgiven you just yet.")
    elif ct("Tsundere"):
        $ rc("It'd be nice if you apologized, you know...!", "...Apologize. APOLOGIZE!"),
    elif ct("Kuudere"):
        $ rc("What, not even a single word of apology?", "Until you apologize I'm not talking to you.")
    elif ct("Kamidere"):
        $ rc("Huh? Apologize first.", "Um... Where is my «I'm sorry»?")
    elif ct("Bokukko"):
        $ rc("Hm, finally feel like apologizin'?", "Hey, don't you think there's something you oughta be apologizing for?", "C'mon now, hurry up and apologize. It's for your own good, y'know?")
    elif ct("Ane"):
        $ rc("Oh dear, do you not know how to apologize?", "I will not forgive you until you reflect on what you've done.")
    elif ct("Yandere"):
        $ rc("Apologize. Did you not hear me? It means tell me you're sorry.", "...I demand an apology.")
    else:
        $ rc("Start apologizing, please! I'll let you know when it's enough.", "Hey, isn't there something you need to apologize for first...?")
    $ char.restore_portrait()
    return
    
label interactions_apology_accepted:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("I understand. However, do not think that this will happen another time.", "...Never again, okay?")
    elif ct("Imouto"):
        $ rc("...If you say you'll never do it again, then... Alright...", "Fine, fine, I'll forgive you...", "Hrmm... just this once, okay?") 
    elif ct("Dandere"):
        $ rc("...I don't really mind.", "I suppose I could...", "...Please do not do it again.")
    elif ct("Tsundere"):
        $ rc("Well I guess I could if you're gonna go that far.", "Hmph... I haven't COMPLETELY forgiven you, okay?"),
    elif ct("Kuudere"):
        $ rc("Hmph... There won't be a next time.", "Hm, I'm too soft... Just this once, alright?", "...I'll let it slide.")
    elif ct("Kamidere"):
        $ rc("...Haah... I'm not mad at you anymore.", "Hmph. You should be grateful I'm so lenient.", "...Yeaaah, yeaaah. I get it. I'll forgive you, just get off my case already.")
    elif ct("Bokukko"):
        $ rc("Hmph... And now you know never to do that again.", "Fine, if you insist...", "It's fine, I don't really care anymore.")
    elif ct("Ane"):
        $ rc("Well, I was being childish too... Sorry.", "Yes... Let's reconcile.", "Hmhm, it seems you've reflected on your actions. Well done.")
    elif ct("Yandere"):
        $ rc("If you do it again, I'll be even angrier, okay?", "Well, I've got no reason not to forgive you.")
    else:
        $ rc("It's okay, I'll forgive you this time.", "...Just this once. Got it?", "...Alright, I'll put my trust in you one more time.")
    $ char.restore_portrait()
    return
    
label interactions_apology_denied:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("Forgiving you is not something I am capable of.", "I won't forgive you...")
    elif ct("Imouto"):
        $ rc("I-I'll never forgive you...!", "I'll never forgive you!", "Aaahhh... can't hear a thing...") 
    elif ct("Dandere"):
        $ rc("I'll never forgive you. Ever.", "I will never forgive you.", "I will definitely not forgive you.")
    elif ct("Tsundere"):
        $ rc("Unforgivable. Absolutely not!", "I am DEFINITELY not letting you off the hook for this one!"),
    elif ct("Kuudere"):
        $ rc("Is this your shitty attempt at 'sincerity'?", "I will not forgive this, definitely not.", "I will not forgive you.")
    elif ct("Kamidere"):
        $ rc("You think I'll forgive you with an apology like that?", "I won't forgive this easily.", "Hmph. You think I'd let you off the hook that easily?")
    elif ct("Bokukko"):
        $ rc("Huh? ...You thought I'd forgive you?", "I'm neeeeever gonna forgive you!", "Wha? As if I'd forgive ya.")
    elif ct("Ane"):
        $ rc("I'll never forgive you.", "I won't forgive you, no matter what.", "I don't think you've properly thought about what you've done yet.")
    elif ct("Yandere"):
        $ rc("I'm not forgiving you, no matter what!", "Unforgivable...")
    else:
        $ rc("I'm not going to forgive you, ever!", "I'll never forgive you, you got that?", "Sorry...I can't trust you just yet.")
    $ char.restore_portrait()
    return
    
label interactions_broken_promise:
    $ char.override_portrait("portrait", "sad")
    if ct("Impersonal"):
        $ rc("I suppose the promise was but lip service... after all.", "You don't keep promises, do you...")
    elif ct("Shy") and dice(50):
        $ rc("It's okay, I'm sure you have your priorities too, right...? But still...", "It's fine... I didn't think you'd show up anyway.")
    elif ct("Imouto"):
        $ rc("I was so lonely, all by myself...", "...I even waited for you.") 
    elif ct("Dandere"):
        $ rc("I was waiting forever...", "You promised...", "It seems I have been thoroughly fooled.")
    elif ct("Tsundere"):
        $ rc("Why didn't you come...? You idiot...", "You idiot! Liar! I can't believe this!"),
    elif ct("Kuudere"):
        $ rc("Tch. I guess a promise with me just isn't worth remembering, huh...", "「Is it too much for you to keep even a single promise?")
    elif ct("Kamidere"):
        $ rc("You're horrible... I was waiting the whole time...", "Jeez, why didn't you show up? Keep your promises!")
    elif ct("Bokukko"):
        $ rc("You're the kind of trash that can't even keep a little promise, aren't you.", "What d'you think promises are for? Hmm?")
    elif ct("Ane"):
        $ rc("No, no, it's okay. Everyone has times when they can't make it...", "If you couldn't make it, I wish you'd just said so... Otherwise, it's just too cruel.")
    elif ct("Yandere"):
        $ rc("I waited so long for you... ", "...You never came. I waited so long and you never came!")
    else:
        $ rc("That's no good. You have to keep your promises...", "Jeez, how come you never came!")
    $ char.restore_portrait()
    return
    
label interactions_got_insulted_hdisp:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("Huh? You kidding?", "Excuse me?")
    elif ct("Shy") and dice(50):
        $ rc("Ah... Eh... Aah! This is a joke... Right?", "Umm... Ah! Th-that was funny, wasn't it?")
    elif ct("Imouto"):
        $ rc("Ufufu, I'm not falling for that joke!", "Haha, I'm not going to fall for that kind of joke!") 
    elif ct("Dandere"):
        $ rc("Not funny.", "I will overlook it this time, but that's harassment, you know?")
    elif ct("Tsundere"):
        $ rc("Wha!? ...That...wasn't very funny, you know?", "W-What are you saying? Jeez..."),
    elif ct("Kuudere"):
        $ rc("That was quite the harsh joke.", "Hah, ain't that a funny joke.")
    elif ct("Kamidere"):
        $ rc("Geez, stop joking around.", "What a supremely boring joke. You've got awful taste.")
    elif ct("Bokukko"):
        $ rc("Jeez, your jokes are so mean.", "Mm, sounds kinda boring, y'know?")
    elif ct("Ane"):
        $ rc("Oh, you, stop it with your childish pranks.", "Mumu... Looking forward to seeing my reaction, are you? Well too bad, I won't give you the satisfaction!")
    elif ct("Yandere"):
        $ rc("Go easy on the jokes, hey?", "Hey now, that's harsh for a joke.")
    else:
        $ rc("Come on, knock it off with the jokes!", "Jeez, stop playing around.")
    $ char.restore_portrait()
    return
    
label interactions_lover_end:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("Don't follow me around anymore. I... want to break up.", "I'm sorry, I can't be with you anymore.", "I feel like I have to bring this to an end, for the sake of the future.")
    elif ct("Shy") and dice(50):
        $ rc("I'm sorry... I can't bring myself to like you anymore...", "Um... Let's break up... I can't keep this up...", "I'm sorry ... I can't love you from my heart... We should break up.")
    elif ct("Imouto"):
        $ rc("Um, you know... Maybe we should go our separate ways...?", "If you don't love someone, you should break up with them, right? So anyway, could we break up?", "Hey, I kinda wanna stop dating you...") 
    elif ct("Dandere"):
        $ rc("My patience with you has come to an end. Our association ends here.", "Let's break up already... It'll definitely be for the best.", "We should break up. I'm no longer in love with you.")
    elif ct("Tsundere"):
        $ rc("You were a disappointment. We're over. Now.", "Hey... I've fallen out of love with you. Let's break up.", "It seems that I'm no longer needed. Isn't that right?"),
    elif ct("Kuudere"):
        $ rc("Haah... It was a mistake to date someone like you...", "I can't keep going out with you anymore. Let's break up.", "Sorry... I can't think of you as my number one anymore.", "I'm sorry, I just can't stand to be with you anymore.")
    elif ct("Kamidere"):
        $ rc("Being in a relationship is more trouble than it's worth. I knew this wouldn't work out.", "When you become as popular as me, you'll never be short on people to date. So I'm done with you.", "I've grown tired of you, so I don't need you anymore.")
    elif ct("Bokukko"):
        $ rc("I have no interest in you anymore. Let's break up.", "Don't you want to break up with me? You do, don't you?", "Ah, sorry, I don't really like you anymore. We're over.")
    elif ct("Ane"):
        $ rc( "I've had enough... I no longer want to be by your side.", "I'm not strong enough to date someone I don't care for...", "Let's break up. It's for the best, for both of us.", "I think it'll be better if you look for someone that's more suited for you.")
    elif ct("Yandere"):
        $ rc("I'm sorry for being so inconsiderate, but... forget about me...", "I... don't think of you as the one anymore...", "I don't have it in me to love you any longer. Let's end this.")
    else:
        $ rc("Jeez, I don't want to date someone I can't stand.", "I can't think of you as my number one anymore. We are done...", "I don't think this is working out. Let's break up.", "I've been thinking a lot lately... I think things would be better off if we broke up.")
    $ char.restore_portrait()
    return
    
label interactions_lover_end_mc:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("Well... There's nothing that can be done about it.", "I...see. That's a shame.", "Hm... Then I suppose this is the end, I understand.", "Starting now, you and I are strangers.")
    elif ct("Shy") and dice(50):
        $ rc("You're... right... Yes, thank you for everything until now...", "I'm sorry... I... I guess I was a failure of a woman...", "I'm sorry... I'm so worthless...", "I-if you hate me, then you should've just said it straight...", "...I see. Thanks for everything...", "...I understand. But, please, don't forget about me...")
    elif ct("Imouto"):
        $ rc("I-I won't be lonely... I'll be fine, so...", "I'm sorry... I was too immature... I'm sorry...", "I see... Still, it was fun while it lasted...") 
    elif ct("Dandere"):
        $ rc("Is that so... I apologize for having been such an imperfect woman...", "Certainly, let us both see the end of this limitless futility.", "Is that so... I guess it couldn't be helped... That makes us strangers now.")
    elif ct("Tsundere"):
        $ rc("Hmph! Fine, then! The one who will crawl back is you!", "Just get out of here already. And don't let me see you again.", "You really don't care about me at all, huh?"),
    elif ct("Kuudere"):
        $ rc("...Fine. Go away. ...I said get the hell away from me!", "I understand... It's going to be a little lonely...", "Is that so. Very well, now disappear before I beat you to a pulp.", "If that's really how you want things... Then I guess I don't have much choice but to accept.")
    elif ct("Kamidere"):
        $ rc("If you didn't love me, you could've said so earlier... Goodbye...", "Hmph, you'll regret breaking up with me, I promise you...", "I see... It had to happen sometime, huh... Yeah... you're right...")
    elif ct("Bokukko"):
        $ rc("Oh... Yeah, I suppose this is as good a time as any...", "I see... that's too bad... Really...", "Man, well I guess I can't do anything about it...")
    elif ct("Ane"):
        $ rc("If being with me bothers you, then leave. You've got others anyway, right?", "Is that so... I guess the time has come... I understand.", "I don't... want to be with you any more.")
    elif ct("Yandere"):
        $ rc("...Yeah. Being with someone like me is impossible, I guess. It's fine. Bye bye...", "If that is what you desire... Then so be it...", "I'm grateful for the time we spent together...")
    else:
        $ rc("What a shame, I'd thought it would have worked out better... It really is a shame...", "...If you say it has to be like that, then it can't helped...", "I understand... Thank you for having loved me...")
    $ char.restore_portrait()
    return
    
label interactions_lover_end_refuse:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("I'll never let go of you. For the rest of my life.", "...Impossible. That could never, ever happen.", "I have no intention of letting you go.", "Denied. That's not for you to decide.")
    elif ct("Shy") and dice(50):
        $ rc("N-Never! I'll do anything... I'll love you even more...!", "I'm afraid we cannot be separated. We are bound by fate after all...", "Huh? ...Y-you must be really tired, let's take it easy for now, okay?", "...Sorry, there's no way I could give you up.", "I'll do better, I promise... so... I'm sorry... I'm so pathetic...", "I... I don't want that! Please, don't leave me...")
    elif ct("Imouto"):
        $ rc("Eh? Why? I still love you lots, you know?", "Oh you, always with the jokes ♪ You're just testing my love, right? You big meanie! ♪", "Abso. Lutely. Not! I'm not letting you go! We'll always be together!") 
    elif ct("Dandere"):
        $ rc("I am terribly sorry. I did not show you enough affection, did I?", "Don't even try. I never want to leave you.", "That's impossible. We're gonna be together forever.")
    elif ct("Tsundere"):
        $ rc("You're my life partner, this' already been decided. There's nothing that can keep us apart at this point.", "What are you saying...? Our bond is eternal, don't you know?", "Oh, are you being tsundere? You don't need to be that way, dummy ♪"),
    elif ct("Kuudere"):
        $ rc("What do you mean? The two of us are fated to never be apart.", "You own me. And I own you.", "Rest assured. You don't need to test me like that, I won't let you go. Hmhm ♪")
    elif ct("Kamidere"):
        $ rc("Why is that? There's no reason for us to break up, is there?", "Oh please, you're just trying grab more of my attention, aren't you? Geez ♪", "Oh..? do you really think I'd let you slip through my fingers?")
    elif ct("Bokukko"):
        $ rc("Hehe... You're testing me, aren't you? ...I get it, I get it already... hehehe", "I gotcha, I just have to try harder, right? Ehehe...♪", "Eh? You and I share the same fate. Breaking up is unthinkable!")
    elif ct("Ane"):
        $ rc("W-why are you saying that...? Even though I love you so much... Why...!?", "If there's something about me that's inadequate, I swear I'll fix it...! So, please... Let me stay by your side...!")
    elif ct("Yandere"):
        $ rc("...Who's the one trying to lead you astray? Who is it! Hey, tell me. TELL ME!", "What are you saying? Until they put us in the same grave, you're mine!", "...Who stole you from me? Who's the one trying to stand between us?")
    else:
        $ rc("Come on, knock it off with the jokes!", "Jeez, stop playing around.", "Huh? No way, you're mine, after all.")
    $ char.restore_portrait()
    return
    
label interactions_relover:
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $ rc("I want to mend our broken relationship. Please.", "Hey... Can we... start over?", "Can we... start over?")
    elif ct("Shy") and dice(50):
        $ rc("I... I can't go on without you... So please, let me date you again.", "I know it's selfish of me... But...I just can't forget about you...")
    elif ct("Imouto"):
        $ rc("...D-don't you think it's about time we... went back to how we were before?", "Hey... I... want to get back together.", "Umm... Seems like I'm still in love with you... So, can we get back together...?") 
    elif ct("Dandere"):
        $ rc("I just can't forget about you... Do you want to try starting over?","Would it be possible for us to fix what we had?", "Be with me again. ...I need you.")
    elif ct("Tsundere"):
        $ rc("Um, so...I, I wanna go out with you again...", "I can't... I simply can't give up on you... Let me be with you, one more time.", "Call me weak or whatever, I don't care. I just...I want us to start over!"),
    elif ct("Kuudere"):
        $ rc("I want to be by your side again. It's all I can think about lately...", "You're the one who soothes my heart the most, after all... Want to start over again?", "Perhaps it is stubborn of me, but... I would like to reconcile with you.")
    elif ct("Kamidere"):
        $ rc("Hey, I'd like a chance for us to start things over.", "We can still go back to how things used to be, you know?", "I realized... I'm still in love with you after all.")
    elif ct("Bokukko"):
        $ rc("Y'see, like... Y'wanna try goin' back to the way things were before?", "Mmh, it just doesn't do it for me if it isn't you. Can we...go out again?", "I-if you're okay with it, I'd like us to get back together... What do you think?")
    elif ct("Ane"):
        $ rc("I'll fix whatever's wrong with me, so... Please, just let me be with you again.", "I can't seem to forget about you no matter what I do... I want to start things over with you.")
    elif ct("Yandere"):
        $ rc("I want to give us another try. ...Please.", "Sorry... No matter what I do, I can't get you out of my head... So...")
    else:
        $ rc("Hey, could we maybe... see if we can work things out again?", "If we were to be together again, I'd... No... Please, one more time, be with me!")
    $ char.restore_portrait()
    return
    
label interactions_yandere_attack:
    $ char.override_portrait("portrait", "indifferent")
    $ rc("Ufufu... If I had done this from the very start, I would have avoided all of those painful memories...", "Let's love each other again in the afterlife...", "Huhuhuh... You didn't think you could betray me and get off scott free, did you...? Come on... say something for yourself... come ooon...!", "Huhuhuh... I wonder how warm it would be to bathe in your blood...?", "If you won't belong to me... Then you won't... belong to anyone...", "Everything is your fault. Yours... YOUUUUUURS! ! !", "Pft... kuku... Ahaha... Ahahaha... HAH HAH HAH HAH HAH!!", "Hahah... I just figured out how we can be together forever...", "Hey... If you're reborn... Be sure to find me again... okay...", "Ah, hahahahahahahaha... diediediediediediediediediediedie DIE!!", "You're not good enough to live in this world. So I'll erase you. Bye-bye.")
    $ char.restore_portrait()
    return
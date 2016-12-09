label tavern_town:
    if not "tavern_inside" in ilists.world_music:
        $ ilists.world_music["tavern_inside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("tavern")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["tavern_inside"])
    $ global_flags.del_flag("keep_playing_music")

    
    scene bg tavern_inside   
    with dissolve
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    show npc tavern_rita_novel
    with dissolve
    define tavern_rita = Character('Rita', color=honeydew, show_two_window=True)
    
    if not global_flags.flag('visited_tavern'):
        $ global_flags.set_flag('visited_tavern')
        tavern_rita "Oh, hello! Welcome to our tavern! Enjoy your stay!"
    else:
        tavern_rita "Oh, [hero.nickname]! How you been?"
        tavern_rita "We will always have a free seat for you *wink*"
    hide npc
    with dissolve
label city_tavern_menu:
    show screen city_tavern_inside
    while 1:
        $ result = ui.interact()
    # if not global_flags.has_flag("still_in_tavern"):    
        # $ global_flags.set_flag("still_in_tavern", value=False) 
    

    # python:
        # if global_flags.flag("tavern_entry_event") != (day + hero.AP) and global_flags.flag("still_in_tavern") == False:
            # global_flags.set_flag("tavern_entry_event", value=(day + hero.AP))
            # tavern_event_list = []
            # if "tavern_entry" in os.listdir(content_path('events')):
                # if dice(40):
                    # for file in os.listdir(content_path("events/tavern_entry/cozy/")):
                            # tavern_event_list.append('content/events/tavern_entry/cozy/%s' % (file))
                    # img = ProportionalScale(choice(tavern_event_list), 1000, 600)
                    # renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
                    # renpy.with_statement(dissolve)
                    # renpy.say("","The tavern in warm and cozy with only a handfull of drunkards enjoying the stay.")       
                # elif dice(65):
                # else:
                    # for file in os.listdir(content_path("events/tavern_entry/lively/")):
                            # tavern_event_list.append('content/events/tavern_entry/lively/%s' % (file))
                    # img = ProportionalScale(choice(tavern_event_list), 1000, 600)
                    # renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
                    # renpy.with_statement(dissolve)
                    # renpy.say("","The place is lound and lively today, with townsmen drinking and talking at every table.")        
                # else:
                    # global_flags.set_flag("tavern_entry_brawl", value=(day + hero.AP))
                    # for file in os.listdir(content_path("events/tavern_entry/brawl/")):
                            # tavern_event_list.append('content/events/tavern_entry/brawl/%s' % (file))
                    # img = ProportionalScale(choice(tavern_event_list), 1000, 600)
                    # renpy.show("event", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
                    # renpy.with_statement(dissolve)
                    # renpy.music.stop(channel="world")
                    # renpy.music.play("brawl.mp3",channel="world") 
                    # n(choice(["You step into the room... right into a fierce tavern brawl!"]))        
        # else:
            # renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
            # renpy.with_statement(dissolve)
            # if global_flags.flag("tavern_entry_brawl") == (day + hero.AP): 
                # renpy.music.stop(channel="world")
                # renpy.music.play("brawl.mp3",channel="world")
        # global_flags.set_flag("still_in_tavern", value=True)
    

        # if pytfall.world_actions.location("tavern_inside"):
            # pytfall.world_actions.add("brawl_join", "Join in!", Show("wip_screen"),
                                      # condition=Iff(global_flag_complex("tavern_entry_brawl"), "==", S(renpy_store_complex("day"), "+", (hero, "AP"))))
            
            # pytfall.world_actions.add("brawl_stay", "Stay", Show("wip_screen"),
                                      # condition=Iff(global_flag_complex("tavern_entry_brawl"), "!=", S(renpy_store_complex("day"), "+", (hero, "AP"))))
            # pytfall.world_actions.finish()

screen city_tavern_inside():
    use top_stripe(True)
    frame:
        xalign 0.95
        ypos 50
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_tavern_inside"), Jump("tavern_shopping")]
                text "Buy a drink" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_tavern_inside"), Jump("city")]
                text "Leave" size 15
                
label tavern_shopping:

    python:
        focus = None
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.tavern
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    
    call shop_control from _call_shop_control_6
                    
    $ global_flags.del_flag("keep_playing_music")      
    hide screen shopping
    with dissolve
    jump city_tavern_menu
                
#to be deleted later    
screen wip_screen(size=(500, 300), use_return=False):
    modal True
    zorder 10
    
    fixed:
        align(0.5, 0.5)
        xysize(size[0], size[1])
        xfill True
        yfill True
        
        add im.Scale("content/gfx/frame/frame_bg.png", size[0], size[1])
        add "content/gfx/interface/icons/wip.png" xalign 0.9 yalign 0.5
        
        vbox:
            spacing 30
            align(0.2, 0.5)
            vbox:
                xmaximum (size[0] - 50) 
                text "Sorry! Not ready yet!" xalign 0.5 yalign 0.4
                
            textbutton "Ok" action If(use_return, true=Return(), false=Hide("wip_screen")) minimum(150, 30) xalign 0.3

    
screen tavern_inside():

    use top_stripe(True)
    
    use location_actions("tavern_inside")

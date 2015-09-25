label hero_profile:
    scene bg h_profile
    
    $ global_flags.set_flag("keep_playing_music")
    
    # $ pytfall.world_quests.run_quests("auto") Goes against squelching policy?
    $ pytfall.world_events.run_events("auto")
    $ renpy.retain_after_load()
    
    show screen pyt_hero_profile
    with dissolve
    
    $ hero.inventory.set_page_size(18)
    
    while 1:
        $ result = ui.interact()
        
        # To kill input error during team renaming:
        if not result:
            pass
        
        elif result[0] == 'control':
            if result[1] == 'return':
                $ pytfall.hp.show_item_info = False
                $ pytfall.hp.item = False
                hide screen pyt_hero_profile
                hide screen pyt_hero_equip
                
                # Reset filters (prevents crap from happening in shops):
                $ hero.inventory.male_filter = False
                $ hero.inventory.apply_filter('all')
                
                # Taking care of Ren'Pys annoying reserves... <-- Prolly obsolete after I rewrote the last label func.
                if pytfall.hp.came_from.startswith("_"):
                    jump mainscreen
                else:
                    jump expression pytfall.hp.came_from
                    
        elif result[0] == "dropdown":
            if result[1] == "loc":
                $ renpy.show_screen("set_location_dropdown", hero, pos=renpy.get_mouse_pos())
            elif result[1] == "home":
                $ renpy.show_screen("set_home_dropdown", hero, pos=renpy.get_mouse_pos())
                
        elif result[0] == 'hero':
            if result[1] == 'equip':
                if renpy.get_screen('pyt_hero_equip'):
                    hide screen pyt_hero_equip
                    $ pytfall.hp.show_item_info = False
                    $ pytfall.hp.item = False
                else:    
                    show screen pyt_hero_equip 
                    
            elif result[1] == 'first_page':
                $ hero.inventory.first()
            elif result[1] == 'last_page':
                $ hero.inventory.last()
            elif result[1] == 'next_page':
                $ hero.inventory.next()
            elif result[1] == 'prev_page':
                $ hero.inventory.prev()
            elif result[1] == 'prev_filter':
                $ hero.inventory.apply_filter('prev')
            elif result[1] == 'next_filter':
                $ hero.inventory.apply_filter('next')
            elif result[1] == 'male_filter':
                $ hero.inventory.male_filter = True
                $ hero.inventory.apply_filter('all')
            elif result[1] == 'unisex_filter':
                $ hero.inventory.male_filter = False
                $ hero.inventory.apply_filter('all')
            
        elif result[0] == 'item':
            if result[1] == 'get':
                $ pytfall.hp.show_item_info = True
                $ pytfall.hp.item = result[2]

            elif result[1] == 'equip':
                $ equip_item(pytfall.hp.item, hero)
                $ pytfall.hp.show_item_info = False
                $ pytfall.hp.item = False
                
            elif result[1] == "transfer":
                $ renpy.hide_screen("pyt_hero_profile")
                $ pytfall.it = GuiItemsTransfer("personal_transfer", char=ap, last_label=last_label)
                jump items_transfer
                
            elif result[1] == 'unequip':
                $ hero.unequip(pytfall.hp.item)
                $ pytfall.hp.show_item_info = False
                $ pytfall.hp.item = False

        elif result[0] == "remove_from_team":
            $ hero.team.remove(result[1])
            
        elif result[0] == "rename_team":
            if result[1] == "set_name":
                $ hero.team.name = renpy.call_screen("pyt_ht_input")
    
    
    # $ pytfall.hp.screen_loop()

    # hide screen pyt_hero_equip
    # hide screen pyt_hero_profile
    # jump mainscreen

# screen pyt_hero_dropdown_loc(pos=()):
    # # Trying to create a drop down screen with choices of buildings:
    # zorder 3
    # modal True
     
    # key "mousedown_4" action NullAction()
    # key "mousedown_5" action NullAction()
     
    # # Get mouse coords:
    # python:
        # x, y = pos
        # if x > 1000:
            # xval = 1.0
        # else:
            # xval = 0.0
        # if y > 500:
            # yval = 1.0
        # else:
            # yval = 0.0
    # frame:
        # style_group "dropdown"
        # pos (x, y)
        # anchor (xval, yval)
        # vbox:
            # for building in hero.buildings:
                # textbutton "[building.name]":
                    # action [SetField(hero, "location", building), Hide("pyt_hero_dropdown_loc")]
            # textbutton "None":
                # action [SetField(hero, "location", hero), Hide("pyt_hero_dropdown_loc")]
            # textbutton "Close":
                # action [Hide("pyt_hero_dropdown_loc")]

screen pyt_hero_profile():
    
    default tt = Tooltip("")
    default lframe_display = "status"
    default rframe_display = "skills"
    
    # HERO SPRITE ====================================>
    add Transform(hero.show("sprofile", resize=(550, 550)), alpha=0.97) align(0.65, 0.9)
    
    # BASE FRAME 2 "bottom layer" and portrait ====================================>
    add "content/gfx/frame/h_profile.png"
    add (hero.show("cportrait", resize=(100, 100))) pos (64, 8) # portrait should be between "Base Frame 2" and "Base Frame 1" :Gismo
    
    # BATTLE STATS ====================================>
    fixed:
        xysize (270, 270)
        pos (300, 413)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 112, 126, 148, blue), alpha=0.4) align (0.5, 0.5)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 65, 126, 148, blueviolet), alpha=0.3) align (0.5, 0.5)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 33, 126, 148, aquamarine), alpha=0.2) align (0.5, 0.5)
        add ProportionalScale("content/gfx/interface/images/pentagon1.png", 250, 250) align (0.01, 0.5)
        
    fixed:
        frame:
            xysize (100,40)
            pos(375, 402)
            background Frame(Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
            has hbox xfill True yfill True
            add ProportionalScale("content/gfx/interface/images/atk.png", 24, 24) align (0.5, 0.5)
            text("{size=-5}{font=fonts/Rubius.ttf}{color=[red]}[hero.attack]|%d"%(hero.get_max("attack"))) align (0.5, 0.63) outlines [(1, "#0d0d0d", 0, 0)]
        frame:
            xysize (100,40)
            pos(223, 483)
            background Frame(Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
            has hbox xfill True yfill True
            add ProportionalScale("content/gfx/interface/images/def.png", 24, 24) align (0.5, 0.5)
            text("{size=-5}{font=fonts/Rubius.ttf}{color=#dc762c}[hero.defence]|%d"%(hero.get_max("defence"))) align (0.5, 0.63) outlines [(1, "#0d0d0d", 0, 0)]
        frame:
            xysize (100,40)
            pos(255, 643)
            background Frame(Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
            has hbox xfill True yfill True
            add ProportionalScale("content/gfx/interface/images/agi.png", 24, 24) align (0.5, 0.5)
            text("{size=-5}{font=fonts/Rubius.ttf}{color=#1E90FF} [hero.agility]|%d"%(hero.get_max("agility"))) align (0.5, 0.63) outlines [(1, "#0d0d0d", 0, 0)]
        frame:
            xysize (100,40)
            pos(495, 643)
            background Frame(Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
            has hbox xfill True yfill True
            add ProportionalScale("content/gfx/interface/images/luck.png", 24, 24) align (0.5, 0.5)
            text("{size=-5}{font=fonts/Rubius.ttf}{color=#00FA9A}[hero.luck]|%d"%(hero.get_max("luck"))) align (0.5, 0.63) outlines [(1, "#0d0d0d", 0, 0)]
        frame:
            xysize (100,40)
            pos(526, 483)
            background Frame(Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
            has hbox xfill True yfill True
            add ProportionalScale("content/gfx/interface/images/mag.png", 24, 24) align (0.5, 0.5)
            text("{size=-5}{font=fonts/Rubius.ttf}{color=#8470FF}[hero.magic]|%d"%(hero.get_max("magic"))) align (0.5, 0.63) outlines [(1, "#0d0d0d", 0, 0)]
    
    # LEFT FRAME ====================================>
    
    vbox:
        xsize 217
        pos (8, 110)
        
        # NAME^   LVL   (ok for 1m lvls) ====================================>
        text (u"{color=#ecc88a}[hero.name]") font "fonts/TisaOTM.otf" size 28 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.492 ypos 5
        hbox:
            spacing 1
            if (hero.level) <10:
                pos (89, 11)
            elif (hero.level) <100:
                pos (86, 11)
            elif (hero.level) <10000:
                pos (77, 11)
            else:
                pos (73, 11)
            label "{color=#CDAD00}Lvl" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]
            label "{color=#CDAD00}[hero.level]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]
            
        if lframe_display == "status":
            # STATS ====================================>
            vbox:
                yoffset -30
                hbox:
                    $ stats = ["constitution", "charisma", "intelligence", "fame", "reputation", "libido"]
                    ypos 40
                    vbox:
                        style_group "stats"
                        spacing -7
                        xanchor 2
                        xmaximum 113
                        frame:
                            xysize (215, 8)
                            text "{color=#CD4F39}Health:" xalign (0.02)
                        frame:
                            xysize (215, 8)
                            text "{color=#009ACD}MP:" size 16 xalign (0.02)
                        frame:
                            xysize (215, 8)
                            text "{color=#43CD80}Vitality:" xalign (0.02)
                        for stat in stats:
                            frame:
                                xysize (215, 8)
                                text ('{color=#79CDCD}%s'%stat.capitalize()) color ivory size 17 xalign (0.02) 
                    vbox:
                        yalign (0.65)
                        spacing 8
                        xanchor 20
                        xfill True
                        xminimum 0
                        xmaximum 120
                    
                        if hero.health <= hero.get_max("health")*0.3:
                            text (u"{color=[red]}%s/%s"%(hero.health, hero.get_max("health"))) style "stats_value_text" xalign (1.0)
                        else:
                            text (u"{color=#F5F5DC}%s/%s"%(hero.health, hero.get_max("health"))) style "stats_value_text" xalign (1.0)
    
                        if hero.mp <= hero.get_max("mp")*0.3:
                            text (u"{color=[red]}%s/%s"%(hero.mp, hero.get_max("mp"))) style "stats_value_text" xalign (1.0)
                        else:
                            text (u"{color=#F5F5DC}%s/%s"%(hero.mp, hero.get_max("mp"))) style "stats_value_text" xalign (1.0)
    
                        if hero.vitality <= hero.get_max("vitality")*0.3:
                            text (u"{color=[red]}%s/%s"%(hero.vitality, hero.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                        else:
                            text (u"{color=#F5F5DC}%s/%s"%(hero.vitality, hero.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                        
                        for stat in stats:
                            text ('{color=#F5F5DC}%d/%d'%(getattr(hero, stat), hero.get_max(stat))) style "stats_value_text" xalign (1.0)
                    
                # LOCATION ====================================>
                vbox:
                    pos (10, 8)
                    button:
                        ypos 35
                        style_group "ddlist"
                        action Return(["dropdown", "loc"])
                        alternate Return(["dropdown", "home"])
                        text "{image=content/gfx/interface/icons/move15.png}Location:\n       [hero.location]":
                            if len(str(hero.location)) > 18:
                                size 15
                            else:
                                size 16
                        hovered tt.Action("Change MCs Home/Location.")
                        
                    # AP ====================================>
                    frame:
                        ypos 37
                        xysize (100, 80)
                        background ProportionalScale("content/gfx/frame/frame_ap2.png", 190, 80)
                        label "[hero.AP]":
                            pos (130, -2)
                            style "content_label"
                            text_color ivory
                            text_size 22
                            
                null height 10
                
                # ELEMENTAL ALIGNMENT ====================================>
                $ els = [Transform(e.icon, size=(90, 90)) for e in hero.elements]
                frame:
                    style_group "content"
                    background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 10, 10)
                    xysize (210, 120)
                    xalign 0.5
                    xoffset -10
                    
                    $ x = 0
                    $ els = [Transform(i, crop=(90/len(els)*els.index(i), 0, 90/len(els), 90), subpixel=True, xpos=(x + 90/len(els)*els.index(i))) for i in els]
                    $ f = Fixed(*els, xysize=(90, 90))
                    add f xcenter 150 ycenter 50
                    
                    viewport:
                        draggable True
                        edgescroll (15, 10)
                        xysize (200, 110)
                        align (0, 0.5)
                        # yoffset 33
                        has vbox spacing -4
                        for e in hero.elements:
                            textbutton "{=tisa_otm}{size=15}[e.id]":
                                background None
                                action NullAction()
                                hovered tt.Action("%s" % e.desc)
    
        elif lframe_display == "friends":
            # FRIEND LIST ====================================>
            null height 26
            viewport:
                xysize (190, 500)
                scrollbars "vertical"
                draggable True
                mousewheel True
                xalign 0.5
                has vbox spacing 2
                $ temp = sorted(list(hero.friends | hero.lovers), key=attrgetter("name"))
                for char in temp:
                    button:
                        xalign 0.5
                        xysize (180, 170)
                        action NullAction()
                        has fixed xysize (175, 170) xalign 0.5
                        add char.show("portrait", resize=(123, 123), cache=True) align (1.0, 0)
                        frame:
                            align (1.0, 1.0)
                            xysize (155, 25)
                            if char in hero.lovers:
                                text "lover" color pink xalign 0.5
                            else:
                                text "Friend" color blue xalign 0.5
                        text char.nickname:
                            pos (0, 0)
                            xoffset -10
                            yoffset - 15
                            layout "subtitle"
                            text_align 0.5
                            vertical True
                            ymaximum 160
                            if len(char.nickname) > 8:
                                size 12
                            else:
                                size 15
        
    # BUTTONS on the "bottom layer" ------------------------------------>
    hbox:
        style_group "pb"
        spacing 1
        pos (1131, 155)
        button:
            action SetScreenVariable("rframe_display", "skills"), With(dissolve)
            text "Skills" style "pb_button_text"
        button:
            action SetScreenVariable("rframe_display", "traits"), With(dissolve)
            text "Traits" style "pb_button_text"
        
    # RIGHT FRAME ====================================>
    vbox:
        pos (1124, 60)
        xysize (153, 140)
        frame:
            xalign 0.5
            yfill True
            background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
            xysize (153, 60)
            text (u"{color=#CDAD00} Day [day]") font "fonts/Rubius.ttf" size 26 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.6)
        null height -8
        frame:
            xalign 0.5
            xsize 140
            background Frame(Transform("content/gfx/frame/stat_box.png", alpha=0.8), 10, 10)
            hbox:
                xfill True
                text "{color=#DAA520}Gold:" size 14  outlines [(1, "#3a3a3a", 0, 0)] align (0.0, 0.5)
                text (u"{color=#DAA520}%d"%int(hero.gold)) size 14 outlines [(1, "#3a3a3a", 0, 0)] align (1.0, 0.5)
        
    if rframe_display == "skills":
            
        # ATTACKS/MAGIC ====================================>
        vbox:
            pos (1125, 205)
            style_group "stats"
            spacing 5
            
            frame:
                background Frame("content/gfx/frame/hp_1.png", 5, 5)
                xysize (160, 192)
                has vbox
                label (u"Attack:") text_size 19 text_color ivory text_bold True align(0.43, 0.5) text_outlines [(3, "#3a3a3a", 0, 0), (2, "#8B0000", 0, 0), (1, "#3a3a3a", 0, 0)]
                xpos -3
                viewport:
                    xysize (160, 150)
                    scrollbars "vertical"
                    draggable True
                    mousewheel True
                    has vbox spacing -7
                    for entry in hero.attack_skills:
                        frame:
                            xysize (128, 10)
                            button:
                                background Null()
                                xysize (128, 10)
                                action NullAction()
                                text "{color=#F5F5DC}[entry.name]" size 15 xanchor(10)
                                hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)
                                hovered tt.action(entry)#, With(dissolve)
            
            frame:
                background Frame("content/gfx/frame/hp_1.png", 5, 5)
                xysize (160, 192)
                has vbox
                label (u"Magic:") text_size 19 text_color ivory text_bold True align(0.41, 0.5) text_outlines [(3, "#3a3a3a", 0, 0), (2, "#104E8B", 0, 0), (1, "#3a3a3a", 0, 0)]
                xpos -3
                viewport:
                    xysize (160, 150)
                    scrollbars "vertical"
                    draggable True
                    mousewheel True
                    has vbox spacing -7
                    for entry in hero.magic_skills:
                        frame:
                            xysize (128, 10)
                            button:
                                background Null()
                                xysize (128, 10)
                                action NullAction()
                                text "{color=#F5F5DC}[entry.name]" size 15 xanchor(10)
                                hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)
                                hovered tt.action(entry)# , With(dissolve)
    
    elif rframe_display == "traits":
        
        # TRAITS ====================================>
        vbox:
            pos (1125, 205)
            style_group "stats"
            spacing 5
            
            frame:
                background Frame("content/gfx/frame/hp_1long.png", 5, 5)
                xysize (160, 389)
                
                # Traits (Baseclasses for now):
                #has vbox
                #for t in hero.traits:
                    #textbutton "[t.id]" action NullAction() hovered tt.action(t.desc)
    
    # EQUIPMENT   -------------------------------------------------->
    # showif not renpy.get_screen('pyt_hero_equip'):
        # use pyt_eqdoll(active_mode=False, char=hero)
    
    # TOOLTIP TEXT ====================================>
    hbox:
        spacing 1
        pos (621, 602)
        xysize (657, 114)
        yfill True
        if isinstance(tt.value, BE_Action):
            $ element = tt.value.get_element()
            if element:
                fixed:
                    xysize (100, 100)
                    yalign 0.5
                    if element.icon:
                        $ img = ProportionalScale(element.icon, 90, 90)
                        add img align (0.5, 0.5)
            text tt.value.desc style "content_text" size 18 color "#ecc88a" yalign 0.1
        else:
            text (u"{=content_text}{color=#ecc88a}%s" % tt.value) size 18
            
    # BASE FRAME 1 "top layer" ====================================>
    add "content/gfx/frame/h_profile2.png"
    
    # BUTTONS and UI elements on the "top layer" ====================================>
    hbox:
        style_group "pb"
        spacing 3
        pos (459, 9)
        button:
            xsize 75
            action SetScreenVariable("lframe_display", "status"), With(dissolve)
            text "Status" style "pb_button_text"
            hovered tt.Action("Show Hero Stats")
        button:
            xsize 75
            action Show("pyt_hero_team", transition=dissolve)#, With(dissolve)
            text "Team" style "pb_button_text"
            hovered tt.Action("Show [hero.team.name]!")#, With(dissolve)
        button:
            action Return(['hero', 'equip'])#, With(dissolve)
            text "Equipment" style "pb_button_text"
            hovered tt.Action("Take a look at your inventory.")
        button:
            action Show("pyt_hero_finances")#, With(dissolve)
            text "Finance" style "pb_button_text"
        button:
            xsize 75
            action If(hero.friends | hero.lovers, true=[SetScreenVariable("lframe_display", "friends"), With(dissolve)])
            text "Friends" style "pb_button_text"
    
    imagebutton:
        pos (900, 7) # (178, 70)
        idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
        hover im.Scale("content/gfx/interface/buttons/close2_h.png", 35, 35)
        action Return(['control', 'return'])
        hovered tt.Action("Return to previous screen!")
    
    # EXP BAR ====================================>
    fixed:
        pos (259, 697)
        bar:
            value hero.stats.exp + hero.stats.goal_increase - hero.stats.goal
            range hero.stats.goal_increase
            left_bar ("content/gfx/interface/bars/exp_full.png")
            right_bar ("content/gfx/interface/bars/exp_empty.png")
            thumb None
            maximum (324, 18)
        hbox:
            spacing 10
            pos (90, -17)
            xmaximum 160
            xfill True
            add "content/gfx/interface/images/exp_b.png" ypos 2 xalign 0.8
            text "[hero.exp]/[hero.goal]" style "stats_value_text" bold True outlines [(1, "#181818", 0, 0)] color "#DAA520"

screen pyt_hero_equip():
    modal True
    zorder 1
    default tt = Tooltip(None)
    # Useful keymappings (first time I try this in PyTFall):
    if pytfall.hp.show_unequip_button():
        key "mousedown_2" action Return(["item", "unequip"])
    elif pytfall.hp.show_equip_button():
        key "mousedown_2" action Return(["item", "equip"])
    else:
        key "mousedown_2" action NullAction()
        
    key "mousedown_4" action Return(["hero", "next_page"])
    key "mousedown_5" action Return(["hero", "prev_page"])
    
    # Doll...
    use pyt_eqdoll(char=hero)
    
    # Inventory ------------------------------------------------------------>
    vbox:
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)
        pos (394, 440)
        spacing 3
        hbox:
            spacing 52
            use paging(root='hero', ref=hero.inventory, use_filter=True)
            use items_inv(char=hero)
            
        # Buttons:    
        frame:
            background Frame("content/gfx/frame/p_frame2.png", 10, 10)
            style_group "basic"
            xpadding 10
            ypadding 10
            yanchor 60
            has hbox
            textbutton 'Close':
                hovered tt.Action("Take a look at your inventory.")
                action Return(['hero', 'equip'])
            if renpy.get_screen('pyt_hero_equip') and not hero.inventory.male_filter:
                textbutton "Male Filter":
                    hovered tt.Action("Filter out all items suitible for only girls.")
                    action Return(['hero', 'male_filter'])
            if renpy.get_screen('pyt_hero_equip') and hero.inventory.male_filter:
                textbutton "Unisex Filter":
                    hovered tt.Action("Show all items.")
                    action Return(['hero', 'unisex_filter'])
            if pytfall.hp.show_equip_button():
                textbutton "Equip":
                    hovered tt.Action("Equip this item.")
                    action Return(['item', 'equip'])
            if pytfall.hp.show_unequip_button():
                textbutton "Unequip":
                    hovered tt.Action("Unequip this item.")
                    action Return(['item', 'unequip'])  
                        
    # Item Info ------------------------------------------------------------------------>                    
    showif pytfall.hp.show_item_info:
        frame:
            at fade_in_out()
            xalign 0.986
            ypos 43
            background Frame("content/gfx/frame/frame_dec_1.png", 30, 30)
            xpadding 30
            ypadding 30
            xysize (555, 400)
            use itemstats(item=pytfall.hp.item, size=(580, 350), style_group="content", mc_mode=True)
    
            
screen pyt_ht_input():
    zorder 1
    modal True

    fixed:
        align(0.5, 0.5)
        xysize (350, 150)
        add im.Scale("content/gfx/frame/frame_bg.png", 350, 150)
        vbox:
            spacing 30
            align(0.5, 0.5)
            text "{color=[ivory]}Enter your team name:" xalign 0.5
            input default "Player Team" length 20 xalign 0.5

screen pyt_hero_team():
    zorder 1
    modal True
    
    default tt = Tooltip("Welcome to MC profile screen!")
    
    # Hero team ---------------------------------------------->
    frame:
        style_group "content"
        align (0.5, 0.5)
        background Frame(Transform(im.Twocolor("content/gfx/frame/ink_box.png", white, black), alpha=0.7), 10, 10)
        # xysize (400, 500)
        ypadding 20
        xpadding 20
        has vbox
        null height 5
        label ("[hero.team.name]") align(0.5, 0.02) text_size 30 text_color ivory
        null height 5
        vbox:
            # xysize (350, 450)
            spacing 10
            for member in hero.team:
                frame:
                    background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                    xpadding 20
                    ypadding 10
                    has hbox
                    frame:
                        background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                        xysize (10, 10)
                        add (member.show("portrait", resize=(120, 120))) align (0.5, 0.5)
                    null width 10
                    vbox:
                        style_group "stats"
                        spacing 1
                        vbox:
                            text "HP:" color ivory style "stats_value_text"
                            bar:
                                value member.health
                                range member.get_max("health")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), red, red)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), red, red)
                                thumb None
                                maximum (110, 20)
                        vbox:
                            text "MP:" color ivory style "stats_value_text"
                            bar:
                                value member.mp
                                range member.get_max("mp")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), green, green)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), green, green)
                                thumb None
                                maximum (110, 20)
                        vbox:
                            text "Vitality:" color ivory style "stats_value_text"
                            bar:
                                value member.vitality
                                range member.get_max("vitality")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), blue, blue)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), blue, blue)
                                thumb None
                                maximum (110, 20)
                                
                    null width 25
                    vbox:
                        yalign 0.5
                        ysize 50
                        spacing 10
                        text "AP: [member.AP]" xalign 0.5 size 16 color ivory style "stats_value_text"
                        button:
                            style_group "basic"
                            xalign 0.5
                            if member == hero:
                                action Return(["rename_team", "set_name"])
                                hovered tt.Action("Rename Heroes team!")
                                text "RT"
                            else:
                                action Return(["remove_from_team", member])
                                hovered tt.Action("Remove %s for %s!"%(member.nickname, hero.team.name))
                                text "RM"
          
        null height 20
        button:
            style_group "basic"
            xalign 0.5
            action Hide("pyt_hero_team")
            text "Close"

screen pyt_hero_finances():
    modal True
    zorder 1
    
    frame at slide(so1=(0, 700), t1=0.7, so2=(0, 0), t2=0.3, eo2=(0, -config.screen_height)):
        background Frame (Transform("content/gfx/frame/arena_d.png", alpha=1.2), 5, 5)
        align (0.5, 0.5)
        xysize (1120, 600)
        # side "c r":
            # area (20, 43, 1110, 495)
        viewport id "herofin_vp":
            style_group "stats"
            draggable True
            mousewheel True
            if day > 1 and hero.fin.game_fin_log.has_key(str(day-1)):
                $ fin_inc = hero.fin.game_fin_log[str(day-1)][0]["private"]
                $ fin_exp = hero.fin.game_fin_log[str(day-1)][1]["private"]
                
                if pytfall.hp.finance_filter == 'day':
                    label (u"Fin Report (Yesterday)") xalign 0.4 ypos 30 text_size 30
                    # Income:
                    vbox:
                        pos (50, 100)
                        label "Income:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in fin_inc:
                                    text "[key]"
                            vbox:
                                null height 1
                                spacing 4
                                for key in fin_inc:
                                    $ val = fin_inc[key]
                                    text "[val]" style "stats_value_text"
                                    
                    # Expense:
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in fin_exp:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in fin_exp:
                                    $ val = fin_exp[key]
                                    text ("[val]") style "stats_value_text"
                                
                    python:
                        total_income = 0
                        total_expenses = 0
                        for key in fin_inc:
                            total_income += fin_inc[key]
                        for key in fin_exp:
                            total_expenses += fin_exp[key]
                        total = total_income - total_expenses
                        
                    vbox:
                        align (0.80, 0.60)
                        text "----------------------------------------"
                        text ("Revenue: [total]"):
                            size 20
                            xpos 15
                            if total > 0:
                                color lawngreen style "stats_value_text"
                            else:
                                color red style "stats_value_text"
                        
                    hbox:
                        style_group "basic"
                        align (0.5, 0.9)
                        textbutton "Show Total" action SetField(pytfall.hp, "finance_filter", "total")
                    
                elif pytfall.hp.finance_filter == 'total':
                    label (u"Fin Report (Game)") xalign 0.4 ypos 30 text_size 30
                    python:
                        income = dict()
                        for _day in hero.fin.game_fin_log:
                            for key in hero.fin.game_fin_log[_day][0]["private"]:
                                income[key] = income.get(key, 0) + hero.fin.game_fin_log[_day][0]["private"][key]
                    # Income:
                    vbox:
                        pos (50, 100)
                        label "Income:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in income:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in income:
                                    $ val = income[key]
                                    text ("[val]") style "stats_value_text"
                                    
                    python:
                        expenses = dict()
                        for _day in hero.fin.game_fin_log:
                            for key in hero.fin.game_fin_log[_day][1]["private"]:
                                expenses[key] = expenses.get(key, 0) + hero.fin.game_fin_log[_day][1]["private"][key]
                    # Expense:
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in expenses:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in expenses:
                                    $ val = expenses[key]
                                    text ("[val]") style "stats_value_text"
                                
                    python:
                        game_total = 0
                        total_income = sum(income.values())
                        total_expenses = sum(expenses.values())
                        game_total = total_income - total_expenses
                        
                    vbox:
                        align (0.80, 0.60)
                        text "----------------------------------------"
                        text ("Revenue: [game_total]"):
                            size 20
                            xpos 15
                            if game_total > 0:
                                color lawngreen style "stats_value_text"
                            else:
                                color red style "stats_value_text"
                        
                    hbox:
                        style_group "basic"
                        align (0.5, 0.9)
                        textbutton "{size=-3}Show Daily" action SetField(pytfall.hp, "finance_filter", "day")
                
                hbox:
                    pos (750, 100)
                    vbox:
                        xmaximum 140
                        xfill True
                        if hero.fin.property_tax_debt:
                            text ("Property:\n(Tax Debt") color red size 20 outlines [(2, "#424242", 0, 0)]
                        if hero.fin.income_tax_debt:
                            text ("Income:\n(Tax Debt)") color crimson size 20 outlines [(2, "#424242", 0, 0)]
                        if day != 1:
                            text "Taxes:\n(This week)" size 20 outlines [(2, "#424242", 0, 0)]
                    vbox:
                        if hero.fin.property_tax_debt:
                            null height 4
                            spacing 4
                            text ("[hero.fin.property_tax_debt]\n ") color red style "stats_value_text"
                        if hero.fin.income_tax_debt:
                            null height 4
                            spacing 4
                            text ("[hero.fin.income_tax_debt]\n ") color crimson style "stats_value_text"
                        if day != 1:
                            python:
                                days = calendar.days.index(calendar.weekday())
                                taxes = hero.fin.get_total_taxes(days)
                            null height 4
                            spacing 4
                            text ("[taxes]\n ") style "stats_value_text"
                                
            # vbar value YScrollValue("herofin_vp")
        button:
            style_group "basic"
            action Hide('pyt_hero_finances')
            minimum (250, 30)
            align (0.5, 0.96)
            text "OK"
